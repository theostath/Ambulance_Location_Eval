"""Generate docs/usage.gif demonstrating the run.py CLI.

Pure-Python renderer using Pillow only. Captures real output by invoking
`python run.py` for each demo command, filters the pymprog/GLPK preamble
out, and animates the result as a terminal recording. Regenerate with:

    python docs/generate_demo.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent

# Catppuccin Mocha palette
BG       = (30, 30, 46)
FG       = (205, 214, 244)
PROMPT   = (137, 180, 250)
COMMENT  = (108, 112, 134)
HIGHLIGHT = (166, 227, 161)  # green for headline percentages
ACCENT   = (249, 226, 175)   # yellow for section breaks

WIDTH, HEIGHT = 980, 540
PADDING = 22
LINE_HEIGHT = 22
FONT_SIZE = 15

FRAME_MS = 90
PROMPT_TEXT = "PS C:\\Ambulance_Location_Eval> "

Line = Tuple[str, Tuple[int, int, int]]


def _load_font() -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/CascadiaMono.ttf",
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/Consolas.ttf",
        "C:/Windows/Fonts/lucon.ttf",
    ]
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, FONT_SIZE)
    return ImageFont.load_default()


FONT = _load_font()


def make_frame(lines: List[Line]) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    max_visible = (HEIGHT - 2 * PADDING) // LINE_HEIGHT
    visible = lines[-max_visible:]
    y = PADDING
    for text, color in visible:
        draw.text((PADDING, y), text, font=FONT, fill=color)
        y += LINE_HEIGHT
    return img


def run_capture(extra_args: List[str]) -> List[str]:
    """Run `python run.py <extra_args>` and return the clean report lines."""
    proc = subprocess.run(
        [sys.executable, "run.py", *extra_args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    out_lines = proc.stdout.splitlines()
    start = next(
        (i for i, ln in enumerate(out_lines) if ln.startswith("Single-coverage floor")),
        0,
    )
    return out_lines[start:]


def append_typing(frames: List[Image.Image], base: List[Line], command: str) -> List[Line]:
    """Emit progressive-typing frames; return state after command is fully typed."""
    chunks = max(1, len(command) // 4)
    step = max(1, len(command) // chunks)
    for n in range(step, len(command) + 1, step):
        frames.append(make_frame(base + [(PROMPT_TEXT + command[:n], FG)]))
    final = base + [(PROMPT_TEXT + command, FG)]
    for _ in range(3):
        frames.append(make_frame(final))
    return final


def main() -> int:
    commands = [
        (["--case", "1", "--rt1", "10"], "Case 1 - USEMSA standard"),
        (["--case", "1", "--rt1", "8"],  "Case 1 - heart-attack threshold"),
        (["--case", "2", "--rt1", "10"], "Case 2 - USEMSA standard"),
        (["--case", "2", "--rt1", "8"],  "Case 2 - heart-attack threshold"),
    ]

    frames: List[Image.Image] = []
    state: List[Line] = [
        ("# Ambulance Location Evaluation - CLI demo", HIGHLIGHT),
        ("", FG),
    ]
    # Hold the title
    for _ in range(8):
        frames.append(make_frame(state))

    for args, label in commands:
        # Section comment
        state.append((f"# {label}", COMMENT))
        for _ in range(2):
            frames.append(make_frame(state))

        # Type the command
        command_str = "python run.py " + " ".join(args)
        state = append_typing(frames, state, command_str)

        # Reveal output line by line
        output = run_capture(args)
        for line in output:
            color = HIGHLIGHT if "%" in line and "/" in line else FG
            state = state + [(line, color)]
            frames.append(make_frame(state))
            frames.append(make_frame(state))

        # Pause between sections
        state = state + [("", FG)]
        for _ in range(5):
            frames.append(make_frame(state))

    # Final hold
    for _ in range(14):
        frames.append(make_frame(state))

    out_path = ROOT / "docs" / "usage.gif"
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {out_path}  ({len(frames)} frames, {FRAME_MS} ms/frame)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
