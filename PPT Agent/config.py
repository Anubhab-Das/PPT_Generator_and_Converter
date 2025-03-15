import os

class Config:
    
    SERP_API_KEY = "key"
    
    OPENAI_API_KEY= "key"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_PATH = os.path.join(BASE_DIR, "output")
    ASSETS_PATH = os.path.join(BASE_DIR, "assets")
    TEMPLATE_PATH = os.path.join(BASE_DIR, "templates/basic_template.pptx")

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    os.makedirs(ASSETS_PATH, exist_ok=True)
