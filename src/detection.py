from ultralytics import YOLO
from pathlib import Path
import cv2


MODEL_PATH = "yolo11n.pt"


def analyze_classroom(
    image_path,
    output_dir="outputs",
    classroom_capacity=60
):
    """
    Detect people in a classroom image and estimate occupancy.

    Returns:
        Dictionary containing person count, occupancy percentage,
        occupancy level, and annotated image path.
    """

    model = YOLO(MODEL_PATH)

    results = model.predict(
        source=image_path,
        conf=0.40,
        save=False
    )

    result = results[0]

    # COCO class ID 0 = person
    person_count = 0

    if result.boxes is not None:
        for cls in result.boxes.cls:
            if int(cls) == 0:
                person_count += 1

    # Calculate occupancy percentage
    occupancy_percentage = (
        person_count / classroom_capacity
    ) * 100

    # Occupancy classification
    if person_count == 0:
        occupancy = "EMPTY"
    elif occupancy_percentage < 25:
        occupancy = "LOW"
    elif occupancy_percentage < 50:
        occupancy = "MODERATE"
    else:
        occupancy = "HIGH"

    # Save annotated image
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    annotated_image = result.plot()

    output_path = output_dir / "classroom_detection.jpg"

    cv2.imwrite(
        str(output_path),
        annotated_image
    )

    return {
        "persons_detected": person_count,
        "classroom_capacity": classroom_capacity,
        "occupancy_percentage": round(
            occupancy_percentage, 2
        ),
        "occupancy_level": occupancy,
        "annotated_image": str(output_path)
    }


if __name__ == "__main__":

    image_path = "data/test_images/real_classroom.jpg"

    result = analyze_classroom(image_path)

    print(
        "\n===== EcoCampus AI — Classroom Analysis ====="
    )

    print(
        f"Persons detected   : "
        f"{result['persons_detected']}"
    )

    print(
        f"Classroom capacity : "
        f"{result['classroom_capacity']}"
    )

    print(
        f"Occupancy          : "
        f"{result['occupancy_percentage']}%"
    )

    print(
        f"Occupancy level    : "
        f"{result['occupancy_level']}"
    )

    print(
        f"Output image       : "
        f"{result['annotated_image']}"
    )