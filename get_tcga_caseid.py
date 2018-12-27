#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import time
import requests
import pandas as pd
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_opt():
    parse = ArgumentParser()
    parse.add_argument("-i", help="Input manifest file")
    parse.add_argument("-o", help="Output file prefix")
    parse.add_argument("-t", help="Thread number, default=30", default=30)
    return parse.parse_args()

def get_barcode(file_uuid):
    # The 'fields' parameter is passed as a comma-separated string of single names.
    fields = [
        "cases.samples.portions.analytes.aliquots.submitter_id"
        ]
    fields = ','.join(fields)
    params = {
        "fields": fields,
        "format": "tsv"
        }
    file_endpt = 'https://api.gdc.cancer.gov/files/'
    response = requests.get(file_endpt + file_uuid, params = params)
    barcode = response.text.split("\r\n")[1]
    return barcode

if __name__ == "__main__":
    opt = get_opt()
    df = pd.read_table(opt.i)
    res = []
    print("Start {}".format(time.ctime()))
    print("-" * 60)
    with ThreadPoolExecutor(max_workers=opt.t) as executor:
        future_to_file_uuid = {executor.submit(get_barcode, file_uuid): file_uuid for file_uuid in df["id"].tolist()}
        for future in as_completed(future_to_file_uuid):
            file_uuid = future_to_file_uuid[future]
            try:
                data = future.result()
                res.append([file_uuid, data])
            except Exception as exc:
                print('%r generated an exception: %s' % (file_uuid, exc))
            else:
                print('%r page is success' % (file_uuid))
    
    res = pd.DataFrame(res)
    res.columns = ["id", "case_id"]
    res.to_csv("{}.txt".format(opt.o), sep="\t", index=False)
    print("-" * 60)
    print("End {}".format(time.ctime()))


