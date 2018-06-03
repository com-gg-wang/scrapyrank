

from scrapy import cmdline

if __name__ == '__main__':

    cmdline.execute("scrapy crawl entrey -s LOG_FILE=scrapy.log".split())