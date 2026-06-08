"""Streamlit scaffold for the Day 8 group RAG chatbot."""

from __future__ import annotations

import streamlit as st

from src.rag_pipeline import generate_answer


st.set_page_config(page_title="Day 8 RAG Chatbot", layout="wide")
st.title("Day 8 RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Hỏi về pháp luật ma túy hoặc tin tức liên quan"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    result = generate_answer(question, history=st.session_state.messages)
    answer = result["answer"]
    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
        if result["sources"]:
            with st.expander("Nguồn đã sử dụng"):
                for source in result["sources"]:
                    st.write(source)
