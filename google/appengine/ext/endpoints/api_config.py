#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


"""Library for generating an API configuration document for a ProtoRPC backend.

The protorpc.remote.Service is inspected and a JSON document describing
the API is returned.

    class MyResponse(messages.Message):
      bool_value = messages.BooleanField(1)
      int32_value = messages.IntegerField(2)

    class MyService(remote.Service):

      @remote.method(message_types.VoidMessage, MyResponse)
      def entries_get(self, request):
        pass

    api = ApiConfigGenerator().pretty_print_config_to_json(MyService)
"""



try:
  import json
except ImportError:
  import simplejson as json
import logging
import re

from protorpc import message_types
from protorpc import messages
from protorpc import remote
from protorpc import util

from google.appengine.api import app_identity
from google.appengine.ext.endpoints import message_parser
from google.appengine.ext.endpoints import users_id_token


__all__ = [
    'API_EXPLORER_CLIENT_ID',
    'ApiConfigGenerator',
    'CacheControl',
    'EMAIL_SCOPE',
    'api',
    'method',
]


API_EXPLORER_CLIENT_ID = '292824132082.apps.googleusercontent.com'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/userinfo.email'


def _CheckListType(settings, allowed_type, name, allow_none=True):
  """Verify that settings in list are of the allowed type or raise TypeError.

  Args:
    settings: The list of settings to check.
    allowed_type: The allowed type of items in 'settings'.
    name: Name of the setting, added to the exception.
    allow_none: If set, None is also allowed.

  Raises:
    TypeError: if setting is not of the allowed type.

  Returns:
    The list of settings, for convenient use in assignment.
  """
  if settings is None:
    if not allow_none:
      raise TypeError('%s is None, which is not allowed.' % name)
    return settings
  if not isinstance(settings, (tuple, list)):
    raise TypeError('%s is not a list.' % name)
  if not all(isinstance(i, allowed_type) for i in settings):
    type_list = list(set(type(setting) for setting in settings))
    raise TypeError('%s contains types that don\'t match %s: %s' %
                    (name, allowed_type.__name__, type_list))
  return settings


def _CheckType(value, check_type, name, allow_none=True):
  """Check that the type of an object is acceptable.

  Args:
    value: The object whose type is to be checked.
    check_type: The type that the object must be an instance of.
    name: Name of the object, to be placed in any error messages.
    allow_none: True if value can be None, false if not.

  Raises:
    TypeError: If value is not an acceptable type.
  """
  if value is None and allow_none:
    return
  if not isinstance(value, check_type):
    raise TypeError('%s type doesn\'t match %s.' % (name, check_type))



class _ApiInfo(object):
  """Configurable attributes of an API.

  A structured data object used to store API information associated with each
  remote.Service-derived class that implements an API.  This stores properties
  that could be different for each class (such as the path or
  collection/resource name), as well as properties common to all classes in
  the API (such as API name and version).
  """

  @util.positional(2)
  def __init__(self, common_info, resource_name=None, path=None, audiences=None,
               scopes=None, allowed_client_ids=None):
    """Constructor for _ApiInfo.

    Args:
      common_info: _ApiDecorator.__ApiCommonInfo, Information that's common for
        all classes that implement an API.
      resource_name: string, The collection that the annotated class will
        implement in the API. (Default: None)
      path: string, Base request path for all methods in this API.
        (Default: None)
      audiences: list of strings, Acceptable audiences for authentication.
        (Default: None)
      scopes: list of strings, Acceptable scopes for authentication.
        (Default: None)
      allowed_client_ids: list of strings, Acceptable client IDs for auth.
        (Default: None)
    """
    _CheckType(resource_name, basestring, 'resource_name')
    _CheckType(path, basestring, 'path')
    _CheckListType(audiences, basestring, 'audiences')
    _CheckListType(scopes, basestring, 'scopes')
    _CheckListType(allowed_client_ids, basestring, 'allowed_client_ids')

    self.__common_info = common_info
    self.__resource_name = resource_name
    self.__path = path
    self.__audiences = audiences
    self.__scopes = scopes
    self.__allowed_client_ids = allowed_client_ids

  @property
  def name(self):
    """Name of the API."""
    return self.__common_info.name

  @property
  def version(self):
    """Version of the API."""
    return self.__common_info.version

  @property
  def description(self):
    """Description of the API."""
    return self.__common_info.description

  @property
  def hostname(self):
    """Hostname for the API."""
    return self.__common_info.hostname

  @property
  def audiences(self):
    """List of audiences accepted for the API, overriding the defaults."""
    if self.__audiences is not None:
      return self.__audiences
    return self.__common_info.audiences

  @property
  def scopes(self):
    """List of scopes accepted for the API, overriding the defaults."""
    if self.__scopes is not None:
      return self.__scopes
    return self.__common_info.scopes

  @property
  def allowed_client_ids(self):
    """List of client IDs accepted for the API, overriding the defaults."""
    if self.__allowed_client_ids is not None:
      return self.__allowed_client_ids
    return self.__common_info.allowed_client_ids

  @property
  def resource_name(self):
    """Resource name for the class this decorates."""
    return self.__resource_name

  @property
  def path(self):
    """Base path prepended to any method paths in the class this decorates."""
    return self.__path


