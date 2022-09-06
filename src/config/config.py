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
DATA_FILE = str(Path().absolute()) + "/src/backend/data"
