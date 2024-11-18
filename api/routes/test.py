from fastapi import APIRouter, Response
from xml.etree.ElementTree import Element, SubElement, tostring


test_router = APIRouter(prefix="/test", include_in_schema=False)


@test_router.get("/xml")
async def test_fetch_xml():
    _root = Element("sales_data", date="2024-01-01")

    products = SubElement(_root, "products")

    product = SubElement(products, "product")
    SubElement(product, "id").text = "1"
    SubElement(product, "name").text = "Product A"
    SubElement(product, "quantity").text = "100"
    SubElement(product, "price").text = "1500.00"
    SubElement(product, "category").text = "Electronics"

    product2 = SubElement(products, "product")
    SubElement(product2, "id").text = "2"
    SubElement(product2, "name").text = "Product B"
    SubElement(product2, "quantity").text = "200"
    SubElement(product2, "price").text = "1000.00"
    SubElement(product2, "category").text = "Home Appliances"

    xml_str = tostring(_root, "utf-8")
    return Response(content=xml_str, media_type="application/xml")