class _ApiDecorator(object):
  """Decorator for single- or multi-class APIs.

  An instance of this class can be used directly as a decorator for a
  single-class API.  Or call the collection() method to decorate a multi-class
  API.
  """

  @util.positional(3)
  def __init__(self, name, version, description=None, hostname=None,
               audiences=None, scopes=None, allowed_client_ids=None):
    """Constructor for _ApiDecorator.

    Args:
      name: string, Name of the API.
      version: string, Version of the API.
      description: string, Short description of the API (Default: None)
      hostname: string, Hostname of the API (Default: app engine default host)
      audiences: list of strings, Acceptable audiences for authentication.
      scopes: list of strings, Acceptable scopes for authentication.
      allowed_client_ids: list of strings, Acceptable client IDs for auth.
    """
    self.__common_info = self.__ApiCommonInfo(
        name, version, description=description, hostname=hostname,
        audiences=audiences, scopes=scopes,
        allowed_client_ids=allowed_client_ids)

  class __ApiCommonInfo(object):
    """API information that's common among all classes that implement an API.

    When a remote.Service-derived class implements part of an API, there is
    some common information that remains constant across all such classes
    that implement the same API.  This includes things like name, version,
    hostname, and so on.  __ApiComminInfo stores that common information, and
    a single __ApiCommonInfo instance is shared among all classes that
    implement the same API, guaranteeing that they share the same common
    information.

    Some of these values can be overridden (such as audiences and scopes),
    while some can't and remain the same for all classes that implement
    the API (such as name and version).
    """

    @util.positional(3)
    def __init__(self, name, version, description=None, hostname=None,
                 audiences=None, scopes=None, allowed_client_ids=None):
      """Constructor for _ApiCommonInfo.

      Args:
        name: string, Name of the API.
        version: string, Version of the API.
        description: string, Short description of the API (Default: None)
        hostname: string, Hostname of the API (Default: app engine default host)
        audiences: list of strings, Acceptable audiences for authentication.
        scopes: list of strings, Acceptable scopes for authentication.
        allowed_client_ids: list of strings, Acceptable client IDs for auth.
      """
      _CheckType(name, basestring, 'name', allow_none=False)
      _CheckType(version, basestring, 'version', allow_none=False)
      _CheckType(description, basestring, 'description')
      _CheckType(hostname, basestring, 'hostname')
      _CheckListType(audiences, basestring, 'audiences')
      _CheckListType(scopes, basestring, 'scopes')
      _CheckListType(allowed_client_ids, basestring, 'allowed_client_ids')

      if hostname is None:
        hostname = app_identity.get_default_version_hostname()
      if audiences is None and hostname is not None:
        audiences = [hostname]
      if scopes is None:
        scopes = [EMAIL_SCOPE]
      if allowed_client_ids is None:
        allowed_client_ids = [API_EXPLORER_CLIENT_ID]

      self.__name = name
      self.__version = version
      self.__description = description
      self.__hostname = hostname
      self.__audiences = audiences
      self.__scopes = scopes
      self.__allowed_client_ids = allowed_client_ids

    @property
    def name(self):
      """Name of the API."""
      return self.__name

    @property
    def version(self):
      """Version of the API."""
      return self.__version

    @property
    def description(self):
      """Description of the API."""
      return self.__description

    @property
    def hostname(self):
      """Hostname for the API."""
      return self.__hostname

    @property
    def audiences(self):
      """List of audiences accepted by default for the API."""
      return self.__audiences

    @property
    def scopes(self):
      """List of scopes accepted by default for the API."""
      return self.__scopes

    @property
    def allowed_client_ids(self):
      """List of client IDs accepted by default for the API."""
      return self.__allowed_client_ids

  def __call__(self, api_class):
    """Decorator for ProtoRPC class that configures Google's API server.

    Args:
      api_class: remote.Service class, ProtoRPC service class being wrapped.

    Returns:
      Same class with API attributes assigned in api_info.
    """
    return self.collection()(api_class)

  def collection(self, resource_name=None, path=None, audiences=None,
                 scopes=None, allowed_client_ids=None):
    """Get a decorator for a class that implements an API.

    This can be used for single-class or multi-class implementations.  It's
    used implicitly in simple single-class APIs that only use @api directly.

    Args:
      resource_name: string, Resource name for the class this decorates.
        (Default: None)
      path: string, Base path prepended to any method paths in the class this
        decorates. (Default: None)
      audiences: list of strings, Acceptable audiences for authentication.
        (Default: None)
      scopes: list of strings, Acceptable scopes for authentication.
        (Default: None)
      allowed_client_ids: list of strings, Acceptable client IDs for auth.
        (Default: None)

    Returns:
      A decorator function to decorate a class that implements an API.
    """

    def apiserving_api_decorator(api_class):
      """Decorator for ProtoRPC class that configures Google's API server.

      Args:
        api_class: remote.Service class, ProtoRPC service class being wrapped.

      Returns:
        Same class with API attributes assigned in api_info.
      """
      api_class.api_info = _ApiInfo(
          self.__common_info, resource_name=resource_name,
          path=path, audiences=audiences, scopes=scopes,
          allowed_client_ids=allowed_client_ids)
      return api_class

    return apiserving_api_decorator


