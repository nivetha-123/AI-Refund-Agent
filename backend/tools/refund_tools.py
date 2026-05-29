import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.database import get_conn

POLICY_PATH = os.getenv("POLICY_PATH", "/app/data/refund_policy.txt")


# ── Tool 1: lookup_customer ──────────────────────────────────
def lookup_customer(email: str) -> dict:
    """Look up a customer by email address."""
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM customers WHERE LOWER(email) = LOWER(?)",
            (email.strip(),)
        ).fetchone()
        if not row:
            return {"found": False, "message": f"No customer found: {email}"}
        return {
            "found": True,
            "customer": {
                "id": row["id"],
                "email": row["email"],
                "name": row["name"],
                "account_tier": row["account_tier"],
                "joined_date": row["joined_date"],
                "total_orders": row["total_orders"],
                "lifetime_value": row["lifetime_value"],
            }
        }
    finally:
        conn.close()


# ── Tool 2: lookup_order ─────────────────────────────────────
def lookup_order(order_id: str) -> dict:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM orders WHERE UPPER(order_id) = UPPER(?)",
            (order_id.strip(),)
        ).fetchone()
        if not row:
            return {"found": False, "message": f"No order found: {order_id}"}

        days_since = None
        within_window = None
        if row["delivery_date"]:
            delivery = datetime.strptime(row["delivery_date"], "%Y-%m-%d").date()
            days_since = (date.today() - delivery).days
            within_window = days_since <= 30

        return {
            "found": True,
            "order": {
                "order_id": row["order_id"],
                "customer_email": row["customer_email"],
                "product_name": row["product_name"],
                "product_category": row["product_category"],
                "amount": row["amount"],
                "order_date": row["order_date"],
                "delivery_date": row["delivery_date"],
                "status": row["status"],
                "is_final_sale": bool(row["is_final_sale"]),
                "is_digital": bool(row["is_digital"]),
                "payment_method": row["payment_method"],
                "days_since_delivery": days_since,
                "within_30_day_window": within_window,
            }
        }
    finally:
        conn.close()


# ── Tool 3: check_refund_history ─────────────────────────────
def check_refund_history(customer_email: str) -> dict:
    """Check refund requests in last 90 days for fraud detection."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """SELECT * FROM refund_requests
               WHERE LOWER(customer_email) = LOWER(?)
               AND requested_at >= date('now','-90 days')
               ORDER BY requested_at DESC""",
            (customer_email.strip(),)
        ).fetchall()
        return {
            "customer_email": customer_email,
            "recent_requests_90_days": len(rows),
            "fraud_flag": len(rows) >= 3,
            "history": [
                {"request_id": r["request_id"], "order_id": r["order_id"],
                 "status": r["status"], "requested_at": r["requested_at"]}
                for r in rows
            ]
        }
    finally:
        conn.close()


# ── Tool 4: get_policy ───────────────────────────────────────
def get_policy(section: str = "all") -> dict:
    """Retrieve the refund policy document or a specific section."""
    policy_file = POLICY_PATH
    if not os.path.exists(policy_file):
        policy_file = os.path.join(
            os.path.dirname(__file__), "../../data/refund_policy.txt"
        )
    try:
        with open(policy_file, "r") as f:
            full_text = f.read()
    except FileNotFoundError:
        return {"error": "Policy document not found."}

    if section.lower() == "all":
        return {"policy": full_text}

    lines = full_text.split("\n")
    relevant = []
    capture = False
    for line in lines:
        if section.upper() in line.upper():
            capture = True
        if capture:
            relevant.append(line)
            if len(relevant) > 30:
                break

    if relevant:
        return {"section_query": section, "policy_excerpt": "\n".join(relevant)}
    return {"policy": full_text, "note": f"Section '{section}' not found, returning full policy."}


# ── Claude tool definitions ──────────────────────────────────
TOOL_DEFINITIONS = [
    {
        "name": "lookup_customer",
        "description": "Look up a customer profile by email address. Returns account tier, join date, and order history. Always call this first to verify the customer exists.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Customer email address"}
            },
            "required": ["email"]
        }
    },
    {
        "name": "lookup_order",
        "description": "Look up an order by order ID. Returns product details, amount, delivery date, final_sale flag, digital flag, and whether within 30-day return window.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order ID e.g. ORD-10001"}
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "check_refund_history",
        "description": "Check how many refund requests a customer made in the last 90 days. Returns fraud_flag=true if 3 or more requests.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_email": {"type": "string", "description": "Customer email"}
            },
            "required": ["customer_email"]
        }
    },
    {
        "name": "get_policy",
        "description": "Retrieve the refund policy document. Pass a keyword like 'FINAL SALE', 'DIGITAL', 'ESCALATION' to get a specific section, or 'all' for the full document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "description": "Keyword to search in policy, or 'all'",
                    "default": "all"
                }
            },
            "required": []
        }
    }
]

TOOL_MAP = {
    "lookup_customer": lookup_customer,
    "lookup_order": lookup_order,
    "check_refund_history": check_refund_history,
    "get_policy": get_policy,
}
