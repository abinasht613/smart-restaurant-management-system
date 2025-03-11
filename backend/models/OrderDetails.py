from backend.extensions import db

# Order Details (Links Orders with ItemDetails)
class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    item_detail_id = db.Column(db.Integer, db.ForeignKey("item_details.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sub_tot = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", backref="order_details")
    item_detail = db.relationship("ItemDetails", backref="order_details")