#!/usr/bin/env python3
"""Conservative 68000/data geometry candidate scanner.

Finds repeated signed-word triplets and pointer-like runs. It does NOT label candidates
as cars/scenery without code-reference evidence.
"""
import argparse,struct,json,pathlib
def scan(b,min_vertices=6):
    out=[]
    # Candidate XYZ word runs: values in a conservative world-coordinate range.
    vals=[struct.unpack_from(">h",b,i)[0] for i in range(0,len(b)-1,2)]
    start=None
    for wi in range(0,len(vals)-2,3):
        tri=vals[wi:wi+3]
        good=all(-16384<=v<=16384 for v in tri)
        if good and start is None:start=wi
        if (not good or wi+3>=len(vals)) and start is not None:
            n=(wi-start)//3
            if n>=min_vertices: out.append({"kind":"xyz_word_candidate","offset":start*2,"vertices":n})
            start=None
    # big-endian even pointers within image
    for off in range(0,max(0,len(b)-16),2):
        ps=[struct.unpack_from(">I",b,off+j*4)[0] for j in range(4)]
        if all((p&1)==0 and p<len(b) for p in ps):
            out.append({"kind":"pointer_run_candidate","offset":off,"values":ps})
    return out
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("input");ap.add_argument("-o","--output");a=ap.parse_args()
 r=scan(pathlib.Path(a.input).read_bytes());s=json.dumps(r,indent=2)
 pathlib.Path(a.output).write_text(s) if a.output else print(s)
