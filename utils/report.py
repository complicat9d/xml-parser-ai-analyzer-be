import openai
import backoff
from typing import List
from celery import shared_task

from schemas.product import ProductSchema
from utils.log import logger
from config import settings

openai.api_key = settings.API_KEY


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def generate_report(products: List[ProductSchema]) -> str:
    total_revenue = sum(product.quantity * product.price for product in products)
    top_products = sorted(products, key=lambda x: x.quantity, reverse=True)[:3]
    categories = {
        category: sum(
            product.quantity for product in products if product.category == category
        )
        for category in set(product.category for product in products)
    }

    prompt = f"""
    Проанализируй данные о продажах:
    1. Общая выручка: {total_revenue}
    2. Топ-3 товара по продажам: {', '.join([p.name for p in top_products])}
    3. Распределение по категориям: {categories}
    Составь краткий аналитический отчет с выводами и рекомендациями.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-instruct",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
    except openai.RateLimitError:
        logger.warning("The limit of tokens for the given API key has been exceeded")
    except openai.NotFoundError:
        logger.warning(
            "The given model name does not exist or you do not have access to it"
        )
