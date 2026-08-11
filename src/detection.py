from ultralytics import YOLO
from pathlib import Path


MODEL_PATH = "yolo11n.pt"


def analyze_classroom(image_path, output_dir="outputs"):
    """
    Detect people in a classroom image and estimate occupancy level.
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

    # Simple occupancy classification
    if person_count == 0:
        occupancy = "EMPTY"
    elif person_count <= 5:
        occupancy = "LOW"
    elif person_count <= 15:
        occupancy = "MODERATE"
    else:
        occupancy = "HIGH"

    # Save annotated image
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    annotated_image = result.plot()

    output_path = output_dir / "classroom_detection.jpg"

    import cv2
    cv2.imwrite(str(output_path), annotated_image)

    return {
        "persons_detected": person_count,
        "occupancy_level": occupancy,
        "annotated_image": str(output_path)
    }


if __name__ == "__main__":

    image_path = "data/test_images/classroomtest.jpg"

    result = analyze_classroom(image_path)

    print("\n===== EcoCampus AI — Classroom Analysis =====")
    print(f"Persons detected : {result['persons_detected']}")
    print(f"Occupancy level   : {result['occupancy_level']}")
    print(f"Output image      : {result['annotated_image']}")