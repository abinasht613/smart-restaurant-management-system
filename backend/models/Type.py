from backend.extensions import db


# Type Model (Veg, Non-Veg, Drinks, etc.)
class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(50), unique=True, nullable=False)