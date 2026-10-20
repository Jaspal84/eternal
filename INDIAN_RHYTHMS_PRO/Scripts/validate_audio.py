#!/usr/bin/env python3
import hashlib,json,re
from datetime import datetime,timezone
import mido
import numpy as np
import soundfile as sf
from core import ROOT,SR,ARTS,BY_NOTE,RHYTHMS,SECTIONS,BARS

def main():
 failures=[];checks=0;hashes={};rows=[]
 def check(ok,message):
  nonlocal checks
  checks+=1
  if not ok: failures.append(message)
 samples=json.loads((ROOT/'Documentation/samples.json').read_text());grooves=json.loads((ROOT/'Documentation/grooves.json').read_text())
 check(len(samples)==len(ARTS)*6,'sample count')
 check(len(grooves)==len(RHYTHMS)*3*len(SECTIONS)*len(BARS),'groove count')
 expected={s['path'] for s in samples}|{g['wav'] for g in grooves}
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.wav')}
 check(expected==actual,'missing or unexpected WAVs')
 check(len({g['stem'] for g in grooves})==len(grooves),'duplicate groove names')
 check({str(p.relative_to(ROOT)) for p in ROOT.rglob('*.mid')}=={g['midi'] for g in grooves},'MIDI inventory')
 smap={s['path']:s for s in samples};gmap={g['wav']:g for g in grooves}
 for rel in sorted(expected):
  path=ROOT/rel
  if not path.exists(): check(False,f'missing {rel}');continue
  try: x,sr=sf.read(path,always_2d=True,dtype='float64');info=sf.info(path)
  except Exception as e: check(False,f'{rel}: {e}');continue
  check(sr==SR and info.subtype=='PCM_24' and info.format=='WAV',f'format {rel}')
  check(np.isfinite(x).all(),f'nonfinite {rel}')
  peak=float(np.max(np.abs(x)));check(0<peak<1,f'peak {rel}')
  digest=hashlib.sha256(path.read_bytes()).hexdigest();check(digest not in hashes,f'duplicate audio {rel}');hashes[digest]=rel
  if rel in smap:
   s=smap[rel];check(x.shape==(s['frames'],1),f'mono frames {rel}')
   check(bool(re.fullmatch(r'SYNTH_[A-Za-z_]+_v[123]_rr[12]\.wav',path.name)),f'name {rel}')
   check(np.max(np.abs(x[-1]))<1e-6,f'one-shot tail {rel}')
  else:
   g=gmap[rel];frames=round(g['ticks']/960*g['tempo']/1e6*SR)
   check(x.shape==(frames,2),f'loop duration/channels {rel}')
   rms=float(20*np.log10(np.sqrt(np.mean(x*x))));check(-45<rms<-10,f'loop RMS {rel}')
   # Compare circular seam derivative with the strongest normal sample step.
   seam=float(np.max(np.abs(x[0]-x[-1])));internal=float(np.max(np.abs(np.diff(x,axis=0))))
   check(seam<=max(.02,internal*1.25),f'boundary discontinuity {rel}')
   check(np.any(x[:min(SR//4,len(x))]),f'leading silence {rel}')
   rows.append(dict(path=rel,peak=peak,rms_dbfs=rms,seam_step=seam))
 for g in grooves:
  path=ROOT/g['midi']
  if not path.exists():check(False,f'missing {path}');continue
  m=mido.MidiFile(path);tick=0;notes=0;active={};tempo=[];sig=[]
  check(m.type==0 and m.ticks_per_beat==960,f'MIDI format {path}')
  for msg in m.tracks[0]:
   tick+=msg.time
   if msg.type=='set_tempo':tempo.append(msg.tempo)
   if msg.type=='time_signature':sig.append((msg.numerator,msg.denominator))
   if msg.type=='note_on' and msg.velocity:
    notes+=1;check(msg.note in BY_NOTE and msg.channel==9,f'note map {path}');active[msg.note]=active.get(msg.note,0)+1
   if msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
    active[msg.note]=active.get(msg.note,0)-1;check(active[msg.note]>=0,f'orphan note-off {path}')
  check(notes==g['notes'] and notes>0,f'note count {path}')
  check(all(v==0 for v in active.values()),f'stuck note {path}')
  check(tick==g['ticks'] and tempo==[g['tempo']] and sig==[(g['numerator'],g['denominator'])],f'timing metadata {path}')
  check(abs(m.length-g['ticks']/960*g['tempo']/1e6)<1e-7,f'MIDI duration {path}')
 for sfz in (ROOT/'11_SFZ_Instrument_Maps').glob('*.sfz'):
  refs=re.findall(r'sample=(.+)',sfz.read_text());check(len(refs)>0,f'empty SFZ {sfz}')
  check('loop_mode=one_shot' in sfz.read_text(),f'SFZ one-shot playback {sfz}')
  for ref in refs:check((ROOT/ref).is_file(),f'SFZ missing sample {ref}')
 report=dict(created_utc=datetime.now(timezone.utc).isoformat(),checks=checks,failures=failures,samples=len(samples),midi=len(grooves),loops=len(grooves),unique_audio_hashes=len(hashes),loop_rms_range=[min(r['rms_dbfs'] for r in rows),max(r['rms_dbfs'] for r in rows)],loop_metrics=rows)
 (ROOT/'Documentation/validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (ROOT/'Documentation/VALIDATION_REPORT.md').write_text(f"# Automated validation\n\n{checks} checks; {len(failures)} failures.\n\n{len(samples)} mono samples, {len(grooves)} MIDI files, {len(grooves)} stereo loops.\n\nLoop RMS range: {report['loop_rms_range']} dBFS. RMS matching is not a perceptual LUFS guarantee.\n\n"+'\n'.join(f'- {f}' for f in failures)+"\n\nChecks cover PCM24/48kHz, finite audio, peaks, mono/stereo, manifest inventories, unique audio hashes, names, sample tails, exact MIDI and WAV duration, tempo/signatures, note mapping, note balance, circular boundary steps and SFZ sample references.\n\nNot validated: listening quality, acoustic realism, expert ethnomusicological review, Logic/Sonic Atlas/SFZ host playback, or macOS execution. Periodized loops contain preceding-cycle tails by design; endings are loopable phrases, not isolated final decay exports.\n")
 print(f'Validation: {checks} checks, {len(failures)} failures.',flush=True)
 for f in failures[:20]: print(f)
 if failures: raise SystemExit(1)
if __name__=='__main__':main()
