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


_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='apphosting/api/blobstore/blobstore_service.proto',
  package='apphosting',
  syntax='proto2',
  serialized_options=_b('\n\"com.google.appengine.api.blobstore\020\002(\001B\022BlobstoreServicePb'),
  serialized_pb=_b('\n0apphosting/api/blobstore/blobstore_service.proto\x12\napphosting\"\xeb\x01\n\x15\x42lobstoreServiceError\"\xd1\x01\n\tErrorCode\x12\x06\n\x02OK\x10\x00\x12\x12\n\x0eINTERNAL_ERROR\x10\x01\x12\x10\n\x0cURL_TOO_LONG\x10\x02\x12\x15\n\x11PERMISSION_DENIED\x10\x03\x12\x12\n\x0e\x42LOB_NOT_FOUND\x10\x04\x12\x1b\n\x17\x44\x41TA_INDEX_OUT_OF_RANGE\x10\x05\x12\x1d\n\x19\x42LOB_FETCH_SIZE_TOO_LARGE\x10\x06\x12\x19\n\x15\x41RGUMENT_OUT_OF_RANGE\x10\x08\x12\x14\n\x10INVALID_BLOB_KEY\x10\t\"\xae\x01\n\x16\x43reateUploadURLRequest\x12\x14\n\x0csuccess_path\x18\x01 \x02(\t\x12\x1d\n\x15max_upload_size_bytes\x18\x02 \x01(\x03\x12&\n\x1emax_upload_size_per_blob_bytes\x18\x03 \x01(\x03\x12\x16\n\x0egs_bucket_name\x18\x04 \x01(\t\x12\x1f\n\x17url_expiry_time_seconds\x18\x05 \x01(\x05\"&\n\x17\x43reateUploadURLResponse\x12\x0b\n\x03url\x18\x01 \x02(\t\"4\n\x11\x44\x65leteBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x03(\t\x12\r\n\x05token\x18\x02 \x01(\t\"L\n\x10\x46\x65tchDataRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\t\x12\x13\n\x0bstart_index\x18\x02 \x02(\x03\x12\x11\n\tend_index\x18\x03 \x02(\x03\"&\n\x11\x46\x65tchDataResponse\x12\x11\n\x04\x64\x61ta\x18\xe8\x07 \x02(\x0c\x42\x02\x08\x01\"N\n\x10\x43loneBlobRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\x0c\x12\x11\n\tmime_type\x18\x02 \x02(\x0c\x12\x15\n\rtarget_app_id\x18\x03 \x02(\x0c\"%\n\x11\x43loneBlobResponse\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\x0c\"(\n\x14\x44\x65\x63odeBlobKeyRequest\x12\x10\n\x08\x62lob_key\x18\x01 \x03(\t\"(\n\x15\x44\x65\x63odeBlobKeyResponse\x12\x0f\n\x07\x64\x65\x63oded\x18\x01 \x03(\t\"8\n$CreateEncodedGoogleStorageKeyRequest\x12\x10\n\x08\x66ilename\x18\x01 \x02(\t\"9\n%CreateEncodedGoogleStorageKeyResponse\x12\x10\n\x08\x62lob_key\x18\x01 \x02(\tB<\n\"com.google.appengine.api.blobstore\x10\x02(\x01\x42\x12\x42lobstoreServicePb')
)



_BLOBSTORESERVICEERROR_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='apphosting.BlobstoreServiceError.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OK', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INTERNAL_ERROR', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='URL_TOO_LONG', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PERMISSION_DENIED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOB_NOT_FOUND', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DATA_INDEX_OUT_OF_RANGE', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BLOB_FETCH_SIZE_TOO_LARGE', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ARGUMENT_OUT_OF_RANGE', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_BLOB_KEY', index=8, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=91,
  serialized_end=300,
)
_sym_db.RegisterEnumDescriptor(_BLOBSTORESERVICEERROR_ERRORCODE)


_BLOBSTORESERVICEERROR = _descriptor.Descriptor(
  name='BlobstoreServiceError',
  full_name='apphosting.BlobstoreServiceError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BLOBSTORESERVICEERROR_ERRORCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=300,
)


