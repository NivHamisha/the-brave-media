import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class FirebaseActions:
    def __init__(self, cred_file, database_url, hashtag_ref, posts_ref):
        self.database_url = database_url
        try:
            self.cred = credentials.Certificate(cred_file)
            self.app = firebase_admin.initialize_app(self.cred, {'databaseURL': database_url})
        except Exception as err:
            raise err
        self.hashtag_ref = hashtag_ref
        self.posts_ref = posts_ref

    def check_hashtag_exists(self, hashtag_name):
        try:
            ref = db.reference(self.hashtag_ref)
            result = ref.get()
        except Exception as err:
            raise err
        for hashtag in result:
            if hashtag == hashtag_name:
                return True
        return False

    def add_hashtag(self, hashtag):
        try:
            ref = db.reference(self.hashtag_ref)
            result = ref.get()
        except Exception as err:
            raise err
        result.append(hashtag)
        ref = db.reference(self.hashtag_ref.rsplit('/', 1)[0])
        ref.child(self.hashtag_ref.rsplit('/', 1)[-1]).set(result)

    def delete_hashtag(self, hashtag):
        try:
            ref = db.reference(self.hashtag_ref)
            result = ref.get()
            result.remove(hashtag)
        except ValueError as err:
            return False
        except Exception as err:
            raise err
        ref = db.reference(self.hashtag_ref.rsplit('/', 1)[0])
        ref.child(self.hashtag_ref.rsplit('/', 1)[-1]).set(result)

    def add_post(self, post):
        try:
            ref = db.reference(self.posts_ref)
            ref.push(value=post)
        except Exception as err:
            raise err

    def update_post(self, post):
        try:
            ref = db.reference(self.posts_ref)
            result = ref.get()
        except Exception as err:
            raise err
        post_key_to_update = ""
        for post_key, post_content in result.items():
            if post['image_url'] in post_content['image_url']:
                post_key_to_update = post_key

        try:
            ref = db.reference(self.posts_ref)
            ref.child(post_key_to_update).set(post)
        except Exception as err:
            raise err

    def check_post_exists(self, post):
        try:
            ref = db.reference(self.posts_ref)
            result = ref.get()
        except Exception as err:
            raise err
        posts = []
        for post_key, post_content in result.items():
            if 'image_url' in post_content.keys():
                if post['image_url'] in post_content['image_url']:
                    return post_key
        return False

    def get_posts_by_hashtag(self, hashtag):
        try:
            ref = db.reference(self.posts_ref)
            result = ref.get()
        except Exception as err:
            raise err
        posts = []
        for post_key, post_content in result.items():
            if 'hashtags' in post_content.keys():
                if hashtag in post_content['hashtags']:
                    posts.append(post_content)
        return posts

    def delete_post(self, post):
        try:
            ref = db.reference(self.posts_ref)
            result = ref.get()
        except Exception as err:
            raise err
        post_key_to_delete = ""
        for post_key, post_content in result.items():
            if post['image_url'] in post_content['image_url']:
                post_key_to_delete = post_key

        try:
            ref = db.reference(f"{self.posts_ref}/{post_key_to_delete}")
            ref.delete()
        except Exception as err:
            raise err

    def add_hashtag_to_post(self, post, hashtag):
        post_key = self.check_post_exists(post=post)
        if 'hashtag' in post.keys():
            if hashtag not in post["hashtags"]:
                post["hashtags"].append(hashtag)
        try:
            ref = db.reference(self.posts_ref)
            ref.child(post_key).set(post)
        except Exception as err:
            raise err

    def get_hashtags(self):
        try:
            ref = db.reference(self.hashtag_ref)
            return ref.get()
        except Exception as err:
            raise err


def push_posts_to_firebase(posts, firebase, hashtag):
    for post in posts:
        if firebase.check_post_exists(post):
            firebase.add_hashtag_to_post(post, hashtag)
        else:
            firebase.add_post(post)


def delete_posts_from_firebase(firebase, hashtag):
    try:
        posts = firebase.get_posts_by_hashtag(hashtag=hashtag)
    except AttributeError as err:
        return False
    for post in posts:
        firebase.delete_post(post)
    firebase.delete_hashtag(hashtag=hashtag)
