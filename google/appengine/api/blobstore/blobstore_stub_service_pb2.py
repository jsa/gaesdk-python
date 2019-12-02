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




import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
import google
from google.net.proto2.python.public import descriptor as _descriptor
from google.net.proto2.python.public import message as _message
from google.net.proto2.python.public import reflection as _reflection
from google.net.proto2.python.public import symbol_database as _symbol_database
import abc
import sys
try:
  __import__('google.net.rpc.python.proto_python_api_2_stub')
  __import__('google.net.rpc.python.pywraprpc')
  proto_python_api_2_stub = sys.modules.get('google.net.rpc.python.proto_python_api_2_stub')
  pywraprpc = sys.modules.get('google.net.rpc.python.pywraprpc')
  _client_stub_base_class = proto_python_api_2_stub.Stub
except ImportError:
  _client_stub_base_class = object
try:
  __import__('google.net.rpc.python.rpcserver')
  rpcserver = sys.modules.get('google.net.rpc.python.rpcserver')
  _server_stub_base_class = rpcserver.BaseRpcServer
except ImportError:
  _server_stub_base_class = object


_sym_db = _symbol_database.Default()


from google.appengine.api import api_base_pb2 as google_dot_apphosting_dot_api_dot_api__base__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='apphosting/api/blobstore/blobstore_stub_service.proto',
  package='apphosting',
  syntax='proto2',
  serialized_options=_b('\n\"com.google.appengine.api.blobstoreB\026BlobstoreStubServicePb'),
  serialized_pb=_b('\n5apphosting/api/blobstore/blobstore_stub_service.proto\x12\napphosting\x1a\x1d\x61pphosting/api/api_base.proto\"5\n\x10StoreBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\x89\x01\n\x19SetBlobStorageTypeRequest\x12G\n\x0cstorage_type\x18\x01 \x02(\x0e\x32\x31.apphosting.SetBlobStorageTypeRequest.StorageType\"#\n\x0bStorageType\x12\n\n\x06MEMORY\x10\x00\x12\x08\n\x04\x46ILE\x10\x01\x32\xba\x01\n\x14\x42lobstoreStubService\x12G\n\tStoreBlob\x12\x1c.apphosting.StoreBlobRequest\x1a\x1a.apphosting.base.VoidProto\"\x00\x12Y\n\x12SetBlobStorageType\x12%.apphosting.SetBlobStorageTypeRequest\x1a\x1a.apphosting.base.VoidProto\"\x00\x42<\n\"com.google.appengine.api.blobstoreB\x16\x42lobstoreStubServicePb')
  ,
  dependencies=[google_dot_apphosting_dot_api_dot_api__base__pb2.DESCRIPTOR,])



_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE = _descriptor.EnumDescriptor(
  name='StorageType',
  full_name='apphosting.SetBlobStorageTypeRequest.StorageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MEMORY', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FILE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=258,
  serialized_end=293,
)
_sym_db.RegisterEnumDescriptor(_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE)


_STOREBLOBREQUEST = _descriptor.Descriptor(
  name='StoreBlobRequest',
  full_name='apphosting.StoreBlobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.StoreBlobRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='apphosting.StoreBlobRequest.content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=153,
)


_SETBLOBSTORAGETYPEREQUEST = _descriptor.Descriptor(
  name='SetBlobStorageTypeRequest',
  full_name='apphosting.SetBlobStorageTypeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='storage_type', full_name='apphosting.SetBlobStorageTypeRequest.storage_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=156,
  serialized_end=293,
)

_SETBLOBSTORAGETYPEREQUEST.fields_by_name['storage_type'].enum_type = _SETBLOBSTORAGETYPEREQUEST_STORAGETYPE
_SETBLOBSTORAGETYPEREQUEST_STORAGETYPE.containing_type = _SETBLOBSTORAGETYPEREQUEST
DESCRIPTOR.message_types_by_name['StoreBlobRequest'] = _STOREBLOBREQUEST
DESCRIPTOR.message_types_by_name['SetBlobStorageTypeRequest'] = _SETBLOBSTORAGETYPEREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StoreBlobRequest = _reflection.GeneratedProtocolMessageType('StoreBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOREBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_stub_service_pb2'

  })
_sym_db.RegisterMessage(StoreBlobRequest)

SetBlobStorageTypeRequest = _reflection.GeneratedProtocolMessageType('SetBlobStorageTypeRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETBLOBSTORAGETYPEREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_stub_service_pb2'

  })
_sym_db.RegisterMessage(SetBlobStorageTypeRequest)


DESCRIPTOR._options = None

