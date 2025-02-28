import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize the project id to connect with your google cloud account
project = "gemini-explorer-431005"
vertexai.init(project = project)

# Initialize the configurations for the LLM model
config = generative_models.GenerationConfig(
    temperature = 0.4
)

# Initializing the Generative Model
model = GenerativeModel(
    "gemini-pro",
    generation_config  = config
)
chat = model.start_chat()

# Initializing two roles - user and model. This ensures the multiturn capability of the model. Basically, gives the feel of a chat!
def llm_function(chat: ChatSession, query):

    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    st.session_state.messages.append(
        {
            "role" : "model",
            "content": output
        }
    )

# Creating the Streamlit UI components
st.title("RadicalAI Gemini Explorer")

if "messages" not in st.session_state:
    st.session_state.messages = []

for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )

    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    chat.history.append(content)

# Personalizing the initial message that appears. This ensures a character and creates a more interactive experience for the user. 
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as Dr.Gemini, a scholar powered by Google Gemini. You use emojis to be interactive and show your personality. Try and incoporate user responses into the conversation"
    llm_function(chat, initial_prompt)

query = st.chat_input("Interact with Gemini Pro")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
