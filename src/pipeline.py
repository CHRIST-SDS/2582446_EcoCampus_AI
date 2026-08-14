"""
EcoCampus AI
Integrated Local AI Pipeline

Workflow:

Classroom Image
       ↓
YOLO11n Occupancy Detection
       ↓
Energy Analysis
       ↓
Local Gemma Energy Audit
       ↓
Local SD-Turbo Visualization
"""

from pathlib import Path
import sys

from src.detection import analyze_classroom
from src.energy_analysis import calculate_energy, print_report
from src.llm import generate_energy_report
from src.image_generation import generate_classroom_image



# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_IMAGE_PATH = (
    PROJECT_ROOT
    / "data"
    / "test_images"
    / "real_classroom.jpg"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs"


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------

def run_pipeline(image_path):
    """
    Run the complete EcoCampus AI pipeline.

    Parameters
    ----------
    image_path : str or Path
        Classroom image to analyze.

    Returns
    -------
    dict
        Detection, energy, report, and generated-image results.
    """

    image_path = Path(image_path)

    print("\n" + "=" * 65)
    print("              ECOCAMPUS AI")
    print("        LOCAL AI CLASSROOM ANALYSIS")
    print("=" * 65)

    print("\nInput image:")
    print(image_path)

    # ---------------------------------------------------------
    # VALIDATE INPUT
    # ---------------------------------------------------------

    if not image_path.exists():
        raise FileNotFoundError(
            f"Input image not found: {image_path}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # STEP 1 — YOLO OCCUPANCY DETECTION
    # ---------------------------------------------------------

    print("\n" + "-" * 65)
    print("STEP 1 — YOLO11n OCCUPANCY DETECTION")
    print("-" * 65)

    detection = analyze_classroom(
        image_path,
        output_dir=OUTPUT_DIR
    )

    people_detected = detection["persons_detected"]

    print(
        f"Persons detected   : {people_detected}"
    )

    print(
        f"Occupancy level     : "
        f"{detection['occupancy_level']}"
    )

    print(
        f"Detection output    : "
        f"{detection['annotated_image']}"
    )

    # ---------------------------------------------------------
    # STEP 2 — ENERGY ANALYSIS
    # ---------------------------------------------------------

    print("\n" + "-" * 65)
    print("STEP 2 — ENERGY ANALYSIS")
    print("-" * 65)

    energy = calculate_energy(
        people_detected=people_detected,
        duration_hours=1.0,

        # Prototype appliance inputs.
        # These are NOT detected from the image.
        lights_on=True,
        fans_on=True,
        ac_on=True,
        projector_on=False,
    )

    print_report(energy)

    # ---------------------------------------------------------
    # STEP 3 — LOCAL GEMMA ENERGY AUDIT
    # ---------------------------------------------------------

    print("\n" + "-" * 65)
    print("STEP 3 — LOCAL GEMMA ENERGY AUDIT")
    print("-" * 65)

    report = generate_energy_report(
    persons_detected=energy["people_detected"],
    classroom_capacity=energy["classroom_capacity"],
    occupancy_percentage=energy["occupancy_percentage"],
    occupancy_level=detection["occupancy_level"],

    energy_kwh=energy["energy_kwh"],
    estimated_cost=energy["estimated_cost_inr"],
    estimated_co2=energy["estimated_co2_kg"],

    recommended_power_kw=energy["recommended_power_kw"],
    recommended_energy_kwh=energy["recommended_energy_kwh"],

    potential_saving=energy["potential_saving_inr"],
    potential_co2_reduction=energy[
        "potential_co2_reduction_kg"
    ],

    priority=energy["priority"],

    lights_on=True,
    fans_on=True,
    ac_on=True,
    projector_on=False,
)

    print("\n----- GEMMA ENERGY AUDIT -----\n")
    print(report)

    report_path = OUTPUT_DIR / "energy_report.txt"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(report)

    print(
        f"\nReport saved to: {report_path}"
    )

    # ---------------------------------------------------------
    # STEP 4 — LOCAL SD-TURBO VISUALIZATION
    # ---------------------------------------------------------

    print("\n" + "-" * 65)
    print("STEP 4 — LOCAL SD-TURBO VISUALIZATION")
    print("-" * 65)

    if people_detected == 0:

        scenario = (
            "an empty university classroom with "
            "energy-saving systems recommended"
        )

    elif energy["occupancy_percentage"] < 25:

        scenario = (
            "a university classroom with very low occupancy "
            "and unnecessary energy usage"
        )

    else:

        scenario = (
            "a normally occupied university classroom "
            "using energy-efficient systems"
        )

    visualization_prompt = (
        "Photorealistic university sustainability scene, "
        f"{scenario}, "
        "modern academic classroom, "
        "energy-efficient LED lighting, "
        "responsible electricity usage, "
        "sustainable campus environment, "
        "professional facility-management visualization, "
        "realistic architecture, "
        "high quality"
    )

    generated_path = (
        OUTPUT_DIR / "generated_classroom.png"
    )

    generate_classroom_image(
        visualization_prompt,
        output_path=str(generated_path)
    )

    # ---------------------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------------------

    return {
        "detection": detection,
        "energy": energy,
        "report": report,
        "detection_image": Path(
            detection["annotated_image"]
        ),
        "generated_image": generated_path,
        "report_path": report_path,
    }


# ---------------------------------------------------------
# COMMAND-LINE ENTRY POINT
# ---------------------------------------------------------

def main():

    # If an image path is supplied:
    #
    # python src/pipeline.py "path/to/image.jpg"
    #
    # use that image.
    #
    # Otherwise use the default classroom image.

    if len(sys.argv) > 1:

        image_path = Path(sys.argv[1])

    else:

        image_path = DEFAULT_IMAGE_PATH

    results = run_pipeline(image_path)

    detection = results["detection"]
    energy = results["energy"]
    generated_path = results["generated_image"]

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------

    print("\n" + "=" * 65)
    print("          ECOCAMPUS AI PIPELINE COMPLETED")
    print("=" * 65)

    print("\nFinal Outputs:")

    print(
        f"✓ YOLO detection : "
        f"{detection['annotated_image']}"
    )

    print(
        f"✓ Energy analysis: "
        f"{energy['energy_kwh']:.2f} kWh"
    )

    print(
        "✓ Gemma report   : "
        "Generated successfully"
    )

    print(
        f"✓ SD-Turbo image : "
        f"{generated_path}"
    )

    print("\n" + "=" * 65)


# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------

if __name__ == "__main__":
    main()