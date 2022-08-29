# call retrieve
# create dataframe

from backend import Retrieve
from config import config

if __name__ == "__main__":
    f = Retrieve(config.URL, config.TAG, config.CLASS)
    dat = f.retrieve_info().to_dataframe()
    dat.to_csv('record.csv')
    print(dat)
