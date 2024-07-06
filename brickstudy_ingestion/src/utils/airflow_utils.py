import json
from datetime import datetime

def check_quota():
    try:
        #TODO (1)쿼타 count 해서 25000개 채웠는지 확인 or (2)쿼타 넘어서 오류나는거 exception catch? test
        #TODO (1)로 할 경우 아래처럼 파일로 관리할지 DB로 관리할지(어차피 postgre 띄울거니까)
        with open('./quota_file.json', 'r') as file:
            data = json.load(file)
            if data['date'] == datetime.today().strftime('%Y-%m-%d'):
                return data['count']
            else:
                return 0
    except FileNotFoundError:
        return 0

def update_quota(count):
    with open('./quota_file.json', 'w') as file:
        data = {
            'date': datetime.today().strftime('%Y-%m-%d'),
            'count': count
        }
        json.dump(data, file)
