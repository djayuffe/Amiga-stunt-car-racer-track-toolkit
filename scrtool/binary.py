from .errors import TruncatedError,ValidationError
import struct
class Reader:
 def __init__(self,b):self.b=memoryview(b);self.p=0
 def need(self,n):
  if n<0 or self.p+n>len(self.b):raise TruncatedError(f"need {n} bytes at {self.p}, size={len(self.b)}")
 def u8(self):self.need(1);v=int(self.b[self.p]);self.p+=1;return v
 def u16be(self):self.need(2);v=struct.unpack_from(">H",self.b,self.p)[0];self.p+=2;return v
 def bytes(self,n):self.need(n);v=bytes(self.b[self.p:self.p+n]);self.p+=n;return v
class Writer:
 def __init__(self):self.b=bytearray()
 def u8(self,v):
  if not 0<=v<=255:raise ValidationError("u8 range")
  self.b.append(v)
 def u16be(self,v):
  if not 0<=v<=65535:raise ValidationError("u16 range")
  self.b+=struct.pack(">H",v)
 def bytes(self,v):self.b+=v
 def finish(self):return bytes(self.b)
