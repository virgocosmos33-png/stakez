"""Named flipbook speed curves for Spine 3.8 attachment tracks.

Attachment timelines are stepped (name + time only). Speed is non-uniform
frame duration around 1/fps, not a Bezier blend between two attachments.
"""
from __future__ import annotations

CURVE_LINEAR = "linear"
CURVE_EASE_IN = "easeIn"
CURVE_EASE_OUT = "easeOut"
CURVE_EASE_IN_OUT = "easeInOut"
CURVE_ATTACK = "attack"
NAMED_CURVES = (
    CURVE_LINEAR,
    CURVE_EASE_IN,
    CURVE_EASE_OUT,
    CURVE_EASE_IN_OUT,
    CURVE_ATTACK,
)

PHASE_IDLE = "idle"
PHASE_ANTICIPATE = "anticipate"
PHASE_STRIKE = "strike"
PHASE_RECOVER = "recover"
NAMED_PHASES = (PHASE_IDLE, PHASE_ANTICIPATE, PHASE_STRIKE, PHASE_RECOVER)

SCALE_LINEAR = 1.0
SCALE_WINDUP = 1.4
SCALE_HIT = 0.55
SCALE_RECOVER = 1.25

PHASE_SCALES = {
    PHASE_IDLE: SCALE_LINEAR,
    PHASE_ANTICIPATE: SCALE_WINDUP,
    PHASE_STRIKE: SCALE_HIT,
    PHASE_RECOVER: SCALE_RECOVER,
}

# Art-read Hazard Hood clips. 12 fps base. Do not invent extra packs here.
HAZARD_HOOD_PHASES: dict[str, list[str]] = {
    "hazard-hood-pistol": [
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
    ],
    "hazard-hood-knife": [
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
    ],
    "hazard-hood-bomb": [
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
    ],
    "hazard-hood-toxic-smoke": [
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
    ],
    "hazard-hood-knife-throw": [
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_ANTICIPATE,
        PHASE_STRIKE,
        PHASE_STRIKE,
        PHASE_RECOVER,
        PHASE_RECOVER,
        PHASE_RECOVER,
    ],
}


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def normalize_curve_name(value: object) -> str:
    name = str(value or CURVE_LINEAR).strip()
    return name if name in NAMED_CURVES else CURVE_LINEAR


def normalize_phase_name(value: object) -> str:
    name = str(value or PHASE_IDLE).strip()
    return name if name in NAMED_PHASES else PHASE_IDLE


