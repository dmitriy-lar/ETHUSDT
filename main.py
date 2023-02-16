import asyncio
from aiohttp import ClientSession
import datetime

URL = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-product-by-symbol?symbol=ETHUSDT"


async def get_current_price() -> str:
    async with ClientSession() as session:
        async with session.get(url=URL) as response:
            price = await response.json()
            return price["data"]["c"]


def make_prediction(price: float) -> None:
    top_level = 1717
    if price <= top_level:
        print("Можно продавать")
    else:
        print("Можно покупать")

    if price > 1717:
        print("Можно покупать")


async def main():
    count = 0
    start_price = await get_current_price()
    start_time = datetime.datetime.now()

    while True:
        count += 1

        task = asyncio.create_task(get_current_price())
        price = await task
        print(f"Текущая цена ETHUSDT - {price}")

        current_time = datetime.datetime.now()

        if current_time < (start_time + datetime.timedelta(minutes=60)):
            if abs((float(start_price) - float(price)) / float(start_price) * 100) >= 1:
                print(
                    f"За последние 60 минут цена изменилась на 1%, текущая цена {price}"
                )
                start_price = price
        else:
            start_time = current_time

        if count % 10 == 0:
            make_prediction(float(price))


if __name__ == "__main__":
    asyncio.run(main())
