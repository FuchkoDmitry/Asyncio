import asyncio
import time

import aiohttp
import asyncpg
import more_itertools
from decouple import config


BASE_URI = 'https://swapi.dev/api/people/'
PERSON_COUNT = 82


async def get_details(urls_list, key, session):
    titles = set()
    for title in urls_list:
        async with session.get(title) as response:
            json_data = await response.json()
            titles.add(json_data[key].replace("'", ''))
            return ','.join(titles)


async def get_homeworld(url, session):
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data['name']


async def get_character(character_id, session):
    async with session.get(f'{BASE_URI}{character_id}') as response:
        json_data = await response.json()
        if json_data.get('detail', None) is not None:
            return None
        json_data['films'] = await get_details(json_data['films'], 'title', session)
        json_data['species'] = await get_details(json_data['species'], 'name', session)
        json_data['starships'] = await get_details(json_data['starships'], 'name', session)
        json_data['vehicles'] = await get_details(json_data['vehicles'], 'name', session)
        json_data['homeworld'] = await get_homeworld(json_data['homeworld'], session)
        json_data['id'] = character_id
        del json_data['created'], json_data['edited'], json_data['url']
        return json_data


async def get_people():
    async with aiohttp.ClientSession() as session:
        character_coroutine_generator = (
            get_character(i, session) for i in range(1, PERSON_COUNT + 1)
        )
        for character_coroutine_chunk in more_itertools.chunked(
                character_coroutine_generator, 10):
            result = await asyncio.gather(*character_coroutine_chunk)
            await insert_to_db(result)


async def prepare_to_db(data):
    values = []
    for value in data.values():
        if value is None:
            value = 'N/A'
        values.append(value)
    return tuple(values)


async def insert_to_db(result):
    dp_pool = await asyncpg.create_pool(config('PG_DSN'))
    tasks = []
    for data in result:
        if data is None:
            continue
        prepared_data = asyncio.create_task(prepare_to_db(data))
        tasks.append(prepared_data)
    result = await asyncio.gather(*tasks)

    query = f"INSERT INTO characters (name, height, mass, hair_color," \
            f" skin_color, eye_color, birth_year, gender, homeworld, films," \
            f" species, vehicles, starships, id) " \
            f"VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)"
    async with dp_pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, result)
    await dp_pool.close()


if __name__ == "__main__":
    start = time.time()
    asyncio.run(get_people())
    print(time.time() - start)
