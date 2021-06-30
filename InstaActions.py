from instaloader import Instaloader


class InstaActions:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.loader = Instaloader()
        self.create_session()

    def login(self):
        self.loader.login(self.user, self.password)

    def get_hashtags_posts(self, hashtag):
        return self.loader.get_hashtag_posts(hashtag)

    def get_location_posts(self, location):
        return self.loader.get_location_posts(location)

    def save_session(self, filename):
        self.loader.save_session_to_file(filename)

    def load_session(self, filename):
        self.loader.load_session_from_file(username=self.user, filename=filename)

    def create_session(self):
        try:
            self.load_session("session")
        except FileNotFoundError as err:
            self.login()
            self.save_session("session")


def create_posts_list(posts, hashtag, posts_number=None):
    posts_data = []
    count = 0
    for post in posts:
        posts_data.append({"image_url": post.url,
                           "caption": post.caption,
                           "hashtags": [hashtag],
                           "brave_words": [""],
                           "reactions": {"likes": 0,
                                         "happy": 0,
                                         "sad": 0,
                                         "brave": 0,
                                         "love": 0}})
        count += 1
        if count == posts_number:
            break
    return posts_data
