import os
import streamlit as st
from datetime import datetime
from src.graph.stategraph import create_graph
from src.graph.state.graph_state import ResumeState

# Define upload folder (inside data/)
UPLOAD_DIR = "src/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Streamlit App ---
st.set_page_config(page_title="Resume Evaluator", layout="centered")
st.title("📄 Resume Evaluator (AI-Powered)")

st.markdown(
    """
    Upload a PDF resume and let the system analyze it for skills, projects, 
    personal details, and relevance to AI/Tech roles.  
    The results will show inferred role, personal info, and a skill-fit score.
    """
)

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # --- Save file to data folder ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(UPLOAD_DIR, f"resume_{timestamp}.pdf")

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File saved successfully: `{file_path}`")

    # --- Initialize State ---
    state: ResumeState = {
        "pdf_path": file_path
    }

    # --- Create Graph ---
    graph = create_graph()

    with st.spinner("⚙️ Evaluating resume... please wait..."):
        try:
            # Invoke LangGraph pipeline
            result_state = graph.invoke(state)

            st.success("🎯 Resume evaluation completed!")
            st.divider()

            # --- Section 1: Personal Info ---
            st.subheader("👤 Candidate Information")
            name = result_state.get("name", None)
            email = result_state.get("email", None)
            phone = result_state.get("phone_number", None)
            languages = result_state.get("languages", None)

            if name or email or phone or languages:
                st.write(f"**Name:** {name or 'Not Found'}")
                st.write(f"**Email:** {email or 'Not Found'}")
                st.write(f"**Phone:** {phone or 'Not Found'}")
                st.write(f"**Languages:** {', '.join(languages) if languages else 'Not Found'}")
            else:
                st.warning("No personal information could be extracted.")

            st.divider()

            # --- Section 2: Evaluation Summary ---
            st.subheader("📊 Skills & Role Evaluation")
            if "role_inferred" in result_state:
                st.write(f"**Inferred Role:** {result_state.get('role_inferred', 'Unknown')}")

            if "skills_score" in result_state:
                st.write(f"**Skills Score:** {result_state.get('skills_score', 0) * 100:.1f}%")

            if "matched_skills" in result_state:
                st.write("**Matched Skills:** ", ", ".join(result_state.get("matched_skills", [])))

            if "missing_skills" in result_state:
                st.write("**Missing Skills:** ", ", ".join(result_state.get("missing_skills", [])))

            # --- Section 3: Raw Output ---
            with st.expander("🧠 Full State Output"):
                st.json(result_state)

        except Exception as e:
            st.error(f"❌ Error during evaluation: {e}")
