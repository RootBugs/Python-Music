import wave
import struct
import math
import array

SAMPLE_RATE = 44100

NOTES = {
    'Sa': 261.63, 'Re': 293.66, 'Ga': 329.63, 'Ma': 349.23,
    'Pa': 392.00, 'Dha': 440.00, 'Ni': 493.88, 'Sa2': 523.25,
    'Re2': 587.33,
}

# --- SITAR (melody) ---
def gen_sitar(freq, dur, vol=0.5):
    n = int(SAMPLE_RATE * dur)
    out = array.array('h', [0] * n)
    attack = int(0.03 * SAMPLE_RATE)
    release = int(0.1 * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        # Rich harmonics like sitar
        val = (math.sin(6.2832 * freq * t) * 0.45 +
               math.sin(6.2832 * freq * 2 * t) * 0.25 +
               math.sin(6.2832 * freq * 3 * t) * 0.12 +
               math.sin(6.2832 * freq * 4 * t) * 0.06 +
               math.sin(6.2832 * freq * 5 * t) * 0.04)
        # Slight buzz modulation (jivari effect)
        val *= 1.0 + 0.06 * math.sin(6.2832 * 4.5 * t)
        # Envelope
        if i < attack:
            env = (i / attack) ** 1.5
        elif i > n - release:
            env = ((n - i) / release) ** 2
        else:
            env = 1.0
        out[i] = int(max(-1.0, min(1.0, val * vol * env)) * 32767)
    return out

# --- BAYAN (bass tabla) with pitch bend ---
def gen_bayan(dur=0.35):
    n = int(SAMPLE_RATE * dur)
    out = array.array('h', [0] * n)
    base_freq = 85
    for i in range(n):
        t = i / SAMPLE_RATE
        # Pitch rises slightly then falls (glissando)
        progress = i / n
        freq_bend = base_freq * (1.0 + 0.25 * math.sin(6.2832 * 0.4 * t) * (1 - progress))
        # Multiple harmonics for resonance
        val = (math.sin(6.2832 * freq_bend * t) * 0.5 +
               math.sin(6.2832 * freq_bend * 2 * t) * 0.25 +
               math.sin(6.2832 * freq_bend * 3 * t) * 0.1)
        # Slow exponential decay with resonance
        env = math.exp(-t * 5) * (1 + 0.3 * math.exp(-t * 15))
        out[i] = int(max(-1.0, min(1.0, val * 0.55 * env)) * 32767)
    return out

# --- DAYAN (treble tabla) with ring ---
def gen_dayan(dur=0.3):
    n = int(SAMPLE_RATE * dur)
    out = array.array('h', [0] * n)
    base_freq = 210
    for i in range(n):
        t = i / SAMPLE_RATE
        # Sharp attack with metallic ring
        val = (math.sin(6.2832 * base_freq * t) * 0.35 +
               math.sin(6.2832 * base_freq * 2.02 * t) * 0.2 +  # slight detuning
               math.sin(6.2832 * base_freq * 3.05 * t) * 0.1 +
               math.sin(6.2832 * base_freq * 4.1 * t) * 0.05)
        # Fast decay then slow ring
        env = math.exp(-t * 12) * 0.7 + math.exp(-t * 3) * 0.3
        out[i] = int(max(-1.0, min(1.0, val * 0.5 * env)) * 32767)
    return out

# --- BOL COMBINATIONS ---
def bol_dha():
    """Bayan + Dayan together"""
    b = gen_bayan(0.4)
    d = gen_dayan(0.3)
    n = max(len(b), len(d))
    out = array.array('h', [0] * n)
    for i in range(n):
        bv = b[i] / 32767.0 if i < len(b) else 0
        dv = d[i] / 32767.0 if i < len(d) else 0
        out[i] = int(max(-1.0, min(1.0, (bv + dv) * 0.7)) * 32767)
    return out

def bol_dhin():
    """Bayan + Dayan (softer, deeper)"""
    b = gen_bayan(0.45)
    d = gen_dayan(0.35)
    n = max(len(b), len(d))
    out = array.array('h', [0] * n)
    for i in range(n):
        bv = b[i] / 32767.0 if i < len(b) else 0
        dv = d[i] / 32767.0 if i < len(d) else 0
        out[i] = int(max(-1.0, min(1.0, (bv * 0.6 + dv * 0.8) * 0.65)) * 32767)
    return out

def bol_tin():
    """Dayan only (ringing)"""
    return gen_dayan(0.35)

def bol_na():
    """Dayan sharp (sharp attack)"""
    n = int(SAMPLE_RATE * 0.25)
    out = array.array('h', [0] * n)
    freq = 230
    for i in range(n):
        t = i / SAMPLE_RATE
        val = (math.sin(6.2832 * freq * t) * 0.4 +
               math.sin(6.2832 * freq * 2 * t) * 0.2 +
               math.sin(6.2832 * freq * 3 * t) * 0.08)
        env = math.exp(-t * 18)
        out[i] = int(max(-1.0, min(1.0, val * 0.5 * env)) * 32767)
    return out

def bol_tun():
    """Bayan deep hit"""
    return gen_bayan(0.4)

# --- TANPURA DRONE ---
def gen_drone(dur):
    n = int(SAMPLE_RATE * dur)
    out = array.array('h', [0] * n)
    sa, pa = NOTES['Sa'], NOTES['Pa']
    for i in range(n):
        t = i / SAMPLE_RATE
        # Rich tanpura with jivari buzz
        val = (math.sin(6.2832 * sa * t) * 0.4 +
               math.sin(6.2832 * sa * 2 * t) * 0.2 +
               math.sin(6.2832 * sa * 3 * t) * 0.08 +
               math.sin(6.2832 * pa * t) * 0.4 +
               math.sin(6.2832 * pa * 2 * t) * 0.15) * 0.07
        val *= 0.85 + 0.15 * math.sin(6.2832 * 0.12 * t)
        out[i] = int(max(-1.0, min(1.0, val)) * 32767)
    return out

# --- CROSSFADE ---
def crossfade(a, b, overlap):
    result = array.array('h', a)
    if overlap > len(a):
        overlap = len(a)
    if overlap > len(b):
        overlap = len(b)
    for i in range(overlap):
        t = i / overlap
        idx = len(a) - overlap + i
        val = result[idx] * (1 - t) + b[i] * t
        result[idx] = int(max(-32767, min(32767, val)))
    result.extend(b[overlap:])
    return result

# --- MELODY ---
print("Generating Raag Yaman (Sitar)...")
melody_notes = [
    ('Sa', 0.7), ('Re', 0.5), ('Ga', 0.5), ('Ma', 0.8), ('Pa', 0.6),
    ('Dha', 0.5), ('Ni', 0.7), ('Sa2', 0.9),
    ('Ni', 0.4), ('Dha', 0.5), ('Pa', 0.7), ('Ma', 0.6),
    ('Ga', 0.5), ('Re', 0.7), ('Sa', 0.9),
    ('Pa', 0.25), ('Pa', 0.25), ('Dha', 0.35), ('Sa2', 0.45),
    ('Ni', 0.25), ('Dha', 0.25), ('Pa', 0.45),
    ('Ma', 0.25), ('Pa', 0.25), ('Dha', 0.35), ('Sa2', 0.45),
    ('Re2', 0.35), ('Sa2', 0.35), ('Ni', 0.25), ('Dha', 0.45),
    ('Pa', 0.35), ('Ma', 0.25), ('Ga', 0.25), ('Re', 0.45),
    ('Sa', 0.5), ('Re', 0.25), ('Ga', 0.35), ('Ma', 0.45),
    ('Pa', 0.6), ('Ga', 0.25), ('Re', 0.35), ('Sa', 0.7),
    ('Pa', 0.25), ('Pa', 0.25), ('Dha', 0.35), ('Sa2', 0.45),
    ('Sa2', 0.25), ('Ni', 0.25), ('Dha', 0.35), ('Pa', 0.45),
    ('Dha', 0.25), ('Pa', 0.25), ('Ma', 0.35), ('Ga', 0.45),
    ('Re', 0.35), ('Ga', 0.25), ('Ma', 0.35), ('Pa', 0.45),
    ('Dha', 0.25), ('Sa2', 0.25), ('Ni', 0.35), ('Dha', 0.45),
    ('Pa', 0.6), ('Ma', 0.25), ('Ga', 0.35), ('Re', 0.45), ('Sa', 0.9),
    ('Sa', 0.12), ('Re', 0.12), ('Ga', 0.12), ('Ma', 0.12),
    ('Pa', 0.12), ('Dha', 0.12), ('Ni', 0.12), ('Sa2', 0.2),
    ('Ni', 0.12), ('Dha', 0.12), ('Pa', 0.12), ('Ma', 0.12),
    ('Ga', 0.12), ('Re', 0.12), ('Sa', 0.4),
    ('Pa', 0.5), ('Dha', 0.4), ('Sa2', 0.7),
    ('Ni', 0.4), ('Dha', 0.4), ('Pa', 0.6),
    ('Ma', 0.5), ('Ga', 0.4), ('Re', 0.6), ('Sa', 1.0),
]

fade_len = int(0.025 * SAMPLE_RATE)
melody = array.array('h', [0] * fade_len)
for note, dur in melody_notes:
    tone = gen_sitar(NOTES[note], dur, 0.5)
    melody = crossfade(melody, tone, fade_len)

total_dur = len(melody) / SAMPLE_RATE

# --- TABLA (real bols in Teental) ---
print("Adding realistic Tabla (Teental - Dha Dhin Dhin Dha)...")
# Teental: Dha Dhin Dhin Dha | Dha Dhin Dhin Dha | Dha Tin Tin Ta | Ta Dhin Dhin Dha
teental_bols = [
    'dha', 'dhin', 'dhin', 'dha',
    'dha', 'dhin', 'dhin', 'dha',
    'dha', 'tin', 'tin', 'na',
    'na', 'dhin', 'dhin', 'dha',
]
bol_fns = {
    'dha': bol_dha, 'dhin': bol_dhin, 'tin': bol_tin,
    'na': bol_na, 'tun': bol_tun,
}

tabla_track = array.array('h', [0] * len(melody))
pos = 0
beat_samples = int(0.38 * SAMPLE_RATE)
for b in range(int(total_dur / 0.38) + 1):
    if pos + beat_samples > len(tabla_track):
        break
    bol_name = teental_bols[b % 16]
    bol_sound = bol_fns[bol_name]()
    for i in range(min(len(bol_sound), beat_samples)):
        tabla_track[pos + i] = bol_sound[i]
    pos += beat_samples

# --- DRONE ---
print("Adding Tanpura drone...")
drone = gen_drone(total_dur)

# --- MIX ---
print("Mixing all tracks...")
min_len = min(len(melody), len(drone), len(tabla_track))
final = array.array('h', [0] * min_len)
for i in range(min_len):
    m = melody[i] / 32767.0
    d = drone[i] / 32767.0
    t = tabla_track[i] / 32767.0
    val = max(-1.0, min(1.0, m * 0.5 + d * 0.2 + t * 0.4))
    final[i] = int(val * 32767)

# --- WRITE ---
out_file = 'Raag_Yaman_Indian_Classical.wav'
print(f"Saving {out_file}...")
with wave.open(out_file, 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SAMPLE_RATE)
    w.writeframes(final.tobytes())

print(f"\nDone! Duration: {total_dur:.1f}s")
print("Tabla: Real bols with Bayan (bass glissando) + Dayan (treble ring)")
print("Bols used: Dha, Dhin, Tin, Na")
print("Sitar: Rich harmonics + jivari buzz")
print("Tanpura: Sa + Pa drone with shimmer")
