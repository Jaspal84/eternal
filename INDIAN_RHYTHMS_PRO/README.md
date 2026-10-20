# INDIAN RHYTHMS PRO

Original synthesized Bollywood & Punjabi percussion library for sample-based music production. All sounds are **synthetic approximations**, not recordings of acoustic instruments or proprietary Pitch Innovations content. Developer: Jaspal project; generated implementation and audio supplied with this library.

## Included

- 41 articulations across tabla, dholak, Punjabi dhol, dandiya, duff/dafli, manjira/khartal, ghatam/kanjira, electronic kick/snare/clap/hat.
- Three velocity layers × two round robins: 246 mono PCM24 / 48 kHz WAV one-shots.
- 12 named rhythm/meter variants × three tempos × seven sections × four lengths: 1,008 MIDI files and 1,008 stereo PCM24 / 48 kHz WAV loops.
- Nine SFZ maps: eight folder kits and one combined kit, with velocity and sequential round-robin mapping.
- Complete reproducible source and machine-readable sample/groove manifests, note mapping and validation results.

These are newly arranged educational groove approximations, not definitive performances of every regional tradition. Garba, Raas, Bhangra, wedding and Bollywood patterns are stylized production grooves. No expert performance or listening review has been performed. See Documentation/RHYTHMS.md for taal structure and tempo conventions.

## Use the finished library

Unzip the archive. Import a WAV loop into an audio track, or load an SFZ kit into a compatible SFZ sampler and import the matching MIDI. These MIDI files use a custom mapping on channel 10, not General MIDI. `Documentation/NOTE_MAP.csv` is authoritative; octave names vary by host. Loading MIDI into an unrelated kit produces different sounds.

Use the BPM in the filename for the original playback tempo. Loop BPM is measured in quarter notes per minute, including 6/8; dotted-quarter pulse is two-thirds of the named BPM. In 16/4 and 7/4 files, one filename “bar” means one complete taal cycle. Sections are phrase variants, including loopable ending phrases rather than single final hits with exported trailing silence.

## Rebuild on Apple Silicon macOS or Linux

Use Python 3.12 or newer. Python, NumPy, SciPy and SoundFile must match your machine architecture; no external DSP hardware is required. On Apple Silicon, use native arm64 Python (verify `python3 -c 'import platform; print(platform.machine())'` returns `arm64`). A macOS build was not executed here.

```sh
cd INDIAN_RHYTHMS_PRO
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r Scripts/requirements.txt
bash Scripts/build_library.sh
```

The build regenerates the named WAV/MIDI files and mappings, tests DSP/timing behavior, validates outputs, and creates `../INDIAN_RHYTHMS_PRO.zip` plus a SHA-256 checksum. It excludes the venv and Python caches. Dependencies are pinned; Python/libsndfile/platform differences can affect exact encoded bytes across systems. Deterministic random seeds reproduce synthesis and phrasing under the same software stack. Build outputs overwrite generated paths: keep personal edits elsewhere. Remove obsolete generated WAV/MIDI files before rebuilding after changing the library definitions; inventory validation rejects extras.

Allow several GB of free disk space for the expanded library, archive and working buffers. Audio rendering and full ZIP integrity checking take time. No network is used during generation after dependencies are installed.

## Audio design

Modal oscillators, pitch envelopes, filtered noise and delayed transients create the percussion. Open/muted variants are explicitly named; tabla bol names describe modeled gestures rather than authentic recorded bol timbres. Dha/Dhin use composite synthetic modes. Dandiya double/roll articulations include internal delayed hits. Round-robin variants have reproducible pitch/noise variation.

One-shots have short attack shaping, DC filtering and faded decays. Layers peak at 0.24/0.48/0.78 full scale. The MIDI adds restrained timing, velocity and optional swing changes; traditional Teen Taal and Rupak avoid the extra swing offset. Timing variation in MIDI is expressed in quarter-note units, not fixed milliseconds.

The renderer reads exported MIDI, alternates round robins, assigns gentle stereo positions and uses the same velocity-layer boundaries as the SFZ. It sums every tail modulo the exact loop length, including tails longer than a loop. This creates a steady-state repeat without discarding tail energy. At a first playback start, preceding-cycle tail energy can be audible by design. No separate reverb or acoustic room was recorded.

Loops target -22 dBFS RMS with a -1 dBFS peak ceiling through static gain, not clipping/limiting. Peak constraints may lower RMS. RMS matching is not guaranteed equal perceived loudness or LUFS normalization. Automated seam checks detect suspicious jumps but do not replace listening to repeated loops.

## Compatibility and licensing

See Documentation/LOGIC_PRO.md and 12_Sonic_Atlas_Import/README.md. Logic/Sonic Atlas/SFZ-host playback has not been tested in this Linux environment. No proprietary Sonic Atlas preset is supplied and no vendor endorsement is implied.

See LICENSE.txt: you may use the original generated samples and grooves royalty-free, including commercial music, and redistribute this library under its included permissive license. No exclusivity, acoustic authenticity, or vendor certification is claimed.
