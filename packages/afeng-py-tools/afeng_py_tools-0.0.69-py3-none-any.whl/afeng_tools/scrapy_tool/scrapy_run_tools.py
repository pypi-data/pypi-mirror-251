import os.path

from scrapy.cmdline import execute

import sys


def run_spider(spider_dir: str, spider_name: str):
    sys.path.append(spider_dir)
    tmp_cwd = os.getcwd()
    os.chdir(spider_dir)
    execute(['scrapy', 'crawl', spider_name])
    os.chdir(tmp_cwd)


if __name__ == '__main__':
    spider_path = os.path.dirname(os.path.abspath(__file__))
    run_spider(spider_path, 'quotes')
