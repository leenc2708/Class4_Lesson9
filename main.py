import os
from typing import Any
import streamlit as st
from pydantic import BaseModel, ValidationError
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass
try:
    from openai import OpenAI
except Exception:  # pragma: no cover - optional dependency at this step
    OpenAI = None  # type: ignore

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


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def create_openrouter_client(api_key: str, *, app_title: str = "Streaming Prompt Tester") -> Any:
    if not api_key or not api_key.strip():
        raise ValueError("api_key is required")
    if OpenAI is None:
        raise RuntimeError("The 'openai' package is required. Install with: pip install openai")

    default_headers = {
        "HTTP-Referer": os.getenv("APP_URL", "http://localhost"),
        "X-Title": app_title,
    }
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        default_headers=default_headers,
    )
    return client


def build_messages(prompt: PromptInput) -> list[dict[str, str]]:
    user_content = prompt.question if not prompt.context else f"{prompt.context}\n\n{prompt.question}"
    return [
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": user_content},
    ]


def render_sidebar() -> None:
    st.sidebar.header("App Settings")
    st.sidebar.text_input("OPENROUTER_API_KEY", key="openrouter_api_key", type="password", placeholder="••••••••••••••••")
    st.sidebar.button("Check OpenRouter connection", key="btn_check_conn", use_container_width=True)
    #st.sidebar.text_input("LANGFUSE_PUBLIC_KEY", key="langfuse_public_key", type="password", placeholder="••••••••••••••••")
    #st.sidebar.text_input("LANGFUSE_SECRET_KEY", key="langfuse_secret_key", type="password", placeholder="••••••••••••••••")
    st.sidebar.selectbox("Model", [
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "anthropic/claude-3.5-sonnet",
        "google/gemini-1.5-pro",
        "meta-llama/llama-3.1-70b-instruct",
        "mistralai/mixtral-8x7b-instruct",
    ], index=0, key="model_select")
    st.sidebar.checkbox("Enable Langfuse tracing", value=True, key="enable_langfuse")


def render_main() -> None:
    st.title("Streaming Prompt Tester")
    st.caption("Enter system prompt, context, and question. Streaming output will render below.")

    with st.container():
        #st.markdown('<div class="frame-16x9">', unsafe_allow_html=True)

        # Inputs
        st.markdown("Inputs", help="Placeholders only. No logic or integrations.")
        with st.container():
            #st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.text_area("System prompt", key="system_prompt", height=100, placeholder="You are a helpful assistant…")
            st.text_area("Context", key="context", height=120, placeholder="Optional contextual information, documents, or metadata…")
            st.text_area("Question", key="question", height=100, placeholder="What would you like to ask?")
            st.markdown('</div>', unsafe_allow_html=True)

        # Actions
        with st.container():
            #st.markdown('<div class="section-box">', unsafe_allow_html=True)
            col_a, col_b = st.columns([1, 1])
            with col_a:
                start_clicked = st.button("Start streaming", key="btn_start", use_container_width=True)
            with col_b:
                clear_clicked = st.button("Clear", key="btn_clear", use_container_width=True)
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

    # Validation-only behavior (no integrations)
    if st.session_state.get('btn_start'):
        api_key = st.session_state.get('openrouter_api_key') or os.getenv('OPENROUTER_API_KEY')
        if not api_key or not api_key.strip():
            st.error("OPENROUTER_API_KEY is required. Provide it in the sidebar or environment.")
            return

        system_prompt = (st.session_state.get('system_prompt') or '').strip()
        question = (st.session_state.get('question') or '').strip()
        context = st.session_state.get('context') or None
        model = st.session_state.get('model_select') or ''

        if not system_prompt:
            st.error("System prompt is required.")
            return
        if not question:
            st.error("Question is required.")
            return

        try:
            _ = PromptInput(system_prompt=system_prompt, context=context, question=question, model=model)
        except ValidationError as e:
            st.error(f"Input validation failed: {e.errors()}")
            return

        st.success("Inputs validated. Ready to stream (integration not connected).")

    # Connection check button behavior
    if st.session_state.get('btn_check_conn'):
        api_key = st.session_state.get('openrouter_api_key') or os.getenv('OPENROUTER_API_KEY')
        if not api_key or not api_key.strip():
            st.sidebar.error("Provide OPENROUTER_API_KEY above or in .env")
        else:
            try:
                client = create_openrouter_client(api_key)
                # lightweight call: list models endpoint is not available via SDK; do a trivial non-streaming
                # test by creating a minimal, non-billable request with an obviously invalid model to get 400/404
                # but confirm auth (401 would indicate bad key). We avoid sending user text.
                client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[{"role": "system", "content": "ping"}, {"role": "user", "content": "ping"}],
                    max_tokens=1,
                )
                st.sidebar.success("OpenRouter: connection OK")
            except Exception as e:
                st.sidebar.error(f"OpenRouter check failed: {e}")

    if st.session_state.get('btn_clear'):
        for key in [
            'system_prompt', 'context', 'question', 'openrouter_api_key',
            'langfuse_public_key', 'langfuse_secret_key'
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


def main() -> None:
    configure_page()
    render_sidebar()
    render_main()


if __name__ == "__main__":
    main()


