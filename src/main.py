from backend import Retrieve
from config import config

if __name__ == "__main__":
    f = Retrieve(config.URL, config.TAG, config.CLASS)
    f.retrieve_info()
