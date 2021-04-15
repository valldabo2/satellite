from dataclasses import dataclass
from project import db

@dataclass
class Fire(db.Model):
    __tablename__ = "fires"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(128), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    processing_date = db.Column(db.Date(), default=True, nullable=False)
    confidence_level = db.Column(db.Float, nullable=False)
    cloud_coverage = db.Column(db.Float, default=0.0, nullable=True)
    shot_date = db.Column(db.DateTime(), default=True, nullable=False)
    shot_date_end = db.Column(db.DateTime(), default=True, nullable=False)