from http import HTTPStatus

from api.v1.queries.person import query_person
from api.v1.schemas.person import PersonDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException
from services.collection import CollectionService
from services.detail import DetailService
from utils.pagination import paginate_response
from utils.service import get_collection_service, get_detail_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=dict)
async def writer_collection(
    writers_service: CollectionService = Depends(get_collection_service),
    page: int = 1, size: int = 10
) -> dict:
    """Get writers collection with related films ordered by rating."""
    writers = await writers_service.get_items(
        query_person(
        ), PersonDetailSchema, CONFIG["ELASTIC_WRITER_INDEX"]
    )
    if not writers:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="writers not found")
    return paginate_response(writers, page, size)


@router.get("/{writer_id}", response_model=PersonDetailSchema)
async def actor_detail(
    writer_id: str, writer_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one writer with related films ordered by rating."""
    writer = await writer_service.get_item_by_id(PersonDetailSchema, CONFIG["ELASTIC_WRITER_INDEX"], writer_id)
    if not writer:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="writer not found")
    return writer
