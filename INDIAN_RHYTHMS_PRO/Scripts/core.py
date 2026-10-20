"""Original synthetic percussion and educational groove definitions. No sampled sources."""
from pathlib import Path
import hashlib
import numpy as np
SR = 48000
ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['01_Tabla', '02_Dholak', '03_Punjabi_Dhol', '04_Dandiya',
 '05_Duff_Dafli', '06_Manjira_Khartal', '07_Ghatam_Kanjira', '08_Bollywood_Drums',
 '09_MIDI_Grooves', '10_WAV_Loops', '11_SFZ_Instrument_Maps', '12_Sonic_Atlas_Import', 'Documentation']
# name, folder index, synthesis family, fundamental Hz, decay seconds
DEFS = [
 ('Tabla_Na',0,'tabla',420,.22),('Tabla_Tin',0,'tabla',570,.42),
 ('Tabla_Tun',0,'tabla',310,.65),('Tabla_Ta',0,'muted',470,.075),
 ('Tabla_Dha',0,'compound',170,.46),('Tabla_Dhin',0,'compound',210,.52),
 ('Tabla_Ge',0,'bass',95,.50),('Tabla_Ke',0,'muted',140,.07),
 ('Dholak_Bass_Open',1,'bass',105,.40),('Dholak_Bass_Muted',1,'muted',105,.09),
 ('Dholak_Treble_Open',1,'skin',350,.28),('Dholak_Treble_Muted',1,'muted',350,.07),
 ('Dhol_Dagga_Open',2,'bass',75,.55),('Dhol_Dagga_Muted',2,'muted',80,.12),
 ('Dhol_Tilli_Open',2,'skin',310,.34),('Dhol_Tilli_Muted',2,'muted',320,.08),
 ('Dhol_Accent',2,'compound',115,.48),
 ('Dandiya_Single_Open',3,'wood',1600,.12),('Dandiya_Single_Muted',3,'wood',1300,.045),
 ('Dandiya_Double',3,'double',1600,.12),('Dandiya_Roll',3,'roll',1500,.14),
 ('Duff_Open',4,'skin',135,.48),('Duff_Muted',4,'muted',150,.10),
 ('Dafli_Open',4,'jingle',210,.42),('Dafli_Muted',4,'jingle',260,.10),
 ('Manjira_Open',5,'metal',2100,.70),('Manjira_Muted',5,'metal',2300,.11),
 ('Khartal_Open',5,'wood',1250,.15),('Khartal_Muted',5,'wood',1450,.045),
 ('Ghatam_Open',6,'clay',220,.29),('Ghatam_Muted',6,'clay',380,.07),
 ('Kanjira_Open',6,'jingle',165,.30),('Kanjira_Muted',6,'jingle',230,.07),
 ('Electronic_Kick_Open',7,'kick',52,.28),('Electronic_Kick_Muted',7,'kick',65,.11),
 ('Electronic_Snare_Open',7,'snare',180,.20),('Electronic_Snare_Muted',7,'snare',210,.07),
 ('Electronic_Clap_Open',7,'clap',950,.18),('Electronic_Clap_Muted',7,'clap',1100,.07),
 ('Electronic_Hat_Open',7,'hat',6500,.32),('Electronic_Hat_Muted',7,'hat',7200,.045)]
ARTS = {d[0]:dict(folder=FOLDERS[d[1]],kind=d[2],freq=d[3],decay=d[4],note=36+i) for i,d in enumerate(DEFS)}
BY_NOTE = {a['note']:name for name,a in ARTS.items()}
def rng_for(key):
 return np.random.default_rng(int.from_bytes(hashlib.sha256(key.encode()).digest()[:8],'little'))
