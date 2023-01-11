import csv
import logging
import os
import time
import uuid

import requests
from colorthief import ColorThief
from joblib import delayed
from joblib import Parallel

LOG_FORMAT = (
    "%(levelname)s | %(asctime)s | %(message)s | %(module)s.%(filename)s:%(lineno)d"
)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


source_file = "dress.csv"


def create_image(image_name: str, url: str):
    with open(image_name, "wb") as f:
        f.write(requests.get(url).content)


def get_links(file: str, sample: int = 0):
    with open(file) as f:
        counter = 1
        for i in csv.reader(f):
            if sample and counter > sample:
                break
            counter += 1
            link = i[-1]
            yield link


def get_color(image: str, quality: int = 1):
    return ColorThief(image).get_color(quality=quality)


def extract_image_colors(url: str):
    file_name = f"{uuid.uuid4()}.png"
    create_image(file_name, url)
    logging.info(f"Colors on file {file_name}: {get_color(file_name)}")
    os.remove(file_name)


def run(parallel: bool = False, sample: int = 0, csv_file: str = source_file):
    t1 = time.perf_counter()

    logging.info(
        f'{"Parallel" if parallel else "Regular"} execution using {"all" if not sample else sample} rows'
    )

    if parallel:
        Parallel(n_jobs=-1)(
            delayed(extract_image_colors)(i) for i in get_links(csv_file, sample)
        )
        logging.info(f"Took: {round(time.perf_counter()-t1,2)} seconds")
        return

    for i in get_links(source_file, sample):
        extract_image_colors(i)

    logging.info(f"Took: {round(time.perf_counter()-t1,2)} seconds")


run(0, 5)
run(1, 5)
