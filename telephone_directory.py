import requests
from bs4 import BeautifulSoup
import collections


def lookup_name(name):
	details = []
	Person = collections.namedtuple('Person', 'name address telephone')
	url = "http://rainbowpages.lk/search-directory?search=%s" % (name)

	try:
		print "[*] Looking up name '%s' from SLT RainbowPages .." % (name)
		response = requests.get(url)
		parsed_html = BeautifulSoup(response.text)
		misc_records = parsed_html.find_all("div", {"class":"jd-item"})
		for stuff in misc_records:
			# Extract Name
			un_names = stuff.find('div', {'class':'jd-itemTtile'})
			record_name = un_names.text

			# Extract Address
			un_address = stuff.find('div', {'class':'jd-itemAddress'})
			record_address = un_address.text.replace('Address','').strip()

			# Extract Telephone Number
			un_telephone = stuff.find('div', {'class':'jd-block-row'})
			record_telephone = un_telephone.find('span', {'class':'jd-fields-li-value'}).text

			# Append to list
			details.append(Person(name=record_name, address=record_address, telephone=record_telephone))

		return details

	except Exception as e:
		print '[!] An error occured while accessing the site'


def main():
	search_query = raw_input("Enter name to search: ")
	all_entries = lookup_name(search_query)
	for record in all_entries:
		print record.name
		print record.address
		print record.telephone

if __name__ == '__main__':
	main()	