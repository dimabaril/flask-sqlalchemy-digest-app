from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<User {self.name}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)
    user = db.relationship("User", backref="subscriptions")
    tag = db.relationship("Tag", backref="subscriptions")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Subscription {self.user_id} - {self.tag_id}>"


# Промежуточная таблица для связи постов и тегов, тег в текущем исполнении по сути источник новостей и в данном случае многие ко многим не требуется, но изначально тег задумался как тег, пока оставлю так.
post_tag = db.Table(
    "post_tag",
    db.Column(
        "post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column(
        "created_at", db.DateTime, nullable=False, default=datetime.utcnow
    ),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False, default="")
    popularity = db.Column(
        db.Integer,
        nullable=False,
    )
    tags = db.relationship("Tag", secondary="post_tag", backref="posts")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"


digest_post = db.Table(
    "digest_post",
    db.Column(
        "digest_id", db.Integer, db.ForeignKey("digest.id"), primary_key=True
    ),
    db.Column(
        "post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True
    ),
    db.Column(
        "created_at", db.DateTime, nullable=False, default=datetime.utcnow
    ),
)


class Digest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref="digests")
    posts = db.relationship("Post", secondary=digest_post, backref="digests")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Digest {self.id}>"
