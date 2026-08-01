import os
import cv2
import pandas as pd
from quality_assessment import FingerprintQualityAssessment

qa = FingerprintQualityAssessment()

DATASET_PATH = "test_dataset"

results = []

for root, dirs, files in os.walk(DATASET_PATH):

    for file in files:

        if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):

            image_path = os.path.join(root, file)

            image = cv2.imread(image_path)

            if image is None:
                continue

            output = qa.quality_gate(image)

            results.append({
                "Image": file,
                "Category": os.path.basename(root),
                "Composite Score": output["composite_score"],
                "Passed": output["passed"],
                "Blur Score": output["blur"]["blur_score"],
                "Brightness": output["brightness"]["brightness"],
                "Glare": output["glare"]["glare_fraction"],
                "ROI": output["roi"]["roi_fraction"],
                "Ridge": output["ridge"]["ridge_score"],
                "Guidance": output["guidance"]
            })

df = pd.DataFrame(results)

print(df)

df.to_csv("quality_results.csv", index=False)

print("\nResults saved to quality_results.csv")