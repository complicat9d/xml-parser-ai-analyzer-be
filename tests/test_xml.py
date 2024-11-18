import httpx
import pytest
from datetime import datetime

from utils.xml_utils import parse_xml, fetch_xml_data


def test_data_fetch():
    try:
        xml_content = fetch_xml_data("http://localhost:8000/api/test/xml")
        date, products = parse_xml(xml_content)
        sample_1 = products[0]
        sample_2 = products[1]
        assert date == datetime.strptime("2024-01-01", "%Y-%m-%d")
        assert (
            sample_1.product_id,
            sample_1.name,
            sample_1.quantity,
            sample_1.price,
            sample_1.category,
        ) == (1, "Product A", 100, 1500.0, "Electronics")
        assert (
            sample_2.product_id,
            sample_2.name,
            sample_2.quantity,
            sample_2.price,
            sample_2.category,
        ) == (2, "Product B", 200, 1000.0, "Home Appliances")
    except httpx.ConnectError:
        pytest.fail("API is not running")
