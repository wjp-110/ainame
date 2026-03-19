from fastapi import APIRouter

from schemas.agent import NameResultSchema
from schemas.name import NameIn, NameOut
from core.agent import generate_names


router = APIRouter(prefix="/name")


@router.post("/", response_model=NameOut)
async def take_ainame(data: NameIn):
    name_result = await generate_names(data)
    return NameResultSchema(names=name_result.names)