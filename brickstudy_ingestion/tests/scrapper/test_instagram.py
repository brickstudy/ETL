from src.scrapper.ins_url import InsURLCrawler
from src.scrapper.ins_data import InsDataCrawler


def test_get_urls():
    keyword = '올리브영'
    url_crawler = InsURLCrawler()
    url_crawler.get_urls(keyword)
    url_crawler.materialize()

    crawler = InsDataCrawler(url_crawler.data)
    crawler.get_post_data()
    crawler.materialize()