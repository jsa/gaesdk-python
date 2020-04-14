# Copyright 2002, Google Inc.
"""The base class for protorpc protobuf encoding and decoding.

This module has been branched from //net/proto/ProtocolBuffer.py

For more details about protocol buffer encoding and decoding please see:

  http://code.google.com/apis/protocolbuffers/docs/encoding.html
"""

import array
import struct

__all__ = [
    "Encoder", "Decoder", "ProtocolBufferDecodeError",
    "ProtocolBufferEncodeError"
]


class ProtocolBufferDecodeError(Exception):
  """Raised if protocol buffer cannot be decoded."""


class ProtocolBufferEncodeError(Exception):
  """Raised if protocol buffer cannot be encoded."""


# Disable linters to keep code in sync with //net/proto/ProtocolBuffer.py
# It will ease the downstream propagation in the event of proto1 changes.

# pylint: disable=old-style-class
# pylint: disable=old-raise-syntax
# pylint: disable=g-bad-name
# pylint: disable=missing-docstring
# pylint: disable=superfluous-parens


class Encoder:
  """Base encoder for Protocol Buffers."""

  # types of data
  NUMERIC = 0
  DOUBLE = 1
  STRING = 2
  STARTGROUP = 3
  ENDGROUP = 4
  FLOAT = 5
  MAX_TYPE = 6

  def __init__(self):
    self.buf = array.array("B")
    return

  def buffer(self):
    return self.buf

  def put8(self, v):
    if v < 0 or v >= (1 << 8):
      raise ProtocolBufferEncodeError("u8 too big")
    self.buf.append(v & 255)
    return

  def put16(self, v):
    if v < 0 or v >= (1 << 16):
      raise ProtocolBufferEncodeError("u16 too big")
    self.buf.append((v >> 0) & 255)
    self.buf.append((v >> 8) & 255)
    return

  def put32(self, v):
    if v < 0 or v >= (1 << 32):
      raise ProtocolBufferEncodeError("u32 too big")
    self.buf.append((v >> 0) & 255)
    self.buf.append((v >> 8) & 255)
    self.buf.append((v >> 16) & 255)
    self.buf.append((v >> 24) & 255)
    return

  def put64(self, v):
    if v < 0 or v >= (1 << 64):
      raise ProtocolBufferEncodeError("u64 too big")
    self.buf.append((v >> 0) & 255)
    self.buf.append((v >> 8) & 255)
    self.buf.append((v >> 16) & 255)
    self.buf.append((v >> 24) & 255)
    self.buf.append((v >> 32) & 255)
    self.buf.append((v >> 40) & 255)
    self.buf.append((v >> 48) & 255)
    self.buf.append((v >> 56) & 255)
    return

  def putVarInt32(self, v):
    # Profiling has shown this code to be very performance critical
    # so we duplicate code, go for early exits when possible, etc.
    # VarInt32 gets more unrolling because VarInt32s are far and away
    # the most common element in protobufs (field tags and string
    # lengths), so they get more attention.  They're also more
    # likely to fit in one byte (string lengths again), so we
    # check and bail out early if possible.

    buf_append = self.buf.append  # cache attribute lookup
    if v & 127 == v:
      buf_append(v)
      return
    if v >= 0x80000000 or v < -0x80000000:  # python2.4 doesn't fold constants
      raise ProtocolBufferEncodeError("int32 too big")
    if v < 0:
      v += 0x10000000000000000
    while True:
      bits = v & 127
      v >>= 7
      if v:
        bits |= 128
      buf_append(bits)
      if not v:
        break
    return

  def putVarInt64(self, v):
    buf_append = self.buf.append
    if v >= 0x8000000000000000 or v < -0x8000000000000000:
      raise ProtocolBufferEncodeError("int64 too big")
    if v < 0:
      v += 0x10000000000000000
    while True:
      bits = v & 127
      v >>= 7
      if v:
        bits |= 128
      buf_append(bits)
      if not v:
        break
    return

  def putVarUint64(self, v):
    buf_append = self.buf.append
    if v < 0 or v >= 0x10000000000000000:
      raise ProtocolBufferEncodeError("uint64 too big")
    while True:
      bits = v & 127
      v >>= 7
      if v:
        bits |= 128
      buf_append(bits)
      if not v:
        break
    return

  def putFloat(self, v):
    a = array.array("B")
    a.fromstring(struct.pack("<f", v))
    self.buf.extend(a)
    return

  def putDouble(self, v):
    a = array.array("B")
    a.fromstring(struct.pack("<d", v))
    self.buf.extend(a)
    return

  def putBoolean(self, v):
    if v:
      self.buf.append(1)
    else:
      self.buf.append(0)
    return

  def putPrefixedString(self, v):
    # This change prevents corrupted encoding an YouTube, where
    # our default encoding is utf-8 and unicode strings may occasionally be
    # passed into ProtocolBuffers.
    v = str(v)
    self.putVarInt32(len(v))
    self.buf.fromstring(v)
    return

  def putRawString(self, v):
    self.buf.fromstring(v)


