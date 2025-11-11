import os
import streamlit as st
from datetime import datetime
from src.graph.stategraph import create_graph
from src.graph.state.graph_state import ResumeState
from src.utils.llm_utils import get_llm, validate_role

# Define upload folder (inside data/)
UPLOAD_DIR = "src/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Streamlit App ---
st.set_page_config(page_title="Resume Evaluator", layout="centered")
st.title("📄 Resume Evaluator (AI-Powered)")

st.markdown(
    """
    Upload a PDF resume and let the system analyze it for:
    - 👤 Personal details  
    - 💡 Skills  
    - 💼 Project Experience  
    - 🎓 Education Background  
    - 🧑‍💻 Experience

    The results will include inferred role, evaluator scores, and AI-generated insights.
    """
)

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
user_role = st.text_input("Enter the role you want to analyze this resume for:")

if user_role:
    result = validate_role(user_role)
    if result!=False:
        st.success(f"✅ Valid role detected: **{result}**")
    else:
        st.warning("⚠️ Invalid or unrecognized role. Please enter a valid professional job title.")
        st.stop()

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
    state["target_role"] = user_role

    # --- Create Graph ---
    graph = create_graph()

    with st.spinner("⚙️ Evaluating resume... please wait..."):
        try:
            # Invoke LangGraph pipeline
            result_state = graph.invoke(state)

            st.success("🎯 Resume evaluation completed!")
            st.divider()

            # ============ 👤 PERSONAL INFO ============
            st.subheader("👤 Candidate Information")
            name = result_state.get("name")
            email = result_state.get("email")
            phone = result_state.get("phone_number")
            languages = result_state.get("languages")

            if name or email or phone or languages:
                st.write(f"**Name:** {name or 'Not Found'}")
                st.write(f"**Email:** {email or 'Not Found'}")
                st.write(f"**Phone:** {phone or 'Not Found'}")
                st.write(f"**Languages:** {', '.join(languages) if languages else 'Not Found'}")
            else:
                st.warning("No personal information could be extracted.")
            st.divider()

            # ============ 💡 SKILLS EVALUATION ============
            st.subheader("💡 Skills Evaluation")
            if "role_inferred" in result_state:
                st.write(f"**Inferred Role:** {result_state.get('role_inferred', 'Unknown')}")

            if "skills_score" in result_state:
                st.progress(result_state.get("skills_score", 0.0))
                st.write(f"**Skills Score:** {result_state.get('skills_score', 0.0) * 100:.1f}%")

            if "matched_skills" in result_state:
                st.write("**Matched Skills:** ", ", ".join(result_state.get("matched_skills", [])))

            if "missing_skills" in result_state:
                st.write("**Missing Skills:** ", ", ".join(result_state.get("missing_skills", [])))

            st.divider()

             # ============ 🧑‍💻 EXPERIENCE EVALUATION ============
            st.subheader("🧑‍💻 Experience Evaluation")
            if "experience_score" in result_state:
                st.progress(result_state.get("experience_score", 0.0))
                st.write(f"**Experience Score:** {result_state.get('experience_score', 0.0) * 100:.1f}%")

            if "total_experience" in result_state:
                st.write(f"**Total expreience:** {result_state.get('total_experience', 0.0) * 1:.1f} years")

            if "best_fit_role" in result_state:
                st.write(f"**Inferred Role:** {result_state.get('best_fit_role', 'Unknown')}")

            if "companies" in result_state:
                st.write("**Companies:** ", ", ".join(result_state.get("companies", [])))

            if "job_switch_pattern" in result_state:
                st.write(f"**Job switch pattern:** {result_state.get('job_switch_pattern', 'Unknown')}")    

            st.divider()

            # ============ 💼 PROJECT EVALUATION ============
            st.subheader("💼 Project Evaluation")
            project_score = result_state.get("project_score", None)
            if project_score is not None:
                st.progress(project_score)
                st.write(f"**Project Score:** {project_score * 100:.1f}%")

            projects_section = result_state.get("projects_section", "")
            tech_stack = result_state.get("project_tech_stack", [])

            if projects_section:
                st.write("**Projects Summary:**")
                st.markdown(f"<pre>{projects_section}</pre>", unsafe_allow_html=True)

            if tech_stack:
                st.write("**Tech Stack Used:** ", ", ".join(tech_stack))
            st.divider()

            # ============ 🎓 EDUCATION EVALUATION ============
            st.subheader("🎓 Education Evaluation")
            edu_score = result_state.get("education_score", None)
            if edu_score is not None:
                st.progress(edu_score)
                st.write(f"**Education Score:** {edu_score * 100:.1f}%")

            degrees = result_state.get("degrees", [])
            institutions = result_state.get("institutions", [])

            if degrees:
                st.write("**Degrees / Qualifications:** ", ", ".join(degrees))

            if institutions:
                st.write("**Institutions / Universities:** ", ", ".join(institutions))

            if not (edu_score or degrees or institutions):
                st.warning("No education information extracted.")

            
            st.subheader("🎓 Final Score")
            if "final_score" in result_state:
                st.title(f"**Final Score:** {result_state.get('final_score', 0)}")

            st.divider()

            st.subheader("🏆 Achievements & Certifications")
            achievements = result_state.get("achievements", [])
            if achievements:
                st.write("**Found:**")
                for a in achievements:
                    st.write(f"- {a}")
                st.write(f"**Bonus Score Added:** {result_state.get('achievement_score',0)*100:.1f}%")
            else:
                st.write("No notable achievements detected.")

            st.divider()

            # ============ 🧾 SUMMARY ============
            st.subheader("🧾 Summary")
            final_summary = result_state.get("final_summary", None)
            is_suitable = result_state.get("is_suitable", None)
            suitability_reason = result_state.get("suitability_reason", None)

            if final_summary:
                st.write(f"**Final summary:** {final_summary}")
            
            if is_suitable:
                st.write(f"**Is it suitable? :** {is_suitable}")

            if suitability_reason:
                st.write(f"**Reason:** {suitability_reason}")


            st.divider()

            # ============ 🧠 FULL OUTPUT ============
            with st.expander("🧠 Full State Output"):
                st.json(result_state)

        except Exception as e:
            st.error(f"❌ Error during evaluation: {e}")
