# from backend import Retrieve
from config import config
from backend.load import *

if __name__ == "__main__":
    # f = Retrieve(config.URL, config.TAG, config.CLASS)
    # f.retrieve_info()
    db: List[FacultyMember] = load_in(config.DATA_FILE)
    save_object(db, config.SAVED_FILE)
