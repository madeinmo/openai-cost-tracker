import asyncio
from openai import AsyncClient
import httpx
from openai_cost_tracker import AsyncCostEstimator
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROXY = os.getenv("OPENAI_PROXY")

client = AsyncClient(
    api_key=OPENAI_API_KEY,
    http_client=httpx.AsyncClient(
        proxy=OPENAI_PROXY
    ),
)

async def generate():
    r = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Привет! Сосчитай 2+2."}],
        )
    return r
    
async def main():
    global client

    async with AsyncCostEstimator(client) as client:
        r = await generate()
        r = await generate()
    
    print(type(client))
    
        # print(r)
        # Streaming через Responses API
        # async with (await c.responses.stream(
        #     model="gpt-4o-mini",
        #     input=[{"role": "user", "content": "Напиши 3 факта о банках."}],
        # )) as stream:
        #     async for event in stream:
        #         # ваш обычный разбор и вывод chunk’ов
        #         pass
        #     # вызов get_final_response() внутри __aexit__ уже словит usage,
        #     # но вы можете и явно:
        #     final = await stream.get_final_response()

    # По выходу из контекста в stdout будет сводка по стоимости.
    # Пример:
    # === OpenAI Cost Summary ===
    # Total cost: $0.0012
    # Tokens: in=123  out=456  total=579
    # By model:
    #   - gpt-4o-mini: $0.0012  (in=123, out=456, total=579)

asyncio.run(main())
