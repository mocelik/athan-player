# athan-player

A small Python CLI that plays the athan at the five daily prayer times. Prayer
times are calculated with `adhanpy`; by default the location is determined from
the machine's IP address using `geocoder`, but you can also provide explicit
latitude and longitude.

**Install**

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

**Usage**

Play the athan (provide a sound file):

```bash
python play_athan.py path/to/athan.mp3
```

Provide an explicit latitude/longitude (format: `lat,lon`):

```bash
python play_athan.py path/to/athan.mp3 --latlon "40.7128,-74.0060"
```

The script also accepts `--latlong` as an alternative flag name.

**Notes**

- Make sure your environment can play sound (pygame uses the system audio).
- If running on a server without audio, consider forwarding sound or using a
	different mechanism to play/stream the file.

See `requirements.txt` for the list of Python packages needed.
