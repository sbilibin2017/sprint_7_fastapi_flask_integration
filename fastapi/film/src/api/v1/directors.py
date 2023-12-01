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
async def director_collection(
    directors_service: CollectionService = Depends(get_collection_service),
    page: int = 1, size: int = 10
) -> dict:
    """Get directors collection with related films ordered by rating."""
    directors = await directors_service.get_items(
        query_person(
        ), PersonDetailSchema, CONFIG["ELASTIC_DIRECTOR_INDEX"]
    )
    if not directors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="directors not found")
    return paginate_response(directors, page, size)


@router.get("/{director_id}", response_model=PersonDetailSchema)
async def director_detail(
    director_id: str, director_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one director with related films ordered by rating."""
    director = await director_service.get_item_by_id(
        PersonDetailSchema, CONFIG["ELASTIC_DIRECTOR_INDEX"], director_id
    )
    if not director:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="director not found")
    return director
