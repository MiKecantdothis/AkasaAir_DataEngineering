import pandas as pd
import os
import re
import xml.etree.ElementTree as ET

class Transform:
    def normalize_mobile(mobile):
        if pd.isna(mobile):
            return None
        digits = re.sub(r"\\D+", "", str(mobile))
        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]
        if len(digits) > 10 and digits.startswith("0"):
            digits = digits.lstrip("0")
        return digits

class Extract:

    def read_customers_csv(path):
        df = pd.read_csv(path, dtype=str)
        df["mobile_number"] = df["mobile_number"].apply(Transform.normalize_mobile)
        df["ingested_at"] = pd.Timestamp.utcnow()
        df = df.drop_duplicates(subset=["mobile_number"], keep='last')

        return df


    def read_orders_xml(path):
        tree = ET.parse(path)
        root = tree.getroot()
        records = []
        for order in root.findall(".//order"):
            records.append({
            "order_id": order.findtext("order_id"),
            "mobile_number": Transform.normalize_mobile(order.findtext("mobile_number")),
            "order_date_time": order.findtext("order_date_time"),
            "sku_id": order.findtext("sku_id"),
            "sku_count": int(order.findtext("sku_count") or 1),
            "total_amount": float(order.findtext("total_amount") or 0),
            "ingested_at": pd.Timestamp.utcnow(),
        })
        df = pd.DataFrame(records)
        df["order_date_time"] = pd.to_datetime(df["order_date_time"], utc=True, errors="coerce")
        df = df.drop_duplicates(subset=["order_id"], keep='last')
        return df
