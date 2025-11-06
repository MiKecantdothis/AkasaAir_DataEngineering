import os
import pandas as pd
import xml.etree.ElementTree as ET
import re
from datetime import datetime




from Extract_Transform import Extract
from Load import Load

loader = Load()

def run_pipeline(customer_csv, orders_xml):
    customers = Extract.read_customers_csv(customer_csv)
    orders = Extract.read_orders_xml(orders_xml)
    loader.chunk_upload("customers", customers)
    loader.chunk_upload("orders", orders)
    print("✅ Data uploaded successfully to Supabase.")


if __name__ == "__main__":
    run_pipeline("task_DE_new_customers.csv", "task_DE_new_orders.xml")

