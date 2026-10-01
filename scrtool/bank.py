from .track import SIZE,decode,encode
from .errors import ValidationError
def split_bank(b):
 if len(b)%SIZE: raise ValidationError("bank size not multiple of 804")
 return [decode(b[i:i+SIZE]) for i in range(0,len(b),SIZE)]
def join_bank(ts): return b"".join(encode(t) for t in ts)
