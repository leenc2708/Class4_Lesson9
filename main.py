import streamlit as st
from pydantic import BaseModel

def configure_page() -> None:
    st.set_page_config(page_title="Streaming Prompt Tester", layout="wide")
    st.markdown(
        """
        <style>
        .frame-16x9 {
            width: 100%;
            aspect-ratio: 16 / 9;
            border: 1px solid #E0E0E0;
            border-radius: 10px;
            padding: 12px 16px;
            box-sizing: border-box;
            background: #FFFFFF;
        }
        .section-box {
            border: 1px dashed #D0D0D0;
            border-radius: 8px;
            padding: 10px 12px;
            margin-top: 8px;
            margin-bottom: 12px;
            background: #FAFAFA;
        }
        .chat-box {
            border: 1px solid #EEE;
            border-radius: 8px;
            background: #FFFFFF;
            padding: 10px 12px;
        }
        .chat-msg {
            background: #F3F6FF;
            border: 1px solid #E2E8FF;
            padding: 8px 10px;
            border-radius: 6px;
            margin-bottom: 8px;
            color: #14213D;
        }
        .meta-row {
            font-size: 12px;
            color: #666;
        }
        .footer-note {
            font-size: 12px;
            color: #777;
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


class PromptInput(BaseModel):
    system_prompt: str
    context: str | None = None
    question: str
    model: str


def render_sidebar() -> None:
    st.sidebar.header("App Settings")
    st.sidebar.text_input("OPENROUTER_API_KEY", type="password", placeholder="••••••••••••••••")
    st.sidebar.text_input("LANGFUSE_PUBLIC_KEY", type="password", placeholder="••••••••••••••••")
    st.sidebar.text_input("LANGFUSE_SECRET_KEY", type="password", placeholder="••••••••••••••••")
    st.sidebar.selectbox("Model", [
        "openrouter/model-a",
        "openrouter/model-b",
        "openrouter/model-c",
    ], index=0)
    st.sidebar.checkbox("Enable Langfuse tracing", value=True)


def render_main() -> None:
    st.title("Streaming Prompt Tester")
    st.caption("Enter system prompt, context, and question. Streaming output will render below.")

    with st.container():
        #st.markdown('<div class="frame-16x9">', unsafe_allow_html=True)

        # Inputs
        st.markdown("Inputs", help="Placeholders only. No logic or integrations.")
        with st.container():
            #st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.text_area("System prompt", height=100, placeholder="You are a helpful assistant…")
            st.text_area("Context", height=120, placeholder="Optional contextual information, documents, or metadata…")
            st.text_area("Question", height=100, placeholder="What would you like to ask?")
            st.markdown('</div>', unsafe_allow_html=True)

        # Actions
        with st.container():
            #st.markdown('<div class="section-box">', unsafe_allow_html=True)
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.button("Start streaming", use_container_width=True)
            with col_b:
                st.button("Clear", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Output
        #st.markdown("Output")
        with st.container():
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<div class="chat-box">', unsafe_allow_html=True)
            st.markdown('<div class="chat-msg">Assistant: Streaming output will appear here…</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="meta-row">Tokens — | Latency —</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Footer
        st.markdown('<div class="footer-note">No logic or integrations implemented</div>', unsafe_allow_html=True)

        # Removed 16:9 frame wrapper closing tag (no 16:9 frame on screen)


def main() -> None:
    configure_page()
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()


