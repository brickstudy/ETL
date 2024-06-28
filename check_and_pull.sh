#!/bin/bash

# 원격 저장소의 변경 사항을 가져옵니다.
git fetch

# 원격 브랜치와 로컬 브랜치 간의 차이점이 있는지 확인합니다.
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    echo "로컬 저장소가 최신 상태입니다."
elif [ $LOCAL = $BASE ]; then
    echo "변경 사항이 있습니다. git pull을 실행합니다."
    git pull origin main
    docker restart etl-airflow-scheduler-1
elif [ $REMOTE = $BASE ]; then
    echo "로컬 저장소에 커밋되지 않은 변경 사항이 있습니다. 먼저 커밋을 하세요."
else
    echo "로컬 저장소와 원격 저장소가 다릅니다. 충돌이 있을 수 있습니다."
fi
