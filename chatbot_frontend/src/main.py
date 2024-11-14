
import streamlit as st


user_avatar = "👨‍💻"

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer your questions.
        The agent uses  retrieval-augment generation (RAG) over (unstructured) data which you provide.

        As an example we try to answer questions about :red[__Perry Rhodan__]
        """
    )

    st.header("Example Questions")
    st.markdown("- Who is Perry Rhodan?")


st.title("Nexus")

st.info(
    "Ask me questions about Perry's family, friends, and enemies! "
    "Enjoy Perry's adventure!"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

#    print(message)

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

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):

#        response = requests.post(CHATBOT_API, json=data)

        output_text = """At this stage of my development am not connected to any Generative AI assistant. Stay tunded!"""
        explanation = ''

        st.chat_message("assistant").markdown(output_text)

#        st.status("How was this generated", state="complete").info(explanation)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "output": output_text,
                "explanation": '',
            }
        )


