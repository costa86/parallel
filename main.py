import csv
import requests
from colorthief import ColorThief
import time
import os
from joblib import Parallel, delayed
import uuid

source_file = 'dress.csv'

def create_image(image_name: str, url: str):
    with open(image_name, 'wb') as f:
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
    file_name = f'{uuid.uuid4()}.png'
    create_image(file_name, url)
    print(get_color(file_name))
    os.remove(file_name)


def run(parallel: bool = False, sample: int = 0, csv_file: str = source_file):
    t1 = time.time()
    
    if parallel:
        print(f'Parallel execution using {"all" if not sample else sample} rows')
        Parallel(n_jobs=-1)(delayed(extract_image_colors)(i)for i in get_links(csv_file, sample))
        print(f'Took: {time.time()-t1}')
        return
    
    print(f'Regular execution using {"all" if not sample else sample} rows')
    for i in get_links(source_file, sample):
        extract_image_colors(i)
    print(f'Took: {time.time()-t1}')

run(0,5)