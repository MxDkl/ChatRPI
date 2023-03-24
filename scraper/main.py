import requests
from bs4 import BeautifulSoup


# get all text from a url
def get_p_tags(url):
    try:
        r = requests.get(url)
    except:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    text = (soup.find_all('p') + 
            soup.find_all('li') + 
            soup.find_all('hr') +
            soup.find_all('div'))
    return text

# get all urls from a url. make sure they contain rpi.edu
def get_urls(url, key):
    try:
        r = requests.get(url)
    except:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = [] 
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            if key in href:
                urls.append(href)
    return urls

# write all p tags to a file
def write_to_file(p_tags, file_name):
    with open(file_name, 'w') as f:
        for p in p_tags:
            f.write(p.text)

key = "rpi.edu"
path = "../text/"
urls = [
    "https://www.rpi.edu/",
    "http://catalog.rpi.edu/content.php?catoid=24&navoid=606",
    "https://itssc.rpi.edu/hc/en-us",
    "https://rpi.edu/academics/",
    "https://en.wikipedia.org/wiki/Rensselaer_Polytechnic_Institute"
    ]
visited = []
url = "rpi.edu"
counter = 0
while (len(urls) != 0):
    #remove http or https from url
    url = url.replace("https://", "").replace("http://", "")
    if url in visited:
        url = urls.pop()
        continue
    visited.append(url)
    url = urls.pop()
    p_tags = get_p_tags(url)
    print(url)
    write_to_file(p_tags, path + str(counter) + ".txt")
    urls += get_urls(url, key)
    counter += 1
