from soccer_scraper.views import website


@website.route('/')
def index():
    return('Hello World!')
