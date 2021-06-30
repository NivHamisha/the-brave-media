from flask import Flask, request
from InstaActions import InstaActions, create_posts_list
from FirebaseActions import FirebaseActions, push_posts_to_firebase, delete_posts_from_firebase
from Setup import configuration_load
from flask_api import status
import json

app = Flask(__name__)

ENV_VARS = configuration_load()
INSTAACTIONS = InstaActions(ENV_VARS["INSTA_USER"], ENV_VARS["INSTA_PASSWORD"])
FIREBASE = FirebaseActions(ENV_VARS["CRED"], ENV_VARS["FIREBASE_DB_URL"],
                           ENV_VARS["HASHTAGS_REF"], ENV_VARS["POSTS_REF"])


@app.route('/', methods=['GET'])
def root():
    return "Up & Running!", status.HTTP_200_OK


@app.route('/api/posts/get_by_hashtag', methods=['GET'])
def get_hashtag_posts():
    hashtag = request.args.get("hashtag")
    posts_number = request.args.get("posts_number")

    if not posts_number:
        posts_number = 10
    else:
        posts_number = int(posts_number)

    if not hashtag:
        return "Error: empty hashtag", status.HTTP_400_BAD_REQUEST
    try:
        if FIREBASE.check_hashtag_exists(hashtag):
            posts = FIREBASE.get_posts_by_hashtag(hashtag)
        else:
            posts = create_posts_list(posts=INSTAACTIONS.get_hashtags_posts(hashtag=hashtag), posts_number=posts_number,
                                      hashtag=hashtag)
            FIREBASE.add_hashtag(hashtag)
            push_posts_to_firebase(posts, firebase=FIREBASE, hashtag=hashtag)
    except Exception as err:
        return "Error: failed getting posts", status.HTTP_500_INTERNAL_SERVER_ERROR

    return json.dumps(posts), status.HTTP_200_OK


@app.route('/api/hashtags', methods=['GET'])
def get_hashtags():
    try:
        return json.dumps(FIREBASE.get_hashtags())
    except Exception as err:
        return err, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/api/posts/update_post', methods=['POST'])
def update_post():
    try:
        post = request.json
        FIREBASE.update_post(post)
    except Exception as err:
        return err, status.HTTP_500_INTERNAL_SERVER_ERROR

    return "Post Updated!", status.HTTP_200_OK


@app.route('/api/posts/delete_by_hashtag', methods=['GET'])
def delete_hashtag_posts():
    hashtag = request.args.get("hashtag")

    if not hashtag:
        return "Error: empty hashtag", status.HTTP_400_BAD_REQUEST

    delete_posts_from_firebase(hashtag=hashtag, firebase=FIREBASE)

    return f"Posts with hashtag {hashtag} deleted", status.HTTP_200_OK


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
