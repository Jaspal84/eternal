#!/usr/bin/env python3
import json
import soundfile as sf
from core import ROOT,FOLDERS,ARTS,synth

def main():
 for folder in FOLDERS: (ROOT/folder).mkdir(exist_ok=True)
 manifest=[]
 for name,a in ARTS.items():
  for layer in range(1,4):
   for rr in range(1,3):
    path=f"{a['folder']}/SYNTH_{name}_v{layer}_rr{rr}.wav"
    data=synth(name,layer,rr); sf.write(ROOT/path,data,48000,subtype='PCM_24')
    manifest.append(dict(path=path,name=name,note=a['note'],layer=layer,rr=rr,frames=len(data)))
 (ROOT/'Documentation/samples.json').write_text(json.dumps(manifest,indent=2)+'\n')
 for folder in FOLDERS[:8]+['All_Instruments']:
  regions=['// Original synthesized approximations. MIDI note numbers are authoritative.', '<control> default_path=../', '<global> loop_mode=one_shot ampeg_release=0.03 amp_veltrack=0']
  for name,a in ARTS.items():
   if folder!='All_Instruments' and a['folder']!=folder: continue
   for layer,(lo,hi) in enumerate([(1,42),(43,85),(86,127)],1):
    regions.append(f"<group> key={a['note']} lovel={lo} hivel={hi} seq_length=2")
    for rr in [1,2]:
     regions.append(f"<region> seq_position={rr} sample={a['folder']}/SYNTH_{name}_v{layer}_rr{rr}.wav")
  (ROOT/f'11_SFZ_Instrument_Maps/{folder}.sfz').write_text('\n'.join(regions)+'\n')
 (ROOT/'Documentation/NOTE_MAP.csv').write_text('note,articulation,folder\n'+''.join(f"{a['note']},{n},{a['folder']}\n" for n,a in ARTS.items()))
 print(f'Generated {len(manifest)} mono one-shots and 9 SFZ maps.',flush=True)
if __name__=='__main__': main()
