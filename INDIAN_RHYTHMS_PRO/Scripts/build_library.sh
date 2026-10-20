#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Use an activated Python 3.12+ virtual environment; see README.
python3 generate_samples.py
python3 generate_midi.py
python3 render_loops.py
python3 -m unittest discover -s . -p 'test_*.py' -v 2>&1 | tee ../Documentation/UNIT_TESTS.txt
python3 validate_audio.py
python3 package_library.py
