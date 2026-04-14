import pdfplumber
import docx
import streamlit as st
from pipeline.graph import build_graph
from pipeline import AgentState

st.set_page_config(page_title="Resume Gap Analyzer", page_icon="🤖")
st.title("🤖 Resume Gap Analyzer Bot")
st.caption("Powered by Groq · llama-3.3-70b-versatile · LangGraph 3-Agent System")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.stage = "get_resume"
    st.session_state.resume_text = ""
    st.session_state.jd_text = ""

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if st.session_state.stage == "get_resume" and len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write("Hi! Upload your resume as PDF or Word doc, or paste it below.")
    st.session_state.messages.append({"role": "assistant", "content": "Hi! Upload your resume as PDF or Word doc, or paste it below."})

if st.session_state.stage == "get_resume":
    uploaded_file = st.file_uploader("Upload resume PDF or Word doc", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "\n".join([page.extract_text() for page in pdf.pages])
        else:
            doc = docx.Document(uploaded_file)
            resume_text = "\n".join([para.text for para in doc.paragraphs])
        st.session_state.resume_text = resume_text
        st.session_state.stage = "get_jd"
        with st.chat_message("assistant"):
            st.write("Got your resume! Now paste the job description.")
        st.session_state.messages.append({"role": "assistant", "content": "Got your resume! Now paste the job description."})
        st.rerun()

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if st.session_state.stage == "get_resume":
        st.session_state.resume_text = prompt
        st.session_state.stage = "get_jd"
        response = "Got your resume! Now paste the job description."
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

    elif st.session_state.stage == "get_jd":
        st.session_state.jd_text = prompt
        st.session_state.stage = "analyzing"
        with st.chat_message("assistant"):
            st.write("Analyzing your resume now... 🔍")

        graph = build_graph()
        state = AgentState(
            resume_text=st.session_state.resume_text,
            jd_text=st.session_state.jd_text,
            resume_profile=None, jd_profile=None,
            comparison=None, retry_count=0, max_retries=3,
            fit_score=None, label=None, missing_skills=None, feedback=None
        )
        result = graph.invoke(state)

        response = f"""
**Fit Score:** {result['fit_score']}/100  
**Label:** {result['label']}  
**Missing Skills:** {', '.join(result['missing_skills'])}  
**Feedback:** {result['feedback']}
        """
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.stage = "done"

if st.session_state.stage == "done":
    if st.button("🔄 Analyze another job description"):
        st.session_state.stage = "get_jd"
        st.session_state.jd_text = ""
        st.rerun()