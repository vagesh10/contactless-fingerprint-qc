import streamlit as st
import cv2
import numpy as np
from quality_assessment import FingerprintQualityAssessment

# --------------------------------------------------
# Initialize Quality Assessment Object
# --------------------------------------------------
qa = FingerprintQualityAssessment()

# --------------------------------------------------
# Streamlit Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Contactless Fingerprint Quality Assessment",
    page_icon="🔍",
    layout="wide"
)

st.title("📱 Contactless Fingerprint Quality Assessment")
st.write("Upload a fingerprint image to evaluate its quality.")

# --------------------------------------------------
# Sidebar Threshold Controls
# --------------------------------------------------
st.sidebar.header("⚙️ Threshold Settings")

qa.blur_threshold = st.sidebar.slider(
    "Blur Threshold",
    min_value=1.0,
    max_value=100.0,
    value=float(qa.blur_threshold),
)

qa.dark_threshold = st.sidebar.slider(
    "Dark Brightness",
    min_value=0,
    max_value=100,
    value=int(qa.dark_threshold),
)

qa.bright_threshold = st.sidebar.slider(
    "Bright Brightness",
    min_value=150,
    max_value=255,
    value=int(qa.bright_threshold),
)

qa.glare_threshold = st.sidebar.slider(
    "Glare Threshold",
    min_value=0.01,
    max_value=0.20,
    value=float(qa.glare_threshold),
)

qa.roi_threshold = st.sidebar.slider(
    "ROI Threshold",
    min_value=0.05,
    max_value=0.50,
    value=float(qa.roi_threshold),
)

qa.ridge_threshold = st.sidebar.slider(
    "Ridge Threshold",
    min_value=1.0,
    max_value=100.0,
    value=float(qa.ridge_threshold),
)

# --------------------------------------------------
# Upload Image
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload Fingerprint",
    type=["jpg", "jpeg", "png", "bmp"]
)
# --------------------------------------------------
# Process Uploaded Image
# --------------------------------------------------
if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        st.error("Unable to read the uploaded image.")
        st.stop()

    # Display Image
    st.image(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        caption="Uploaded Fingerprint",
        use_container_width=True,
    )

    # Run Quality Assessment
    result = qa.quality_gate(image)

    st.divider()

    # --------------------------------------------------
    # Composite Score
    # --------------------------------------------------
    st.header("📊 Composite Quality Score")

    score = result["composite_score"]

    if result["passed"]:
        st.success(f"✅ PASSED : {score}/100")
    else:
        st.error(f"❌ REJECTED : {score}/100")

    # --------------------------------------------------
    # Quality Metrics
    # --------------------------------------------------
    st.subheader("Quality Metrics")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Blur:** {'✅ PASS' if not result['blur']['is_blurry'] else '❌ FAIL'}"
        )
        st.write(f"Score : {result['blur']['blur_score']}")

        st.write(
            f"**Brightness:** {'✅ PASS' if not (result['brightness']['too_dark'] or result['brightness']['too_bright']) else '❌ FAIL'}"
        )
        st.write(f"Value : {result['brightness']['brightness']}")

        st.write(
            f"**Glare:** {'✅ PASS' if not result['glare']['has_glare'] else '❌ FAIL'}"
        )
        st.write(f"Fraction : {result['glare']['glare_fraction']}")

    with col2:

        st.write(
            f"**ROI Completeness:** {'✅ PASS' if result['roi']['roi_complete'] else '❌ FAIL'}"
        )
        st.write(f"ROI Fraction : {result['roi']['roi_fraction']}")

        st.write(
            f"**Ridge Clarity:** {'✅ PASS' if result['ridge']['ridges_clear'] else '❌ FAIL'}"
        )
        st.write(f"Score : {result['ridge']['ridge_score']}")

    st.divider()

    # --------------------------------------------------
    # Guidance
    # --------------------------------------------------
    st.subheader("💡 Guidance")

    st.info(result["guidance"])

else:
    st.info("Please upload a fingerprint image to begin.")