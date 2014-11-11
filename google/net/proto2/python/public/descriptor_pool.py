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



import sys

from google.net.proto2.python.public import descriptor
from google.net.proto2.python.public import descriptor_database
from google.net.proto2.python.public import text_encoding


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


class DescriptorPool(object):
  """A collection of protobufs dynamically constructed by descriptor protos."""

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
    self._file_descriptors = {}

  def Add(self, file_desc_proto):
    """Adds the FileDescriptorProto and its types to this pool.

    Args:
      file_desc_proto: The FileDescriptorProto to add.
    """

    self._internal_db.Add(file_desc_proto)

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

    self._descriptors[desc.full_name] = desc
    self.AddFileDescriptor(desc.file)

  def AddEnumDescriptor(self, enum_desc):
    """Adds an EnumDescriptor to the pool.

    This method also registers the FileDescriptor associated with the message.

    Args:
      enum_desc: An EnumDescriptor.
    """

    if not isinstance(enum_desc, descriptor.EnumDescriptor):
      raise TypeError('Expected instance of descriptor.EnumDescriptor.')

    self._enum_descriptors[enum_desc.full_name] = enum_desc
    self.AddFileDescriptor(enum_desc.file)

  def AddFileDescriptor(self, file_desc):
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
      KeyError: if the file can not be found in the pool.
    """

    try:
      return self._file_descriptors[file_name]
    except KeyError:
      pass

    try:
      file_proto = self._internal_db.FindFileByName(file_name)
    except KeyError:
      _, error, _ = sys.exc_info()
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
      KeyError: if the file can not be found in the pool.
    """

    symbol = _NormalizeFullyQualifiedName(symbol)
    try:
      return self._descriptors[symbol].file
    except KeyError:
      pass

    try:
      return self._enum_descriptors[symbol].file
    except KeyError:
      pass

    try:
      file_proto = self._internal_db.FindFileContainingSymbol(symbol)
    except KeyError:
      _, error, _ = sys.exc_info()
      if self._descriptor_db:
        file_proto = self._descriptor_db.FindFileContainingSymbol(symbol)
      else:
        raise error
    if not file_proto:
      raise KeyError('Cannot find a file containing %s' % symbol)
    return self._ConvertFileProtoToFileDescriptor(file_proto)

  def FindMessageTypeByName(self, full_name):
    """Loads the named descriptor from the pool.

    Args:
      full_name: The full name of the descriptor to load.

    Returns:
      The descriptor for the named type.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._descriptors:
      self.FindFileContainingSymbol(full_name)
    return self._descriptors[full_name]

  def FindEnumTypeByName(self, full_name):
    """Loads the named enum descriptor from the pool.

    Args:
      full_name: The full name of the enum descriptor to load.

    Returns:
      The enum descriptor for the named type.
    """

    full_name = _NormalizeFullyQualifiedName(full_name)
    if full_name not in self._enum_descriptors:
      self.FindFileContainingSymbol(full_name)
    return self._enum_descriptors[full_name]

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

      file_descriptor = descriptor.FileDescriptor(
          name=file_proto.name,
          package=file_proto.package,
          options=file_proto.options,
          serialized_pb=file_proto.SerializeToString(),
          dependencies=direct_deps)
      scope = {}





      for dependency in built_deps:
        scope.update(self._ExtractSymbols(
            dependency.message_types_by_name.values()))
        scope.update((_PrefixWithDot(enum.full_name), enum)
                     for enum in dependency.enum_types_by_name.values())

      for message_type in file_proto.message_type:
        message_desc = self._ConvertMessageDescriptor(
            message_type, file_proto.package, file_descriptor, scope)
        file_descriptor.message_types_by_name[message_desc.name] = message_desc

      for enum_type in file_proto.enum_type:
        file_descriptor.enum_types_by_name[enum_type.name] = (
            self._ConvertEnumDescriptor(enum_type, file_proto.package,
                                        file_descriptor, None, scope))

      for index, extension_proto in enumerate(file_proto.extension):
        extension_desc = self.MakeFieldDescriptor(
            extension_proto, file_proto.package, index, is_extension=True)
        extension_desc.containing_type = self._GetTypeFromScope(
            file_descriptor.package, extension_proto.extendee, scope)
        self.SetFieldType(extension_proto, extension_desc,
                          file_descriptor.package, scope)
        file_descriptor.extensions_by_name[extension_desc.name] = extension_desc

      for desc_proto in file_proto.message_type:
        self.SetAllFieldTypes(file_proto.package, desc_proto, scope)

      if file_proto.package:
        desc_proto_prefix = _PrefixWithDot(file_proto.package)
      else:
        desc_proto_prefix = ''

      for desc_proto in file_proto.message_type:
        desc = self._GetTypeFromScope(desc_proto_prefix, desc_proto.name, scope)
        file_descriptor.message_types_by_name[desc_proto.name] = desc
      self.Add(file_proto)
      self._file_descriptors[file_proto.name] = file_descriptor

    return self._file_descriptors[file_proto.name]

  def _ConvertMessageDescriptor(self, desc_proto, package=None, file_desc=None,
                                scope=None):
    """Adds the proto to the pool in the specified package.

    Args:
      desc_proto: The descriptor_pb2.DescriptorProto protobuf message.
      package: The package the proto should be located in.
      file_desc: The file containing this message.
      scope: Dict mapping short and full symbols to message and enum types.

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
        self._ConvertMessageDescriptor(nested, desc_name, file_desc, scope)
        for nested in desc_proto.nested_type]
    enums = [
        self._ConvertEnumDescriptor(enum, desc_name, file_desc, None, scope)
        for enum in desc_proto.enum_type]
    fields = [self.MakeFieldDescriptor(field, desc_name, index)
              for index, field in enumerate(desc_proto.field)]
    extensions = [
        self.MakeFieldDescriptor(extension, desc_name, index, is_extension=True)
        for index, extension in enumerate(desc_proto.extension)]
    oneofs = [
        descriptor.OneofDescriptor(desc.name, '.'.join((desc_name, desc.name)),
                                   index, None, [])
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
        options=desc_proto.options,
        is_extendable=is_extendable,
        extension_ranges=extension_ranges,
        file=file_desc,
        serialized_start=None,
        serialized_end=None)
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
    self._descriptors[desc_name] = desc
    return desc

  def _ConvertEnumDescriptor(self, enum_proto, package=None, file_desc=None,
                             containing_type=None, scope=None):
    """Make a protobuf EnumDescriptor given an EnumDescriptorProto protobuf.

    Args:
      enum_proto: The descriptor_pb2.EnumDescriptorProto protobuf message.
      package: Optional package name for the new message EnumDescriptor.
      file_desc: The file containing the enum descriptor.
      containing_type: The type containing this enum.
      scope: Scope containing available types.

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
                                     options=enum_proto.options)
    scope['.%s' % enum_name] = desc
    self._enum_descriptors[enum_name] = desc
    return desc

  def MakeFieldDescriptor(self, field_proto, message_name, index,
                          is_extension=False):
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
        options=field_proto.options)

  def SetAllFieldTypes(self, package, desc_proto, scope):
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
      self.SetFieldType(field_proto, field_desc, nested_package, scope)

    for extension_proto, extension_desc in (
        zip(desc_proto.extension, main_desc.extensions)):
      extension_desc.containing_type = self._GetTypeFromScope(
          nested_package, extension_proto.extendee, scope)
      self.SetFieldType(extension_proto, extension_desc, nested_package, scope)

    for nested_type in desc_proto.nested_type:
      self.SetAllFieldTypes(nested_package, nested_type, scope)

  def SetFieldType(self, field_proto, field_desc, package, scope):
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
      field_desc.default_value = None

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
        options=value_proto.options,
        type=None)

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
