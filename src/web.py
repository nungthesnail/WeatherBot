import requests
from bs4 import BeautifulSoup


headers: dict = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1 AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
}


def get_page_source(url) -> str | None:
    response = requests.get(url, headers)
    if response.status_code != 200:
        return None
    return response.text


def get_class_elements(source, tag, class_name) -> list[str]:
    soup = BeautifulSoup(source, "lxml")
    return [i.text for i in soup.find_all(tag, {"class": class_name})]
