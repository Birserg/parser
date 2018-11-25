import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool


def get_html(url: object) -> object:
    r = requests.get(url)
    return r.text


def get_all_pages(html):
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find("div", class_="navi").find_all("a")[-2].text.strip()
    return int(pages)


def get_all_links(html):
    soup = BeautifulSoup(html, "lxml")
    tds = soup.find_all("div", class_="title")
    links = []
    for td in tds:
        a = td.find("a").get("href")
        links.append(a)
    return links


def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    # data = []
    try:
        name = soup.find("h1", class_="titlfull").text.strip()
    except:
        name = ""

    try:
        rate = soup.find("b", itemprop="ratingValue").text.strip()
        # rate = rate.split('>')[1]
    except:
        rate = ""

    data = {"name": name, "rate": rate}

    return data


def write_csv(data):
    with open("datarate.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow((data["name"], data["rate"]))
        print(data["name"], data["rate"], "parsed")


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = "https://online.anidub.com/anime_movie/"
    page_part = "page/"
    total_pages = get_all_pages((get_html(url)))
    for i in range(1, total_pages + 1):
        url_gen = url + page_part + str(i) + "/"
        html = get_html(url_gen)
        all_links = get_all_links(html)
        # rint (all_links)
        for u in all_links:
            make_all(u)
        # with Pool (40) as p:
        #   p.map (make_all, all_links)

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == "__main__":
    main()
