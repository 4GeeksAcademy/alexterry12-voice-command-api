from fastapi import APIRouter

from src.app.schemas.voice import InstructionPayload, InstructionRequest
from src.app.services.groq_service import get_instruction_from_text

router = APIRouter(tags=["instruction"])


@router.post("/instruction", response_model=InstructionPayload)
def route_instruction(payload: InstructionRequest) -> InstructionPayload:
    return get_instruction_from_text(payload.transcription)