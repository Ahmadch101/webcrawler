# Scrapy settings for ScrappingApplication project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
BOT_NAME = 'ScrappingApplication'

SPIDER_MODULES = ['ScrappingApplication.spiders']
NEWSPIDER_MODULE = 'ScrappingApplication.spiders'

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangowebcrawler.settings'

# This is required only if Django Version > 1.8
import django
django.setup()
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ScrappingApplication (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docss3_client.upload_fileobj(f, "wppdfupload", file_name)
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ScrappingApplication.middlewares.ScrappingapplicationSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ScrappingApplication.middlewares.ScrappingapplicationDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ScrappingApplication.pipelines.ScrappingapplicationPipeline': 300,
   'ScrappingApplication.pipelines.ScrappingSqLitePipeline': 310,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


#########################################################################

AWS_ACCESS_KEY_ID = 'AKIAIEK4JH24IA3ISIBQ'
AWS_SECRET_ACCESS_KEY = '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'
DB_PATH = 'C:\\Users\\ahmad\\PycharmProjects\\mscrapper\\ScrappingApplication\\ScrappingApplication\\database\\movies.db'
FILE_PATH = 'C:\\Users\\ahmad\\PycharmProjects\\mscrapper\\ScrappingApplication\\ScrappingApplication\\letters'