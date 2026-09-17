from sqlalchemy import func

from app import db

experience_tag = db.Table(
    "experience_tag",
    db.Column("experience_id", db.Integer, db.ForeignKey("experiences.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = db.relationship("User", backref=db.backref("tags", lazy=True))

    def __repr__(self):
        return f"<Tag {self.name}>"
