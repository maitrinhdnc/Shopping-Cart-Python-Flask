from app.main.model.order import Order
from app.main import db

def update_order_status(data):
    if type(data) is dict:
        order = Order.query.filter_by(order_id = data.get("order_id")).first()
        order.payment_status = data.get('status')
        db.session.commit()
    else:
        if(len(data)>0):
            for item in data:
                order = Order.query.filter_by(order_id = item.get("order_id")).first()
                order.payment_status = item.get('status')
                db.session.commit()
   