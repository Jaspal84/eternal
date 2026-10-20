#!/usr/bin/env python3
"""Split an existing ZIP without changing it. Verify full and part SHA-256 hashes."""
import argparse,hashlib,json
from pathlib import Path
CHUNK=1024**3
BLOCK=8*1024**2

def digest(path):
 with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('output',type=Path)
 args=p.parse_args();archive=args.archive.resolve();out=args.output.resolve()
 if not archive.is_file():p.error('Archive does not exist')
 # Never overwrite pre-existing assets; original library/archive remain untouched.
 out.mkdir(parents=True,exist_ok=False)
 original_hash=digest(archive);parts=[];joined=hashlib.sha256()
 with archive.open('rb') as src:
  index=1
  while True:
   data=src.read(min(BLOCK,CHUNK))
   if not data:break
   path=out/f'{archive.name}.part{index:03d}';written=0;h=hashlib.sha256()
   with path.open('xb') as target:
    while data:
     target.write(data);h.update(data);joined.update(data);written+=len(data)
     if written==CHUNK:break
     data=src.read(min(BLOCK,CHUNK-written))
   parts.append(dict(name=path.name,size=written,sha256=h.hexdigest()));index+=1
 if joined.hexdigest()!=original_hash:raise RuntimeError('Reconstructed stream differs from source')
 for part in parts:
  if digest(out/part['name'])!=part['sha256']:raise RuntimeError('Part reread hash mismatch')
 manifest=dict(archive=archive.name,size=archive.stat().st_size,sha256=original_hash,parts=parts)
 (out/'assets.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (out/'SHA256SUMS').write_text(''.join(f"{x['sha256']}  {x['name']}\n" for x in parts))
 (out/f'{archive.name}.sha256').write_text(f'{original_hash}  {archive.name}\n')
 print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
