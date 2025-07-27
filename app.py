import streamlit as st
import requests

def query_bot(message):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": message}
    try:
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        messages = res.json()
        text = ""
        for m in messages:
            if "text" in m:
                text += m["text"] + "\n\n"
        return text.strip() or "No response from the bot."
    except Exception as e:
        return f"Error talking to backend: {e}"

def main():
    st.set_page_config(page_title="SOP Chat Assistant")
    st.title("SOP Chat Assistant 🤖")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for sender, msg in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(msg)

    # Get user input
    user_input = st.chat_input("Ask an SOP question...")
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Bot is searching documents..."):
            bot_answer = query_bot(user_input)

        with st.chat_message("assistant"):
            st.markdown(bot_answer, unsafe_allow_html=True)  # This makes links clickable!

        st.session_state.chat_history.append(("assistant", bot_answer))

if __name__ == "__main__":
    main()