from typing import Dict, TypedDict
from pydantic import BaseSettings, Field

class ErrorDetail(TypedDict):
    message_code: int
    message: str

class Settings(BaseSettings):
    ERROR_CODES: Dict[str, ErrorDetail] = Field(default_factory=lambda: {
        "UNKNOWN_SOURCE": {
            "message_code": 1001,
            "message": "Content is empty or invalid"
        },
        "PREPROCESSING_FAILED": {
            "message_code": 1002,
            "message": "Preprocessing failed"
        },
        "EMPTY_CONTENT": {
            "message_code": 1003,
            "message": "Content is empty"
        }
    })
