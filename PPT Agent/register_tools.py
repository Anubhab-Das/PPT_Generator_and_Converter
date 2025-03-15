# register_tools.py
from tool_registry import ToolRegistry
from ppt_generator import PPTGeneratorTool
from image_fetcher import ImageFetcherTool
from text_generation import OpenAITextGenerationTool
from pdf_to_ppt_converter import PDFToPPTConverterTool  

def register_all_tools():
    ToolRegistry.register("ppt_generator", PPTGeneratorTool())
    ToolRegistry.register("image_fetcher", ImageFetcherTool())
    ToolRegistry.register("text_generation", OpenAITextGenerationTool())
    ToolRegistry.register("pdf_to_ppt_converter", PDFToPPTConverterTool())
    print("✅ Registered Tools:", ToolRegistry.list_tools())

if __name__ == "__main__":
    register_all_tools()
