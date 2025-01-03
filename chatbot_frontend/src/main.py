
import requests
import streamlit as st

user_avatar = "👨‍💻"

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer your questions.
        - The chatbot interface with the backend API to generate answers to your questions.
        - At the end, the chatbot will use retrieval-augment generation (RAG) over (unstructured) data which you provide.

        As an example we try to answer questions about :red[__Nexus-Lumina__]
        """
    )

    st.header("Example Questions")
    st.markdown("- Who is AiA?")


st.title("AiA")

st.info(
    "Ask me any questions! "
    "I try to answer them to my best knowledge!"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    # print(message)

    avatar = user_avatar

    role = message["role"]

    if role != "user":
        avatar = "assistant"

    with st.chat_message(role, avatar=avatar):
        if "output" in message.keys():
            st.markdown( message["output"])

#        if "explanation" in message.keys():
#            with st.status("How was this generated", state="complete"):
#                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message('user', avatar=user_avatar).markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    # print(f"prompt: {prompt}")

    with st.spinner("Searching for an answer..."):

        # Send a request to initiate streaming
        chatbot_api_url = f"http://localhost:8000/query-stream?query={prompt}"
        response = requests.get(chatbot_api_url, stream=True)

        # Iterate over the generator and update the content dynamically
        output_text = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(f"> {chunk}")
                explanation = ''
                output_text += chunk.decode("utf-8")


        # Close the response stream
        response.close()

        st.chat_message("assistant").markdown(f'<div>{output_text}</div>', unsafe_allow_html=True)

        # output_text = """At this stage of my development I am not connected to any Generative AI assistant. Stay tunded!"""

        # st.status("How was this generated", state="complete").info(explanation)

        # st.session_state.messages.append(
        #    {
        #        "role": "assistant",
        #        "output": output_text,
        #        "explanation": '',
        #    }
        #)


