from tracker import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String, nullable=False, default="P")
    archive_status = db.Column(db.Boolean, nullable=False, default=False)
    category = db.Column(db.String(30), nullable=False, default="Dev")
    date_of_allotment = db.Column(db.Date, nullable=False, default=datetime.today)
    due_date = db.Column(db.Date, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    progress_status = db.Column(db.String, nullable=False, default="Not Started")
    blockers = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String, nullable=False, default="Medium")
    time_spent = db.Column(db.Float, nullable=True)
    external_link = db.Column(db.Text, nullable=True)
    last_worked_on = db.Column(db.Date, nullable=False, default=datetime.today)
    close_date = db.Column(db.Date, nullable=True)
    progress_counter = db.Column(db.Integer, default=0)
    attachments = db.relationship('Attachment', backref='task', lazy=True, cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"<Task {self.name} {self.category}"


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    def __repr__(self):
        return f'<Attachment {self.original_filename}>'
