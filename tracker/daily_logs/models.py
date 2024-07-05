from tracker import db
from datetime import datetime


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String, nullable=False, default="P")
    task_ids = db.Column(db.String, nullable=False, default="")
    explanation = db.Column(db.String, nullable=True)
    blockers = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, nullable=True, default=datetime.today)
