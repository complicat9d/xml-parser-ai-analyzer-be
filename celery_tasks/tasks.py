import asyncio
from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession

from utils.xml_utils import fetch_xml_data, parse_xml
from utils.db.sale import create_sale, add_report
from utils.db.product import save_products
from utils.report import generate_report


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    name="data:fetch",
)
def fetch_and_process_sales_data(self):
    loop = asyncio.get_event_loop()
    xml_content = fetch_xml_data()
    date, products = parse_xml(xml_content)
    sale_id = loop.run_until_complete(create_sale(date))
    loop.run_until_complete(save_products(products, sale_id))

    report = generate_report(products)

    loop.run_until_complete(add_report(sale_id, report))
