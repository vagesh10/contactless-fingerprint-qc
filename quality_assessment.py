import cv2
import numpy as np


class FingerprintQualityAssessment:
    """
    Contactless Fingerprint Quality Assessment Pipeline
    """

    def __init__(self):
        self.blur_threshold = 10.0
        self.dark_threshold = 65
        self.bright_threshold = 210
        self.glare_threshold = 0.08
        self.roi_threshold = 0.15
        self.ridge_threshold = 15.0
        
    def check_blur(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        return {
            "blur_score": round(float(blur_score), 2),
            "is_blurry": blur_score < self.blur_threshold
        }

    def check_brightness(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        brightness = np.mean(gray)

        return {
            "brightness": round(float(brightness), 2),
            "too_dark": brightness < self.dark_threshold,
            "too_bright": brightness > self.bright_threshold
        }

    def check_glare(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        _, finger_mask = cv2.threshold(
          gray,
          240,
        255,
        cv2.THRESH_BINARY_INV
        )

        roi_pixels = gray[finger_mask > 0]

        if len(roi_pixels) == 0:
            glare_fraction = 0.0
        else:
            glare_pixels = np.sum(roi_pixels > 230)
            glare_fraction = glare_pixels / len(roi_pixels)

        return {
            "has_glare": glare_fraction > self.glare_threshold,
            "glare_fraction": round(float(glare_fraction), 4)
          }
    
    def check_roi_completeness(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        _, binary = cv2.threshold(
            blurred,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        foreground_pixels = np.sum(binary == 255)
        total_pixels = binary.size
        roi_fraction = foreground_pixels / total_pixels

        return {
            "roi_fraction": round(float(roi_fraction), 4),
            "roi_complete": roi_fraction >= self.roi_threshold
        }

    def check_ridge_clarity(self, image_bgr):
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        kernel = cv2.getGaborKernel(
            ksize=(21, 21),
            sigma=5,
            theta=np.pi / 4,
            lambd=10,
            gamma=0.5,
            psi=0,
            ktype=cv2.CV_32F
        )

        filtered = cv2.filter2D(gray, cv2.CV_32F, kernel)

        ridge_score = np.var(filtered)

        return {
            "ridge_score": round(float(ridge_score), 2),
            "ridges_clear": ridge_score >= self.ridge_threshold
        }

    def quality_gate(self, image):
        """
        Main quality assessment pipeline.
        Accepts an OpenCV image (NumPy array).
        """

        if image is None:
            raise ValueError("Invalid image.")

        blur = self.check_blur(image)
        brightness = self.check_brightness(image)
        glare = self.check_glare(image)
        roi = self.check_roi_completeness(image)
        ridge = self.check_ridge_clarity(image)

        blur_norm = min(1.0, blur["blur_score"] / 100)

        brightness_norm = max(
            0,
            1 - abs(brightness["brightness"] - 128) / 128
        )

        glare_norm = max(
            0,
            1 - glare["glare_fraction"] / self.glare_threshold
        )

        roi_norm = min(
            1,
            roi["roi_fraction"] / 0.30
        )

        ridge_norm = min(
            1,
            ridge["ridge_score"] / 100
        )

        composite = (
            0.25 * blur_norm +
            0.15 * brightness_norm +
            0.15 * glare_norm +
            0.20 * roi_norm +
            0.25 * ridge_norm
        ) * 100

        composite = round(composite, 2)

        passed = (
            composite >= 60
            and not blur["is_blurry"]
            and not brightness["too_dark"]
            and not brightness["too_bright"]
            and not glare["has_glare"]
            and roi["roi_complete"]
            and ridge["ridges_clear"]
        )

        if blur["is_blurry"]:
            guidance = "Too blurry. Hold your phone steady."
        elif brightness["too_dark"]:
            guidance = "Image is too dark. Increase lighting."
        elif brightness["too_bright"]:
            guidance = "Image is overexposed. Reduce lighting."
        elif glare["has_glare"]:
            guidance = "Glare detected. Tilt your finger slightly."
        elif not roi["roi_complete"]:
            guidance = "Move your finger closer to the camera."
        elif not ridge["ridges_clear"]:
            guidance = "Fingerprint ridges are unclear."
        else:
            guidance = "Good capture. Ready for processing."

        return {
            "passed": passed,
            "composite_score": composite,
            "blur": blur,
            "brightness": brightness,
            "glare": glare,
            "roi": roi,
            "ridge": ridge,
            "guidance": guidance
        }