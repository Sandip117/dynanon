import pandas as pd
import json
import itertools
from collections import ChainMap

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def create_query(df: pd.DataFrame, srch_idx: int, l_anon_idx: list[int]):
    for row in df.iterrows():
        pacs_search_tag = df.columns[srch_idx]
        pacs_search_val = row[1][srch_idx]
        print(f"Search PACS for {pacs_search_tag}:{pacs_search_val}")
        col=(df.columns[l_anon_idx].values)
        row=(row[1][l_anon_idx].values)
        d = [{k:v} for k,v in zip(col,row)]

        print(f"Anonymize with { json.dumps(dict(ChainMap(*d)), indent=4) }")


def serialize_csv(file_path: str, search_tag: str, anon_all: bool):
    df = pd.read_csv(file_path)
    search_col_idx = df.columns.get_loc(search_tag)
    print(f"index of {search_tag} is {search_col_idx}")
    anon_col_idx = [i for i, col in enumerate(df.columns) if col != search_tag]
    print(f"indices of anon columns are {anon_col_idx}")
    create_query(df,search_col_idx,anon_col_idx)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_path: str ="./sample2.csv"
    search_for: str = "AccessionNumber"
    anon_tags: str = ""
    anon_all: bool = False
    serialize_csv(file_path, search_for, anon_all)
