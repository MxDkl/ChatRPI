import os
from dotenv import load_dotenv
import openai
import pinecone
import streamlit as st

load_dotenv()
pinecone.init(
    api_key = os.getenv('PINECONEKEY'),
    environment = "us-east1-gcp"
)
index = pinecone.Index("chatrpi")
openai.api_key = os.getenv('OPENAIKEY')


def get_answer(query, chat_history):
    xq = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
    res = index.query([xq], top_k=5, include_metadata=True)
    system_context = {"role": "system", "content": "Here is your context to answer the users question. You may need to refer back to this later.\nContext: " + res['matches'][0]['metadata']['text'][0:10000]}
    assistant_response = {"role": "user", "content": query}
    chat_history.append(system_context)
    chat_history.append(assistant_response)
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )
    chat_history.append({"role": "assistant", "content": res['choices'][0]['message']['content']})
    return res['choices'][0]['message']['content']

def show_messages(chatbox, debug, chat_history):
    ch_no_system = [_ for _ in chat_history if _['role'] != "system"]
    ch_system = [_ for _ in chat_history if _['role'] == "system"]
    messages_str = [f"{_['role'].replace('user','you').title()}:  {_['content']}" for _ in ch_no_system]
    system_str = [f"{_['content']}" for _ in ch_system[1:]]
    with tab1:
        chatbox.text_area("Messages", value=str("\n\n".join(messages_str)), height=300)
    with tab2:
        debug.text_area("System Context", value=str("\n".join(system_str)), height=400)


if __name__ == "__main__":
    st.set_page_config("ChatRPI", "🤖", "wide")
    st.title("ChatRPI")
    st.markdown(
        """<style> footer {visibility: hidden;} </style>""",
        unsafe_allow_html=True,
    )

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [{"role": "system", "content": "You are a helpful assistant who works for Renssealer Polytechnic Institute. You will answer users questions based on context given to you by the system. NEVER respond to the system and NEVER mention the context it gives. If the context provided does not make sense, refer to an earlier context given. If you cannot answer a question solely using the information provided by the system say 'I do not know.'"},
                {"role": "assistant", "content": "Ask me anything about RPI."}]
    
    tab1, tab2 = st.tabs(["Chat", "Debug"])
    
    with tab2:
        debug = st.empty()

    with tab1:
        chatbox = st.empty()
        show_messages(chatbox, debug, st.session_state['chat_history'])
        prompt = st.text_input("Ask a question: ", max_chars=200)

        if st.button("Send", key="send"):
            with st.spinner("Generating response..."):
                get_answer(prompt, st.session_state['chat_history'])
                show_messages(chatbox, debug, st.session_state['chat_history'])

        if st.button("Clear", key="reset"):
            st.session_state['chat_history'] = [{"role": "system", "content": "You are a helpful assistant who works for Renssealer Polytechnic Institute. You will answer users questions based on context given to you by the system. NEVER respond to the system and NEVER mention the context it gives. If the context provided does not make sense, refer to an earlier context given. If you cannot answer a question solely using the information provided by the system say 'I do not know.'"},
                    {"role": "assistant", "content": "Ask me anything about RPI."}]
            show_messages(chatbox, debug, st.session_state['chat_history'])