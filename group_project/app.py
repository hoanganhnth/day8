"""Streamlit UI for the Day 8 group RAG chatbot."""

from __future__ import annotations

import streamlit as st

from src.rag_pipeline import generate_answer


st.set_page_config(page_title="Day 8 RAG Chatbot", page_icon="🔎", layout="wide")


def _init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []


def _source_label(source: dict, index: int) -> str:
    metadata = source.get("metadata", {}) or {}
    name = metadata.get("source") or source.get("source") or f"Source {index}"
    score = source.get("score")
    if isinstance(score, (int, float)):
        return f"{index}. {name} · score {score:.3f}"
    return f"{index}. {name}"


def _render_sources(sources: list[dict]) -> None:
    if not sources:
        st.caption("Chưa có source documents. Retrieval/generation branch cần tích hợp pipeline thật.")
        return

    for index, source in enumerate(sources, start=1):
        with st.expander(_source_label(source, index)):
            metadata = source.get("metadata", {}) or {}
            if metadata:
                st.json(metadata)
            content = source.get("content", "")
            if content:
                st.markdown(content)


_init_state()

with st.sidebar:
    st.header("RAG Settings")
    top_k = st.slider("Top K sources", min_value=1, max_value=10, value=5)
    use_reranking = st.toggle("Use reranking", value=True)

    st.divider()
    st.subheader("Project Status")
    st.write("UI branch: `feature/chatbot-ui`")
    st.write("Pipeline status: waiting for retrieval/generation integration")

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.rerun()

st.title("Day 8 RAG Chatbot")
st.caption("Hỏi đáp về pháp luật ma túy và tin tức liên quan. Câu trả lời cuối cùng phải có citation và source documents.")

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Xin chào. Hãy đặt câu hỏi về pháp luật ma túy hoặc tin tức liên quan. "
            "Khi pipeline nhóm được tích hợp, mình sẽ trả lời kèm citation và nguồn."
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Hỏi về pháp luật ma túy hoặc tin tức liên quan"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Đang truy xuất tài liệu và tạo câu trả lời..."):
            try:
                result = generate_answer(
                    question,
                    history=st.session_state.messages,
                    top_k=top_k,
                    use_reranking=use_reranking,
                )
            except Exception as exc:
                result = {
                    "answer": f"Không thể tạo câu trả lời do lỗi pipeline: `{exc}`",
                    "sources": [],
                    "history": st.session_state.messages,
                    "question": question,
                }

        answer = result["answer"]
        st.markdown(answer)

        sources = result.get("sources", [])
        st.session_state.last_sources = sources
        with st.expander("Nguồn đã sử dụng", expanded=bool(sources)):
            _render_sources(sources)

    if result.get("history"):
        st.session_state.messages = result["history"]
        if not st.session_state.messages or st.session_state.messages[-1].get("role") != "assistant":
            st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.session_state.messages.append({"role": "assistant", "content": answer})
