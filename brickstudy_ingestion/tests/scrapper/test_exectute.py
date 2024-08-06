import json
from dataclasses import asdict

from src.scrapper.oliveyoung import Brand
from src.scrapper.models import OliveyoungBrand


def brand_metadata_cutter(data: dict, level: int):
    total_n = len(data)
    partition_n = total_n // level
    partition_remain = total_n % level

    brand_lst = list(data.keys())
    start = 0
    for i in range(level):
        end = start + partition_n + (1 if i < partition_remain else 0)
        part = {key: data[key] for key in brand_lst[start:end]}
        return part  # TODO yield로 변경
        start = end


def test_get_brand_metadata():
    brand = Brand()
    brand.crawl_brand_metadata()
    json_data = {b_name: asdict(details) for b_name, details in brand.brand_metadata.items()}
    with open('brand_metadata.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def test_read_from_previous_written_metadata_and_get_item_data_in_partitioned_way():
    with open('brand_metadata.json', 'r', encoding='utf-8') as json_file:
        loaded_data = json.load(json_file)

    for key, val in loaded_data.items():
        loaded_data[key] = OliveyoungBrand(**val)
    partitioned = brand_metadata_cutter(loaded_data, 8)
    print(partitioned)
    brand = Brand(partitioned)
    brand.crawl_items()
    json_data = {b_name: asdict(details) for b_name, details in brand.brand_metadata.items()}
    with open('brand_itemdata.json', 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

