## Viral project data ingestion code

```
brickstudy_ingestion/src/scrapper
├── __init__.py     # scrapper 모듈 entrypoint
├── Dockerfile      # [Twitter] twitter crawler 동작 환경
├── browser.py      # [Instagram] selenium으로 크롤링하는데에 사용되는 로직 정의 모듈
├── inscrawler.py   # [Instagram]instagram crawler main 모듈
├── models.py       # [Oliveyoung] 올리브영 브랜드 수집 데이터 구조
├── oliveyoung.py   # [Oliveyoung] scrapper main 모듈
└── utils.py        # 공통 유틸리티 메소드
```


