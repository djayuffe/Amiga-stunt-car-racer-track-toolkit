import pathlib,subprocess,sys,json
r=pathlib.Path(__file__).parents[1]
p=subprocess.run([sys.executable,str(r/"tools/normalize_emulator_trace.py"),str(pathlib.Path(__file__).parent/"sample_trace.txt")],capture_output=True,text=True)
assert p.returncode==0
j=json.loads(p.stdout);assert len(j)==2 and j[0]["kind"]=="IO" and j[1]["kind"]=="MEMW"
print("dynamic trace contract: PASS")
