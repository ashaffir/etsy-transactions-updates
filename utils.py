"""
1) Loading a CSV file with the details of the invoices that are updated
2) Accessing Etsy API to make updates

Notes:
- Throttling the API requests to avoid Etsy limit
"""
import time
import requests
import csv
from config import (
    ETSY_SHOP_ID,
)


def update_transactions(csv_file, headers):

    with open(csv_file, "r") as f:
        transactions = []
        lines = csv.reader(f)
        header = next(f)

        for line in lines:
            if line != header:

                receipt_id = line[0]
                courier_name = line[1]
                tracking_number = line[2]
                request_url = f"https://api.etsy.com/v3/application/shops/{ETSY_SHOP_ID}/receipts/{receipt_id}/tracking"
                payload = {
                    "tracking_code": f"{tracking_number}",
                    "carrier_name": f"{courier_name}",
                }

                print(f"Updating: {receipt_id=} | {courier_name=} | {tracking_number=}")

                response = requests.post(request_url, data=payload, headers=headers)
                if response.ok:
                    transactions.append({"receipt": receipt_id, "status": "ok"})
                else:
                    transactions.append({"receipt": receipt_id, "status": "fail"})
                time.sleep(0.5)

        return {"ok": "success", "content": transactions}
