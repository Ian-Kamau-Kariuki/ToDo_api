from app import db, ma
from sqlalchemy import func


class UserModel(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    tasks = db.relationship('TaskModel', backref='user', lazy=True)

    def create_record(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def fetch_all(cls):
        return cls.query.all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ("_id", "email", "full_name", "created_at")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
