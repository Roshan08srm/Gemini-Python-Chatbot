import streamlit as st
from google import genai

# 1. Set the Title of the Web Page
st.title("🌌 Gemini Simple Chatbot")
st.write("A clean, easy-to-understand AI assistant interface.")

# 2. Connect to the Gemini API
# This function initializes the Gemini client. We use st.cache_resource
# so Streamlit doesn't recreate the connection every time the user types.
@st.cache_resource
def get_client():
    return genai.Client()

try:
    client = get_client()
except Exception as e:
    st.error("Missing Gemini API Key! Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# 3. Create a state to store our messages so they don't disappear when the page reloads
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Create a stateful chat session to remember the conversation context
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

# 5. Display all previous messages on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. Capture new user input
if user_input := st.chat_input("Type your message here..."):
    
    # 7. Show user message on screen and save it to our history
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 8. Send the message to Gemini and stream the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response chunk by chunk (real-time typing effect)
        response_stream = st.session_state.chat.send_message_stream(user_input)
        for chunk in response_stream:
            if chunk.text:
                full_response += chunk.text
                message_placeholder.write(full_response + "▌")
                
        # Show final cleaned-up text (remove the typing indicator cursor)
        message_placeholder.write(full_response)
        
    # 9. Save the assistant response to our history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
