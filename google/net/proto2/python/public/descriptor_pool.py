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


"""Provides DescriptorPool to use as a container for proto2 descriptors.

The DescriptorPool is used in conjection with a DescriptorDatabase to maintain
a collection of protocol buffer descriptors for use when dynamically creating
message types at runtime.

For most applications protocol buffers should be used via modules generated by
the protocol buffer compiler tool. This should only be used when the type of
protocol buffers used in an application or library cannot be predetermined.

Below is a straightforward example on how to use this class:

  pool = DescriptorPool()
  file_descriptor_protos = [ ... ]
  for file_descriptor_proto in file_descriptor_protos:
    pool.Add(file_descriptor_proto)
  my_message_descriptor = pool.FindMessageTypeByName('some.package.MessageType')

The message descriptor can be used in conjunction with the message_factory
module in order to create a protocol buffer class that can be encoded and
decoded.

If you want to get a Python class for the specified proto, use the
helper functions inside google.net.proto2.python.public.message_factory
directly instead of this class.
"""



import collections
import warnings

from google.net.proto2.python.public import descriptor
from google.net.proto2.python.public import descriptor_database
from google.net.proto2.python.public import text_encoding


_USE_C_DESCRIPTORS = descriptor._USE_C_DESCRIPTORS


def _NormalizeFullyQualifiedName(name):
  """Remove leading period from fully-qualified type name.

  Due to b/13860351 in descriptor_database.py, types in the root namespace are
  generated with a leading period. This function removes that prefix.

  Args:
    name: A str, the fully-qualified symbol name.

  Returns:
    A str, the normalized fully-qualified symbol name.
  """
  return name.lstrip('.')


def _OptionsOrNone(descriptor_proto):
  """Returns the value of the field `options`, or None if it is not set."""
  if descriptor_proto.HasField('options'):
    return descriptor_proto.options
  else:
    return None


def _IsMessageSetExtension(field):
  return (field.is_extension and
          field.containing_type.has_options and
          field.containing_type.GetOptions().message_set_wire_format and
          field.type == descriptor.FieldDescriptor.TYPE_MESSAGE and
          field.label == descriptor.FieldDescriptor.LABEL_OPTIONAL)


