#!/usr/bin/env python3
"""Render actual MIDI files; periodize every tail rather than truncate at loop end."""
import json
import numpy as np
import soundfile as sf
import mido
from core import ROOT,SR,ARTS,BY_NOTE

def add_wrapped(dest,source,start,gain):
 offset=0
 while offset<len(source):
  p=(start+offset)%len(dest);n=min(len(source)-offset,len(dest)-p)
  dest[p:p+n]+=source[offset:offset+n,None]*gain[None,:];offset+=n

def main():
 manifest=json.loads((ROOT/'Documentation/grooves.json').read_text()); cache={};metrics=[]
 for index,g in enumerate(manifest):
  frames=round(g['ticks']/960*g['tempo']/1e6*SR);out=np.zeros((frames,2),dtype=np.float64)
  midi=mido.MidiFile(ROOT/g['midi']);tick=0;counts={}
  for msg in midi.tracks[0]:
   tick+=msg.time
   if msg.type!='note_on' or msg.velocity==0: continue
   name=BY_NOTE[msg.note];a=ARTS[name];layer=1 if msg.velocity<=42 else 2 if msg.velocity<=85 else 3
   rr=counts.get(msg.note,0)%2+1;counts[msg.note]=counts.get(msg.note,0)+1
   key=(name,layer,rr)
   if key not in cache: cache[key]=sf.read(ROOT/f"{a['folder']}/SYNTH_{name}_v{layer}_rr{rr}.wav",dtype='float64')[0]
   pan=((msg.note-36)%7-3)*.085
   gains=np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
   start=round(tick/midi.ticks_per_beat*g['tempo']/1e6*SR)
   add_wrapped(out,cache[key],start,gains)
  # A shared -22 dBFS RMS target, limited to -1 dBFS peak; no limiting/clipping.
  rms=np.sqrt(np.mean(out*out));peak=np.max(np.abs(out));gain=min(10**(-22/20)/max(rms,1e-12),10**(-1/20)/max(peak,1e-12));out*=gain
  path=ROOT/g['wav'];path.parent.mkdir(parents=True,exist_ok=True);sf.write(path,out,SR,subtype='PCM_24')
  metrics.append(dict(stem=g['stem'],frames=frames,peak=float(np.max(np.abs(out))),rms_dbfs=float(20*np.log10(np.sqrt(np.mean(out*out))))))
  if index%100==0: print(f'Rendered {index+1}/{len(manifest)}',flush=True)
 (ROOT/'Documentation/render_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
 print(f'Rendered {len(manifest)} stereo loops.',flush=True)
if __name__=='__main__': main()
