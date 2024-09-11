import requests
from bs4 import BeautifulSoup
import re
import arrow
# from dotenv import load_dotenv


def remove_html(text):
    txt = re.sub("<[^<]+?>", "", text).replace("\n", "")
    return txt


def data_dot_gov(metadata_urls):
    assets = []
    for url in metadata_urls:
        resp = requests.get(url).json()
        description = remove_html(resp["description"])
        title = resp["title"]
        modified = arrow.get(resp["modified"])
        keywords = resp["keyword"]

        asset = {
            "title": title,
            "description": description,
            "modified": modified,
            "metadata_url": url,
            "keywords": keywords,
        }

        assets.append(asset)

    return assets


def fsgeodata(metadata_urls):
    # base_url = "https://data.fs.usda.gov/geodata/edw/datasets.php"
    assets = []

    # Read the page that has the matedata links and cache locally
    # resp = requests.get(base_url)
    # soup = BeautifulSoup(resp.content, "html.parser")

    # anchors = soup.find_all("a")
    # for anchor in anchors:
    #     if anchor and anchor.get_text() == "metadata":
    #         metadata_urls.append(anchor["href"])

    for url in metadata_urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        title = remove_html(soup.find("title").get_text())
        desc_block = soup.find("descript")
        if desc_block:
            abstract = remove_html(desc_block.find("abstract").get_text())
        else:
            abstract = ""
        themekeys = soup.find_all("themekey")
        keywords = [tk.get_text() for tk in themekeys]
        idinfo_citation_citeinfo_pubdate = soup.find("pubdate")
        if idinfo_citation_citeinfo_pubdate:
            modified = arrow.get(idinfo_citation_citeinfo_pubdate.get_text())
        else:
            modified = ""

        asset = {
            "title": title,
            "description": abstract,
            "modified": modified,
            "metadata_url": url,
            "keywords": keywords,
        }

        assets.append(asset)

    return assets


def climate_risk_viewer(metadata_urls):
    assets = []

    for url in metadata_urls[:]:
        resp = requests.get(url)
        if resp.status_code == 200:
            content = resp.json()
            title = None
            description = remove_html(content["description"])
            if "documentInfo" in content.keys() and content["documentInfo"]:
                doc_info = content["documentInfo"]
                title = doc_info["Title"]
                keywords = [kw.strip() for kw in doc_info["Keywords"].split(" ")]
                # comments = remove_html(doc_info["Comments"])

                asset = {
                    "title": title,
                    "description": description,
                    "modified": "",
                    "metadata_url": url,
                    "keywords": keywords,
                }

                assets.append(asset)

    return assets


# def main():
#     import pprint

#     assets = data_dot_gov()
#     assets.extend(fsgeodata())
#     assets.extend(climate_risk_viewer())

#     pprint.pprint(assets)


# if __name__ == "__main__":
#     main()
