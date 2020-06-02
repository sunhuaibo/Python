#!/usr/bin/env python
# -*- coding=utf-8 -*-

import pandas as pd
import requests
import json
import time
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_opt():
    parse = ArgumentParser()
    parse.add_argument("-i", help="Input manifest file", required=True)
    parse.add_argument("-o", help="Output file prefix, default=res", default="res")
    parse.add_argument("-t", help="Thread number, default=30", default=30)
    return parse.parse_args()

def get_query_id(query_id):
    url =  "https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json?method=db2db&format=row"
    url_params = {"input":"genesymbol",'inputValues':query_id, "outputs":"geneid,ensemblgeneid", "taxonId":"9606"} 
    response = requests.get(url, params = url_params)
    return json.loads(response.text)[0]

def main():
    opt = get_opt()
    df = pd.read_csv(opt.i, sep="\t")
    df2 = df.loc[~df["id"].duplicated(),]
    res = []
    print("Start {}".format(time.ctime()), flush=True)
    print("-" * 60, flush=True)
    with ThreadPoolExecutor(max_workers=int(opt.t)) as executor:
        future_query_id = {executor.submit(get_query_id, query_id): query_id for query_id in df2["id"].tolist()}
        for future in as_completed(future_query_id):
            query_id = future_query_id[future]
            try:
                res.append(future.result())
            except Exception as exc:
                print('%s generated an exception: %s' % (query_id, exc), flush=True)
            else:
                print('%s page is success' % (query_id), flush=True)
    res = pd.DataFrame(res)
    res.to_csv("{}.txt".format(opt.o), sep="\t", index=False)
    print("-" * 60, flush=True)
    print("End {}".format(time.ctime()), flush=True)

if __name__ == "__main__":
    main()