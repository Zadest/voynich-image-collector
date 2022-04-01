
from urllib import response
import requests



BASE_URL_1 = "https://collections.library.yale.edu/iiif/2/"
START_IMG_INDEX = 1006076
LAST_IMG_INDEX = 1006279
BASE_URL_2 = "/full/1000,1354/0/default.jpg"

def create_url(image_number:int)->str or None:
    """ Create a request URL with Variable Image Index"""
    if image_number < 0 or image_number+START_IMG_INDEX >= LAST_IMG_INDEX:
        return None
    
    return BASE_URL_1+str(START_IMG_INDEX+image_number)+BASE_URL_2

def request_url(url: str):
    name_appendix = "v" if int(url.split('/')[-5]) % 2 == 1 else "r"
    number = int(url.split('/')[-5])-START_IMG_INDEX+1
    number = number - int(number//2)
    name_number = str(number)
    name = name_number+name_appendix
    
    response = requests.get(url)
    
    if response and response.status_code == 200:
        with open("./data/"+name+".jpg","wb") as f:
            f.write(response.content)

def main():
    i = 0
    urls =[]
    url = create_url(i)
    while(url):
        i+=1
        urls.append(url)
        url = create_url(i)
    
    print(urls)
    for url in urls:
        print(f'requesting {url}')
        request_url(url)

if __name__ =="__main__":
    main()