_CREATEUPLOADURLREQUEST = _descriptor.Descriptor(
  name='CreateUploadURLRequest',
  full_name='apphosting.CreateUploadURLRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success_path', full_name='apphosting.CreateUploadURLRequest.success_path', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_upload_size_bytes', full_name='apphosting.CreateUploadURLRequest.max_upload_size_bytes', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_upload_size_per_blob_bytes', full_name='apphosting.CreateUploadURLRequest.max_upload_size_per_blob_bytes', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gs_bucket_name', full_name='apphosting.CreateUploadURLRequest.gs_bucket_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url_expiry_time_seconds', full_name='apphosting.CreateUploadURLRequest.url_expiry_time_seconds', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=303,
  serialized_end=477,
)


_CREATEUPLOADURLRESPONSE = _descriptor.Descriptor(
  name='CreateUploadURLResponse',
  full_name='apphosting.CreateUploadURLResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='apphosting.CreateUploadURLResponse.url', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=479,
  serialized_end=517,
)


_DELETEBLOBREQUEST = _descriptor.Descriptor(
  name='DeleteBlobRequest',
  full_name='apphosting.DeleteBlobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.DeleteBlobRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='token', full_name='apphosting.DeleteBlobRequest.token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=519,
  serialized_end=571,
)


_FETCHDATAREQUEST = _descriptor.Descriptor(
  name='FetchDataRequest',
  full_name='apphosting.FetchDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.FetchDataRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_index', full_name='apphosting.FetchDataRequest.start_index', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end_index', full_name='apphosting.FetchDataRequest.end_index', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=573,
  serialized_end=649,
)


_FETCHDATARESPONSE = _descriptor.Descriptor(
  name='FetchDataResponse',
  full_name='apphosting.FetchDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='apphosting.FetchDataResponse.data', index=0,
      number=1000, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\010\001'), file=DESCRIPTOR),
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
  serialized_start=651,
  serialized_end=689,
)


_CLONEBLOBREQUEST = _descriptor.Descriptor(
  name='CloneBlobRequest',
  full_name='apphosting.CloneBlobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.CloneBlobRequest.blob_key', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mime_type', full_name='apphosting.CloneBlobRequest.mime_type', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='target_app_id', full_name='apphosting.CloneBlobRequest.target_app_id', index=2,
      number=3, type=12, cpp_type=9, label=2,
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
  serialized_start=691,
  serialized_end=769,
)


_CLONEBLOBRESPONSE = _descriptor.Descriptor(
  name='CloneBlobResponse',
  full_name='apphosting.CloneBlobResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.CloneBlobResponse.blob_key', index=0,
      number=1, type=12, cpp_type=9, label=2,
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
  serialized_start=771,
  serialized_end=808,
)


_DECODEBLOBKEYREQUEST = _descriptor.Descriptor(
  name='DecodeBlobKeyRequest',
  full_name='apphosting.DecodeBlobKeyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.DecodeBlobKeyRequest.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=810,
  serialized_end=850,
)


_DECODEBLOBKEYRESPONSE = _descriptor.Descriptor(
  name='DecodeBlobKeyResponse',
  full_name='apphosting.DecodeBlobKeyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='decoded', full_name='apphosting.DecodeBlobKeyResponse.decoded', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=852,
  serialized_end=892,
)


_CREATEENCODEDGOOGLESTORAGEKEYREQUEST = _descriptor.Descriptor(
  name='CreateEncodedGoogleStorageKeyRequest',
  full_name='apphosting.CreateEncodedGoogleStorageKeyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='apphosting.CreateEncodedGoogleStorageKeyRequest.filename', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=894,
  serialized_end=950,
)


_CREATEENCODEDGOOGLESTORAGEKEYRESPONSE = _descriptor.Descriptor(
  name='CreateEncodedGoogleStorageKeyResponse',
  full_name='apphosting.CreateEncodedGoogleStorageKeyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blob_key', full_name='apphosting.CreateEncodedGoogleStorageKeyResponse.blob_key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=952,
  serialized_end=1009,
)

