from sqlalchemy import func

from app import db
from app.models.tag import experience_tag


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True, index=True)
    title = db.Column(db.String(250), nullable=False)
    experience_date = db.Column(db.Date, nullable=False)
    context = db.Column(db.Text, nullable=False)
    problem = db.Column(db.Text, nullable=False)
    investigation = db.Column(db.Text, nullable=False)
    action = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    lessons_learned = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = db.relationship("User", backref=db.backref("experiences", lazy=True))
    company = db.relationship("Company", backref=db.backref("experiences", lazy=True))
    project = db.relationship("Project", backref=db.backref("experiences", lazy=True))
    role = db.relationship("Role", backref=db.backref("experiences", lazy=True))
    tags = db.relationship("Tag", secondary=experience_tag, backref=db.backref("experiences", lazy="dynamic"))

    def __repr__(self):
        return f"<Experience {self.title}>"