_BLOBSTORESTUBSERVICE = _descriptor.ServiceDescriptor(
  name='BlobstoreStubService',
  full_name='apphosting.BlobstoreStubService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=296,
  serialized_end=482,
  methods=[
  _descriptor.MethodDescriptor(
    name='StoreBlob',
    full_name='apphosting.BlobstoreStubService.StoreBlob',
    index=0,
    containing_service=None,
    input_type=_STOREBLOBREQUEST,
    output_type=google_dot_apphosting_dot_api_dot_api__base__pb2._VOIDPROTO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetBlobStorageType',
    full_name='apphosting.BlobstoreStubService.SetBlobStorageType',
    index=1,
    containing_service=None,
    input_type=_SETBLOBSTORAGETYPEREQUEST,
    output_type=google_dot_apphosting_dot_api_dot_api__base__pb2._VOIDPROTO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_BLOBSTORESTUBSERVICE)

DESCRIPTOR.services_by_name['BlobstoreStubService'] = _BLOBSTORESTUBSERVICE



class BlobstoreStubServiceStub(object):
  """Makes Stubby RPC calls to a BlobstoreStubService server."""

  __metaclass__ = abc.ABCMeta

  __slots__ = ()

  @abc.abstractmethod
  def StoreBlob(self, request, rpc=None, callback=None, response=None):
    """Make a StoreBlob RPC call.

    Args:
      request: a StoreBlobRequest instance.
      rpc: Optional RPC instance to use for the call.
      callback: Optional final callback. Will be called as
          callback(rpc, result) when the rpc completes. If None, the
          call is synchronous.
      response: Optional ProtocolMessage to be filled in with response.

    Returns:
      The google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto if callback is None. Otherwise, returns None.
    """
    raise NotImplementedError()

  @abc.abstractmethod
  def SetBlobStorageType(self, request, rpc=None, callback=None, response=None):
    """Make a SetBlobStorageType RPC call.

    Args:
      request: a SetBlobStorageTypeRequest instance.
      rpc: Optional RPC instance to use for the call.
      callback: Optional final callback. Will be called as
          callback(rpc, result) when the rpc completes. If None, the
          call is synchronous.
      response: Optional ProtocolMessage to be filled in with response.

    Returns:
      The google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto if callback is None. Otherwise, returns None.
    """
    raise NotImplementedError()


class _BlobstoreStubService_ClientBaseStub(
    BlobstoreStubServiceStub, _client_stub_base_class):
  """Makes Stubby RPC calls to a BlobstoreStubService server."""

  __slots__ = (
      '_protorpc_StoreBlob', '_full_name_StoreBlob',
      '_protorpc_SetBlobStorageType', '_full_name_SetBlobStorageType',
  )

  def __init__(self, rpc_stub, rpc_factory=None):
    super(_BlobstoreStubService_ClientBaseStub, self).__init__(
        None, inject_stub=rpc_stub, rpc_factory=rpc_factory)

    self._protorpc_StoreBlob = pywraprpc.RPC()
    self._full_name_StoreBlob = self._stub.GetFullMethodName(
        'StoreBlob')

    self._protorpc_SetBlobStorageType = pywraprpc.RPC()
    self._full_name_SetBlobStorageType = self._stub.GetFullMethodName(
        'SetBlobStorageType')

  def StoreBlob(self, request, rpc=None, callback=None, response=None):
    """Make a StoreBlob RPC call.

    Args:
      request: a StoreBlobRequest instance.
      rpc: Optional RPC instance to use for the call.
      callback: Optional final callback. Will be called as
          callback(rpc, result) when the rpc completes. If None, the
          call is synchronous.
      response: Optional ProtocolMessage to be filled in with response.

    Returns:
      The google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto if callback is None. Otherwise, returns None.
    """

    if response is None:
      response = google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto
    return self._MakeCall(rpc,
                          self._full_name_StoreBlob,
                          'StoreBlob',
                          request,
                          response,
                          callback,
                          self._protorpc_StoreBlob,
                          package_name='apphosting')

  def SetBlobStorageType(self, request, rpc=None, callback=None, response=None):
    """Make a SetBlobStorageType RPC call.

    Args:
      request: a SetBlobStorageTypeRequest instance.
      rpc: Optional RPC instance to use for the call.
      callback: Optional final callback. Will be called as
          callback(rpc, result) when the rpc completes. If None, the
          call is synchronous.
      response: Optional ProtocolMessage to be filled in with response.

    Returns:
      The google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto if callback is None. Otherwise, returns None.
    """

    if response is None:
      response = google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto
    return self._MakeCall(rpc,
                          self._full_name_SetBlobStorageType,
                          'SetBlobStorageType',
                          request,
                          response,
                          callback,
                          self._protorpc_SetBlobStorageType,
                          package_name='apphosting')


class _BlobstoreStubService_ClientStub(_BlobstoreStubService_ClientBaseStub):
  __slots__ = ('_params',)
  def __init__(self, rpc_stub_parameters, service_name, rpc_factory=None):
    if service_name is None:
      service_name = 'BlobstoreStubService'
    stub = pywraprpc.RPC_GenericStub(service_name, rpc_stub_parameters)
    super(_BlobstoreStubService_ClientStub, self).__init__(stub, rpc_factory=rpc_factory)
    self._params = rpc_stub_parameters


class _BlobstoreStubService_RPC2ClientStub(_BlobstoreStubService_ClientBaseStub):
  __slots__ = ()
  def __init__(self, server, channel, service_name, rpc_factory=None):
    if service_name is None:
      service_name = 'BlobstoreStubService'
    if channel is None:
      if server is None:
        raise RuntimeError('Invalid argument combination to create a stub')
      channel = pywraprpc.NewClientChannel(server)
    elif channel.version() == 1:
      raise RuntimeError('Expecting an RPC2 channel to create the stub')
    stub = pywraprpc.RPC_GenericStub(service_name, channel)
    super(_BlobstoreStubService_RPC2ClientStub, self).__init__(stub, rpc_factory=rpc_factory)


class BlobstoreStubService(_server_stub_base_class):
  """Base class for BlobstoreStubService Stubby servers."""

  @classmethod
  def _MethodSignatures(cls):
    """Returns a dict of {<method-name>: (<request-type>, <response-type>)}."""
    return {
      'StoreBlob': (StoreBlobRequest, google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto),
      'SetBlobStorageType': (SetBlobStorageTypeRequest, google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto),
      }

  @classmethod
  def _StreamMethodSignatures(cls):
    """Returns a dict of {<method-name>: (<request-type>, <stream-type>, <response-type>)}."""
    return {
      }

  def __init__(self, *args, **kwargs):
    """Creates a Stubby RPC server.

    The arguments to this constructor are the same as the arguments to
    BaseRpcServer.__init__ in rpcserver.py *MINUS* export_name. This
    constructor passes its own value for export_name to
    BaseRpcServer.__init__, so callers of this constructor should only
    pass to this constructor values corresponding to
    BaseRpcServer.__init__'s remaining arguments.
    """
    if _server_stub_base_class is object:
      raise NotImplementedError('Add //net/rpc/python:rpcserver as a '
                                'dependency for Stubby server support.')
    _server_stub_base_class.__init__(self, 'apphosting.BlobstoreStubService', *args, **kwargs)

  @staticmethod
  def NewStub(rpc_stub_parameters, service_name=None, rpc_factory=None):
    """USE NewRPC2Stub INSTEAD."""
    if _client_stub_base_class is object:
      raise RuntimeError('Add //net/rpc/python as a dependency to use Stubby')
    return _BlobstoreStubService_ClientStub(
        rpc_stub_parameters, service_name, rpc_factory=rpc_factory)

  @staticmethod
  def NewRPC2Stub(
      server=None, channel=None, service_name=None, rpc_factory=None):
    """Creates a new BlobstoreStubService Stubby2 client stub.

    Args:
      server: host:port or bns address (favor passing a channel instead).
      channel: directly use a channel to create a stub. Will ignore server
          argument if this is specified.
      service_name: the service name used by the Stubby server.
      rpc_factory: the rpc factory to use if no rpc argument is specified.

    Returns:
     A BlobstoreStubServiceStub to be used to invoke RPCs.
    """

    if _client_stub_base_class is object:
      raise RuntimeError('Add //net/rpc/python:proto_python_api_2_stub (or maybe //net/rpc/python:proto_python_api_1_stub, but eww and b/67959631) as a dependency to create Stubby stubs')
    return _BlobstoreStubService_RPC2ClientStub(
        server, channel, service_name, rpc_factory=rpc_factory)

  def StoreBlob(self, rpc, request, response):
    """Handles a StoreBlob RPC call. You should override this.

    Args:
      rpc: a Stubby RPC object
      request: a StoreBlobRequest that contains the client request
      response: a google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto that should be modified to send the response
    """
    raise NotImplementedError()


  def SetBlobStorageType(self, rpc, request, response):
    """Handles a SetBlobStorageType RPC call. You should override this.

    Args:
      rpc: a Stubby RPC object
      request: a SetBlobStorageTypeRequest that contains the client request
      response: a google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto that should be modified to send the response
    """
    raise NotImplementedError()

  def _AddMethodAttributes(self):
    """Sets attributes on Python RPC handlers.

    See BaseRpcServer in rpcserver.py for details.
    """
    rpcserver._GetHandlerDecorator(
        getattr(self.StoreBlob, '__func__'),
        StoreBlobRequest,
        google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto,
        None,
        'INTEGRITY')
    rpcserver._GetHandlerDecorator(
        getattr(self.SetBlobStorageType, '__func__'),
        SetBlobStorageTypeRequest,
        google_dot_apphosting_dot_api_dot_api__base__pb2.VoidProto,
        None,
        'INTEGRITY')


