import requests
import os
import io
from PIL import Image
from config import Config
from base_tool import BaseTool
from tool_registry import ToolRegistry

class ImageFetcherTool(BaseTool):
    """
    Fetches an image from SerpAPI and converts it to JPEG.
    """

    def run(self, topic):
        # Always store the final image as .jpeg
        image_path = os.path.join(
            Config.ASSETS_PATH, f"{topic.lower().replace(' ', '_')}.jpeg"
        )

        # ✅ Return existing image if found
        if os.path.exists(image_path):
            print(f"✅ Using cached image for {topic}")
            return image_path  

        # Query SerpAPI for images
        url = (
            f"https://serpapi.com/search?engine=google_images&q={topic}"
            f"&api_key={Config.SERP_API_KEY}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            print(f"⚠️ SerpAPI Error {response.status_code}: {response.text}")
            return None

        try:
            # Get the first image's original URL
            image_url = response.json()["images_results"][0]["original"]
            img_data = requests.get(image_url).content

            # Convert whatever format we get into JPEG
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            img.save(image_path, "JPEG")

            print(f"✅ Image saved: {image_path}")
            return image_path
        except Exception as e:
            print(f"❌ Image Fetch Failed: {e}")
            return None

# Register the tool
ToolRegistry.register("image_fetcher", ImageFetcherTool())
print("✅ image_fetcher tool registered successfully.")