class Decoder:
  """Base decoder for Protocol Buffers."""

  def __init__(self, buf, idx, limit):
    self.buf = buf
    self.idx = idx
    self.limit = limit
    return

  def avail(self):
    return self.limit - self.idx

  def buffer(self):
    return self.buf

  def pos(self):
    return self.idx

  def skip(self, n):
    if self.idx + n > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    self.idx += n
    return

  def skipData(self, tag):
    t = tag & 7  # tag format type
    if t == Encoder.NUMERIC:
      self.getVarInt64()
    elif t == Encoder.DOUBLE:
      self.skip(8)
    elif t == Encoder.STRING:
      n = self.getVarInt32()
      self.skip(n)
    elif t == Encoder.STARTGROUP:
      while 1:
        t = self.getVarInt32()
        if (t & 7) == Encoder.ENDGROUP:
          break
        else:
          self.skipData(t)
      if (t - Encoder.ENDGROUP) != (tag - Encoder.STARTGROUP):
        raise ProtocolBufferDecodeError("corrupted")
    elif t == Encoder.ENDGROUP:
      raise ProtocolBufferDecodeError("corrupted")
    elif t == Encoder.FLOAT:
      self.skip(4)
    else:
      raise ProtocolBufferDecodeError("corrupted")

  # these are all unsigned gets
  def get8(self):
    if self.idx >= self.limit:
      raise ProtocolBufferDecodeError("truncated")
    c = self.buf[self.idx]
    self.idx += 1
    return c

  def get16(self):
    if self.idx + 2 > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    c = self.buf[self.idx]
    d = self.buf[self.idx + 1]
    self.idx += 2
    return (d << 8) | c

  def get32(self):
    if self.idx + 4 > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    c = self.buf[self.idx]
    d = self.buf[self.idx + 1]
    e = self.buf[self.idx + 2]
    f = long(self.buf[self.idx + 3])
    self.idx += 4
    return (f << 24) | (e << 16) | (d << 8) | c

  def get64(self):
    if self.idx + 8 > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    c = self.buf[self.idx]
    d = self.buf[self.idx + 1]
    e = self.buf[self.idx + 2]
    f = long(self.buf[self.idx + 3])
    g = long(self.buf[self.idx + 4])
    h = long(self.buf[self.idx + 5])
    i = long(self.buf[self.idx + 6])
    j = long(self.buf[self.idx + 7])
    self.idx += 8
    return ((j << 56) | (i << 48) | (h << 40) | (g << 32) | (f << 24)
            | (e << 16) | (d << 8) | c)

  def getVarInt32(self):
    # getVarInt32 gets different treatment than other integer getter
    # functions due to the much larger number of varInt32s and also
    # varInt32s that fit in one byte.  See the comment at putVarInt32.
    b = self.get8()
    if not (b & 128):
      return b

    result = long(0)
    shift = 0

    while 1:
      result |= (long(b & 127) << shift)
      shift += 7
      if not (b & 128):
        if result >= 0x10000000000000000:  # (1L << 64):
          raise ProtocolBufferDecodeError("corrupted")
        break
      if shift >= 64:
        raise ProtocolBufferDecodeError("corrupted")
      b = self.get8()

    if result >= 0x8000000000000000:  # (1L << 63)
      result -= 0x10000000000000000  # (1L << 64)
    if result >= 0x80000000 or result < -0x80000000:  # (1L << 31)
      raise ProtocolBufferDecodeError("corrupted")
    return result

  def getVarInt64(self):
    result = self.getVarUint64()
    if result >= (1 << 63):
      result -= (1 << 64)
    return result

  def getVarUint64(self):
    result = long(0)
    shift = 0
    while 1:
      if shift >= 64:
        raise ProtocolBufferDecodeError("corrupted")
      b = self.get8()
      result |= (long(b & 127) << shift)
      shift += 7
      if not (b & 128):
        if result >= (1 << 64):
          raise ProtocolBufferDecodeError("corrupted")
        return result
    return result  # make pychecker happy

  def getFloat(self):
    if self.idx + 4 > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    a = self.buf[self.idx:self.idx + 4]
    self.idx += 4
    return struct.unpack("<f", a)[0]

  def getDouble(self):
    if self.idx + 8 > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    a = self.buf[self.idx:self.idx + 8]
    self.idx += 8
    return struct.unpack("<d", a)[0]

  def getBoolean(self):
    b = self.get8()
    if b != 0 and b != 1:
      raise ProtocolBufferDecodeError("corrupted")
    return b

  def getPrefixedString(self):
    length = self.getVarInt32()
    if self.idx + length > self.limit:
      raise ProtocolBufferDecodeError("truncated")
    r = self.buf[self.idx:self.idx + length]
    self.idx += length
    return r.tostring()

  def getRawString(self):
    r = self.buf[self.idx:self.limit]
    self.idx = self.limit
    return r.tostring()
