from pydantic import BaseModel
from typing import List

class PPTRequest(BaseModel):
    main_topic: str
    subtopics: List[str]
