#!/bin/bash

# log 폴더
# log 폴더 경로
log_dir="log"

# log 폴더가 존재하지 않으면 생성
if [ ! -d "$log_dir" ]; then
    mkdir "$log_dir"
fi

# log 파일 생성
# 현재 날짜를 "YYYY-MM-DD.log" 형식의 문자열로 변환
today_date=$(date +"%Y-%m-%d.log")

# 파일 경로 설정
log_file="$log_dir/$today_date"

# 파일이 존재하는지 확인
if [ ! -f "$log_file" ]; then
    # 파일이 존재하지 않으면 파일을 생성
    touch "$log_file"
    echo "$log_file 파일이 생성되었습니다."
else
    echo "$log_file 파일이 이미 존재합니다."
fi

# 원격 저장소의 변경 사항을 가져옵니다.
git fetch

# 원격 브랜치와 로컬 브랜치 간의 차이점이 있는지 확인합니다.
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})


echo "$(date): Your script is running" >> $log_file 2>&1


if [ $LOCAL = $REMOTE ]; then
    echo "$(date): 로컬 저장소가 최신 상태입니다." >> $log_file 2>&1
elif [ $LOCAL = $BASE ]; then
    echo "$(date): 변경 사항이 있습니다. git pull을 실행합니다." >> $log_file 2>&1
    
    git pull origin main
    echo "$(date): 정상적으로 git pull을 실행했습니다." >> $log_file 2>&1
    
    docker restart etl-airflow-scheduler-1
    echo "$(date): 정상적으로 docer scheduler을 재실행 했습니다." >> $log_file 2>&1
elif [ $REMOTE = $BASE ]; then
    echo "$(date): 로컬 저장소에 커밋되지 않은 변경 사항이 있습니다. 먼저 커밋을 하세요." >> $log_file 2>&1
else
    echo "$(date): 로컬 저장소와 원격 저장소가 다릅니다. 충돌이 있을 수 있습니다." >> $log_file 2>&1
fi
