from backend.extensions import db

# Item Details Model (Links Item, Size, Type, Price, and Quantity)
class ItemDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey("size.id"), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("type.id"), nullable=True)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    item = db.relationship("Item", backref="details")
    size = db.relationship("Size", backref="details")
    type = db.relationship("Type", backref="details")