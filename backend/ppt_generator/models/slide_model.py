import uuid
from typing import List, Optional
from pydantic import BaseModel

from ppt_generator.models.other_models import SlideType
from ppt_generator.models.content_type_models import (
    CONTENT_TYPE_MAPPING,
    Type1Content,
    Type2Content,
    Type3Content,
    Type4Content,
    Type5Content,
    Type6Content,
    Type7Content,
    Type8Content,
    Type9Content,
)


class SlideModel(BaseModel):
    id: Optional[str] = None
    index: int
    type: SlideType
    design_index: Optional[int] = None
    images: Optional[List[str]] = None
    presentation: str
    content: (
        Type1Content
        | Type2Content
        | Type3Content
        | Type4Content
        | Type5Content
        | Type6Content
        | Type7Content
        | Type8Content
        | Type9Content
    )
    properties: Optional[dict] = None

    @classmethod
    def from_dict(cls, data):
        slide_model = cls(**data)
        content = data["content"]
        slide_model.content = CONTENT_TYPE_MAPPING[slide_model.type](**content)
        return slide_model

    def to_create_dict(self, auto_id: bool = False):
        temp = self.model_dump(mode="json")
        if not self.id:
            if auto_id:
                temp["id"] = str(uuid.uuid4())
            else:
                temp.pop("id")
        return temp

    @property
    def images_count(self):
        if not hasattr(self.content, "image_prompts"):
            return 0
        return len(self.content.image_prompts or [])