@util.positional(2)
def api(name, version, description=None, hostname=None, audiences=None,
        scopes=None, allowed_client_ids=None):
  """Decorate a ProtoRPC Service class for use by the framework above.

  This decorator can be used to specify an API name, version, description, and
  hostname for your API.

  Sample usage (python 2.7):
    @endpoints.api(name='guestbook', version='v0.2',
                   description='Guestbook API')
    class PostService(remote.Service):
      pass

  Sample usage (python 2.5):
    class PostService(remote.Service):
      pass
    endpoints.api(name='guestbook', version='v0.2',
                  description='Guestbook API')(PostService)

  Args:
    name: string, Name of the API.
    version: string, Version of the API.
    description: string, Short description of the API (Default: None)
    hostname: string, Hostname of the API (Default: app engine default host)
    audiences: list of strings, Acceptable audiences for authentication.
    scopes: list of strings, Acceptable scopes for authentication.
    allowed_client_ids: list of strings, Acceptable client IDs for auth.

  Returns:
    Class decorated with api_info attribute, an instance of ApiInfo.
  """

  return _ApiDecorator(name, version, description=description,
                       hostname=hostname, audiences=audiences, scopes=scopes,
                       allowed_client_ids=allowed_client_ids)


class CacheControl(object):
  """Cache control settings for an API method.

  Setting is composed of a directive and maximum cache age.
  Available types:
    PUBLIC - Allows clients and proxies to cache responses.
    PRIVATE - Allows only clients to cache responses.
    NO_CACHE - Allows none to cache responses.
  """
  PUBLIC = 'public'
  PRIVATE = 'private'
  NO_CACHE = 'no-cache'
  VALID_VALUES = (PUBLIC, PRIVATE, NO_CACHE)

  def __init__(self, directive=NO_CACHE, max_age_seconds=0):
    """Constructor.

    Args:
      directive: string, Cache control directive, as above. (Default: NO_CACHE)
      max_age_seconds: int, Maximum age of cache responses. (Default: 0)
    """
    if directive not in self.VALID_VALUES:
      directive = self.NO_CACHE
    self.__directive = directive
    self.__max_age_seconds = max_age_seconds

  @property
  def directive(self):
    """The cache setting for this method, PUBLIC, PRIVATE, or NO_CACHE."""
    return self.__directive

  @property
  def max_age_seconds(self):
    """The maximum age of cache responses for this method, in seconds."""
    return self.__max_age_seconds


