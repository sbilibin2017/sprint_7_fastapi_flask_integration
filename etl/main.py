import asyncio
import time

from settings import settings
from src.extract import extract
from src.load import load
from src.transform import transform
from utils.db_connections import close_connections, get_film_total_count, setup_connections
from utils.logger import logger


async def main():

    postgres_cur, es_cur, redis_conn, state = await setup_connections()
    film_total_count = await get_film_total_count(postgres_cur)
    film_state = await state.get_state(settings.REDIS_FILM_STATE)
    film_current_count = len(film_state)

    try:
        if film_current_count != film_total_count:
            df, df_fwg, df_fwp, new_ids = await extract(postgres_cur, film_state)
            data_film, data_genre, data_actor, data_writer, data_director = await transform(df, df_fwg, df_fwp)
            await load(data_film, data_genre, data_actor, data_writer, data_director, new_ids, es_cur, state)
            logger.info(
                f'Done: film_current_count={film_current_count}, film_total_count={film_total_count}')
            return film_current_count, film_total_count
        else:
            logger.info('Done: no new ids')
            return film_current_count, film_total_count
    except Exception as error:
        logger.error(error)
        return film_current_count, film_total_count
    # close postgres connection
    finally:
        await close_connections(postgres_cur, es_cur)
        logger.info("Closing postgres connection ...")
        return film_current_count, film_total_count

if __name__ == "__main__":
    ITER = 1
    while True:
        film_current_count, film_total_count = asyncio.run(main())
        logger.info(
            f"ITERATION {ITER}: film_current_count={film_current_count}, film_total_count={film_total_count}")
        ITER += 1
        time.sleep(settings.SLEEP)