# Denominator defines MIDI time signature; sequence pulses equally divide one cycle.
RHYTHMS = [
 ('Keherwa',4,4,[80,110,140],['Tabla_Dha','Tabla_Ge','Tabla_Na','Tabla_Tin','Tabla_Na','Tabla_Ke','Tabla_Dhin','Tabla_Na'],[0,4],1),
 ('Dadra',6,8,[70,95,120],['Tabla_Dha','Tabla_Dhin','Tabla_Na','Tabla_Dha','Tabla_Tin','Tabla_Na'],[0,3],1),
 ('Teen_Taal',16,4,[70,105,140],['Tabla_Dha','Tabla_Dhin','Tabla_Dhin','Tabla_Dha','Tabla_Dha','Tabla_Dhin','Tabla_Dhin','Tabla_Dha','Tabla_Na','Tabla_Tin','Tabla_Tin','Tabla_Ta','Tabla_Ta','Tabla_Dhin','Tabla_Dhin','Tabla_Dha'],[0,4,8,12],0),
 ('Rupak',7,4,[70,95,120],['Tabla_Tin','Tabla_Tin','Tabla_Na','Tabla_Dhin','Tabla_Na','Tabla_Dhin','Tabla_Na'],[0,3,5],0),
 ('Garba_4_4',4,4,[100,130,160],['Duff_Open','Khartal_Open','Dafli_Open','Khartal_Muted','Duff_Open','Manjira_Open','Dafli_Open','Khartal_Open'],[0,4],1),
 ('Garba_6_8',6,8,[100,130,160],['Duff_Open','Khartal_Open','Khartal_Muted','Dafli_Open','Khartal_Open','Manjira_Open'],[0,3],1),
 ('Dandiya_Raas',4,4,[110,135,160],['Dandiya_Single_Open','Dandiya_Single_Muted','Dandiya_Double','Dandiya_Single_Open','Dandiya_Single_Open','Dandiya_Single_Muted','Dandiya_Double','Dandiya_Roll'],[0,4],1),
 ('Punjabi_Bhangra',4,4,[90,120,150],['Dhol_Dagga_Open','Dhol_Tilli_Muted','Dhol_Tilli_Open','Dhol_Dagga_Muted','Dhol_Accent','Dhol_Tilli_Open','Dhol_Dagga_Open','Dhol_Tilli_Open'],[0,4],1),
 ('Bollywood_Dance',4,4,[100,120,140],['Electronic_Kick_Open','Electronic_Hat_Muted','Electronic_Snare_Open','Electronic_Hat_Muted','Electronic_Kick_Open','Electronic_Clap_Open','Electronic_Snare_Open','Electronic_Hat_Open'],[0,2,4,6],1),
 ('Bollywood_Romantic_4_4',4,4,[65,85,105],['Dholak_Bass_Open','Dholak_Treble_Muted','Dholak_Treble_Open','Tabla_Na','Dholak_Bass_Muted','Dholak_Treble_Open','Tabla_Tin','Dholak_Treble_Muted'],[0,4],1),
 ('Bollywood_Romantic_6_8',6,8,[65,85,105],['Dholak_Bass_Open','Dholak_Treble_Muted','Tabla_Na','Dholak_Treble_Open','Tabla_Tin','Dholak_Treble_Muted'],[0,3],1),
 ('Wedding_Dhol',4,4,[95,125,155],['Dhol_Accent','Dhol_Tilli_Open','Dhol_Dagga_Open','Dhol_Tilli_Muted','Dhol_Accent','Dhol_Tilli_Open','Dhol_Dagga_Muted','Dhol_Tilli_Open'],[0,4],1)]
SECTIONS = ['Intro','Main','Variation_A','Variation_B','Fill','Break','Ending']
BARS = [1,2,4,8]

