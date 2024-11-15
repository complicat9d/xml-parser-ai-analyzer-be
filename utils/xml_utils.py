import httpx
import asyncio
import xml.etree.ElementTree as ET
from pydantic import ValidationError
from typing import List, Tuple
from datetime import datetime


from schemas.product import ProductSchema
from utils.log import logger
from config import settings


def parse_xml(filename: str) -> Tuple[datetime, List[ProductSchema]]:
    tree = ET.parse(filename)
    root = tree.getroot()

    date_str = root.attrib["date"]
    date = datetime.strptime(date_str, "%Y-%m-%d")

    products = root.find("products")

    product_schemas = []
    for product in products.findall("product"):
        product_id = int(product.find("id").text)

        try:
            product_data = ProductSchema(
                product_id=product_id,
                name=product.find("name").text,
                quantity=int(product.find("quantity").text),
                price=float(product.find("price").text),
                category=product.find("category").text,
            )
            product_schemas.append(product_data)
        except ValidationError as e:
            logger.error(f"Validation error for product {product_id}: {e}")

    return date, product_schemas


def fetch_xml_data() -> str:
    with httpx.Client() as client:
        response = client.get(settings.XML_URL)
        response.raise_for_status()
        return response.text
