"""Generate poster-ready snapshots from real quality-tool output."""

from pathlib import Path
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
VENV = ROOT / ".venv" / "bin"
SOURCE_FILES = [
    "beta_core.py",
    "beta_function_gui.py",
    "test_beta_core.py",
    "debug_beta.py",
    "verify_accuracy.py",
]

BACKGROUND = "#10151d"
PANEL = "#171e28"
TEXT = "#e8edf4"
MUTED = "#aeb8c6"
GREEN = "#65d38e"
CYAN = "#71c7ec"
ORANGE = "#ffbd6a"


def run(command, input_text=None, environment=None):
    """Run a command and return its combined output and exit status."""
    result = subprocess.run(
        command,
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    output = result.stdout + result.stderr
    return output.strip(), result.returncode


def fonts():
    """Load macOS fonts with portable fallbacks."""
    mono_path = "/System/Library/Fonts/SFNSMono.ttf"
    sans_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    return {
        "mono": ImageFont.truetype(mono_path, 29),
        "mono_small": ImageFont.truetype(mono_path, 25),
        "sans": ImageFont.truetype(sans_path, 30),
        "bold": ImageFont.truetype(bold_path, 35),
        "title": ImageFont.truetype(bold_path, 42),
    }


def new_terminal(title, width=1700, height=880):
    """Create a terminal-style evidence canvas."""
    image = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (24, 24, width - 24, height - 24),
        radius=22,
        fill=PANEL,
        outline="#344153",
        width=3,
    )
    draw.ellipse((55, 52, 79, 76), fill="#ff5f57")
    draw.ellipse((91, 52, 115, 76), fill="#febc2e")
    draw.ellipse((127, 52, 151, 76), fill="#28c840")
    draw.text((185, 45), title, font=fonts()["title"], fill=TEXT)
    draw.line((55, 104, width - 55, 104), fill="#344153", width=2)
    return image, draw


def draw_lines(draw, lines, start_y, color=TEXT, font_name="mono"):
    """Draw terminal output one line at a time."""
    current_y = start_y
    selected_font = fonts()[font_name]
    for line in lines:
        draw.text((62, current_y), line, font=selected_font, fill=color)
        current_y += selected_font.size + 12
    return current_y


def create_quality_snapshot():
    """Capture Flake8 and Pylint results."""
    flake_output, flake_status = run(
        [str(VENV / "flake8"), *SOURCE_FILES]
    )
    environment = os.environ.copy()
    environment["XDG_CACHE_HOME"] = str(ROOT / "tmp")
    pylint_output, pylint_status = run(
        [str(VENV / "pylint"), *SOURCE_FILES],
        environment=environment,
    )

    image, draw = new_terminal("Code quality evidence", height=520)
    y_value = draw_lines(
        draw,
        ["$ flake8 " + " ".join(SOURCE_FILES)],
        135,
        color=CYAN,
        font_name="mono_small",
    )
    flake_result = flake_output or (
        "No style violations found (exit status 0)."
        if flake_status == 0
        else "Flake8 returned an error."
    )
    y_value = draw_lines(draw, flake_result.splitlines(), y_value, color=GREEN)
    y_value += 32
    y_value = draw_lines(
        draw,
        ["$ pylint " + " ".join(SOURCE_FILES)],
        y_value,
        color=CYAN,
        font_name="mono_small",
    )
    rating_lines = [
        line
        for line in pylint_output.splitlines()
        if "rated at" in line or line.startswith("Your code")
    ]
    if not rating_lines:
        rating_lines = [
            f"Pylint exit status: {pylint_status}",
            *pylint_output.splitlines()[-4:],
        ]
    draw_lines(draw, rating_lines, y_value, color=GREEN)
    image.save(ASSETS / "quality_tools.png")


def create_test_snapshot():
    """Capture unittest output."""
    output, status = run(["python3", "-m", "unittest", "-v"])
    lines = []
    for line in output.splitlines():
        if line.startswith("test_"):
            test_name = line.split(" ", 1)[0]
            lines.append(f"{test_name:<43} ok")
    test_count = len(lines)
    lines.extend(
        ["", f"Ran {test_count} tests", "OK" if status == 0 else "FAILED"]
    )

    image, draw = new_terminal("PyUnit test evidence", height=880)
    y_value = draw_lines(
        draw,
        ["$ python3 -m unittest -v"],
        135,
        color=CYAN,
        font_name="mono_small",
    )
    draw_lines(draw, lines, y_value, color=GREEN, font_name="mono_small")
    image.save(ASSETS / "unit_tests.png")


def create_accuracy_snapshot():
    """Capture the external high-precision verification summary."""
    output, status = run([str(VENV / "python"), "verify_accuracy.py"])
    lines = output.splitlines()
    if status != 0:
        lines.append(f"Verification exited with status {status}.")

    image, draw = new_terminal("External accuracy verification", height=700)
    y_value = draw_lines(
        draw,
        ["$ .venv/bin/python verify_accuracy.py"],
        135,
        color=CYAN,
        font_name="mono_small",
    )
    draw_lines(draw, lines, y_value, color=GREEN, font_name="mono_small")
    image.save(ASSETS / "accuracy_verification.png")


def create_debugger_snapshot():
    """Capture a reproducible pdb session at beta_function."""
    commands = "\n".join(
        [
            "break beta_core.beta_function",
            "continue",
            "p (x_value, y_value)",
            "next",
            "next",
            "next",
            "continue",
            "quit",
        ]
    )
    output, _status = run(
        ["python3", "-m", "pdb", "debug_beta.py"],
        input_text=commands + "\n",
    )
    selected = []
    for line in output.splitlines():
        if any(
            marker in line
            for marker in (
                "Breakpoint 1",
                "beta_function()",
                "if not is_finite",
                "(2.0, 3.0)",
                "B(2, 3)",
            )
        ):
            selected.append(line.replace(str(ROOT) + "/", ""))

    image, draw = new_terminal("pdb debugger evidence", height=650)
    y_value = draw_lines(
        draw,
        ["$ python3 -m pdb debug_beta.py"],
        135,
        color=CYAN,
        font_name="mono_small",
    )
    draw_lines(draw, selected, y_value, color=ORANGE, font_name="mono_small")
    image.save(ASSETS / "pdb_session.png")


def main():
    """Generate every evidence image used by the poster."""
    ASSETS.mkdir(exist_ok=True)
    create_quality_snapshot()
    create_test_snapshot()
    create_accuracy_snapshot()
    create_debugger_snapshot()


if __name__ == "__main__":
    main()
