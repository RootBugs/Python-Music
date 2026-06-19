# Python-Music

Indian Classical Music Generator using pure Python — no external libraries required.

## What it generates

**Raag Yaman** (Evening Raga) with:

- **Sitar** — melody with rich harmonics and jivari buzz effect
- **Tabla** — realistic bols (Dha, Dhin, Tin, Na) in Teental (16-beat cycle) with bass glissando
- **Tanpura** — Sa + Pa drone with shimmer

## Output

| File | Duration | Size |
|------|----------|------|
| `Raag_Yaman_Indian_Classical.wav` | ~34s | ~3MB |

## How to run

```bash
python indian_song.py
```

Generates `Raag_Yaman_Indian_Classical.wav` in the current directory. Play with any media player.

## Requirements

- Python 3.x
- No pip packages needed (uses only `wave`, `struct`, `math`, `array`)

## Structure

```
Python-Music/
├── indian_song.py                    # Music generator script
├── Raag_Yaman_Indian_Classical.wav   # Generated output
└── README.md
```

## How it works

The script synthesizes audio from scratch using sine waves and harmonics:

1. **Sitar**: 5th harmonic stack with amplitude modulation for jivari (string buzz) effect
2. **Tablas**: Separate Bayan (bass, with pitch bend) and Dayan (treble, with metallic ring)
3. **Tanpura**: Continuous drone on Sa and Pa with slow shimmer modulation
4. Crossfading between notes eliminates pops/clicks
