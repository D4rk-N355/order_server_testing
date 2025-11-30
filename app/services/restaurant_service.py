from sqlalchemy import create_engine, MetaData, Table, select
import json

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@0.tcp.jp.ngrok.io:17180/e-system-delivery?charset=utf8mb4"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
metadata = MetaData()
restaurant_table = Table('restaurants', metadata, autoload_with=engine)

def get_restaurant_list():
    """
    取得所有店家清單 (JSON)
    """
    with engine.connect() as conn:
        stmt = select(restaurant_table)
        result = conn.execute(stmt).mappings().all()
        return json.dumps([dict(row) for row in result], ensure_ascii=False)

def get_restaurant_by_id(restaurant_id):
    """
    取得指定店家資訊 (JSON)
    """
    with engine.connect() as conn:
        stmt = select(restaurant_table).where(restaurant_table.c.id == restaurant_id)
        result = conn.execute(stmt).mappings().fetchone()
        if result:
            return json.dumps(dict(result), ensure_ascii=False)
        else:
            return json.dumps({"error": "商家不存在"}, ensure_ascii=False)