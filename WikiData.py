from operator import imod
from random import randint
import requests
import hashlib
from PIL import Image
import time

NAMES = {
	'tacker-talbot':{
		"f16v": ["agave atrovirens"],
		"93r": ["Helianthus annuus", "chimalatl peruiana"],
		"13r": ["Petasites"],
		"33v": ["Psacalium peltigerum"]
	}
}

NAMES_LIST_URL = "http://www.voynich.nu/extra/herb_oldid.html"

API_ENDPOINT = "https://www.wikidata.org/w/api.php"


for name in NAMES:
	for index, value in enumerate(NAMES[name]):

		query = value

		params = {
		'action': 'wbsearchentities',
		'format': 'json',
		'language': 'en',
		'search': query
		}

		r = requests.get(API_ENDPOINT, params=params)
		if len(r.json()['search']) < 1:
			continue
		query = r.json()['search'][0]['id']
		print(query)
		params = {
		'action': 'wbgetclaims',
		'format': 'json',
		'property': 'P18',
		'entity': query
		}

		r1 = requests.get(API_ENDPOINT, params=params)

		if not 'P18' in r1.json()['claims']:
			continue
		image_file = r1.json()['claims']['P18'][0]['mainsnak']['datavalue']['value'].replace(' ', '_')

		md5 = hashlib.md5(image_file.encode("utf-8")).hexdigest()

		image_URL = f"https://upload.wikimedia.org/wikipedia/commons/{md5[0]}/{md5[0:2]}/{image_file}" if len(image_file) > 1 else ""

		print(image_file, md5, image_URL)

		if image_URL:
			print(image_file, md5, image_URL)
			response = requests.get(image_URL, headers={"Accept":
										"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
										"Accept-Encoding":
										"gzip, deflate, br",
										"Accept-Language":
										"en-US,en;q=0.5",
										"Connection":
										"keep-alive",
										"Cookie":
										"WMF-Last-Access-Global=12-Mar-2022",
										"Host":
										"upload.wikimedia.org",
										"Sec-Fetch-Dest":
										"document",
										"Sec-Fetch-Mode":
										"navigate",
										"Sec-Fetch-Site":
										"none",
										"Sec-Fetch-User":
										"?1",
										"Upgrade-Insecure-Requests":
										"1",
										"User-Agent":
										"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"})
			print(response)
			if response.status_code == 200:
				with open(f"./data/real/{value}_{index}.{image_URL.split('.')[-1]}", "wb") as f:
					f.write(response.content)
	time.sleep(randint(1,5))