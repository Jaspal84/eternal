# Logic Pro on Apple Silicon

This is an audio/MIDI library, not an AU plugin. It needs no Rosetta translation or plugin installation for WAV playback. Actual Logic host testing remains outstanding.

## Loops

1. Unzip to a local sample-library folder.
2. Set the project tempo to the BPM in the loop filename and its time signature to the matching meter. Use 16/4 for Teen Taal and 7/4 for Rupak if the installed Logic version permits; otherwise use four 4/4 measures for each Teen Taal cycle and preserve total quarter-note length.
3. Drag a 10_WAV_Loops file onto an audio track without tempo conversion for initial checking. Repeat it at its exact cycle boundary. Listen across repeats and inspect duration before enabling Flex/time stretching.
4. These are plain WAV files, not Apple Loops with embedded tempo tags. Filenames and groove manifests supply the timing; do not assume automatic tempo recognition.

## Quick Sampler

Drag one mono one-shot onto Quick Sampler, choose One Shot playback, and disable looping. This is useful for single-hit auditioning; it does not automatically recreate the full multi-articulation velocity/round-robin kit. Select an open or muted articulation explicitly.

## Sampler: custom multi-articulation kit

1. Create a Software Instrument track and load Sampler. Open its Mapping and Zone views (labels may vary by Logic version).
2. Add each WAV as a zone, using Documentation/NOTE_MAP.csv for its key number. Set low/high key to that single note. Do not rely on filenames' octave names or automatic pitch detection.
3. Set velocity ranges: v1 = 1–42, v2 = 43–85, v3 = 86–127. Both rr1 and rr2 share the note and velocity range.
4. Assign mutually exclusive round-robin/group selection using the installed Sampler version's supported group-selection controls. If unavailable, use rr1 only; stacking both rr files will double-trigger. A compatible SFZ player is the supplied automatic mapping route. No native Logic patch file is provided.
5. Use one-shot playback or sufficiently long amplitude release so short MIDI note-offs do not cut off drum tails. Avoid applying full velocity attenuation a second time if matching the generated layer dynamics is desired.
6. Save the configured Sampler instrument in your user library through Logic's supported Save command. Keep the referenced WAV files available or use the host's supported sample-copy option.
7. Drag matching MIDI from 09_MIDI_Grooves onto this track. Verify note numbers, all velocity layers, round-robin behavior and absence of stuck notes. MIDI channel 10 is used throughout.

MIDI triggering and the pre-rendered loops will not necessarily null because hosts differ in panning, voice release, gain and round-robin reset behavior. Only actual playback on the target Mac can establish host compatibility and musical quality.
