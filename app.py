import streamlit as st
from core.config import get_settings
from core.knowledge import KnowledgeBase
from agents.orchestrator import build_agent

st.set_page_config(
    page_title="UniMind AI V2",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Refined UI theme -----------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #080f1d;
        --panel: #111d31;
        --panel-2: #172640;
        --border: #2b4263;
        --text: #f4f7ff;
        --muted: #b7c5da;
        --accent: #63a8ff;
        --accent2: #9a7bff;
        --success: #4adeb1;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #080f1d !important;
        color: var(--text) !important;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 82% 0%, rgba(64, 103, 190, .20), transparent 34%),
            radial-gradient(ellipse at 5% 35%, rgba(93, 65, 170, .10), transparent 32%),
            #080f1d !important;
    }
    [data-testid="stHeader"] {
        background: rgba(8, 15, 29, .92) !important;
    }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container {
        max-width: 1440px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Global readable typography */
    html, body, [class*="css"], p, label, span, div {
        color: inherit;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
        color: var(--muted);
    }
    h1, h2, h3, h4, h5, h6,
    [data-testid="stSubheader"] {
        color: #f7f9ff !important;
        letter-spacing: -.02em;
    }
    h1 { font-weight: 800 !important; }
    h2, h3 { font-weight: 750 !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111e33 0%, #0d1728 100%) !important;
        border-right: 1px solid #2b4263;
    }
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #dce7f8 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(148, 175, 215, .13);
        border-radius: 11px;
        padding: 9px 11px;
        margin: 4px 0;
        color: #e5edfb !important;
        transition: .18s ease;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(91, 151, 240, .14);
        border-color: #527bb5;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #e5edfb !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + div {
        color: white !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #304765 !important;
    }

    /* Hero banner: no white container above it */
    .hero {
        position: relative;
        overflow: hidden;
        padding: 34px 38px;
        border: 1px solid rgba(133, 170, 235, .30);
        border-radius: 24px;
        background:
            radial-gradient(circle at 88% 18%, rgba(142, 120, 255, .32), transparent 32%),
            linear-gradient(118deg, #173b68 0%, #243d72 48%, #34285f 100%);
        box-shadow: 0 18px 48px rgba(0, 0, 0, .28);
        margin: 0 0 28px 0;
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -65px;
        bottom: -145px;
        border: 1px solid rgba(255,255,255,.18);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(255,255,255,.035),
                    0 0 0 58px rgba(255,255,255,.025);
    }
    .hero-kicker {
        display: inline-block;
        color: #d8e8ff;
        background: rgba(8, 18, 38, .28);
        border: 1px solid rgba(220,235,255,.22);
        border-radius: 999px;
        padding: 6px 11px;
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .10em;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    .hero h1 {
        color: #ffffff !important;
        font-size: clamp(1.8rem, 3.2vw, 2.65rem);
        line-height: 1.12;
        margin: 0 0 12px 0;
        max-width: 850px;
    }
    .hero p {
        color: #e1eaff !important;
        font-size: 1.02rem;
        line-height: 1.65;
        margin: 0;
        max-width: 850px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #152640, #101c30) !important;
        border: 1px solid #2b4263 !important;
        border-radius: 17px !important;
        padding: 18px 20px !important;
        box-shadow: 0 10px 28px rgba(0,0,0,.16);
        min-height: 125px;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label p {
        color: #c4d3e9 !important;
        font-size: .88rem !important;
        font-weight: 650 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: var(--success) !important;
    }

    /* Capability cards */
    .section-heading {
        color: #f6f8ff;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 30px 0 15px 0;
    }
    .capability-card {
        height: 100%;
        min-height: 142px;
        padding: 19px 19px 17px;
        margin-bottom: 14px;
        border-radius: 17px;
        background: linear-gradient(145deg, rgba(23, 39, 64, .98), rgba(15, 27, 46, .98));
        border: 1px solid #2b4263;
        box-shadow: 0 9px 24px rgba(0,0,0,.15);
        transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }
    .capability-card:hover {
        transform: translateY(-3px);
        border-color: #638fd0;
        box-shadow: 0 14px 30px rgba(0,0,0,.24);
    }
    .capability-title {
        color: #f4f7ff !important;
        font-size: 1.02rem;
        font-weight: 750;
        margin-bottom: 10px;
    }
    .capability-desc {
        color: #bdcce1 !important;
        font-size: .90rem;
        line-height: 1.55;
    }
    .capability-icon {
        display: inline-flex;
        width: 34px;
        height: 34px;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: rgba(98, 168, 255, .13);
        margin-right: 9px;
        font-size: 1.05rem;
    }
    .footer-note {
        color: #aebed5;
        background: rgba(17, 30, 50, .72);
        border: 1px solid #293f5e;
        border-radius: 13px;
        padding: 13px 16px;
        margin-top: 13px;
        font-size: .86rem;
    }

    /* Inputs, uploaders, buttons and chat */
    .stButton > button {
        color: #edf5ff !important;
        background: #172943 !important;
        border: 1px solid #3b587d !important;
        border-radius: 11px !important;
        font-weight: 700 !important;
        min-height: 42px;
    }
    .stButton > button:hover {
        color: #ffffff !important;
        background: #203b60 !important;
        border-color: #76a8ed !important;
    }
    .stButton > button[kind="primary"] {
        color: #ffffff !important;
        background: linear-gradient(100deg, #347fe8, #765fe5) !important;
        border: 0 !important;
        box-shadow: 0 8px 22px rgba(68, 111, 218, .25);
    }
    .stTextInput input, .stTextArea textarea {
        color: #f4f7ff !important;
        background: #101d31 !important;
        border: 1px solid #3a5273 !important;
    }
    [data-testid="stFileUploader"] {
        background: #111e32 !important;
        border: 1px dashed #54749e !important;
        border-radius: 15px !important;
        padding: 12px !important;
    }
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #dce8f8 !important;
    }
    div[data-testid="stChatMessage"] {
        background: #13233a !important;
        border: 1px solid #30496d !important;
        border-radius: 15px !important;
        padding: 14px 16px !important;
    }
    /* Chat composer: white input surface with dark, readable typed text */
    [data-testid="stChatInput"],
    div[data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 14px !important;
        padding: 3px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, .16) !important;
    }

    [data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] textarea,
    [data-testid="stChatInputTextArea"],
    textarea[data-testid="stChatInputTextArea"],
    .stChatInput textarea {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        background: #ffffff !important;
        caret-color: #111827 !important;
        border: 0 !important;
        box-shadow: none !important;
        font-size: 1rem !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    div[data-testid="stChatInput"] textarea::placeholder,
    textarea[data-testid="stChatInputTextArea"]::placeholder,
    .stChatInput textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    /* Keep the send button visible against the white composer */
    [data-testid="stChatInput"] button {
        color: #ffffff !important;
        background: #347fe8 !important;
        border-radius: 10px !important;
    }
    [data-testid="stAlert"] {
        border-radius: 13px !important;
    }
    hr { border-color: #2a405e !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

cfg = get_settings()

if "kb" not in st.session_state:
    st.session_state.kb = KnowledgeBase(cfg)
if "history" not in st.session_state:
    st.session_state.history = []
if "agent" not in st.session_state:
    st.session_state.agent = None

# ----------------------------- Sidebar -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding:8px 2px 14px 2px;">
          <div style="font-size:1.55rem;font-weight:850;color:#ffffff;">🎓 UniMind AI</div>
          <div style="font-size:.72rem;font-weight:750;letter-spacing:.10em;color:#a9c6ed;margin-top:5px;">
            V2 · AGENTIC UNIVERSITY
          </div>
          <div style="font-size:.72rem;font-weight:750;letter-spacing:.10em;color:#a9c6ed;">
            KNOWLEDGE WORKSPACE
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("##### WORKSPACE")
    page = st.radio(
        "Navigate workspace",
        ["Dashboard", "Upload Knowledge", "Agent Assistant", "Knowledge Base"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown(
        """
        <div style="padding:8px 2px;color:#b9cbe3;font-size:.82rem;line-height:1.8;">
          <b style="color:#eef5ff;">POWERED BY</b><br>
          <span style="color:#b9cbe3;">● Groq LLM</span><br>
          <span style="color:#b9cbe3;">● LangGraph Agents</span><br>
          <span style="color:#b9cbe3;">● HuggingFace Embeddings</span><br>
          <span style="color:#b9cbe3;">● FAISS Vector Search</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

kb = st.session_state.kb
stats = kb.stats()

# ----------------------------- Dashboard -----------------------------
if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Your intelligent university workspace</div>
          <h1>University knowledge, powered by agents.</h1>
          <p>Ask complex questions. Specialized tools retrieve evidence, search your university documents,
          and coordinate clear answers grounded in your knowledge base.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)
    a.metric("📚  Indexed documents", stats["documents"])
    b.metric("🧩  Indexed chunks", stats["chunks"])
    c.metric("⚡  FAISS index", "Ready" if stats["ready"] else "Not ready")

    st.markdown('<div class="section-heading">Agent capabilities</div>', unsafe_allow_html=True)
    items = [
        ("🎓", "Admission guidance", "Find eligibility criteria, admission requirements and policy details."),
        ("💳", "Fee information", "Retrieve tuition fees, payment schedules and related instructions."),
        ("📘", "Courses & programs", "Explore departments, degree programs and course outlines."),
        ("🔎", "Document search", "Search university files and retrieve relevant supporting evidence."),
        ("📝", "Smart summarization", "Turn lengthy university material into clear, concise summaries."),
        ("🛡️", "Source-grounded answers", "Keep responses connected to information found in your documents."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(items):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="capability-card">
                  <div class="capability-title"><span class="capability-icon">{icon}</span>{title}</div>
                  <div class="capability-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="footer-note">💡 <b>V2 has its own knowledge index.</b> Upload your V1 source documents again here. Your V1 project remains unchanged.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------- Upload Knowledge -----------------------------
elif page == "Upload Knowledge":
    st.markdown("## 📤 Upload university documents")
    st.caption("Add PDF, DOCX or TXT files. UniMind AI extracts the text, creates embeddings and updates its own FAISS index.")
    uploads = st.file_uploader(
        "Choose documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )
    if st.button("🚀  Build / Update Knowledge Base", type="primary", disabled=not uploads):
        with st.spinner("Extracting, embedding and indexing your documents..."):
            try:
                result = kb.add_files(uploads)
                st.success(f"Indexed {result['chunks']} chunks from {result['documents']} documents.")
                for error in result["errors"]:
                    st.warning(error)
                st.rerun()
            except Exception as e:
                st.error(f"Indexing failed: {e}")
    st.markdown(
        '<div class="footer-note">Note: scanned or image-only PDFs require OCR, which is not included in this version.</div>',
        unsafe_allow_html=True,
    )

# ----------------------------- Agent Assistant -----------------------------
elif page == "Agent Assistant":
    st.markdown("## 🤖 Agentic Knowledge Assistant")
    st.caption("Ask a question. The orchestrator selects specialized tools and retrieves relevant university evidence.")
    if not stats["ready"]:
        st.warning("Upload university documents first to activate the assistant.")
    else:
        if st.button("🧹  Clear conversation"):
            st.session_state.history = []
            st.session_state.agent = None
            st.rerun()

        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask about admissions, fees, courses, rules or compare policies...")
        if question:
            st.session_state.history.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                if not cfg.groq_api_key:
                    st.error("Add GROQ_API_KEY in Streamlit App settings → Secrets.")
                else:
                    try:
                        if st.session_state.agent is None:
                            st.session_state.agent = build_agent(kb, cfg)
                        with st.spinner("Agent is selecting tools and retrieving evidence..."):
                            result = st.session_state.agent.invoke(
                                {"messages": [{"role": "user", "content": question}]},
                                config={"recursion_limit": 12},
                            )
                        answer = result["messages"][-1].content
                        st.markdown(answer)
                        st.session_state.history.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Agent execution failed: {e}")

# ----------------------------- Knowledge Base -----------------------------
else:
    st.markdown("## 🗂️ Knowledge Base")
    st.caption("Overview of the documents currently indexed by UniMind AI V2.")
    a, b, c = st.columns(3)
    a.metric("📚  Documents", stats["documents"])
    b.metric("🧩  Chunks", stats["chunks"])
    c.metric("⚡  Status", "Ready" if stats["ready"] else "Empty")

    if stats["files"]:
        st.markdown('<div class="section-heading">Indexed files</div>', unsafe_allow_html=True)
        for filename in stats["files"]:
            st.markdown(f"- 📄 {filename}")
    else:
        st.info("No indexed documents yet. Open Upload Knowledge to add your university files.")
