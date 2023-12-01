import math


def paginate_response(films: list, page: int, size: int) -> dict:
    offset_min = page * size
    offset_max = (page + 1) * size
    response = {}
    response['data'] = films[offset_min:offset_max]
    response['page'] = page
    response['size'] = size
    response['total_pages'] = math.ceil(len(films) / size) - 1,
    response['total_records'] = len(films)
    return response