class DescriptorPool(object):
  """A collection of protobufs dynamically constructed by descriptor protos."""

  if _USE_C_DESCRIPTORS:

    def __new__(cls, descriptor_db=None):

      return descriptor._message.DescriptorPool(descriptor_db)

  def __init__(self, descriptor_db=None):
    """Initializes a Pool of proto buffs.

    The descriptor_db argument to the constructor is provided to allow
    specialized file descriptor proto lookup code to be triggered on demand. An
    example would be an implementation which will read and compile a file
    specified in a call to FindFileByName() and not require the call to Add()
    at all. Results from this database will be cached internally here as well.

    Args:
      descriptor_db: A secondary source of file descriptors.
    """

    self._internal_db = descriptor_database.DescriptorDatabase()
    self._descriptor_db = descriptor_db
    self._descriptors = {}
    self._enum_descriptors = {}
    self._service_descriptors = {}
    self._file_descriptors = {}
    self._toplevel_extensions = {}


    self._file_desc_by_toplevel_extension = {}
    self._top_enum_values = {}



    self._extensions_by_name = collections.defaultdict(dict)
    self._extensions_by_number = collections.defaultdict(dict)

  def _CheckConflictRegister(self, desc, desc_name, file_name):
    """Check if the descriptor name conflicts with another of the same name.

    Args:
      desc: Descriptor of a message, enum, service, extension or enum value.
      desc_name: the full name of desc.
      file_name: The file name of descriptor.
    """
    for register, descriptor_type in [
        (self._descriptors, descriptor.Descriptor),
        (self._enum_descriptors, descriptor.EnumDescriptor),
        (self._service_descriptors, descriptor.ServiceDescriptor),
        (self._toplevel_extensions, descriptor.FieldDescriptor),
        (self._top_enum_values, descriptor.EnumValueDescriptor)]:
      if desc_name in register:
        old_desc = register[desc_name]
        if isinstance(old_desc, descriptor.EnumValueDescriptor):
          old_file = old_desc.type.file.name
        else:
          old_file = old_desc.file.name

        if not isinstance(desc, descriptor_type) or (
            old_file != file_name):
          warn_msg = ('Conflict register for file "' + file_name +
                      '": ' + desc_name +
                      ' is already defined in file "' +
                      old_file + '"')
          if isinstance(desc, descriptor.EnumValueDescriptor):
            warn_msg += ('\nNote: enum values appear as '
                         'siblings of the enum type instead of '
                         'children of it.')
          warnings.warn(warn_msg, RuntimeWarning)

        return

  def Add(self, file_desc_proto):
    """Adds the FileDescriptorProto and its types to this pool.

    Args:
      file_desc_proto: The FileDescriptorProto to add.
    """

    self._internal_db.Add(file_desc_proto)

  def AddSerializedFile(self, serialized_file_desc_proto):
    """Adds the FileDescriptorProto and its types to this pool.

    Args:
      serialized_file_desc_proto: A bytes string, serialization of the
        FileDescriptorProto to add.
    """


    from google.net.proto2.python.internal import descriptor_bootstrap_pb2
    file_desc_proto = descriptor_bootstrap_pb2.FileDescriptorProto.FromString(
        serialized_file_desc_proto)
    self.Add(file_desc_proto)

  def AddDescriptor(self, desc):
    """Adds a Descriptor to the pool, non-recursively.

    If the Descriptor contains nested messages or enums, the caller must
    explicitly register them. This method also registers the FileDescriptor
    associated with the message.

    Args:
      desc: A Descriptor.
    """
    if not isinstance(desc, descriptor.Descriptor):
      raise TypeError('Expected instance of descriptor.Descriptor.')

    self._CheckConflictRegister(desc, desc.full_name, desc.file.name)

    self._descriptors[desc.full_name] = desc
    self._AddFileDescriptor(desc.file)

  def AddEnumDescriptor(self, enum_desc):
    """Adds an EnumDescriptor to the pool.

    This method also registers the FileDescriptor associated with the enum.

    Args:
      enum_desc: An EnumDescriptor.
    """

    if not isinstance(enum_desc, descriptor.EnumDescriptor):
      raise TypeError('Expected instance of descriptor.EnumDescriptor.')

    file_name = enum_desc.file.name
    self._CheckConflictRegister(enum_desc, enum_desc.full_name, file_name)
    self._enum_descriptors[enum_desc.full_name] = enum_desc




    if enum_desc.file.package:
      top_level = (enum_desc.full_name.count('.')
                   - enum_desc.file.package.count('.') == 1)
    else:
      top_level = enum_desc.full_name.count('.') == 0
    if top_level:
      file_name = enum_desc.file.name
      package = enum_desc.file.package
      for enum_value in enum_desc.values:
        full_name = _NormalizeFullyQualifiedName(
            '.'.join((package, enum_value.name)))
        self._CheckConflictRegister(enum_value, full_name, file_name)
        self._top_enum_values[full_name] = enum_value
    self._AddFileDescriptor(enum_desc.file)

  def AddServiceDescriptor(self, service_desc):
    """Adds a ServiceDescriptor to the pool.

    Args:
      service_desc: A ServiceDescriptor.
    """

    if not isinstance(service_desc, descriptor.ServiceDescriptor):
      raise TypeError('Expected instance of descriptor.ServiceDescriptor.')

    self._CheckConflictRegister(service_desc, service_desc.full_name,
                                service_desc.file.name)
    self._service_descriptors[service_desc.full_name] = service_desc

  def AddExtensionDescriptor(self, extension):
    """Adds a FieldDescriptor describing an extension to the pool.

    Args:
      extension: A FieldDescriptor.

    Raises:
      AssertionError: when another extension with the same number extends the
        same message.
      TypeError: when the specified extension is not a
        descriptor.FieldDescriptor.
    """
    if not (isinstance(extension, descriptor.FieldDescriptor) and
            extension.is_extension):
      raise TypeError('Expected an extension descriptor.')

    if extension.extension_scope is None:




      self._CheckConflictRegister(
          extension, extension.full_name, extension.file.name)

      self._toplevel_extensions[extension.full_name] = extension

    try:
      existing_desc = self._extensions_by_number[
          extension.containing_type][extension.number]
    except KeyError:
      pass
    else:
      if extension is not existing_desc:
        raise AssertionError(
            'Extensions "%s" and "%s" both try to extend message type "%s" '
            'with field number %d.' %
            (extension.full_name, existing_desc.full_name,
             extension.containing_type.full_name, extension.number))

    self._extensions_by_number[extension.containing_type][
        extension.number] = extension
    self._extensions_by_name[extension.containing_type][
        extension.full_name] = extension


    if _IsMessageSetExtension(extension):
      self._extensions_by_name[extension.containing_type][
          extension.message_type.full_name] = extension

  def AddFileDescriptor(self, file_desc):
    """Adds a FileDescriptor to the pool, non-recursively.

    If the FileDescriptor contains messages or enums, the caller must explicitly
    register them.

    Args:
      file_desc: A FileDescriptor.
    """

    self._AddFileDescriptor(file_desc)



    for extension in file_desc.extensions_by_name.values():
      self._file_desc_by_toplevel_extension[
          extension.full_name] = file_desc

  def _AddFileDescriptor(self, file_desc):
    """Adds a FileDescriptor to the pool, non-recursively.

    If the FileDescriptor contains messages or enums, the caller must explicitly
    register them.

    Args:
      file_desc: A FileDescriptor.
    """

    if not isinstance(file_desc, descriptor.FileDescriptor):
      raise TypeError('Expected instance of descriptor.FileDescriptor.')
    self._file_descriptors[file_desc.name] = file_desc

  def FindFileByName(self, file_name):
    """Gets a FileDescriptor by file name.

    Args:
      file_name: The path to the file to get a descriptor for.

    Returns:
      A FileDescriptor for the named file.

    Raises:
      KeyError: if the file cannot be found in the pool.
    """

    try:
      return self._file_descriptors[file_name]
    except KeyError:
      pass

    try:
      file_proto = self._internal_db.FindFileByName(file_name)
    except KeyError as error:
      if self._descriptor_db:
        file_proto = self._descriptor_db.FindFileByName(file_name)
      else:
        raise error
    if not file_proto:
      raise KeyError('Cannot find a file named %s' % file_name)
    return self._ConvertFileProtoToFileDescriptor(file_proto)

  def FindFileContainingSymbol(self, symbol):
    """Gets the FileDescriptor for the file containing the specified symbol.

    Args:
      symbol: The name of the symbol to search for.

    Returns:
      A FileDescriptor that contains the specified symbol.

    Raises:
      KeyError: if the file cannot be found in the pool.
    """

    symbol = _NormalizeFullyQualifiedName(symbol)
    try:
      return self._InternalFindFileContainingSymbol(symbol)
    except KeyError:
      pass

    try:

      self._FindFileContainingSymbolInDb(symbol)
      return self._InternalFindFileContainingSymbol(symbol)
    except KeyError:
      raise KeyError('Cannot find a file containing %s' % symbol)

  def _InternalFindFileContainingSymbol(self, symbol):
    """Gets the already built FileDescriptor containing the specified symbol.

    Args:
      symbol: The name of the symbol to search for.

    Returns:
      A FileDescriptor that contains the specified symbol.

    Raises:
      KeyError: if the file cannot be found in the pool.
    """
    try:
      return self._descriptors[symbol].file
    except KeyError:
      pass

    try:
      return self._enum_descriptors[symbol].file
    except KeyError:
      pass

    try:
      return self._service_descriptors[symbol].file
    except KeyError:
      pass

    try:
      return self._top_enum_values[symbol].type.file
    except KeyError:
      pass

    try:
      return self._file_desc_by_toplevel_extension[symbol]
    except KeyError:
      pass


    top_name, _, sub_name = symbol.rpartition('.')
    try:
      message = self.FindMessageTypeByName(top_name)
      assert (sub_name in message.extensions_by_name or
              sub_name in message.fields_by_name or
              sub_name in message.enum_values_by_name)
      return message.file
    except (KeyError, AssertionError):
      raise KeyError('Cannot find a file containing %s' % symbol)

  def FindMessageTypeByName(self, full_name):
    """Loads the named descriptor from the pool.

    Args:
      full_name: The full name of the descriptor to load.

    Returns:
      The descriptor for the named type.

    Raises:
      KeyError: if the message cannot be found in the pool.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._descriptors:
      self._FindFileContainingSymbolInDb(full_name)
    return self._descriptors[full_name]

  def FindEnumTypeByName(self, full_name):
    """Loads the named enum descriptor from the pool.

    Args:
      full_name: The full name of the enum descriptor to load.

    Returns:
      The enum descriptor for the named type.

    Raises:
      KeyError: if the enum cannot be found in the pool.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._enum_descriptors:
      self._FindFileContainingSymbolInDb(full_name)
    return self._enum_descriptors[full_name]

  def FindFieldByName(self, full_name):
    """Loads the named field descriptor from the pool.

    Args:
      full_name: The full name of the field descriptor to load.

    Returns:
      The field descriptor for the named field.

    Raises:
      KeyError: if the field cannot be found in the pool.
    """
    full_name = _NormalizeFullyQualifiedName(full_name)
    message_name, _, field_name = full_name.rpartition('.')
    message_descriptor = self.FindMessageTypeByName(message_name)
    return message_descriptor.fields_by_name[field_name]

  def FindOneofByName(self, full_name):
    """Loads the named oneof descriptor from the pool.

    Args:
      full_name: The full name of the oneof descriptor to load.

    Returns:
      The oneof descriptor for the named oneof.

    Raises:
      KeyError: if the oneof cannot be found in the pool.
    """
    full_name = _NormalizeFullyQualifiedName(full_name)
    message_name, _, oneof_name = full_name.rpartition('.')
    message_descriptor = self.FindMessageTypeByName(message_name)
    return message_descriptor.oneofs_by_name[oneof_name]

  def FindExtensionByName(self, full_name):
    """Loads the named extension descriptor from the pool.

    Args:
      full_name: The full name of the extension descriptor to load.

    Returns:
      A FieldDescriptor, describing the named extension.

    Raises:
      KeyError: if the extension cannot be found in the pool.
    """
    full_name = _NormalizeFullyQualifiedName(full_name)
    try:




      return self._toplevel_extensions[full_name]
    except KeyError:
      pass
    message_name, _, extension_name = full_name.rpartition('.')
    try:

      scope = self.FindMessageTypeByName(message_name)
    except KeyError:

      scope = self._FindFileContainingSymbolInDb(full_name)
    return scope.extensions_by_name[extension_name]

  def FindExtensionByNumber(self, message_descriptor, number):
    """Gets the extension of the specified message with the specified number.

    Extensions have to be registered to this pool by calling
    AddExtensionDescriptor.

    Args:
      message_descriptor: descriptor of the extended message.
      number: integer, number of the extension field.

    Returns:
      A FieldDescriptor describing the extension.

    Raises:
      KeyError: when no extension with the given number is known for the
        specified message.
    """
    return self._extensions_by_number[message_descriptor][number]

  def FindAllExtensions(self, message_descriptor):
    """Gets all the known extension of a given message.

    Extensions have to be registered to this pool by calling
    AddExtensionDescriptor.

    Args:
      message_descriptor: descriptor of the extended message.

    Returns:
      A list of FieldDescriptor describing the extensions.
    """
    return list(self._extensions_by_number[message_descriptor].values())

  def FindServiceByName(self, full_name):
    """Loads the named service descriptor from the pool.

    Args:
      full_name: The full name of the service descriptor to load.

    Returns:
      The service descriptor for the named service.

    Raises:
      KeyError: if the service cannot be found in the pool.
    """
    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._service_descriptors:
      self._FindFileContainingSymbolInDb(full_name)
    return self._service_descriptors[full_name]

  def _FindFileContainingSymbolInDb(self, symbol):
    """Finds the file in descriptor DB containing the specified symbol.

    Args:
      symbol: The name of the symbol to search for.

    Returns:
      A FileDescriptor that contains the specified symbol.

    Raises:
      KeyError: if the file cannot be found in the descriptor database.
    """
    try:
      file_proto = self._internal_db.FindFileContainingSymbol(symbol)
    except KeyError as error:
      if self._descriptor_db:
        file_proto = self._descriptor_db.FindFileContainingSymbol(symbol)
      else:
        raise error
    if not file_proto:
      raise KeyError('Cannot find a file containing %s' % symbol)
    return self._ConvertFileProtoToFileDescriptor(file_proto)

  def _ConvertFileProtoToFileDescriptor(self, file_proto):
    """Creates a FileDescriptor from a proto or returns a cached copy.

    This method also has the side effect of loading all the symbols found in
    the file into the appropriate dictionaries in the pool.

    Args:
      file_proto: The proto to convert.

    Returns:
      A FileDescriptor matching the passed in proto.
    """

    if file_proto.name not in self._file_descriptors:
      built_deps = list(self._GetDeps(file_proto.dependency))
      direct_deps = [self.FindFileByName(n) for n in file_proto.dependency]
      public_deps = [direct_deps[i] for i in file_proto.public_dependency]

      file_descriptor = descriptor.FileDescriptor(
          pool=self,
          name=file_proto.name,
          package=file_proto.package,
          syntax=file_proto.syntax,
          options=_OptionsOrNone(file_proto),
          serialized_pb=file_proto.SerializeToString(),
          dependencies=direct_deps,
          public_dependencies=public_deps)
      scope = {}





      for dependency in built_deps:
        scope.update(self._ExtractSymbols(
            dependency.message_types_by_name.values()))
        scope.update((_PrefixWithDot(enum.full_name), enum)
                     for enum in dependency.enum_types_by_name.values())

      for message_type in file_proto.message_type:
        message_desc = self._ConvertMessageDescriptor(
            message_type, file_proto.package, file_descriptor, scope,
            file_proto.syntax)
        file_descriptor.message_types_by_name[message_desc.name] = (
            message_desc)

      for enum_type in file_proto.enum_type:
        file_descriptor.enum_types_by_name[enum_type.name] = (
            self._ConvertEnumDescriptor(enum_type, file_proto.package,
                                        file_descriptor, None, scope, True))

      for index, extension_proto in enumerate(file_proto.extension):
        extension_desc = self._MakeFieldDescriptor(
            extension_proto, file_proto.package, index, file_descriptor,
            is_extension=True)
        extension_desc.containing_type = self._GetTypeFromScope(
            file_descriptor.package, extension_proto.extendee, scope)
        self._SetFieldType(extension_proto, extension_desc,
                           file_descriptor.package, scope)
        file_descriptor.extensions_by_name[extension_desc.name] = (
            extension_desc)
        self._file_desc_by_toplevel_extension[extension_desc.full_name] = (
            file_descriptor)

      for desc_proto in file_proto.message_type:
        self._SetAllFieldTypes(file_proto.package, desc_proto, scope)

      if file_proto.package:
        desc_proto_prefix = _PrefixWithDot(file_proto.package)
      else:
        desc_proto_prefix = ''

      for desc_proto in file_proto.message_type:
        desc = self._GetTypeFromScope(
            desc_proto_prefix, desc_proto.name, scope)
        file_descriptor.message_types_by_name[desc_proto.name] = desc

      for index, service_proto in enumerate(file_proto.service):
        file_descriptor.services_by_name[service_proto.name] = (
            self._MakeServiceDescriptor(service_proto, index, scope,
                                        file_proto.package, file_descriptor))

      self.Add(file_proto)
      self._file_descriptors[file_proto.name] = file_descriptor

    return self._file_descriptors[file_proto.name]

  def _ConvertMessageDescriptor(self, desc_proto, package=None, file_desc=None,
                                scope=None, syntax=None):
    """Adds the proto to the pool in the specified package.

    Args:
      desc_proto: The descriptor_pb2.DescriptorProto protobuf message.
      package: The package the proto should be located in.
      file_desc: The file containing this message.
      scope: Dict mapping short and full symbols to message and enum types.
      syntax: string indicating syntax of the file ("proto2" or "proto3")

    Returns:
      The added descriptor.
    """

    if package:
      desc_name = '.'.join((package, desc_proto.name))
    else:
      desc_name = desc_proto.name

    if file_desc is None:
      file_name = None
    else:
      file_name = file_desc.name

    if scope is None:
      scope = {}

    nested = [
        self._ConvertMessageDescriptor(
            nested, desc_name, file_desc, scope, syntax)
        for nested in desc_proto.nested_type]
    enums = [
        self._ConvertEnumDescriptor(enum, desc_name, file_desc, None,
                                    scope, False)
        for enum in desc_proto.enum_type]
    fields = [self._MakeFieldDescriptor(field, desc_name, index, file_desc)
              for index, field in enumerate(desc_proto.field)]
    extensions = [
        self._MakeFieldDescriptor(extension, desc_name, index, file_desc,
                                  is_extension=True)
        for index, extension in enumerate(desc_proto.extension)]
    oneofs = [
        descriptor.OneofDescriptor(desc.name, '.'.join((desc_name, desc.name)),
                                   index, None, [], desc.options)
        for index, desc in enumerate(desc_proto.oneof_decl)]
    extension_ranges = [(r.start, r.end) for r in desc_proto.extension_range]
    if extension_ranges:
      is_extendable = True
    else:
      is_extendable = False
    desc = descriptor.Descriptor(
        name=desc_proto.name,
        full_name=desc_name,
        filename=file_name,
        containing_type=None,
        fields=fields,
        oneofs=oneofs,
        nested_types=nested,
        enum_types=enums,
        extensions=extensions,
        options=_OptionsOrNone(desc_proto),
        is_extendable=is_extendable,
        extension_ranges=extension_ranges,
        file=file_desc,
        serialized_start=None,
        serialized_end=None,
        syntax=syntax)
    for nested in desc.nested_types:
      nested.containing_type = desc
    for enum in desc.enum_types:
      enum.containing_type = desc
    for field_index, field_desc in enumerate(desc_proto.field):
      if field_desc.HasField('oneof_index'):
        oneof_index = field_desc.oneof_index
        oneofs[oneof_index].fields.append(fields[field_index])
        fields[field_index].containing_oneof = oneofs[oneof_index]

    scope[_PrefixWithDot(desc_name)] = desc
    self._CheckConflictRegister(desc, desc.full_name, desc.file.name)
    self._descriptors[desc_name] = desc
    return desc

  def _ConvertEnumDescriptor(self, enum_proto, package=None, file_desc=None,
                             containing_type=None, scope=None, top_level=False):
    """Make a protobuf EnumDescriptor given an EnumDescriptorProto protobuf.

    Args:
      enum_proto: The descriptor_pb2.EnumDescriptorProto protobuf message.
      package: Optional package name for the new message EnumDescriptor.
      file_desc: The file containing the enum descriptor.
      containing_type: The type containing this enum.
      scope: Scope containing available types.
      top_level: If True, the enum is a top level symbol. If False, the enum
          is defined inside a message.

    Returns:
      The added descriptor
    """

    if package:
      enum_name = '.'.join((package, enum_proto.name))
    else:
      enum_name = enum_proto.name

    if file_desc is None:
      file_name = None
    else:
      file_name = file_desc.name

    values = [self._MakeEnumValueDescriptor(value, index)
              for index, value in enumerate(enum_proto.value)]
    desc = descriptor.EnumDescriptor(name=enum_proto.name,
                                     full_name=enum_name,
                                     filename=file_name,
                                     file=file_desc,
                                     values=values,
                                     containing_type=containing_type,
                                     options=_OptionsOrNone(enum_proto))
    scope['.%s' % enum_name] = desc
    self._CheckConflictRegister(desc, desc.full_name, desc.file.name)
    self._enum_descriptors[enum_name] = desc


    if top_level:
      for value in values:
        full_name = _NormalizeFullyQualifiedName(
            '.'.join((package, value.name)))
        self._CheckConflictRegister(value, full_name, file_name)
        self._top_enum_values[full_name] = value

    return desc

  def _MakeFieldDescriptor(self, field_proto, message_name, index,
                           file_desc, is_extension=False):
    """Creates a field descriptor from a FieldDescriptorProto.

    For message and enum type fields, this method will do a look up
    in the pool for the appropriate descriptor for that type. If it
    is unavailable, it will fall back to the _source function to
    create it. If this type is still unavailable, construction will
    fail.

    Args:
      field_proto: The proto describing the field.
      message_name: The name of the containing message.
      index: Index of the field
      file_desc: The file containing the field descriptor.
      is_extension: Indication that this field is for an extension.

    Returns:
      An initialized FieldDescriptor object
    """

    if message_name:
      full_name = '.'.join((message_name, field_proto.name))
    else:
      full_name = field_proto.name

    return descriptor.FieldDescriptor(
        name=field_proto.name,
        full_name=full_name,
        index=index,
        number=field_proto.number,
        type=field_proto.type,
        cpp_type=None,
        message_type=None,
        enum_type=None,
        containing_type=None,
        label=field_proto.label,
        has_default_value=False,
        default_value=None,
        is_extension=is_extension,
        extension_scope=None,
        options=_OptionsOrNone(field_proto),
        file=file_desc)

  def _SetAllFieldTypes(self, package, desc_proto, scope):
    """Sets all the descriptor's fields's types.

    This method also sets the containing types on any extensions.

    Args:
      package: The current package of desc_proto.
      desc_proto: The message descriptor to update.
      scope: Enclosing scope of available types.
    """

    package = _PrefixWithDot(package)

    main_desc = self._GetTypeFromScope(package, desc_proto.name, scope)

    if package == '.':
      nested_package = _PrefixWithDot(desc_proto.name)
    else:
      nested_package = '.'.join([package, desc_proto.name])

    for field_proto, field_desc in zip(desc_proto.field, main_desc.fields):
      self._SetFieldType(field_proto, field_desc, nested_package, scope)

    for extension_proto, extension_desc in (
        zip(desc_proto.extension, main_desc.extensions)):
      extension_desc.containing_type = self._GetTypeFromScope(
          nested_package, extension_proto.extendee, scope)
      self._SetFieldType(extension_proto, extension_desc, nested_package, scope)

    for nested_type in desc_proto.nested_type:
      self._SetAllFieldTypes(nested_package, nested_type, scope)

  def _SetFieldType(self, field_proto, field_desc, package, scope):
    """Sets the field's type, cpp_type, message_type and enum_type.

    Args:
      field_proto: Data about the field in proto format.
      field_desc: The descriptor to modiy.
      package: The package the field's container is in.
      scope: Enclosing scope of available types.
    """
    if field_proto.type_name:
      desc = self._GetTypeFromScope(package, field_proto.type_name, scope)
    else:
      desc = None

    if not field_proto.HasField('type'):
      if isinstance(desc, descriptor.Descriptor):
        field_proto.type = descriptor.FieldDescriptor.TYPE_MESSAGE
      else:
        field_proto.type = descriptor.FieldDescriptor.TYPE_ENUM

    field_desc.cpp_type = descriptor.FieldDescriptor.ProtoTypeToCppProtoType(
        field_proto.type)

    if (field_proto.type == descriptor.FieldDescriptor.TYPE_MESSAGE
        or field_proto.type == descriptor.FieldDescriptor.TYPE_GROUP):
      field_desc.message_type = desc

    if field_proto.type == descriptor.FieldDescriptor.TYPE_ENUM:
      field_desc.enum_type = desc

    if field_proto.label == descriptor.FieldDescriptor.LABEL_REPEATED:
      field_desc.has_default_value = False
      field_desc.default_value = []
    elif field_proto.HasField('default_value'):
      field_desc.has_default_value = True
      if (field_proto.type == descriptor.FieldDescriptor.TYPE_DOUBLE or
          field_proto.type == descriptor.FieldDescriptor.TYPE_FLOAT):
        field_desc.default_value = float(field_proto.default_value)
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_STRING:
        field_desc.default_value = field_proto.default_value
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_BOOL:
        field_desc.default_value = field_proto.default_value.lower() == 'true'
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_ENUM:
        field_desc.default_value = field_desc.enum_type.values_by_name[
            field_proto.default_value].number
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_BYTES:
        field_desc.default_value = text_encoding.CUnescape(
            field_proto.default_value)
      else:

        field_desc.default_value = int(field_proto.default_value)
    else:
      field_desc.has_default_value = False
      if (field_proto.type == descriptor.FieldDescriptor.TYPE_DOUBLE or
          field_proto.type == descriptor.FieldDescriptor.TYPE_FLOAT):
        field_desc.default_value = 0.0
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_STRING:
        field_desc.default_value = u''
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_BOOL:
        field_desc.default_value = False
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_ENUM:
        field_desc.default_value = field_desc.enum_type.values[0].number
      elif field_proto.type == descriptor.FieldDescriptor.TYPE_BYTES:
        field_desc.default_value = b''
      else:

        field_desc.default_value = 0

    field_desc.type = field_proto.type

  def _MakeEnumValueDescriptor(self, value_proto, index):
    """Creates a enum value descriptor object from a enum value proto.

    Args:
      value_proto: The proto describing the enum value.
      index: The index of the enum value.

    Returns:
      An initialized EnumValueDescriptor object.
    """

    return descriptor.EnumValueDescriptor(
        name=value_proto.name,
        index=index,
        number=value_proto.number,
        options=_OptionsOrNone(value_proto),
        type=None)

  def _MakeServiceDescriptor(self, service_proto, service_index, scope,
                             package, file_desc):
    """Make a protobuf ServiceDescriptor given a ServiceDescriptorProto.

    Args:
      service_proto: The descriptor_pb2.ServiceDescriptorProto protobuf message.
      service_index: The index of the service in the File.
      scope: Dict mapping short and full symbols to message and enum types.
      package: Optional package name for the new message EnumDescriptor.
      file_desc: The file containing the service descriptor.

    Returns:
      The added descriptor.
    """

    if package:
      service_name = '.'.join((package, service_proto.name))
    else:
      service_name = service_proto.name

    methods = [self._MakeMethodDescriptor(method_proto, service_name, package,
                                          scope, index)
               for index, method_proto in enumerate(service_proto.method)]
    desc = descriptor.ServiceDescriptor(name=service_proto.name,
                                        full_name=service_name,
                                        index=service_index,
                                        methods=methods,
                                        options=_OptionsOrNone(service_proto),
                                        file=file_desc)
    self._CheckConflictRegister(desc, desc.full_name, desc.file.name)
    self._service_descriptors[service_name] = desc
    return desc

  def _MakeMethodDescriptor(self, method_proto, service_name, package, scope,
                            index):
    """Creates a method descriptor from a MethodDescriptorProto.

    Args:
      method_proto: The proto describing the method.
      service_name: The name of the containing service.
      package: Optional package name to look up for types.
      scope: Scope containing available types.
      index: Index of the method in the service.

    Returns:
      An initialized MethodDescriptor object.
    """
    full_name = '.'.join((service_name, method_proto.name))
    input_type = self._GetTypeFromScope(
        package, method_proto.input_type, scope)
    output_type = self._GetTypeFromScope(
        package, method_proto.output_type, scope)
    return descriptor.MethodDescriptor(name=method_proto.name,
                                       full_name=full_name,
                                       index=index,
                                       containing_service=None,
                                       input_type=input_type,
                                       output_type=output_type,
                                       options=_OptionsOrNone(method_proto))

  def _ExtractSymbols(self, descriptors):
    """Pulls out all the symbols from descriptor protos.

    Args:
      descriptors: The messages to extract descriptors from.
    Yields:
      A two element tuple of the type name and descriptor object.
    """

    for desc in descriptors:
      yield (_PrefixWithDot(desc.full_name), desc)
      for symbol in self._ExtractSymbols(desc.nested_types):
        yield symbol
      for enum in desc.enum_types:
        yield (_PrefixWithDot(enum.full_name), enum)

  def _GetDeps(self, dependencies):
    """Recursively finds dependencies for file protos.

    Args:
      dependencies: The names of the files being depended on.

    Yields:
      Each direct and indirect dependency.
    """

    for dependency in dependencies:
      dep_desc = self.FindFileByName(dependency)
      yield dep_desc
      for parent_dep in dep_desc.dependencies:
        yield parent_dep

  def _GetTypeFromScope(self, package, type_name, scope):
    """Finds a given type name in the current scope.

    Args:
      package: The package the proto should be located in.
      type_name: The name of the type to be found in the scope.
      scope: Dict mapping short and full symbols to message and enum types.

    Returns:
      The descriptor for the requested type.
    """
    if type_name not in scope:
      components = _PrefixWithDot(package).split('.')
      while components:
        possible_match = '.'.join(components + [type_name])
        if possible_match in scope:
          type_name = possible_match
          break
        else:
          components.pop(-1)
    return scope[type_name]


def _PrefixWithDot(name):
  return name if name.startswith('.') else '.%s' % name


if _USE_C_DESCRIPTORS:



  _DEFAULT = descriptor._message.default_pool
else:
  _DEFAULT = DescriptorPool()


def Default():
  return _DEFAULT
