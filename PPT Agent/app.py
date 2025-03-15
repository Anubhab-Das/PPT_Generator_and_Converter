import streamlit as st
import requests
import base64  
import os

API_URL = "http://127.0.0.1:8000/generate_ppt/"
TEXT_API_URL = "http://127.0.0.1:8000/generate_text/"
UPLOAD_API_URL = "http://127.0.0.1:8000/upload_pdf/"
DOWNLOAD_URL = "http://127.0.0.1:8000/download_ppt/"
BACKGROUND_IMAGE = os.path.join("templates", "pdfbackground.png")

def add_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    bg_image_style = f"""
    <style>
        .stApp {{
            background: linear-gradient(to right, rgba(255, 255, 255, 0) 50%, transparent 100%),
                        url("data:image/png;base64,{encoded_string}") no-repeat;
            background-size: cover;
            background-position: left;
        }}
        .block-container {{
            max-width: 700px;
            margin-left: auto;
            margin-right: 20px;
            background: rgba(255, 255, 255, 1);
            padding: 120px;
            border-radius: 10px;
        }}
        .stTextInput, .stButton {{
            width: 100%;
        }}
    </style>
    """
    st.markdown(bg_image_style, unsafe_allow_html=True)

st.title("AI-Powered PPT Generator")

if os.path.exists(BACKGROUND_IMAGE):
    add_bg_image(BACKGROUND_IMAGE)

option = st.selectbox(
    "Choose an option:",
    ("Generate PPT from Topics", "Convert PDF to PPT")
)

if option == "Generate PPT from Topics":
    main_topic = st.text_input("Main Topic", "Artificial Intelligence")
    subtopic_1 = st.text_input("Subtopic 1", "Machine Learning")
    subtopic_2 = st.text_input("Subtopic 2", "Deep Learning")

    if st.button("Generate PPT"):
        st.info("⏳ Fetching text, images, and generating PPT...")
        generated_text = {}

        for subtopic in [subtopic_1, subtopic_2]:
            text_response = requests.post(TEXT_API_URL, json={"topic": subtopic})
            if text_response.status_code == 200:
                try:
                    resp = text_response.json()
                    if "data" in resp:
                        generated_text[subtopic] = resp["data"]
                    else:
                        st.error(f"❌ Unexpected response format for {subtopic}")
                        generated_text[subtopic] = {"title": subtopic, "content": "No content found."}
                except Exception as e:
                    st.error(f"❌ Error parsing text generation response for {subtopic}: {e}")
                    generated_text[subtopic] = {"title": subtopic, "content": "Text generation failed."}
            else:
                st.error(f"❌ Text generation failed for {subtopic}")
                generated_text[subtopic] = {"title": subtopic, "content": "Text generation failed."}

        data = {
            "main_topic": main_topic,
            "subtopics": [subtopic_1, subtopic_2],
            "generated_text": generated_text
        }

        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            st.success("✅ PPT generated successfully with images and text!")
            ppt_bytes = response.content
            ppt_filename = "generated_presentation.pptx"
            with open(ppt_filename, "wb") as f:
                f.write(ppt_bytes)
            st.download_button(
                label="📥 Download PPT",
                data=ppt_bytes,
                file_name=ppt_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.error("❌ PPT generation failed. Please check logs for more details.")

elif option == "Convert PDF to PPT":
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        st.info("⏳ Processing PDF and generating PPT...")
        files = {
            "file": (
                uploaded_file.name or "uploaded.pdf",
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }
        response = requests.post(UPLOAD_API_URL, files=files)
        if response.status_code == 200:
            st.success("✅ PPT generated successfully from PDF!")
            ppt_bytes = response.content
            ppt_filename = "converted_presentation.pptx"
            with open(ppt_filename, "wb") as f:
                f.write(ppt_bytes)
            st.download_button(
                label="📥 Download Converted PPT",
                data=ppt_bytes,
                file_name=ppt_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.error("❌ PDF to PPT conversion failed. Please check logs for more details.")