class _MethodInfo(object):
  """Configurable attributes of an API method.

  Consolidates settings from @method decorator and/or any settings that were
  calculating from the ProtoRPC method name, so they only need to be calculated
  once.
  """

  @util.positional(1)
  def __init__(self, name=None, path=None, http_method=None,
               cache_control=None, scopes=None, audiences=None,
               allowed_client_ids=None):
    """Constructor.

    Args:
      name: string, Name of the method, prepended with <apiname>. to make it
        unique.
      path: string, Path portion of the URL to the method, for RESTful methods.
      http_method: string, HTTP method supported by the method.
      cache_control: CacheControl, Cache settings for the API method.
      scopes: list of string, OAuth2 token must contain one of these scopes.
      audiences: list of string, IdToken must contain one of these audiences.
      allowed_client_ids: list of string, Client IDs allowed to call the method.
    """
    self.__name = name
    self.__path = path
    self.__http_method = http_method
    self.__cache_control = cache_control
    self.__scopes = scopes
    self.__audiences = audiences
    self.__allowed_client_ids = allowed_client_ids

  def __safe_name(self, method_name):
    """Restrict method name to a-zA-Z0-9, first char lowercase."""


    safe_name = re.sub('[^\.a-zA-Z0-9]', '', method_name)

    return safe_name[0:1].lower() + safe_name[1:]

  @property
  def name(self):
    """Method name as specified in decorator or derived."""
    return self.__name

  @property
  def path(self):
    """Deprecated: path portion of the URL to the method."""


    logging.warning('_MethodInfopath property is deprecated.  '
                    'Use the get_path method instead.')
    return self.__path

  def get_path(self, api_info):
    """Get the path portion of the URL to the method (for RESTful methods).

    Request path can be specified in the method, and it could have a base
    path prepended to it.

    Args:
      api_info: API information for this API, possibly including a base path.
        This is the api_info property on the class that's been annotated for
        this API.

    Returns:
      This method's request path (not including the http://.../_ah/api/ prefix).
    """
    path = self.__path or ''
    if path and path[0] == '/':

      path = path[1:]
    else:

      if api_info.path:
        path = '%s%s%s' % (api_info.path, '/' if path else '', path)

    return path

  @property
  def http_method(self):
    """HTTP method supported by the method (e.g. GET, POST)."""
    return self.__http_method

  @property
  def cache_control(self):
    """Cache control setting for the API method."""
    return self.__cache_control

  @property
  def scopes(self):
    """List of scopes for the API method."""
    return self.__scopes

  @property
  def audiences(self):
    """List of audiences for the API method."""
    return self.__audiences

  @property
  def allowed_client_ids(self):
    """List of allowed client IDs for the API method."""
    return self.__allowed_client_ids

  def method_id(self, api_info):
    """Computed method name."""



    if api_info.resource_name:
      resource_part = '.%s' % self.__safe_name(api_info.resource_name)
    else:
      resource_part = ''
    return '%s%s.%s' % (self.__safe_name(api_info.name), resource_part,
                        self.__safe_name(self.name))


