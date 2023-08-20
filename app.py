import os
import tempfile
import pdfplumber
import streamlit as st
from streamlit_chat import message
from agent import Agent
from PIL import Image

from pdf2image import convert_from_path


st.set_page_config(page_title="MTI FieldTech AI")
logo = Image.open("Images/mtilogo1.jpg")
st.image(logo, width=400)

def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["agent"].ask(user_text)
        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))
def read_and_save_file():
    if st.session_state["agent"] is not None:  # Check if agent is not None
        st.session_state["agent"].forget()  # Call forget method

    st.session_state["messages"] = []
    st.session_state["user_input"] = ""
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            temp_pdf_path = tf.name
            st.session_state["temp_pdf_path"] = temp_pdf_path
            st.session_state["agent"].ingest(temp_pdf_path)  # Ingest the document
        images = convert_from_path(temp_pdf_path)
        st.session_state["images"] = images


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0

def main():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
        if is_openai_api_key_set():
            st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])
        else:
            st.session_state["agent"] = None
    
    if st.text_input("OpenAI API Key", value=st.session_state["OPENAI_API_KEY"], key="input_OPENAI_API_KEY", type="password"):
        if (
            len(st.session_state["input_OPENAI_API_KEY"]) > 0
            and st.session_state["input_OPENAI_API_KEY"] != st.session_state["OPENAI_API_KEY"]
        ):
            st.session_state["OPENAI_API_KEY"] = st.session_state["input_OPENAI_API_KEY"]
            if st.session_state["agent"] is not None:
                st.warning("Please, upload the files again.")
            st.session_state["messages"] = []
            st.session_state["user_input"] = ""
            st.session_state["agent"] = Agent(st.session_state["OPENAI_API_KEY"])


    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True)
        
    temp_pdf_path = st.session_state.get("temp_pdf_path", "")  # Retrieve the path from session_state



    if temp_pdf_path:  # Check if the path is not an empty string
        text = ""  # Initialize the text variable
        with pdfplumber.open(temp_pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() 
    
    images = st.session_state.get("images", [])
    if images:
        page_number = st.slider('Select Page:', min_value=1, max_value=len(images), value=1) - 1
        st.image(images[page_number])
        st.write("PDF processed. Ask your questions below.")
    
        



    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", disabled=not is_openai_api_key_set(), on_change=process_input)

    st.divider()
    st.markdown("Source code: [Github](https://github.com/sacred-g/chatpdfs)")
    st.markdown("Created by Steven Bouldin")
    st.markdown("Version: 1.1")




if __name__ == "__main__":
    main()