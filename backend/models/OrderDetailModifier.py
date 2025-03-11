from backend.extensions import db


class OrderDetailModifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_detail_id = db.Column(db.Integer, db.ForeignKey("order_details.id"), nullable=False)
    modifier_id = db.Column(db.Integer, db.ForeignKey("modifier.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order_detail = db.relationship("OrderDetails", backref="modifiers")
    modifier = db.relationship("Modifier", backref="modifiers")