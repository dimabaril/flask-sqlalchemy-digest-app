from flask import Flask, jsonify, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload

from config import Config
from models import Digest, Post, Subscription, Tag, User, db

app = Flask(__name__)
app.config.from_object(Config)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config["SECRET_KEY"] = "<replace with a secret key>"
app.config["SQLALCHEMY_RECORD_QUERIES"] = True

toolbar = DebugToolbarExtension(app)

db.init_app(app)


@app.route("/<int:user_id>", methods=["GET"])
def index(user_id):
    return redirect(url_for("json_digest", user_id=user_id))


@app.route("/json_digest/<int:user_id>", methods=["GET"])
def json_digest(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    digest_data = generate_digest(user)
    return jsonify(digest_data), 200


@app.route("/human_readable_digest/<int:user_id>", methods=["GET"])
def human_readable(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template("error404.html"), 404
    digest_data = generate_digest(user)
    return render_template(
        "human_readable_digest.html", digest_data=digest_data
    )


def generate_digest(user):
    # Пункты 2, 3, 4 одним запросом
    popular_posts = (
        Post.query.join(Post.tags)
        .join(Tag.subscriptions)
        .filter(Subscription.user_id == user.id)
        .filter(Post.popularity >= 50)
        .options(joinedload(Post.tags))  # Жадная загрузка тегов
        .all()
    )

    # Создание дайджеста
    digest = Digest(user_id=user.id)
    db.session.add(digest)
    # db.session.commit()

    # Добавление отобранных постов в дайджест
    # for post in popular_posts:
    #     digest.posts.append(post)
    digest.posts = popular_posts

    # db.session.commit()

    # Формируем данные для ответа
    digest_data = {
        "digest_id": digest.id,
        "user_id": user.id,
        "user_name": user.name,
        "posts": [],
    }

    for post in digest.posts:
        post_data = {
            "post_id": post.id,
            "content": post.content,
            "popularity": post.popularity,
            "tags": [tag.name for tag in post.tags],
        }

        digest_data["posts"].append(post_data)

    db.session.commit()
    return digest_data


if __name__ == "__main__":
    app.run(debug=True)
