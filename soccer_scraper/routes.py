from app import website


@website.route('/')
def index():
    return('Hello World!')
