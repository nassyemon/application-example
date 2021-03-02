from datetime import datetime

from application.database import db


class Test(db.Model):
    __tablename__ = 'test'

    __table_args__ = (
        db.UniqueConstraint('title'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50, collation='utf8mb4_general_ci'), nullable=False)
    memo = db.Column(db.String(1000, collation='utf8mb4_general_ci'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, id, name, memo, created_at, updated_at):
        self.id = id
        self.name = titile
        self.memo = memo
        self.created_at = created_at
        self.updated_at = updated_at