from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username