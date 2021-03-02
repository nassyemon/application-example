from datetime import datetime

from application.database import db


class Piyo(db.Model):
    __tablename__ = 'piyo'

    __table_args__ = (
        db.UniqueConstraint('name'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, id, name, created_at, updated_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at