import hashlib
import cachetools
import openai
import backoff
from typing import List

from schemas.product import ProductSchema
from utils.log import logger
from config import settings

openai.api_key = settings.API_KEY

report_cache = cachetools.TTLCache(maxsize=100, ttl=3600)


@backoff.on_exception(backoff.expo, openai.RateLimitError)
def generate_report(products: List[ProductSchema]) -> str:
    product_hash = hashlib.sha256(str(products).encode("utf-8")).hexdigest()
    logger.debug("Hash for the given products: {}".format(product_hash))
    if product_hash in report_cache:
        logger.info("Using cached OpenAI API response")
        return report_cache[product_hash]

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

        report_content = response.choices[0].message.content
        report_cache[product_hash] = report_content

        return report_content

    except openai.RateLimitError:
        logger.warning(
            "The limit of tokens for the given API key has been exceeded, report has not been added"
        )
    except openai.NotFoundError:
        logger.warning(
            "The given model name does not exist or you do not have access to it"
        )
    except Exception as e:
        logger.error(f"Error while generating report: {e}")
