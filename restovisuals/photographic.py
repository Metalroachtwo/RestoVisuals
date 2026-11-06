"""Original explicit linear-Rec.709 photographic reference, not a game hook."""
from dataclasses import dataclass, replace
import json
import math
from pathlib import Path
from .color_reference import decode_srgb, encode_srgb

ROOT = Path(__file__).resolve().parents[1]
LUMA = (0.2126, 0.7152, 0.0722)
LIMITS = {'intensity': (0, 1), 'exposure_ev': (-4, 4), 'highlight': (0, 1),
          'shadow': (-0.25, 0.5), 'saturation': (0, 1.5), 'contrast': (0.8, 1.2)}

def number(value, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError('Nonfinite, nonnumeric or out-of-range photographic value')
    return float(value)

@dataclass(frozen=True)
class Settings:
    intensity: float = 1.0
    exposure_ev: float = 0.0
    highlight: float = 0.0
    shadow: float = 0.0
    saturation: float = 1.0
    contrast: float = 1.0
    white_balance: tuple = (1.0, 1.0, 1.0)

    def __post_init__(self):
        for name, bounds in LIMITS.items():
            number(getattr(self, name), *bounds)
        if not isinstance(self.white_balance, (list, tuple)) or len(self.white_balance) != 3:
            raise ValueError('White balance requires three linear gains')
        object.__setattr__(self, 'white_balance', tuple(number(v, .8, 1.2) for v in self.white_balance))

    @property
    def neutral(self):
        return self.intensity == 0 or (self.exposure_ev == self.highlight == self.shadow == 0
            and self.saturation == self.contrast == 1 and self.white_balance == (1, 1, 1))

def presets():
    data = json.loads((ROOT / 'presets/photographic.json').read_text())
    return {name: Settings(**values) for name, values in data.items()}

def controlled(preset='balanced', *, intensity=1, exposure_ev=0, highlight=1,
               shadow=0, saturation=1, contrast=1):
    bank = presets()
    if preset not in bank:
        raise ValueError('Unknown photographic preset')
    values = locals()
    for name, bounds in LIMITS.items():
        number(values[name], *bounds)
    base = bank[preset]
    return replace(base, intensity=intensity, highlight=highlight,
                   exposure_ev=max(-4, min(4, base.exposure_ev + exposure_ev)),
                   shadow=max(-.25, min(.5, base.shadow + shadow)),
                   saturation=min(1.5, base.saturation * saturation),
                   contrast=max(.8, min(1.2, base.contrast * contrast)))

def process(color, settings=Settings(), *, encoding='linear_rec709', enabled=True):
    if not isinstance(settings, Settings) or type(enabled) is not bool:
        raise ValueError('Validated settings and boolean enable required')
    if encoding not in ('linear_rec709', 'srgb_rec709') or not isinstance(color, (list, tuple)) or len(color) != 4:
        raise ValueError('Explicit encoding and RGBA required')
    rgb = [number(v, 0, 65504 if encoding == 'linear_rec709' else 1) for v in color[:3]]
    alpha = number(color[3], 0, 1)
    if not enabled or settings.neutral:
        return tuple(color)  # Avoid decode/encode or cancellation in identity mode.
    original = [decode_srgb(v) for v in rgb] if encoding == 'srgb_rec709' else rgb
    gain_y = sum(w * g for w, g in zip(LUMA, settings.white_balance))
    exposed = [v * g / gain_y * 2 ** settings.exposure_ev for v, g in zip(original, settings.white_balance)]
    y = sum(w * v for w, v in zip(LUMA, exposed))
    if y > 0:
        tone = .18 * (y / .18) ** settings.contrast
        tone *= 1 + settings.shadow / (1 + tone / .18)
        graded = [v * tone / y for v in exposed]
        grey = sum(w * v for w, v in zip(LUMA, graded))
        graded = [max(0., grey + settings.saturation * (v - grey)) for v in graded]
        peak = max(graded)
        if peak > .72:
            # C1 soft knee, continuous at highlight=0. Full response approaches 1.
            mapped = .72 + (peak - .72) / (1 + settings.highlight * (peak - .72) / .28)
            graded = [v * mapped / peak for v in graded]
    else:
        graded = [0., 0., 0.]
    result = [min(65504., max(0., a + settings.intensity * (b - a))) for a, b in zip(original, graded)]
    if encoding == 'srgb_rec709':
        result = [encode_srgb(v) for v in result]
    return (*result, alpha)

def transition(current, target, dt, tau=.25):
    if not isinstance(current, Settings) or not isinstance(target, Settings):
        raise ValueError('Settings required')
    number(dt, 0, 1); number(tau, .01, 10)
    t = -math.expm1(-dt / tau)
    values = {name: getattr(current, name) + t * (getattr(target, name) - getattr(current, name)) for name in LIMITS}
    values['white_balance'] = tuple(a + t * (b - a) for a, b in zip(current.white_balance, target.white_balance))
    return Settings(**values)

def shader_source(settings):
    if not isinstance(settings, Settings):
        raise ValueError('Settings required')
    values = {'RV_INTENSITY': settings.intensity, 'RV_EV': settings.exposure_ev,
              'RV_HIGHLIGHT': settings.highlight, 'RV_SHADOW': settings.shadow,
              'RV_SATURATION': settings.saturation, 'RV_CONTRAST': settings.contrast,
              'RV_WR': settings.white_balance[0], 'RV_WG': settings.white_balance[1],
              'RV_WB': settings.white_balance[2], 'RV_NEUTRAL': int(settings.neutral)}
    prefix = ''.join(f'#define {name} {float(value):.12g}\n' for name, value in values.items())
    return prefix.encode() + (ROOT / 'shaders/RV_Photographic.hlsl').read_bytes()

def filter_ini(settings, *, temperature=6500):
    """Only keys observed in installed Kunos default.ini; runtime defaults untested."""
    if not isinstance(settings, Settings) or temperature not in (6400, 6500, 6600):
        raise ValueError('Invalid filter calibration')
    return ('; Original RestoVisuals configuration prototype; native calibration unverified.\n'
            '; This INI does not dispatch RV_Photographic.hlsl. Pure retains its bridge.\n'
            '[YEBIS]\nENABLED=1\n[AUTO_EXPOSURE]\nENABLED=1\n'
            '[TONEMAPPING]\nHDR=1\nFUNCTION=2\nEXPOSURE=1\nGAMMA=1\nMAPPING_FACTOR=32\n'
            f'[COLOR]\nHUE=0\nSATURATION={settings.saturation}\nBRIGHTNESS=1\n'
            f'CONTRAST={settings.contrast}\nSEPIA=0\nCOLOR_TEMP={temperature}\nWHITE_BALANCE=6500\n')
