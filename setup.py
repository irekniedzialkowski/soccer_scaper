import setuptools

setuptools.setup(
  name="soccer_scraper",
  version="1.0.0",
  author="Ireneusz Niedziałkowski",
  author_email="irek.niedzialkowski@gmail.com",
  description="Soccer/Football scraping scripts enabling the user to view all the goals and other media highlights directly under results scraped from flashscore.",
  packages=["soccer_scraper"],
  include_package_data=True,
  install_requires=[
        'flask',
],
)
