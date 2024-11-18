import httpx
import pytest

from utils.report import generate_report
from utils.xml_utils import fetch_xml_data, parse_xml


def test_report_generation():
    try:
        xml_content = fetch_xml_data("http://localhost:8000/api/test/xml")
        date, products = parse_xml(xml_content)
        result = generate_report(products)

        assert type(result) is str
    except httpx.ConnectError:
        pytest.fail("API is not running")
