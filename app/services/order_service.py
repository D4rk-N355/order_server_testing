from sqlalchemy import create_engine, MetaData, Table, insert, select, update
from sqlalchemy.orm import Session
from datetime import datetime

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@0.tcp.jp.ngrok.io:17180/e-system-delivery?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
metadata = MetaData()

# 建議表名改成 orders / order_items
orders_table = Table('orders', metadata, autoload_with=engine)
order_items_table = Table('order_items', metadata, autoload_with=engine)

def calculate_total(data):
    """計算訂單總金額"""
    total = 0
    for item in data.get('items', []):
        total += item.get('price', 0) * item.get('quantity', 1)
    return total

def save_order_to_db(data):
    """儲存訂單資料到資料庫，回傳訂單編號"""
    with Session(engine) as session:
        try:
            # 建立訂單主表
            stmt = insert(orders_table).values(
                restaurant_id=data["restaurant_id"],
                table_id=data.get("table_id"),
                note=data.get("note", ""),
                status="pending",
                total_amount=calculate_total(data),
                payment_method=data.get("payment_method", "credit_card"),
                payment_status="unpaid",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            result = session.execute(stmt)
            order_id = result.inserted_primary_key[0]

            # 建立訂單明細
            for item in data.get("items", []):
                item_stmt = insert(order_items_table).values(
                    order_id=order_id,
                    dish_id=item["dish_id"],
                    name=item.get("name"),
                    quantity=item.get("quantity", 1),
                    price=item.get("price", 0)
                )
                session.execute(item_stmt)

            session.commit()
            return order_id
        except Exception as e:
            session.rollback()
            raise e

def get_order_by_id(order_id):
    """查詢訂單主表與明細"""
    with engine.connect() as conn:
        stmt = select(orders_table).where(orders_table.c.order_id == order_id)
        order = conn.execute(stmt).mappings().first()
        if not order:
            return None

        item_stmt = select(order_items_table).where(order_items_table.c.order_id == order_id)
        items = conn.execute(item_stmt).mappings().all()

        return {
            "order_id": order["order_id"],
            "restaurant_id": order["restaurant_id"],
            "table_id": order["table_id"],
            "note": order["note"],
            "status": order["status"],
            "created_at": order["created_at"].isoformat(),
            "updated_at": order["updated_at"].isoformat(),
            "total_amount": float(order["total_amount"]),
            "payment": {
                "method": order["payment_method"],
                "status": order["payment_status"]
            },
            "items": [
                {
                    "dish_id": item["dish_id"],
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": float(item["price"])
                }
                for item in items
            ]
        }

def update_order_status_in_db(order_id, new_status):
    """更新訂單狀態"""
    with Session(engine) as session:
        try:
            stmt = update(orders_table).where(
                orders_table.c.order_id == order_id
            ).values(
                status=new_status,
                updated_at=datetime.now()
            )
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
        except Exception as e:
            session.rollback()
            raise e

def cancel_order_in_db(order_id):
    """取消訂單"""
    return update_order_status_in_db(order_id, "cancelled")

def notify_payment_system(order_id, data):
    """模擬通知支付系統"""
    print(f"通知支付系統：訂單 {order_id} 金額 {calculate_total(data)}")

def notify_restaurant(order_id, data):
    """模擬通知餐廳"""
    print(f"通知商家：新訂單 {order_id}，請準備餐點")