import unittest
import numpy as np
from core import ARTS,RHYTHMS,events_for,synth,rng_for
from render_loops import add_wrapped
class LibraryTests(unittest.TestCase):
 def test_seed_reproduction(self):
  a=synth('Tabla_Tin',2,1);b=synth('Tabla_Tin',2,1);c=synth('Tabla_Tin',2,2)
  np.testing.assert_array_equal(a,b)
  self.assertFalse(np.array_equal(a,c))
 def test_velocity_layers(self):
  peaks=[max(abs(synth('Dhol_Dagga_Open',v,1))) for v in [1,2,3]]
  self.assertTrue(peaks[0]<peaks[1]<peaks[2]<1)
 def test_unique_notes(self):self.assertEqual(len(ARTS),len({a['note'] for a in ARTS.values()}))
 def test_periodization_preserves_all_tail_energy(self):
  out=np.zeros((4,2));add_wrapped(out,np.arange(1.,11.),3,np.ones(2))
  np.testing.assert_array_equal(out[:,0],[18,10,12,15])
  self.assertEqual(out[:,0].sum(),55)
 def test_taal_cycles(self):
  teen=next(r for r in RHYTHMS if r[0]=='Teen_Taal');rupak=next(r for r in RHYTHMS if r[0]=='Rupak')
  self.assertEqual(events_for(teen,'Main',1)[1],16)
  self.assertEqual(events_for(rupak,'Main',1)[1],7)
  self.assertEqual(rupak[5],[0,3,5]);self.assertEqual(teen[5],[0,4,8,12])
 def test_events_in_cycle_and_reproducible(self):
  for r in RHYTHMS:
   a,d=events_for(r,'Fill',8);self.assertEqual(a,events_for(r,'Fill',8)[0])
   self.assertTrue(all(0<=p<d and n in ARTS and 1<=v<=127 for p,n,v in a))
if __name__=='__main__':unittest.main()
