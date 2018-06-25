

from scrapy import cmdline

if __name__ == '__main__':

    cmdline.execute("scrapy crawl entrey ".split())
    # cmdline.execute("scrapy crawl entrey -o LOG_FILE=scrapy.log".split())