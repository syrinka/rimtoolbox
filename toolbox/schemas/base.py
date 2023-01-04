from typing import Optional as opt
from pydantic import BaseModel, Field


class ThingDefsMixin(BaseModel):
    defName: opt[str]
    abstract: opt[bool] = Field(alias='@Abstract')
    abstractName: str

    thingClass: str