@util.positional(2)
def method(request_message=message_types.VoidMessage,
           response_message=message_types.VoidMessage,
           name=None,
           path=None,
           http_method='POST',
           cache_control=None,
           scopes=None,
           audiences=None,
           allowed_client_ids=None):
  """Decorate a ProtoRPC Method for use by the framework above.

  This decorator can be used to specify a method name, path, http method,
  cache control, scopes, audiences, and client ids

  Sample usage:
    @api_config.method(RequestMessage, ResponseMessage,
                       name='insert', http_method='PUT')
    def greeting_insert(request):
      ...
      return response

  Args:
    request_message: Message type of expected request.
    response_message: Message type of expected response.
    name: string, Name of the method, prepended with <apiname>. to make it
      unique. (Default: python method name)
    path: string, Path portion of the URL to the method, for RESTful methods.
    http_method: string, HTTP method supported by the method. (Default: POST)
    cache_control: CacheControl, Cache settings for the API method.
    scopes: list of string, OAuth2 token must contain one of these scopes.
    audiences: list of string, IdToken must contain one of these audiences.
    allowed_client_ids: list of string, Client IDs allowed to call the method.
      Currently limited to 5.  If None, no calls will be allowed.

  Returns:
    'apiserving_method_wrapper' function.

  Raises:
    ValueError: if more than 5 allowed_client_ids are specified.
    TypeError: if the request_type or response_type parameters are not
      proper subclasses of messages.Message.
  """


  DEFAULT_HTTP_METHOD = 'POST'

  def check_type(setting, allowed_type, name, allow_none=True):
    """Verify that the setting is of the allowed type or raise TypeError.

    Args:
      setting: The setting to check.
      allowed_type: The allowed type.
      name: Name of the setting, added to the exception.
      allow_none: If set, None is also allowed.

    Raises:
      TypeError: if setting is not of the allowed type.

    Returns:
      The setting, for convenient use in assignment.
    """
    if (setting is None and allow_none or
        isinstance(setting, allowed_type)):
      return setting
    raise TypeError('%s is not of type %s' % (name, allowed_type.__name__))

  def apiserving_method_decorator(api_method):
    """Decorator for ProtoRPC method that configures Google's API server.

    Args:
      api_method: Original method being wrapped.

    Returns:
      Function responsible for actual invocation.
      Assigns the following attributes to invocation function:
        remote: Instance of RemoteInfo, contains remote method information.
        remote.request_type: Expected request type for remote method.
        remote.response_type: Response type returned from remote method.
        method_info: Instance of _MethodInfo, api method configuration.
      It is also assigned attributes corresponding to the aforementioned kwargs.

    Raises:
      TypeError: if the request_type or response_type parameters are not
        proper subclasses of messages.Message.
    """
    remote_decorator = remote.method(request_message, response_message)
    remote_method = remote_decorator(api_method)

    def invoke_remote(service_instance, request):


      users_id_token._maybe_set_current_user_vars(
          invoke_remote, api_info=getattr(service_instance, 'api_info', None))

      return remote_method(service_instance, request)

    invoke_remote.remote = remote_method.remote
    invoke_remote.method_info = _MethodInfo(
        name=name or api_method.__name__, path=path or '',
        http_method=http_method or DEFAULT_HTTP_METHOD,
        cache_control=cache_control, scopes=scopes, audiences=audiences,
        allowed_client_ids=allowed_client_ids)
    invoke_remote.__name__ = invoke_remote.method_info.name
    return invoke_remote

  check_type(cache_control, CacheControl, 'cache_control')
  _CheckListType(scopes, basestring, 'scopes')
  _CheckListType(audiences, basestring, 'audiences')
  _CheckListType(allowed_client_ids, basestring, 'allowed_client_ids')
  if allowed_client_ids is not None and len(allowed_client_ids) > 5:
    raise ValueError('allowed_client_ids must have 5 or fewer entries.')
  return apiserving_method_decorator


