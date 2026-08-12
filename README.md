# EZ2CV

EZ2CV extracts JSON chart data from EZ2ON REBOOT : R gameplay videos using
OpenCV.

**This project does not include any data (gameplay video, chart, note skins, etc.) from EZ2ON REBOOT: R. If you wish to run this project, please obtain the data yourself.**

## Requirements

- Python 3.14
- [uv](https://github.com/astral-sh/uv) for dependency management
- The pipeline supports **4K, 5K, 6K, and 8K** profiles at 1920×1080.
- The bundled profiles expect the recording setup below.

## Setup

```bash
uv sync
```

### Recording setup

- Resolution: 1920×1080
- FPS: 60
- Key mode: 4K, 5K, 6K, or 8K
- Panel skin: PG-RESPECT
- Note skin: EZ2ON
- Note speed: 8.0
- Judge line: old
- Judgement tracker: off
- Panel opacity: 100%
- Panel alignment: center
- Panel background: none
- Judge height: 700
- Record without player input; LIVE CTRL is recommended.

Event time uses decoded container PTS. The configured FPS must still match the
profile. The bundled profiles correct panel translation up to 32px; scale,
rotation, and other layouts require recalibration.

### Note templates

Template images are not included. Crop them from a clean frame at the same
resolution as the input video.

Place the following files under `config/skins/ez2on/<key_mode>/` (for example,
`config/skins/ez2on/6k/`):

| Filename | Description |
| -------- | ----------- |
| `note_cyan.png` | Cyan (active) note body |
| `note_cyan_lnhead.png` | Cyan long-note head |
| `note_cyan_lntail.png` | Cyan long-note tail |
| `note_white.png` | White (inactive) note body |
| `note_white_lnhead.png` | White long-note head |
| `note_white_lntail.png` | White long-note tail |

## Usage

Use `config/song.toml` as the template for a song config. Supported difficulty
values are `EZ`, `NM`, `HD`, and `SHD`.

Run the full pipeline:

```bash
uv run ez2cv
uv run ez2cv "config/<song>.toml"
```

`--force` accepts an FPS or alignment mismatch and records the fallback in the
raw checkpoint.

With no argument, all song configs directly under `config/` are processed.

The raw detection result is written before chart inference. Rebuild a chart
without decoding the video again:

```bash
uv run ez2cv "out/<song>/<difficulty>/<song>_raw.json" --from-raw
```

## Config layout

| File | Purpose |
| ---- | ------- |
| `config/<song>.toml` | Per-song settings (video path, fps, scroll speed, BPM range, etc.) |
| `config/skins/<skin>/skin.toml` | Per-skin lane colors, templates, detection channels, thresholds |
| `config/profiles/<res>/<key_mode>.toml` | Per-resolution / key-mode playfield geometry |
| `config/skins/<skin>/<key_mode>/*.png` | Note template images (not included; see Note Template Setup) |

## Output

Two JSON files are written under `out/<song>/<difficulty>/`:

- `<song>_raw.json` — reloadable ms-based detection checkpoint (schema 2.3)
- `<song>_chart.json` — `ez2cv.chart` 3.3 tick chart with explicit game, tempo,
  and meter timelines

## Tests

```bash
uv run python -m unittest discover -s tests -v
```

## License

Licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE) for personal,
non-commercial use. This project is not affiliated with or endorsed by
NEONOVICE. Game content belongs to its respective copyright holders.
