"""
EcoCampus AI
Integrated AI Pipeline

Workflow:
Classroom Image
    -> YOLO11n Occupancy Detection
    -> Energy Analysis
    -> Local Gemma LLM Report
    -> Local SD-Turbo Visualization
"""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGE_PATH = PROJECT_ROOT / "data" / "test_images" / "classroomtest.jpg"


def run_detection():
    """Run YOLO occupancy detection."""

    print("\n" + "=" * 60)
    print("STEP 1 — COMPUTER VISION")
    print("=" * 60)

    detection_script = PROJECT_ROOT / "src" / "detection.py"

    result = subprocess.run(
        [sys.executable, str(detection_script)],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("Detection error:")
        print(result.stderr)
        raise RuntimeError("YOLO detection failed.")


def run_llm():
    """Run the local Gemma energy analysis."""

    print("\n" + "=" * 60)
    print("STEP 2 — LOCAL LLM")
    print("=" * 60)

    llm_script = PROJECT_ROOT / "src" / "llm.py"

    result = subprocess.run(
        [sys.executable, str(llm_script)],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("LLM error:")
        print(result.stderr)
        raise RuntimeError("Local LLM analysis failed.")


def run_image_generation():
    """Generate the AI visualization using local SD-Turbo."""

    print("\n" + "=" * 60)
    print("STEP 3 — LOCAL IMAGE GENERATION")
    print("=" * 60)

    image_script = PROJECT_ROOT / "src" / "image_generation.py"

    result = subprocess.run(
        [sys.executable, str(image_script)],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.returncode != 0:
        print("Image generation error:")
        print(result.stderr)
        raise RuntimeError("Image generation failed.")


def main():
    print("\n" + "=" * 60)
    print("        ECOCAMPUS AI — INTEGRATED PIPELINE")
    print("=" * 60)

    print(f"\nInput image: {IMAGE_PATH}")

    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            f"Input image not found: {IMAGE_PATH}"
        )

    run_detection()
    run_llm()
    run_image_generation()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nGenerated outputs:")
    print("  • YOLO detection → outputs/classroom_detection.jpg")
    print("  • Energy report → Local Gemma output")
    print("  • AI visualization → outputs/generated_classroom.png")


if __name__ == "__main__":
    main()