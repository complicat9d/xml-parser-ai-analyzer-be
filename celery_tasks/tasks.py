from celery import shared_task

from database.session import sync_session
from utils.xml_utils import fetch_xml_data, parse_xml
from utils.db.sale import create_sale, add_report
from utils.db.product import save_products
from utils.report import generate_report
from config import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    name="data:fetch",
)
def fetch_and_process_sales_data(self):  # noqa
    xml_content = fetch_xml_data(settings.XML_URL)
    date, products = parse_xml(xml_content)
    with sync_session() as session:
        sale_id = create_sale(date, session)
        save_products(products, sale_id, session)
        report = generate_report(products)
        add_report(sale_id, report, session)