def normalize_scale(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        scale = float(value)
    except (TypeError, ValueError):
        return None
    if scale <= 0.0:
        return None
    return scale


def default_attack_phases(count: int, loop: tuple[int, int] | None) -> list[str]:
    if count <= 0:
        return []
    if loop:
        start, end = loop
        whole = start == 0 and end == count - 1
        if not whole and 0 <= start <= end < count:
            phases: list[str] = []
            for i in range(count):
                if i < start:
                    phases.append(PHASE_ANTICIPATE)
                elif i <= end:
                    phases.append(PHASE_STRIKE)
                else:
                    phases.append(PHASE_RECOVER)
            return phases
    if count == 1:
        return [PHASE_STRIKE]
    if count == 2:
        return [PHASE_ANTICIPATE, PHASE_STRIKE]
    wind = max(1, count // 3)
    recover = max(1, count // 3)
    strike = count - wind - recover
    if strike < 1:
        strike = 1
        recover = max(0, count - wind - strike)
    return (
        [PHASE_ANTICIPATE] * wind
        + [PHASE_STRIKE] * strike
        + [PHASE_RECOVER] * recover
    )


def phases_for_curve(name: str, count: int, loop: tuple[int, int] | None) -> list[str]:
    if count <= 0:
        return []
    if name == CURVE_ATTACK:
        return default_attack_phases(count, loop)
    if name == CURVE_EASE_IN:
        return [
            PHASE_ANTICIPATE if i < count / 2 else PHASE_STRIKE for i in range(count)
        ]
    if name == CURVE_EASE_OUT:
        return [PHASE_STRIKE if i < count / 2 else PHASE_RECOVER for i in range(count)]
    if name == CURVE_EASE_IN_OUT:
        first = max(1, count // 3)
        last = max(1, count // 3)
        mid = max(0, count - first - last)
        return (
            [PHASE_ANTICIPATE] * first
            + [PHASE_STRIKE] * mid
            + [PHASE_RECOVER] * last
        )
    return [PHASE_IDLE] * count


def scales_for_curve(name: str, count: int, phases: list[str]) -> list[float]:
    if count <= 0:
        return []
    if name == CURVE_EASE_IN:
        last = max(1, count - 1)
        return [_lerp(SCALE_WINDUP, SCALE_HIT, i / last) for i in range(count)]
    if name == CURVE_EASE_OUT:
        last = max(1, count - 1)
        return [_lerp(SCALE_HIT, SCALE_RECOVER, i / last) for i in range(count)]
    if name == CURVE_EASE_IN_OUT:
        if count == 1:
            return [SCALE_LINEAR]
        mid = (count - 1) / 2.0
        scales: list[float] = []
        for i in range(count):
            if i <= mid:
                t = i / mid if mid else 0.0
                scales.append(_lerp(SCALE_WINDUP, SCALE_HIT, t))
            else:
                t = (i - mid) / ((count - 1) - mid)
                scales.append(_lerp(SCALE_HIT, SCALE_RECOVER, t))
        return scales
    if name == CURVE_ATTACK:
        return [PHASE_SCALES.get(phase, SCALE_LINEAR) for phase in phases]
    return [SCALE_LINEAR] * count


def read_phase_list(data: dict, count: int) -> list[str] | None:
    raw = data.get("frame_phases", data.get("framePhases"))
    if not isinstance(raw, list) or len(raw) != count:
        return None
    return [normalize_phase_name(item) for item in raw]


def read_scale_overrides(data: dict, count: int) -> list[float | None] | None:
    raw = data.get("frame_scales", data.get("frameScales"))
    if raw is None:
        return None
    if isinstance(raw, dict):
        out: list[float | None] = [None] * count
        for key, value in raw.items():
            try:
                idx = int(key)
            except (TypeError, ValueError):
                continue
            if 0 <= idx < count:
                out[idx] = normalize_scale(value)
        return out
    if not isinstance(raw, list) or len(raw) != count:
        return None
    return [normalize_scale(item) for item in raw]


def resolve_timing(
    data: dict,
    count: int,
    loop: tuple[int, int] | None = None,
) -> dict:
    fps = max(1, int(data.get("fps") or 12))
    name = normalize_curve_name(data.get("speed_curve", data.get("speedCurve")))
    explicit = read_phase_list(data, count)
    phases = explicit if explicit is not None else phases_for_curve(name, count, loop)
    if len(phases) != count:
        phases = phases_for_curve(name, count, loop)
    scales = scales_for_curve(name, count, phases)
    overrides = read_scale_overrides(data, count)
    if overrides:
        for i, scale in enumerate(overrides):
            if scale is not None:
                scales[i] = scale
    durations = [round(scale / fps, 4) for scale in scales]
    return {
        "speed_curve": name,
        "frame_phases": phases,
        "frame_scales": [round(scale, 4) for scale in scales],
        "frame_durations": durations,
        "explicit_phases": explicit is not None,
    }


def catalog_timing(
    data: dict,
    count: int,
    loop: tuple[int, int] | None = None,
) -> dict:
    timing = resolve_timing(data, count, loop)
    return {
        "speedCurve": timing["speed_curve"],
        "framePhases": timing["frame_phases"],
        "frameScales": timing["frame_scales"],
        "frameDurations": timing["frame_durations"],
    }


def remap_indexed_list(values: list | None, kept_old: list[int]) -> list | None:
    if not isinstance(values, list) or not kept_old:
        return None
    out = []
    for old in kept_old:
        if old < 0 or old >= len(values):
            return None
        out.append(values[old])
    return out


def hazard_hood_phases(slug: str, count: int) -> list[str] | None:
    phases = HAZARD_HOOD_PHASES.get(slug)
    if phases is not None and len(phases) == count:
        return list(phases)
    if slug.startswith("hazard-hood-") and count == 9:
        return list(HAZARD_HOOD_PHASES["hazard-hood-bomb"])
    return None
