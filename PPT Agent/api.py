from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import os
import logging
from tool_registry import ToolRegistry
from register_tools import register_all_tools
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

# Register tools (this must happen after all tool classes are defined)
register_all_tools()

app = FastAPI()

class GenerateTextRequest(BaseModel):
    topic: str

@app.post("/generate_text/")
def generate_text(request_data: GenerateTextRequest):
    topic = request_data.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    text_tool = ToolRegistry.get_tool("text_generation")
    if not text_tool:
        raise HTTPException(status_code=500, detail="Text generation tool not found.")
    
    generated_text = text_tool.run(topic)
    if not generated_text or "error" in generated_text:
        logging.error(f"🚨 Text generation failed for {topic}: {generated_text.get('error', 'Unknown Error')}")
        return {"data": [{"title": topic, "content": "Text generation failed."}]}

    if not generated_text.get("data"):
        logging.warning(f"⚠️ No content found for {topic}. Returning fallback response.")
        return {"data": [{"title": topic, "content": "No content found."}]}

    return generated_text  # ✅ Now properly returns a dictionary with "data" as a list

@app.post("/generate_ppt/")
def generate_ppt(request_data: dict):
    main_topic = request_data.get("main_topic")
    subtopics = request_data.get("subtopics", [])
    generated_text = request_data.get("generated_text", {})

    if not main_topic or not subtopics:
        raise HTTPException(status_code=400, detail="Main topic and subtopics are required.")

    ppt_generator = ToolRegistry.get_tool("ppt_generator")
    ppt_path = ppt_generator.run(main_topic, subtopics, generated_text)
    if ppt_path is None or not os.path.exists(ppt_path):
        raise HTTPException(status_code=500, detail="PPT generation failed.")
    
    return FileResponse(
        ppt_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="generated_presentation.pptx"
    )

@app.post("/upload_pdf/")
def upload_pdf(file: UploadFile = File(...)):
    """
    Handles PDF upload and converts it into a structured PPT.
    """
    pdf_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(pdf_path, "wb") as f:
        f.write(file.file.read())

    logging.info(f"📥 PDF received: {pdf_path}")

    pdf_converter = ToolRegistry.get_tool("pdf_to_ppt_converter")
    if not pdf_converter:
        raise HTTPException(status_code=500, detail="PDF to PPT converter tool not found.")

    ppt_path = pdf_converter.run(pdf_path)
    if ppt_path is None or not os.path.exists(ppt_path):
        raise HTTPException(status_code=500, detail="PDF to PPT conversion failed.")

    return FileResponse(
        ppt_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=os.path.basename(ppt_path)
    )

print("✅ API is running!")
