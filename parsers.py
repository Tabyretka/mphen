import json

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()


def papir_parse(query: str):
    BASE_LINK = "https://папироска.рф"
    headers = {
        "user-agent": ua.random
    }

    query = query.lower()
    url = f"{BASE_LINK}/search/?query={query}"
    rs = requests.get(url=url, headers=headers)
    if rs.ok:
        soup = BeautifulSoup(rs.text, "lxml")
        catalog = soup.find("div", class_="catalog", id="catalog-search")
        collected_data = []
        for product in catalog.find_all("div", class_="productBrief"):
            try:
                title = product.find("a", class_="link--secondary").text.strip()
                url = BASE_LINK + product.find("a", class_="link--secondary").get("href").strip()
                price = product.find("div", class_="productBriefCost__price")
                image = BASE_LINK + product.find("div", class_="productBrief__img").find("img").get("src").strip()
                if price:
                    price = price.text.strip().rstrip(" р.")
                else:
                    price = ""
                collected_data.append({"title": title, "url": url, "price": price, "image": image})
            except Exception:
                pass
        return collected_data
    else:
        return []


def zone_parse(query: str):
    BASE_LINK = "https://vapezone.pro"
    headers = {
        "user-agent": ua.random
    }

    query = query.lower()
    url = f"{BASE_LINK}/?match=all&subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q={query}&dispatch=products.search"
    rs = requests.get(url=url, headers=headers)
    if rs.ok:
        soup = BeautifulSoup(rs.text, "lxml")
        collected_data = []
        for product in soup.find("div", id="products_search_pagination_contents").find_all("div", class_="ut2-gl__item"):
            try:
                title = product.find("div", class_="ut2-gl__name").find("a", class_="product-title").get("title").strip()
                url = product.find("div", class_="ut2-gl__name").find("a", class_="product-title").get("href").strip()
                price = product.find("span", class_="ty-price-num").text.strip()
                image = product.find("div", class_="ut2-gl__image").find("img").get("src").strip()
                if " " in price:
                    price = price.replace(" ", "")
                if not price:
                    price = "0"
                collected_data.append({"title": title, "url": url, "price": price, "image": image})
            except Exception:
                pass
        return collected_data
    else:
        return []

