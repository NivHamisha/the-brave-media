import os


def configuration_load():
    env_variables = {"CRED": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None),
                     "FIREBASE_DB_URL": os.getenv("FIREBASE_DB_URL", None),
                     "HASHTAGS_REF": os.getenv("HASHTAGS_REF", None),
                     "POSTS_REF": os.getenv("POSTS_REF", None),
                     "INSTA_USER": os.getenv("INSTA_USER", None),
                     "INSTA_PASSWORD": os.getenv("INSTA_PASSWORD", None)}

    if None in env_variables.values():
        print(env_variables)    
        raise IOError("Error: one or more env variables are not set properly")
    return env_variables
