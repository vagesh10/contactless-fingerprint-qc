import os
import cv2

DATASET = "test_dataset"

def process_blurry():
    folder = os.path.join(DATASET, "blurry")

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        img = cv2.imread(path)

        if img is None:
            continue

        blurred = cv2.GaussianBlur(img, (41, 41), 20)

        cv2.imwrite(path, blurred)

    print("✅ Blurry images created")


def process_dark():
    folder = os.path.join(DATASET, "dark")

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        img = cv2.imread(path)

        if img is None:
            continue

        dark = cv2.convertScaleAbs(img, alpha=0.5, beta=-80)

        cv2.imwrite(path, dark)

    print("✅ Dark images created")


def process_glare():
    folder = os.path.join(DATASET, "glare")

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        img = cv2.imread(path)

        if img is None:
            continue

        h, w = img.shape[:2]

        cv2.circle(
            img,
            (w // 2, h // 2),
            18,
            (255, 255, 255),
            -1
        )

        cv2.imwrite(path, img)

    print("✅ Glare images created")


process_blurry()
process_dark()
process_glare()

print("\nDataset prepared successfully.")