class ApiConfigGenerator(object):
  """Generates an API configuration from a ProtoRPC service.

  Example:

    class HelloRequest(messages.Message):
      my_name = messages.StringField(1, required=True)

    class HelloResponse(messages.Message):
      hello = messages.StringField(1, required=True)

    class HelloService(remote.Service):

      @remote.method(HelloRequest, HelloResponse)
      def hello(self, request):
        return HelloResponse(hello='Hello there, %s!' %
                             request.my_name)

    api_config = ApiConfigGenerator().pretty_print_config_to_json(HelloService)

  The resulting api_config will be a JSON document describing the API
  implemented by HelloService.
  """




  __NO_BODY = 1
  __BODY_ONLY = 2


  __FIELD_TO_PARAM_TYPE_MAP = {
      messages.IntegerField: 'int64',
      messages.FloatField: 'double',
      messages.BooleanField: 'boolean',
      messages.BytesField: 'string',
      messages.StringField: 'string',
      messages.MessageField: 'object',
      messages.EnumField: 'string',
  }

  __DEFAULT_PARAM_TYPE = 'string'

  def __init__(self):
    self.__parser = message_parser.MessageTypeToJsonSchema()


    self.__request_schema = {}


    self.__response_schema = {}


    self.__id_from_name = {}

  def __get_request_kind(self, method_info):
    """Categorize the type of the request.

    Args:
      method_info: _MethodInfo, method information.

    Returns:
      The kind of request.
    """
    if method_info.http_method in ['GET', 'DELETE']:
      return self.__NO_BODY
    else:
      return self.__BODY_ONLY

  def __params_descriptor(self, message_type, request_kind, path):
    """Describe the parameters of a method.

    Args:
      message_type: messages.Message class, Message with parameters to describe.
      request_kind: The type of request being made.
      path: string, HTTP path to method.

    Returns:
      A tuple (dict, list of string): Descriptor of the parameters, Order of the
        parameters

    Raises:
      ValueError: if the method path and request required fields do not match
    """
    params = {}
    param_order = []

    for field in sorted(message_type.all_fields(), key=lambda f: f.number):
      descriptor = {}
      required = field.required
      if '{%s}' % field.name in path:
        required = True
      elif request_kind != self.__NO_BODY:

        continue

      if required:
        param_order.append(field.name)
        descriptor['required'] = True


      param_type = self.__FIELD_TO_PARAM_TYPE_MAP.get(
          type(field), self.__DEFAULT_PARAM_TYPE)
      descriptor['type'] = param_type

      if field.default:
        if isinstance(field, messages.EnumField):
          descriptor['default'] = str(field.default)
        else:
          descriptor['default'] = field.default

      if field.repeated:
        descriptor['repeated'] = True

      if isinstance(field, messages.EnumField):
        enum_descriptor = {}
        for enum_value in field.type.to_dict().keys():
          enum_descriptor[enum_value] = {'backendValue': enum_value}

        descriptor['enum'] = enum_descriptor

      params[field.name] = descriptor

    return params, param_order

  def __request_message_descriptor(self, request_kind, message_type, method_id,
                                   path):
    """Describes the parameters and body of the request.

    Args:
      request_kind: The type of request being made.
      message_type: messages.Message class, The message to describe.
      method_id: string, Unique method identifier (e.g. 'myapi.items.method')
      path: string, HTTP path to method.

    Returns:
      Dictionary describing the request.

    Raises:
      ValueError: if the method path and request required fields do not match
    """
    descriptor = {}

    params, param_order = self.__params_descriptor(message_type, request_kind,
                                                   path)

    if (request_kind == self.__NO_BODY or
        message_type == message_types.VoidMessage()):
      descriptor['body'] = 'empty'
    else:
      descriptor['body'] = 'autoTemplate(backendRequest)'
      descriptor['bodyName'] = 'resource'
      self.__request_schema[method_id] = self.__parser.add_message(
          message_type.__class__)

    if params:
      descriptor['parameters'] = params

    if param_order:
      descriptor['parameterOrder'] = param_order

    return descriptor

  def __response_message_descriptor(self, message_type, method_id,
                                    cache_control):
    """Describes the response.

    Args:
      message_type: messages.Message class, The message to describe.
      method_id: string, Unique method identifier (e.g. 'myapi.items.method')
      cache_control: CacheControl, Cache settings for the API method.

    Returns:
      Dictionary describing the response.
    """
    descriptor = {}

    self.__parser.add_message(message_type.__class__)
    if message_type == message_types.VoidMessage():
      descriptor['body'] = 'empty'
    else:
      descriptor['body'] = 'autoTemplate(backendResponse)'
      descriptor['bodyName'] = 'resource'
      self.__response_schema[method_id] = self.__parser.ref_for_message_type(
          message_type.__class__)

    if cache_control is not None:
      descriptor['cacheControl'] = {
          'type': cache_control.directive,
          'maxAge': cache_control.max_age_seconds,
      }

    return descriptor

  def __method_descriptor(self, service, service_name, method_info,
                          protorpc_method_name, protorpc_method_info):
    """Describes a method.

    Args:
      service: endpoints.Service, Implementation of the API as a service.
      service_name: string, Name of the service.
      method_info: _MethodInfo, Configuration for the method.
      protorpc_method_name: string, Name of the method as given in the
        ProtoRPC implementation.
      protorpc_method_info: protorpc.remote._RemoteMethodInfo, ProtoRPC
        description of the method.

    Returns:
      Dictionary describing the method.

    Raises:
      ValueError: if the method path and request required fields do not match
    """
    descriptor = {}

    request_message_type = protorpc_method_info.remote.request_type()
    request_kind = self.__get_request_kind(method_info)
    remote_method = protorpc_method_info.remote

    descriptor['path'] = method_info.get_path(service.api_info)
    descriptor['httpMethod'] = method_info.http_method
    descriptor['rosyMethod'] = '%s.%s' % (service_name, protorpc_method_name)
    descriptor['request'] = self.__request_message_descriptor(
        request_kind, request_message_type,
        method_info.method_id(service.api_info),
        descriptor['path'])
    descriptor['response'] = self.__response_message_descriptor(
        remote_method.response_type(), method_info.method_id(service.api_info),
        method_info.cache_control)




    scopes = (method_info.scopes
              if method_info.scopes is not None
              else service.api_info.scopes)
    if scopes:
      descriptor['scopes'] = scopes
    audiences = (method_info.audiences
                 if method_info.audiences is not None
                 else service.api_info.audiences)
    if audiences:
      descriptor['audiences'] = audiences
    allowed_client_ids = (method_info.allowed_client_ids
                          if method_info.allowed_client_ids is not None
                          else service.api_info.allowed_client_ids)
    if allowed_client_ids:
      descriptor['clientIds'] = allowed_client_ids

    if remote_method.method.__doc__:
      descriptor['description'] = remote_method.method.__doc__

    return descriptor

  def __schema_descriptor(self, service_name, protorpc_methods):
    """Descriptor for the all the JSON Schema used.

    Args:
      service_name: string, Name of the service.
      protorpc_methods: dict, Map of protorpc_method_name to
        protorpc.remote._RemoteMethodInfo.

    Returns:
      Dictionary containing all the JSON Schema used in the service.
    """
    methods_desc = {}

    for protorpc_method_name in protorpc_methods.iterkeys():
      method_id = self.__id_from_name[protorpc_method_name]

      request_response = {}

      request_schema_id = self.__request_schema.get(method_id)
      if request_schema_id:
        request_response['request'] = {
            '$ref': request_schema_id
            }

      response_schema_id = self.__response_schema.get(method_id)
      if response_schema_id:
        request_response['response'] = {
            '$ref': response_schema_id
            }

      rosy_method = '%s.%s' % (service_name, protorpc_method_name)
      methods_desc[rosy_method] = request_response

    descriptor = {
        'methods': methods_desc,
        'schemas': self.__parser.schemas(),
        }

    return descriptor

  def __api_descriptor(self, service, hostname=None):
    """Builds a description of an API.

    Args:
      service: protorpc.remote.Service, Implementation of the API as a service.
      hostname: string, Hostname of the API, to override the value set on the
        current service. Defaults to None.

    Returns:
      A dictionary that can be deserialized into JSON and stored as an API
      description document.

    Raises:
      ValueError: if any method path and request required fields do not match
    """
    descriptor = self.get_descriptor_defaults(service, hostname=hostname)

    description = service.api_info.description or service.__doc__
    if description:
      descriptor['description'] = description

    method_map = {}

    protorpc_methods = service.all_remote_methods()
    for protorpc_meth_name, protorpc_meth_info in protorpc_methods.iteritems():
      method_info = getattr(protorpc_meth_info, 'method_info', None)

      if method_info is None:
        continue
      method_id = method_info.method_id(service.api_info)
      self.__id_from_name[protorpc_meth_name] = method_id
      method_map[method_id] = self.__method_descriptor(
          service, service.__name__, method_info,
          protorpc_meth_name, protorpc_meth_info)

    if method_map:
      descriptor['methods'] = method_map
      descriptor['descriptor'] = self.__schema_descriptor(
          service.__name__, protorpc_methods)

    return descriptor

  def get_descriptor_defaults(self, service, hostname=None):
    """Gets a default configuration for a service.

    Args:
      service: protorpc.remote.Service, implementation of the API as a service.
      hostname: string, Hostname of the API, to override the value set on the
        current service. Defaults to None.

    Returns:
      A dictionary with the default configuration.
    """
    hostname = hostname or service.api_info.hostname
    return {
        'extends': 'thirdParty.api',
        'root': 'https://%s/_ah/api' % hostname,
        'name': service.api_info.name,
        'version': service.api_info.version,
        'defaultVersion': True,
        'abstract': False,
        'adapter': {
            'bns': 'https://%s/_ah/spi' % hostname,
            'type': 'lily'
        }
    }

  def pretty_print_config_to_json(self, service, hostname=None):
    """Description of a protorpc.remote.Service in API format.

    Args:
      service: protorpc.remote.Service, Implementation of the API as a service.
      hostname: string, Hostname of the API, to override the value set on the
        current service. Defaults to None.

    Returns:
      string, The API descriptor document as JSON.

    Raises:
      ValueError: if any method path and request required fields do not match
    """
    descriptor = self.__api_descriptor(service, hostname=hostname)
    return json.dumps(descriptor, sort_keys=True, indent=2)
