from tool_registry import ToolRegistry
from langgraph.graph import StateGraph
from pydantic import BaseModel

if not ToolRegistry.get_tool("text_generation") or not ToolRegistry.get_tool("ppt_generator"):
    raise ValueError("Error: Required tools are not found in ToolRegistry!")

class PipelineState(BaseModel):
    main_topic: str
    subtopics: list
    generated_text: dict = {}

def generate_text_node(state: PipelineState):
    print(f"Generating text for topic: {state.main_topic}")
    
    text_tool = ToolRegistry.get_tool("text_generation")
    generated_text = text_tool.run(state.main_topic)
    
    print("Generated text:", generated_text)  
    
    return {"generated_text": generated_text}



def generate_ppt_node(state: PipelineState):
    print(f"Generating PPT for topic: {state.main_topic} with subtopics: {state.subtopics}")
    ppt_tool = ToolRegistry.get_tool("ppt_generator")
    ppt_path = ppt_tool.run(state.main_topic, state.subtopics, state.generated_text)
    return {"ppt_path": ppt_path}

def create_pipeline():
    workflow = StateGraph(state_schema=PipelineState)
    workflow.add_node("generate_text", generate_text_node)
    workflow.add_node("generate_ppt", generate_ppt_node)
    workflow.add_edge("generate_text", "generate_ppt")
    workflow.set_entry_point("generate_text")
    return workflow.compile()
