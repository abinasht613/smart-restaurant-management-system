from backend.extensions import db
from datetime import datetime


# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cus_name = db.Column(db.String(100), nullable=False)
    cus_mobile = db.Column(db.String(15), nullable=False)
    tot_amt = db.Column(db.Float, nullable=False)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="orders")