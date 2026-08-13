import streamlit as st
from pathlib import Path
import tempfile

from src.pipeline import run_pipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EcoCampus AI",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# =========================================================
# HEADER
# =========================================================

st.title("🌱 EcoCampus AI")

st.subheader(
    "AI-Powered Classroom Energy Management"
)

st.markdown(
    """
    **EcoCampus AI** combines computer vision, energy analysis,
    local LLM reasoning, and AI visualization to identify
    potential energy waste in classrooms.
    """
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Classroom Analysis")

uploaded_file = st.sidebar.file_uploader(
    "Upload classroom image",
    type=["jpg", "jpeg", "png"]
)

analyze_button = st.sidebar.button(
    "🔍 Analyze Classroom",
    width="stretch"
)


# =========================================================
# UPLOADED IMAGE
# =========================================================

if uploaded_file is not None:

    st.subheader("📷 Uploaded Classroom Image")

    st.image(
        uploaded_file,
        caption="Input classroom image",
        width="stretch"
    )


# =========================================================
# ANALYZE IMAGE
# =========================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "Please upload a classroom image first."
        )

    else:

        try:

            with st.spinner(
                "Running YOLO, energy analysis, Gemma audit, "
                "and SD-Turbo visualization..."
            ):

                # ---------------------------------------------
                # Save uploaded image temporarily
                # ---------------------------------------------

                suffix = Path(
                    uploaded_file.name
                ).suffix

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    temp_image_path = Path(
                        temp_file.name
                    )

                # ---------------------------------------------
                # Run complete pipeline
                # ---------------------------------------------

                results = run_pipeline(
                    temp_image_path
                )

            # Store results
            st.session_state["results"] = results

            st.success(
                "✅ Classroom analysis completed successfully!"
            )

        except Exception as e:

            st.error(
                f"❌ Analysis failed: {e}"
            )

            st.exception(e)


# =========================================================
# DISPLAY RESULTS
# =========================================================

if "results" in st.session_state:

    results = st.session_state["results"]

    detection = results["detection"]
    energy = results["energy"]
    report = results["report"]

    detection_image = Path(
        results["detection_image"]
    )

    generated_image = Path(
        results["generated_image"]
    )


    # =====================================================
    # LATEST ANALYSIS
    # =====================================================

    st.subheader("📊 Latest Analysis")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Occupancy",
            f"{energy['occupancy_percentage']:.1f}%"
        )


    with col2:

        st.metric(
            "Energy",
            f"{energy['energy_kwh']:.2f} kWh"
        )


    with col3:

        st.metric(
            "Estimated Cost",
            f"₹{energy['estimated_cost_inr']:.2f}"
        )


    with col4:

        st.metric(
            "Priority",
            energy["priority"]
        )


    st.divider()


    # =====================================================
    # YOLO + AI VISUALIZATION
    # =====================================================

    left, right = st.columns(2)


    # -----------------------------------------------------
    # YOLO DETECTION
    # -----------------------------------------------------

    with left:

        st.subheader(
            "👥 YOLO Occupancy Detection"
        )

        if detection_image.exists():

            st.image(
                str(detection_image),
                caption="YOLO11n detection output",
                width="stretch"
            )

        else:

            st.info(
                "Detection image not available."
            )

        st.metric(
            "Persons Detected",
            detection["persons_detected"]
        )

        st.write(
            f"**Occupancy Level:** "
            f"{detection['occupancy_level']}"
        )


    # -----------------------------------------------------
    # AI VISUALIZATION
    # -----------------------------------------------------

    with right:

        st.subheader(
            "🤖 AI Visualization"
        )

        if generated_image.exists():

            st.image(
                str(generated_image),
                caption=(
                    "SD-Turbo generated "
                    "sustainability visualization"
                ),
                width="stretch"
            )

        else:

            st.info(
                "Generated visualization not available."
            )


    st.divider()


    # =====================================================
    # ENERGY ANALYSIS
    # =====================================================

    st.subheader("⚡ Energy Analysis")

    energy_col1, energy_col2, energy_col3 = st.columns(3)


    with energy_col1:

        st.metric(
            "Estimated Power",
            f"{energy['total_power_kw']:.2f} kW"
        )


    with energy_col2:

        st.metric(
            "Potential Saving",
            f"₹{energy['potential_saving_inr']:.2f}"
        )


    with energy_col3:

        st.metric(
            "Potential CO₂ Reduction",
            f"{energy['potential_co2_reduction_kg']:.2f} kg"
        )


    st.divider()


    # =====================================================
    # GEMMA REPORT
    # =====================================================

    st.subheader(
        "📝 Local Gemma Energy Audit"
    )

    st.markdown(report)


# =========================================================
# INITIAL MESSAGE
# =========================================================

else:

    st.info(
        "Upload a classroom image and click "
        "'🔍 Analyze Classroom' to begin."
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "EcoCampus AI uses estimated energy values based on "
    "configured appliance power ratings. Appliance states "
    "are prototype inputs and are not directly detected "
    "from the classroom image."
)