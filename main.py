import pandas as pd
import json
import itertools
from collections import ChainMap
from chrisClient import ChrisClient

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def create_query(df: pd.DataFrame, str_srch_idx: str, str_anon_idx: str):
    l_srch_idx = list(map(int,str_srch_idx.split(',')))
    l_anon_idx = list(map(int,str_anon_idx.split(',')))

    # create connection object
    cube_con = ChrisClient("http://cube.chrisproject.org/api/v1/", "sandip", "sandip1234")

    for row in df.iterrows():
        d_job = {}
        s_col = (df.columns[l_srch_idx].values)
        s_row = (row[1][l_srch_idx].values)
        s_d = [{k: v} for k, v in zip(s_col, s_row)]

        d_job["search"] = dict(ChainMap(*s_d))
        a_col=(df.columns[l_anon_idx].values)
        a_row=(row[1][l_anon_idx].values)
        a_d = [{k.split('.')[0]:v} for k,v in zip(a_col,a_row)]
        d_job["anon"] = dict(ChainMap(*a_d))

        print(d_job)
        submit_job(cube_con, d_job)



def serialize_csv(file_path: str, anon_all: bool):
    df = pd.read_csv(file_path)
    search_idx = "1"
    anon_id = "0,2,3,4"
    create_query(df,search_idx,anon_id)


def submit_job(con: ChrisClient, job: dict):
    con.anonymize(job)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path: str ="./sample3.csv"
    anon_all: bool = False
    serialize_csv(file_path, anon_all)
