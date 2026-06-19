import os
import uuid
import streamlit as st
from google import genai
from google.genai import types
from database import (
    init_db,
    save_message,
    load_messages,
    get_all_sessions,
    create_session,
    update_session_title,
    delete_session,
    clear_all_db
)


init_db()


st.set_page_config(
    page_title="Gemini AI Space",
    page_icon="🌌",
    layout="centered"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    /* Global styles */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Center container padding */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 2rem !important;
        max-width: 780px !important;
    }

    /* Premium gradient header */
    .gradient-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    
    .subheader {
        font-size: 1.1rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Style the chat input bar */
    div[data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        background-color: #171c2a !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #a855f7 !important;
        box-shadow: 0 4px 25px rgba(168, 85, 247, 0.25) !important;
    }

    /* Custom Chat Message Styling */
    div[data-testid="stChatMessage"] {
        border-radius: 20px !important;
        padding: 1.25rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
    }
    
    div[data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
    }

    /* Specific bubble styling for User */
    div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.08) 100%) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
    }

    /* Specific bubble styling for Assistant */
    div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
        background-color: #171c2a !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    /* Custom avatars */
    div[data-testid="stChatMessage"] .st-emotion-cache-1idx578 {
        border-radius: 50% !important;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="gradient-header">Gemini AI Space</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">A modern, state-of-the-art conversational interface powered by Gemini 2.5 Flash</div>', unsafe_allow_html=True)

MODEL = "gemini-2.5-flash"


@st.cache_resource
def get_client():
    return genai.Client()

try:
    client = get_client()
except Exception as e:
    st.error("🔑 API Key Error: Could not initialize the Gemini Client.")
    st.info("Please make sure you have set the `GEMINI_API_KEY` environment variable in your terminal.")
    st.stop()



sessions = get_all_sessions()

if "current_session_id" not in st.session_state:
    if sessions:
        st.session_state.current_session_id = sessions[0]["id"]
    else:
        new_id = str(uuid.uuid4())
        create_session(new_id, "New Chat")
        st.session_state.current_session_id = new_id
        sessions = get_all_sessions()

if ("active_session_loaded" not in st.session_state or 
    st.session_state.active_session_loaded != st.session_state.current_session_id):
    
    st.session_state.messages = load_messages(st.session_state.current_session_id)
    st.session_state.active_session_loaded = st.session_state.current_session_id
    
    try:
        history = []
        for msg in st.session_state.messages:
            history.append(
                types.Content(
                    role="user" if msg["role"] == "user" else "model",
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )
        st.session_state.chat = client.chats.create(
            model=MODEL,
            history=history
        )
    except Exception as e:
        st.error(f"Error seeding conversation memory: {e}")
        st.stop()

# --- SIDEBAR USER INTERFACE ---
with st.sidebar:
    st.markdown("### 🌌 Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        create_session(new_id, "New Chat")
        st.session_state.current_session_id = new_id
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(model=MODEL)
        st.session_state.active_session_loaded = new_id
        st.rerun()
        
    st.write("---")
    st.markdown("**Recent Chats**")
    
    if not sessions:
        st.caption("No conversations yet.")
    else:
        for sess in sessions:
            col1, col2 = st.columns([0.8, 0.2])
            
            is_active = (sess["id"] == st.session_state.current_session_id)
            btn_label = f"💬 {sess['title']}" if is_active else f"📄 {sess['title']}"
            btn_type = "primary" if is_active else "secondary"
            
            with col1:
                if st.button(btn_label, key=f"select_{sess['id']}", use_container_width=True, type=btn_type):
                    st.session_state.current_session_id = sess["id"]
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{sess['id']}", use_container_width=True):
                    delete_session(sess["id"])
                    if sess["id"] == st.session_state.current_session_id:
                        # Clear active selections
                        if "current_session_id" in st.session_state:
                            del st.session_state.current_session_id
                        if "active_session_loaded" in st.session_state:
                            del st.session_state.active_session_loaded
                    st.rerun()
                    
    st.write("---")

    if st.button("🚨 Clear All Conversations", use_container_width=True):
        clear_all_db()
        if "current_session_id" in st.session_state:
            del st.session_state.current_session_id
        if "active_session_loaded" in st.session_state:
            del st.session_state.active_session_loaded
        st.rerun()



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Say something to Gemini..."):

    with st.chat_message("user"):
        st.markdown(prompt)
    

    save_message(st.session_state.current_session_id, "user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})


    first_turn = False
    if len(st.session_state.messages) == 1:
        first_turn = True
        title = prompt[:24] + "..." if len(prompt) > 24 else prompt
        update_session_title(st.session_state.current_session_id, title)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:

            response_stream = st.session_state.chat.send_message_stream(prompt)
            
            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {e}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg
            

        save_message(st.session_state.current_session_id, "assistant", full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        

        if first_turn:
            st.rerun()
