from genericpath import exists
from bs4 import BeautifulSoup
import requests
from pathlib import Path
import re
import json

imagesPath = Path("/images")
imagesPath.mkdir(exist_ok=True, parents=True)

# needed to download from the website, otherwise it gives 506 error
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

url = 'https://www.umop.com/rps101/'


def geturl(url):
    data = requests.get(url, headers=headers)
    return data


def download_symbol(name):
    """
    a fonction that downloads a symbol in the website from the file name.
    """
    # creates the full url
    image_url = "/".join(url.split("/")[:-1]) + "/"+name
    # gets the filename
    filename = ''.join(image_url.split("/")[-1:])
    # downloads the image
    img_data = geturl(image_url).content
    path = "images/"+filename
    output_file = Path(path)
    # create file is does not exist
    output_file.parent.mkdir(exist_ok=True, parents=True)
    if exists(path):
        # don't download a picture already downloaded, that would be stupid
        print(filename+' is already downloaded')
        return
    else:
        # download the image in /images folder
        with open(path, "wb+") as f:
            f.write(img_data)
            print("Downloded image: "+filename)
            return


def download_page(num):
    """
    A fonction that downloads and parses data from a symbol page
    """
    raw_html = geturl(url+str(num)+".htm").content
    soup = BeautifulSoup(raw_html, 'html.parser')

    # gets the image
    download_symbol(soup.body.img['src'])
    # gets the name of the symbol
    title = soup.b.contents[0].replace(" ", "")
    # prepares the text to read it
    string = str(soup.findAll("td")).replace(
        ",", "").replace("[", "").replace("]", "")

    wins = {}
    wins["id"] = num
    wins["imagefile"] = soup.body.img['src']
    # get all the wins one by one and add them to a dictionary
    for line in string.split("\n"):
        sign = re.search("\">(.*?)</a", line)
        if sign != None:
            sign = sign.group(1)
            sentence = re.sub("\<.*?\>", "", line).lower()
            sentence = sentence.replace(sign.lower(), sign.upper())
            wins[sign] = sentence
    return wins, title


def download_from_api(item):
    apiurl = "https://rps101.pythonanywhere.com/api/v1/objects/"+item
    result = str(geturl(apiurl).content)[2:-3].replace("\\", "")
    print(result)
    dict = json.loads(result)
    return dict


def api():
    with open("result.json", "r") as f:
        olddict = json.load(f)

    big_dict = {}
    for key in olddict.keys():
        dict = download_from_api(key)
        big_dict[dict["object"]] = dict['winning outcomes']

    with open('data.json', 'w') as f:
        json.dump(big_dict, f, indent=4)


if __name__ == "__main__":
    dict = {}

    for i in range(101):
        resultDict, resultTitle = download_page(i+1)
        dict[resultTitle] = resultDict

    with open('result.json', 'w') as f:
        json.dump(dict, f, indent=4)

        api()
