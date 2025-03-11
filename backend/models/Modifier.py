from backend.extensions import db


# Modifier Model (Extra Cheese, No Onions, etc.)
class Modifier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)