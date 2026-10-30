import streamlit as st

from modules.code_reviewer import review_code
from modules.bug_analyzer import analyze_bug
from modules.resume_analyzer import calculate_match
from utils.pdf_utils import extract_text_from_pdf


# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="DevAI",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------
# Header
# ---------------------------------

st.title("🤖 DevAI")
st.caption("AI-powered developer productivity toolkit")

st.divider()


# ---------------------------------
# Navigation
# ---------------------------------

tab1, tab2, tab3 = st.tabs([
    "🔍 Code Reviewer",
    "🐞 Bug Analyzer",
    "📄 Resume Intelligence"
])


# =================================
# CODE REVIEWER
# =================================

with tab1:

    st.header("🔍 Python Code Reviewer")

    st.write(
        "Analyze Python code for quality, complexity, "
        "security and maintainability issues."
    )

    code = st.text_area(
        "Paste your Python code",
        height=350,
        placeholder="""def calculate(a, b):
    return a + b""",
        key="review_code"
    )

    if st.button(
        "🚀 Review Code",
        type="primary",
        key="review_button"
    ):

        if not code.strip():

            st.warning("Please enter some Python code.")

        else:

            with st.spinner("Analyzing your code..."):

                result = review_code(code)

            if "error" in result:

                st.error(result["error"])

            elif not result["syntax_valid"]:

                st.error("❌ Syntax Error")
                st.code(result["syntax_error"])

            else:

                st.success("✅ Code analysis completed")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Quality Score",
                        f"{result['score']}/100"
                    )

                with col2:
                    st.metric(
                        "Functions",
                        result["functions"]
                    )

                with col3:
                    st.metric(
                        "Complexity",
                        result["complexity"]
                    )

                with col4:
                    st.metric(
                        "Issues",
                        len(result["issues"])
                    )

                st.divider()

                st.subheader("📊 Code Metrics")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Lines of Code",
                        result["lines"]
                    )

                with col2:
                    st.metric(
                        "Maintainability",
                        result["maintainability"]
                    )

                st.subheader("⚠️ Issues Found")

                if not result["issues"]:

                    st.success(
                        "🎉 No major issues detected."
                    )

                else:

                    for issue in result["issues"]:

                        st.warning(
                            f"**{issue['type']}** — "
                            f"Line {issue['line']}: "
                            f"{issue['message']}"
                        )


# =================================
# BUG ANALYZER
# =================================

with tab2:

    st.header("🐞 Python Bug Analyzer")

    st.write(
        "Paste your Python code and the error message "
        "to identify the likely cause and fix."
    )

    bug_code = st.text_area(
        "Python Code",
        height=280,
        placeholder="""numbers = [10, 20, 30]
print(numbers[5])""",
        key="bug_code"
    )

    error_message = st.text_area(
        "Error / Traceback",
        height=180,
        placeholder="""IndexError: list index out of range""",
        key="error_message"
    )

    if st.button(
        "🔎 Analyze Bug",
        type="primary",
        key="bug_button"
    ):

        if not bug_code.strip():

            st.warning("Please enter the Python code.")

        elif not error_message.strip():

            st.warning("Please enter the error message.")

        else:

            with st.spinner("Analyzing the bug..."):

                result = analyze_bug(
                    bug_code,
                    error_message
                )

            st.success("✅ Bug analysis completed")

            st.metric(
                "Detected Error",
                result["error_type"]
            )

            st.subheader("📌 Error")
            st.code(result["error_message"])

            st.subheader("🔍 Likely Cause")
            st.info(result["cause"])

            st.subheader("🛠️ Suggested Fix")
            st.success(result["suggestion"])


# =================================
# RESUME INTELLIGENCE
# =================================

with tab3:

    st.header("📄 Resume Intelligence")

    st.write(
        "Upload your resume and compare it against a "
        "job description using NLP-based similarity analysis."
    )

    resume_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="""We are looking for a Python developer
with experience in Machine Learning, SQL, Git,
Docker and AWS.""",
        key="job_description"
    )

    if st.button(
        "📊 Analyze Resume",
        type="primary",
        key="resume_button"
    ):

        if resume_file is None:

            st.warning("Please upload your resume PDF.")

        elif not job_description.strip():

            st.warning("Please enter the job description.")

        else:

            with st.spinner("Analyzing your resume..."):

                resume_text = extract_text_from_pdf(
                    resume_file
                )

                if not resume_text:

                    st.error(
                        "Could not extract text from this PDF. "
                        "Make sure the resume contains selectable text."
                    )

                else:

                    result = calculate_match(
                        resume_text,
                        job_description
                    )

                    st.success(
                        "✅ Resume analysis completed"
                    )

                    # Score
                    st.subheader("🎯 Job Match Score")

                    st.metric(
                        "Resume Match",
                        f"{result['score']}%"
                    )

                    st.progress(
                        min(result["score"] / 100, 1.0)
                    )

                    # Skills
                    st.subheader("🧠 Skill Analysis")

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write("### ✅ Matching Skills")

                        if result["matching_skills"]:

                            for skill in result["matching_skills"]:
                                st.write(f"• {skill}")

                        else:

                            st.write("No matching skills detected.")

                    with col2:

                        st.write("### ❌ Missing Skills")

                        if result["missing_skills"]:

                            for skill in result["missing_skills"]:
                                st.write(f"• {skill}")

                        else:

                            st.write(
                                "No major missing skills detected."
                            )

                    st.subheader("📋 Detected Resume Skills")

                    if result["resume_skills"]:

                        st.write(
                            ", ".join(result["resume_skills"])
                        )

                    else:

                        st.write(
                            "No recognized technical skills detected."
                        )