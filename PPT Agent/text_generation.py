import json
import logging
import re
from config import Config
from base_tool import BaseTool
from tool_registry import ToolRegistry
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=Config.OPENAI_API_KEY)

class OpenAITextGenerationTool(BaseTool):
    def run(self, topic):
        logging.info(f"🔍 Generating text for topic: {topic}")

        prompt = f"""
You are a PowerPoint presentation specialist. Your task is to generate structured slide content for the topic: "{topic}".

Generate **exactly** three slides, each in JSON format. Each slide must contain:
1. **"title"** - A concise slide title.
2. **"content"** - A short, informative sentence (max 30 words).
3. **"image_query"** - A term for fetching a representative image (if omitted, default to the slide title).

Return only a **valid JSON array** following this structure:
[
    {{"title": "Slide 1 Title", "content": "Slide 1 content", "image_query": "Query 1"}},
    {{"title": "Slide 2 Title", "content": "Slide 2 content", "image_query": "Query 2"}},
    {{"title": "Slide 3 Title", "content": "Slide 3 content", "image_query": "Query 3"}}
]

Ensure:
- No markdown formatting (e.g., no triple backticks).
- No additional commentary.
- Response is fully enclosed in square brackets.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )

            text_response = response.choices[0].message.content.strip()
            logging.info(f"DEBUG: Raw text response: {text_response}")

            # Remove markdown formatting if present
            if text_response.startswith("```"):
                text_response = re.sub(r"```(\w+)?", "", text_response).strip()

            # Fix JSON closing issues
            text_response = re.sub(r",\s*\]", "]", text_response)
            if not text_response.endswith("]"):
                text_response += "]"

            try:
                generated_raw = json.loads(text_response)
            except json.JSONDecodeError:
                logging.error(f"❌ JSON Decode Error: {text_response}")
                return {"data": [{"title": topic, "content": "Text generation failed.", "image_query": topic}]}

            logging.info(f"DEBUG: Parsed JSON structure: {generated_raw}")

            result = []
            if isinstance(generated_raw, list):
                for entry in generated_raw:
                    if isinstance(entry, dict):
                        slide_title = entry.get("title", "Untitled Slide")
                        slide_content = entry.get("content", "No content available.")
                        image_query = entry.get("image_query", slide_title)
                        result.append({"title": slide_title, "content": slide_content, "image_query": image_query})
            else:
                logging.error("❌ Unexpected JSON format from OpenAI.") 
                return {"error": "Invalid JSON structure from OpenAI response"}

            return {"data": result}

        except Exception as e:
            logging.error("Exception in text generation: %s", e, exc_info=True)
            return {"error": f"Text generation failed: {e}"}

ToolRegistry.register("text_generation", OpenAITextGenerationTool())
logging.info("✅ text_generation tool registered successfully.")
