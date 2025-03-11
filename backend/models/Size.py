from backend.extensions import db


# Size Model (Small, Medium, Large)
class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(50), unique=True, nullable=False)