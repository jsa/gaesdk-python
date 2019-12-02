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



from google.net.proto import ProtocolBuffer
import abc
import array
try:
  from thread import allocate_lock as _Lock
except ImportError:
  from threading import Lock as _Lock

if hasattr(__builtins__, 'xrange'): range = xrange

if hasattr(ProtocolBuffer, 'ExtendableProtocolMessage'):
  _extension_runtime = True
  _ExtendableProtocolMessage = ProtocolBuffer.ExtendableProtocolMessage
else:
  _extension_runtime = False
  _ExtendableProtocolMessage = ProtocolBuffer.ProtocolMessage

from google.appengine.api.api_base_pb import *
import google.appengine.api.api_base_pb
google_dot_apphosting_dot_api_dot_api__base__pb = __import__('google.appengine.api.api_base_pb', {}, {}, [''])
class StoreBlobRequest(ProtocolBuffer.ProtocolMessage):
  has_blob_key_ = 0
  blob_key_ = ""
  has_content_ = 0
  content_ = ""

  def __init__(self, contents=None):
    if contents is not None: self.MergeFromString(contents)

  def blob_key(self): return self.blob_key_

  def set_blob_key(self, x):
    self.has_blob_key_ = 1
    self.blob_key_ = x

  def clear_blob_key(self):
    if self.has_blob_key_:
      self.has_blob_key_ = 0
      self.blob_key_ = ""

  def has_blob_key(self): return self.has_blob_key_

  def content(self): return self.content_

  def set_content(self, x):
    self.has_content_ = 1
    self.content_ = x

  def clear_content(self):
    if self.has_content_:
      self.has_content_ = 0
      self.content_ = ""

  def has_content(self): return self.has_content_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_blob_key()): self.set_blob_key(x.blob_key())
    if (x.has_content()): self.set_content(x.content())

  def Equals(self, x):
    if x is self: return 1
    if self.has_blob_key_ != x.has_blob_key_: return 0
    if self.has_blob_key_ and self.blob_key_ != x.blob_key_: return 0
    if self.has_content_ != x.has_content_: return 0
    if self.has_content_ and self.content_ != x.content_: return 0
    return 1

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_blob_key_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: blob_key not set.')
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthString(len(self.blob_key_))
    if (self.has_content_): n += 1 + self.lengthString(len(self.content_))
    return n + 1

  def ByteSizePartial(self):
    n = 0
    if (self.has_blob_key_):
      n += 1
      n += self.lengthString(len(self.blob_key_))
    if (self.has_content_): n += 1 + self.lengthString(len(self.content_))
    return n

  def Clear(self):
    self.clear_blob_key()
    self.clear_content()

  def OutputUnchecked(self, out):
    out.putVarInt32(10)
    out.putPrefixedString(self.blob_key_)
    if (self.has_content_):
      out.putVarInt32(18)
      out.putPrefixedString(self.content_)

  def OutputPartial(self, out):
    if (self.has_blob_key_):
      out.putVarInt32(10)
      out.putPrefixedString(self.blob_key_)
    if (self.has_content_):
      out.putVarInt32(18)
      out.putPrefixedString(self.content_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        self.set_blob_key(d.getPrefixedString())
        continue
      if tt == 18:
        self.set_content(d.getPrefixedString())
        continue


      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError()
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_blob_key_: res+=prefix+("blob_key: %s\n" % self.DebugFormatString(self.blob_key_))
    if self.has_content_: res+=prefix+("content: %s\n" % self.DebugFormatString(self.content_))
    return res


  def _BuildTagLookupTable(sparse, maxtag, default=None):
    return tuple([sparse.get(i, default) for i in range(0, 1+maxtag)])

  kblob_key = 1
  kcontent = 2

  _TEXT = _BuildTagLookupTable({
    0: "ErrorCode",
    1: "blob_key",
    2: "content",
  }, 2)

  _TYPES = _BuildTagLookupTable({
    0: ProtocolBuffer.Encoder.NUMERIC,
    1: ProtocolBuffer.Encoder.STRING,
    2: ProtocolBuffer.Encoder.STRING,
  }, 2, ProtocolBuffer.Encoder.MAX_TYPE)


  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
  _PROTO_DESCRIPTOR_NAME = 'apphosting.StoreBlobRequest'
class SetBlobStorageTypeRequest(ProtocolBuffer.ProtocolMessage):


  MEMORY       =    0
  FILE         =    1

  _StorageType_NAMES = {
    0: "MEMORY",
    1: "FILE",
  }

  def StorageType_Name(cls, x): return cls._StorageType_NAMES.get(x, "")
  StorageType_Name = classmethod(StorageType_Name)

  has_storage_type_ = 0
  storage_type_ = 0

  def __init__(self, contents=None):
    if contents is not None: self.MergeFromString(contents)

  def storage_type(self): return self.storage_type_

  def set_storage_type(self, x):
    self.has_storage_type_ = 1
    self.storage_type_ = x

  def clear_storage_type(self):
    if self.has_storage_type_:
      self.has_storage_type_ = 0
      self.storage_type_ = 0

  def has_storage_type(self): return self.has_storage_type_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_storage_type()): self.set_storage_type(x.storage_type())

  def Equals(self, x):
    if x is self: return 1
    if self.has_storage_type_ != x.has_storage_type_: return 0
    if self.has_storage_type_ and self.storage_type_ != x.storage_type_: return 0
    return 1

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_storage_type_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: storage_type not set.')
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthVarInt64(self.storage_type_)
    return n + 1

  def ByteSizePartial(self):
    n = 0
    if (self.has_storage_type_):
      n += 1
      n += self.lengthVarInt64(self.storage_type_)
    return n

  def Clear(self):
    self.clear_storage_type()

  def OutputUnchecked(self, out):
    out.putVarInt32(8)
    out.putVarInt32(self.storage_type_)

  def OutputPartial(self, out):
    if (self.has_storage_type_):
      out.putVarInt32(8)
      out.putVarInt32(self.storage_type_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 8:
        self.set_storage_type(d.getVarInt32())
        continue


      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError()
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_storage_type_: res+=prefix+("storage_type: %s\n" % self.DebugFormatInt32(self.storage_type_))
    return res


  def _BuildTagLookupTable(sparse, maxtag, default=None):
    return tuple([sparse.get(i, default) for i in range(0, 1+maxtag)])

  kstorage_type = 1

  _TEXT = _BuildTagLookupTable({
    0: "ErrorCode",
    1: "storage_type",
  }, 1)

  _TYPES = _BuildTagLookupTable({
    0: ProtocolBuffer.Encoder.NUMERIC,
    1: ProtocolBuffer.Encoder.NUMERIC,
  }, 1, ProtocolBuffer.Encoder.MAX_TYPE)


  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
  _PROTO_DESCRIPTOR_NAME = 'apphosting.SetBlobStorageTypeRequest'
if _extension_runtime:
  pass

__all__ = ['StoreBlobRequest','SetBlobStorageTypeRequest']
