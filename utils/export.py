from io import BytesIO
from typing import List

import pandas as pd
from fpdf import FPDF

from crud.product import fetch_product
from models.order import Order


def _orders_dataframe(orders: List[Order]) -> pd.DataFrame:
    rows = []
    for o in orders:
        p = fetch_product(o.product_id) or {}
        price = p.get("price", 0)
        title = p.get("title", f"ID {o.product_id}")
        rows.append({
            "OrderID": o.id,
            "ProductID": o.product_id,
            "Title": title,
            "Quantity": o.quantity,
            "UnitPrice": price,
            "Subtotal": price * o.quantity,
        })
    return pd.DataFrame(rows)


def to_csv(orders: List[Order]) -> bytes:
    return _orders_dataframe(orders).to_csv(index=False).encode("utf-8")


def to_excel(orders: List[Order]) -> bytes:
    df = _orders_dataframe(orders)
    buf = BytesIO()
    df.to_excel(buf, index=False, sheet_name="Pedidos")
    return buf.getvalue()


def to_pdf(orders: List[Order]) -> bytes:
    df = _orders_dataframe(orders)

    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    col_w = [20, 25, 80, 25, 25, 30]
    headers = df.columns.tolist()

    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 8, h, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        pdf.cell(col_w[0], 8, str(row["OrderID"]), border=1)
        pdf.cell(col_w[1], 8, str(row["ProductID"]), border=1)
        pdf.cell(col_w[2], 8, str(row["Title"])[:40], border=1)
        pdf.cell(col_w[3], 8, str(row["Quantity"]), border=1)
        pdf.cell(col_w[4], 8, f"{row['UnitPrice']}", border=1)
        pdf.cell(col_w[5], 8, f"{row['Subtotal']}", border=1)
        pdf.ln()

    return pdf.output(dest="S").encode("latin1")
