import requests
from bs4 import BeautifulSoup


#function to get all text from a url
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

#function to get all urls from a url. make sure they contain rpi.eu
def get_urls(url):
    try:
        r = requests.get(url)
    except:
        return []
    soup = BeautifulSoup(r.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            if 'rpi.edu' in href:
                urls.append(href)
    return urls

#function to write all p tags to a file
def write_to_file(p_tags, file_name):
    with open(file_name, 'w') as f:
        for p in p_tags:
            f.write(p.text)



path = "/home/player1/Desktop/RPI/ChatRPI/text/"
url = "https://www.rpi.edu/"
url2 = "http://catalog.rpi.edu/content.php?catoid=24&navoid=606"
urls = [url, url2]
visited = []
counter = 0
while (len(urls) != 0):
    if url in visited:
        print("already visited")
        url = urls.pop()
        continue
    visited.append(url)
    url = urls.pop()
    p_tags = get_p_tags(url)
    print(url)
    #write_to_file(p_tags, path + str(counter) + ".txt")
    urls += get_urls(url)
    counter += 1
