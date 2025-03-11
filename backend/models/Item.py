from backend.extensions import db

# Item Model (Food Items)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iname = db.Column(db.String(100), unique=True, nullable=False)