from pathlib import Path

TAG = "div"
CLASS = "img-card__body"
URL = ["https://dr.ntu.edu.sg/simple-search?query=&location=researcherprofiles&filter_field_1=school&filter_type_1=authority&filter_value_1=ou00030&crisID=&relationName=&sort_by=bi_sort_4_sort&order=asc&rpp=50&etal=0&start=0",
       "https://dr.ntu.edu.sg/simple-search?query=&location=researcherprofiles&filter_field_1=school&filter_type_1=authority&filter_value_1=ou00030&crisID=&relationName=&sort_by=bi_sort_4_sort&order=asc&rpp=50&etal=0&start=50"]
WEBSITE = "display-label-personalsite"
AKA = {"Jagath Chandana Rajapakse": "Jagath C. Rajapakse",
       "Ke Yiping, Kelly": "Yiping Ke",
       "Lana Obraztsova": "Svetlana Obraztsova"
       }
ROOT = str(Path().absolute())
DATA_FILE = ROOT + "/src/backend/data"
FCITES_PATH = ROOT + '/src/frontend/templates/citesperyear.html'
TOT_FCITES_PATH = ROOT + '/src/frontend/templates/summary_cites.html'
NET_PATH = ROOT + '/src/frontend/templates/summary_network.html'
SCATTER_PATH = ROOT + '/src/frontend/templates/summary_scatter.html'
