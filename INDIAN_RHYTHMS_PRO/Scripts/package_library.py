#!/usr/bin/env python3
import hashlib,json,zipfile
from core import ROOT

def main():
 report=json.loads((ROOT/'Documentation/validation.json').read_text())
 if report['failures']:raise SystemExit('Refusing to package failed validation')
 archive=ROOT.parent/(ROOT.name+'.zip')
 files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.venv' not in p.parts)
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for p in files:z.write(p,p.relative_to(ROOT.parent))
 with zipfile.ZipFile(archive) as z:
  bad=z.testzip()
  if bad:raise RuntimeError(f'ZIP integrity failure: {bad}')
 digest=hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()
 archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n')
 print(f'ZIP verified: {archive} ({archive.stat().st_size:,} bytes)',flush=True)
if __name__=='__main__':main()
