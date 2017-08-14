# -*- coding: utf-8 -*-
# !/python 3.6.2
# Created by @_ajnicolas
import requests, json, crayons, sys
from bs4 import BeautifulSoup

useragent =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3124.4 Safari/537.36'
headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36'
        '(KHTML, like Gecko) Chrome/56.0.2924.28 Safari/537.36'}

email = '' #enter email inside ''
password = '' #enter password also
url = "https://www.antonioli.eu/en/US/men/products/cp9890" #url of product
shoesize = '10' #size 

#have a tab open logged onto the site and is on this url to checkout
cart = 'https://www.antonioli.eu/en/US/cart'
session = requests.Session()

loginUrl = 'https://www.antonioli.eu/fr/US/login'
logindata ={
	'utf8':'✓',
	'authenticity_token':'',
	'spree_user[email]':email,
	'spree_user[password]':password,
	'spree_user[remember_me]':'0',
	'commit':'Connexion'
}

def atc():
	reqlog = session.get(loginUrl,headers=headers)
	print ("Logging in...")
	log = session.post(loginUrl,headers=headers,data=logindata)
	print ("Logged in\n")
	if 'Email ou mot de passe invalide' in str(log.content):
		print (crayons.red("check acc info to see everything correct"))
		sys.exit()

	r = session.get(url,headers=headers)
	print(r.url)
	soup = BeautifulSoup(r.content, 'html.parser')

	variants = []
	for x in soup.findAll('input', {'name': 'variant_id'}):
		variants.append(x['value'])

	form = soup.find('div', {'class': 'product-variants'})
	size = form.text
	fix = size.replace(u"½",u".5")

	#sizes is a list btw
	sizes = fix.split("\n")   
	sizes = sizes[::2][1:]
	print (sizes)

	footsize = shoesize
	try:
		#fallback if shoesize is not in index
		if footsize not in sizes:
			footsize = input(crayons.red("Size not available! Input manually from the list above "))

		key = sizes.index(footsize)
		variant = variants[key]
		print ("Variant = " + variant + "\n")
	except (IndexError) as e:
		#Cheap second fallback lol
		variant = 7

	cartheaders = {
	    'User-Agent': useragent,
	    'Content-Type': 'application/json'
	}
	cartpost = {
		'utf8':'✓',
		'authenticity_token':'',
		'variant_id': variant,
		'quantity':'1'
	}
	jsonarray = json.dumps(cartpost)
	cartUrl = 'https://www.antonioli.eu/en/US/orders/populate.json'

	print ("Adding product to cart..")
	r = session.post(cartUrl, headers=cartheaders, data=jsonarray)

	if 'errors' in str(r.content):
		print (crayons.red("Either the item can't have one or more of the same size in cart or oos."))
	else:
		print (r.content)

	req = session.get(cart,headers=headers)
	soup = BeautifulSoup(req.content, 'html.parser')
	auth_token = soup.find('input', {'name': 'authenticity_token'})['value']
	print ("\nAuth token = " + auth_token)

if __name__ == "__main__":
	print ("Created by @_ajnicolas")
	atc()