def synth(name,layer,rr):
 a=ARTS[name]; r=rng_for(f'sample:{name}:{layer}:{rr}')
 k=a['kind']; decay=a['decay']; f=a['freq']*r.uniform(.985,1.015)
 duration=decay*10+.025
 if k in ('double','roll'): duration+=.19
 t=np.arange(int(SR*duration))/SR
 noise=r.normal(size=t.size); attack=1-np.exp(-t*8000)
 env=np.exp(-t/decay)
 signal=np.zeros_like(t)
 if k in ('wood','double','roll'):
  for ratio,amp in [(1,1),(2.71,.5),(4.13,.25)]:
   signal+=amp*np.sin(2*np.pi*f*ratio*t)*np.exp(-t/(decay/ratio))
  signal+=.18*noise*np.exp(-t/.004)
 elif k in ('metal','hat'):
  for ratio in [1,1.342,1.867,2.43,3.12,3.87]:
   signal+=.17*np.sin(2*np.pi*f*ratio*t+r.uniform(-.3,.3))*env
  signal+=.16*np.diff(noise,prepend=0)*np.exp(-t/(decay*.55))
 elif k=='clap':
  from scipy.signal import butter,sosfilt
  n=sosfilt(butter(2,[600,8500],btype='bandpass',fs=SR,output='sos'),noise)
  for offset in [0,.011,.024]:
   j=int(offset*SR); signal[j:]+=n[:len(t)-j]*np.exp(-t[:len(t)-j]/decay)*.45
 else:
  pitch=f*(1+(.9 if k in ('kick','bass') else .12)*np.exp(-t/.022))
  phase=2*np.pi*np.cumsum(pitch)/SR
  ratios=[1,2,3,4.07] if k=='tabla' else [1,1.59,2.14,2.65]
  if k=='clay': ratios=[1,1.78,2.91,4.23]
  for i,ratio in enumerate(ratios):
   signal+=(.72/(i+1))*np.sin(phase*ratio)*np.exp(-t/(decay/(1+i*.7)))
  signal+=noise*(.25 if k in ('skin','muted','snare','jingle') else .09)*np.exp(-t/(.045 if k=='snare' else .009))
  if k=='snare': signal+=.45*noise*env
  if k=='compound': signal+=.65*np.sin(2*np.pi*430*t)*np.exp(-t/.23)
  if k=='jingle': signal+=.09*(np.sin(2*np.pi*3911*t)+np.sin(2*np.pi*5287*t))*np.exp(-t/(decay*.7))
 signal*=attack
 if k in ('double','roll'):
  base=signal.copy()
  for delay,amp in ([(.065,.75)] if k=='double' else [(.046,.7),(.089,.6),(.135,.48)]):
   j=int(SR*delay);signal[j:]+=base[:-j]*amp
 # Remove DC, add a short tail fade; no peak at file start or hard tail cutoff.
 from scipy.signal import butter,sosfilt
 signal=sosfilt(butter(2,25,btype='highpass',fs=SR,output='sos'),signal)
 fade=min(960,len(signal));signal[-fade:]*=np.linspace(1,0,fade)
 signal[0]=0
 signal*=([.24,.48,.78][layer-1]/max(np.max(np.abs(signal)),1e-9))
 return signal

def events_for(rhythm,section,bars):
 name,num,den,tempos,seq,accents,swing=rhythm
 r=rng_for(f'groove:{name}:{section}:{bars}')
 cycle=num*4/den; step=cycle/len(seq); total=cycle*bars
 out=[]
 for bar in range(bars):
  for i,original in enumerate(seq):
   inst=original; vel=(103 if i in accents else 77)+int(r.integers(-6,7))
   if section=='Intro' and bar==0 and i%2: continue
   if section=='Break' and i not in accents: continue
   if section=='Ending' and bar==bars-1 and i>len(seq)//2: continue
   if section=='Variation_A' and i%4==3:
    inst='Tabla_Ke' if name in ('Keherwa','Dadra','Teen_Taal','Rupak') else seq[(i+1)%len(seq)]
   if section=='Variation_B' and i%3==2: vel-=17
   if section=='Fill' and bar==bars-1 and i>=len(seq)//2:
    inst='Tabla_Ta' if name in ('Keherwa','Dadra','Teen_Taal','Rupak') else seq[i];vel+=5
   # Rupak sam is khali, with divisions 3+2+2; Teen taal khali is beat 9.
   if name=='Rupak' and i==0: vel=85
   if name=='Teen_Taal' and i==8: vel=85
   pos=bar*cycle+i*step
   pos+=step*.055 if swing and i%2 else 0
   if pos: pos+=r.uniform(-.008,.008)
   out.append((max(0,min(total-.04,pos)),inst,int(np.clip(vel,25,122))))
   if section=='Fill' and bar==bars-1 and i>=len(seq)//2:
    out.append((min(total-.04,pos+step*.5),inst,max(30,vel-20)))
 return sorted(out),total
