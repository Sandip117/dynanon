import pandas as pd
import json
import itertools
from collections import ChainMap
from chrisClient import ChrisClient

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def create_query(df: pd.DataFrame, l_srch_idx: list[int], l_anon_idx: list[int]):
    # create connection object
    cube_con = ChrisClient("http://ekanite.tch.harvard.edu:32223/api/v1/", "chris", "chris1234")

    for row in df.iterrows():
        d_job = {}
        s_col = (df.columns[l_srch_idx].values)
        s_row = (row[1][l_srch_idx].values)
        s_d = [{k: v} for k, v in zip(s_col, s_row)]

        d_job["search"] = json.dumps(dict(ChainMap(*s_d)), indent=4)
        a_col=(df.columns[l_anon_idx].values)
        a_row=(row[1][l_anon_idx].values)
        a_d = [{k:v} for k,v in zip(a_col,a_row)]

        d_job["anon"] = json.dumps(dict(ChainMap(*a_d)), indent=4)
        submit_job(cube_con, d_job)
        print(d_job)


def serialize_csv(file_path: str, search_tag: str, anon_all: bool):
    df = pd.read_csv(file_path)
    search_col_idx=[1]
    anon_col_idx=[0,2,3]
    create_query(df,search_col_idx,anon_col_idx)


def submit_job(con: ChrisClient, job: dict):
    con.anonymize(job)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path: str ="./sample3.csv"
    search_for: str = "PatientID"
    anon_tags: str = ""
    anon_all: bool = False
    serialize_csv(file_path, search_for, anon_all)
