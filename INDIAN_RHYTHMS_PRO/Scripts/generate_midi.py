#!/usr/bin/env python3
import json
import mido
from core import ROOT,ARTS,RHYTHMS,SECTIONS,BARS,events_for
PPQ=960

def main():
 manifest=[]
 for rhythm in RHYTHMS:
  name,num,den,tempos,*_=rhythm
  for bpm in tempos:
   tempo=mido.bpm2tempo(bpm)
   for section in SECTIONS:
    for bars in BARS:
     events,total=events_for(rhythm,section,bars)
     stem=f'{name}_{bpm:03d}BPM_{section}_{bars}bar'
     path=ROOT/f'09_MIDI_Grooves/{name}/{stem}.mid';path.parent.mkdir(parents=True,exist_ok=True)
     mf=mido.MidiFile(type=0,ticks_per_beat=PPQ);track=mido.MidiTrack();mf.tracks.append(track)
     track.append(mido.MetaMessage('track_name',name=stem))
     track.append(mido.MetaMessage('set_tempo',tempo=tempo))
     track.append(mido.MetaMessage('time_signature',numerator=num,denominator=den))
     track.append(mido.MetaMessage('text',text='ORIGINAL SYNTH KIT: use supplied note map; not General MIDI.'))
     if name=='Teen_Taal': track.append(mido.MetaMessage('text',text='16 matra; vibhag 4+4+4+4; sam 1, tali 5/13, khali 9.'))
     if name=='Rupak': track.append(mido.MetaMessage('text',text='7 matra; vibhag 3+2+2; khali/sam 1, tali 4/6.'))
     messages=[]
     for pos,inst,vel in events:
      tick=round(pos*PPQ);note=ARTS[inst]['note']
      messages.extend([(tick,1,mido.Message('note_on',channel=9,note=note,velocity=vel)),(min(round(total*PPQ),tick+60),0,mido.Message('note_off',channel=9,note=note,velocity=0))])
     last=0
     for tick,_,msg in sorted(messages,key=lambda e:(e[0],e[1])):
      track.append(msg.copy(time=tick-last));last=tick
     total_ticks=round(total*PPQ)
     track.append(mido.MetaMessage('end_of_track',time=total_ticks-last));mf.save(path)
     manifest.append(dict(stem=stem,rhythm=name,bpm=bpm,tempo=tempo,bars=bars,numerator=num,denominator=den,ticks=total_ticks,midi=str(path.relative_to(ROOT)),wav=f'10_WAV_Loops/{name}/{stem}.wav',notes=len(events)))
 (ROOT/'Documentation/grooves.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'Generated {len(manifest)} MIDI grooves.',flush=True)
if __name__=='__main__': main()
