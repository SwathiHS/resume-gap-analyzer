import streamlit as st
from pipeline.graph import build_graph
from pipeline import AgentState

st.set_page_config(page_title="Resume Gap Analyzer", page_icon="🤖")
st.title("🤖 Resume Gap Analyzer Bot")

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
        st.write("Hi! Paste your resume below and I'll analyze how well it matches a job description.")
    st.session_state.messages.append({"role": "assistant", "content": "Hi! Paste your resume below and I'll analyze how well it matches a job description."})

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