_BLOBSTORESERVICEERROR_ERRORCODE.containing_type = _BLOBSTORESERVICEERROR
DESCRIPTOR.message_types_by_name['BlobstoreServiceError'] = _BLOBSTORESERVICEERROR
DESCRIPTOR.message_types_by_name['CreateUploadURLRequest'] = _CREATEUPLOADURLREQUEST
DESCRIPTOR.message_types_by_name['CreateUploadURLResponse'] = _CREATEUPLOADURLRESPONSE
DESCRIPTOR.message_types_by_name['DeleteBlobRequest'] = _DELETEBLOBREQUEST
DESCRIPTOR.message_types_by_name['FetchDataRequest'] = _FETCHDATAREQUEST
DESCRIPTOR.message_types_by_name['FetchDataResponse'] = _FETCHDATARESPONSE
DESCRIPTOR.message_types_by_name['CloneBlobRequest'] = _CLONEBLOBREQUEST
DESCRIPTOR.message_types_by_name['CloneBlobResponse'] = _CLONEBLOBRESPONSE
DESCRIPTOR.message_types_by_name['DecodeBlobKeyRequest'] = _DECODEBLOBKEYREQUEST
DESCRIPTOR.message_types_by_name['DecodeBlobKeyResponse'] = _DECODEBLOBKEYRESPONSE
DESCRIPTOR.message_types_by_name['CreateEncodedGoogleStorageKeyRequest'] = _CREATEENCODEDGOOGLESTORAGEKEYREQUEST
DESCRIPTOR.message_types_by_name['CreateEncodedGoogleStorageKeyResponse'] = _CREATEENCODEDGOOGLESTORAGEKEYRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BlobstoreServiceError = _reflection.GeneratedProtocolMessageType('BlobstoreServiceError', (_message.Message,), {
  'DESCRIPTOR' : _BLOBSTORESERVICEERROR,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(BlobstoreServiceError)

CreateUploadURLRequest = _reflection.GeneratedProtocolMessageType('CreateUploadURLRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUPLOADURLREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateUploadURLRequest)

CreateUploadURLResponse = _reflection.GeneratedProtocolMessageType('CreateUploadURLResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUPLOADURLRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateUploadURLResponse)

DeleteBlobRequest = _reflection.GeneratedProtocolMessageType('DeleteBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DeleteBlobRequest)

FetchDataRequest = _reflection.GeneratedProtocolMessageType('FetchDataRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHDATAREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(FetchDataRequest)

FetchDataResponse = _reflection.GeneratedProtocolMessageType('FetchDataResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHDATARESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(FetchDataResponse)

CloneBlobRequest = _reflection.GeneratedProtocolMessageType('CloneBlobRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLONEBLOBREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CloneBlobRequest)

CloneBlobResponse = _reflection.GeneratedProtocolMessageType('CloneBlobResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLONEBLOBRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CloneBlobResponse)

DecodeBlobKeyRequest = _reflection.GeneratedProtocolMessageType('DecodeBlobKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _DECODEBLOBKEYREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DecodeBlobKeyRequest)

DecodeBlobKeyResponse = _reflection.GeneratedProtocolMessageType('DecodeBlobKeyResponse', (_message.Message,), {
  'DESCRIPTOR' : _DECODEBLOBKEYRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(DecodeBlobKeyResponse)

CreateEncodedGoogleStorageKeyRequest = _reflection.GeneratedProtocolMessageType('CreateEncodedGoogleStorageKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEENCODEDGOOGLESTORAGEKEYREQUEST,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateEncodedGoogleStorageKeyRequest)

CreateEncodedGoogleStorageKeyResponse = _reflection.GeneratedProtocolMessageType('CreateEncodedGoogleStorageKeyResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEENCODEDGOOGLESTORAGEKEYRESPONSE,
  '__module__' : 'google.appengine.api.blobstore.blobstore_service_pb2'

  })
_sym_db.RegisterMessage(CreateEncodedGoogleStorageKeyResponse)


DESCRIPTOR._options = None
_FETCHDATARESPONSE.fields_by_name['data']._options = None

