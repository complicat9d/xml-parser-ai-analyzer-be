import asyncio

import openai
from typing import List

from schemas.product import ProductSchema
from config import settings

openai.api_key = settings.OPEN_API_KEY


def generate_report(sales: List[ProductSchema]) -> str:
    total_revenue = sum(product.quantity * product.price for product in sales)
    top_products = sorted(sales, key=lambda x: x.quantity, reverse=True)[:3]
    categories = {
        category: sum(
            product.quantity for product in sales if product.category == category
        )
        for category in set(product.category for product in sales)
    }

    prompt = f"""
    Проанализируй данные о продажах:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {', '.join([p.name for p in top_products])}
    3. Распределение по категориям: {categories}
    Составь краткий аналитический отчет с выводами и рекомендациями.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    return response["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":

    async def main():
        print(await generate_report([]))

    asyncio.run(main())
