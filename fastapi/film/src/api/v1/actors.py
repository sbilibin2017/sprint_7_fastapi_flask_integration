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
async def actor_collection(
    actors_service: CollectionService = Depends(get_collection_service),
    page: int = 1, size: int = 10
) -> dict:
    """Get actors collection with related films ordered by rating."""
    actors = await actors_service.get_items(
        query_person(
        ), PersonDetailSchema, CONFIG["ELASTIC_ACTOR_INDEX"]
    )
    if not actors:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="actors not found")
    return paginate_response(actors, page, size)


@router.get("/{actor_id}", response_model=PersonDetailSchema)
async def actor_detail(
    actor_id: str, actor_service: DetailService = Depends(get_detail_service)
) -> PersonDetailSchema:
    """Get one actor with related films ordered by rating."""
    actor = await actor_service.get_item_by_id(PersonDetailSchema, CONFIG["ELASTIC_ACTOR_INDEX"], actor_id)
    if not actor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="actor not found")
    return actor
