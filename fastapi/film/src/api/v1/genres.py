from http import HTTPStatus

from api.v1.queries.genre import query_genre
from api.v1.schemas.genre import GenreDetailSchema
from core.config import Settings
from fastapi import APIRouter, Depends, HTTPException
from services.collection import CollectionService
from services.detail import DetailService
from utils.pagination import paginate_response
from utils.service import get_collection_service, get_detail_service

CONFIG = Settings().dict()

router = APIRouter()


@router.get("/", response_model=dict)
async def genres_collection(
    genres_service: CollectionService = Depends(get_collection_service),
    page: int = 1, size: int = 10
) -> dict:
    """Get genre collection with related films ordered by rating."""
    genres = await genres_service.get_items(
        query_genre(
        ), GenreDetailSchema, CONFIG["ELASTIC_GENRE_INDEX"]
    )
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genres not found")
    return paginate_response(genres, page, size)


@router.get("/{genre_id}", response_model=GenreDetailSchema)
async def genres_detail(
    genre_id: str, genres_service: DetailService = Depends(get_detail_service)
) -> GenreDetailSchema:
    """Get one genre with related films ordered by rating."""
    genre = await genres_service.get_item_by_id(GenreDetailSchema, CONFIG["ELASTIC_GENRE_INDEX"], genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="genre not found")
    return genre
