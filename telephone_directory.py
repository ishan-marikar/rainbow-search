import requests
from bs4 import BeautifulSoup
import collections
import urlparse

def get_last_record_number(parsed_html):
	try:
		stuff = parsed_html.find('a', {'title':'End'})
		link = stuff.get('href')
		parsed = urlparse.urlparse(link)
		record_last_number = urlparse.parse_qs(parsed.query)['start']
		return record_last_number[0]
	except Exception as e:
		print '[!] [2] Handling Exception:', e
		pass


def open_site(query, start=0):
	url = "http://rainbowpages.lk/search-directory/"
	payload = {'search':query, 'start':start}
	response = requests.get(url, params=payload)
	parsed_html = BeautifulSoup(response.text)
	return parsed_html

def extract_records(parsed_html):
	details = []
	Person = collections.namedtuple('Person', 'name address telephone')
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
	

def lookup_name(name):
	print "[*] Looking up name '%s' from SLT RainbowPages .." % (name)

	current_record = 0
	last_record = 0
	complete_results = []

	while True:
		try:
			parsed_html = open_site(name, current_record)
			last_record = get_last_record_number(parsed_html)
			current_page_results = extract_records(parsed_html)
			current_record = current_record + 15

		except Exception as e:
			print '[!] [1] Handling Exception:', e
			break

		print "[*] Appending %s of %s" % (current_record, last_record)
		complete_results.extend(current_page_results)
		

	return complete_results


def main():
	search_query = raw_input("Enter name to search: ")
	all_entries = lookup_name(search_query)
	for record in all_entries:
		print "*"*50
		print record.name
		print record.address
		print record.telephone

if __name__ == '__main__':
	main()