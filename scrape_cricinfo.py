import sys
import requests
from bs4 import BeautifulSoup
import csv
import pprint

#-------------------------------------------#
#    CricInfo URL Stats Page Scraping       #
#-------------------------------------------#
BASE_URL='https://stats.espncricinfo.com/'
URL = 'https://stats.espncricinfo.com/ci/engine/records/index.html?class=1'
print ("Scrapping >> ", URL)

page = requests.get(URL)
first_level_page = BeautifulSoup(page.content, 'html.parser')
first_level_links = first_level_page.find('div', class_='pnl386M')

for _link in first_level_links.find_all('ul', class_='Record'):
	for hrefs in _link.find_all('a'):
		_url_suffix = hrefs.get('href')
		actual_url = BASE_URL+_url_suffix
		_string = hrefs.string.replace(" ", "_")
		filename = _string+".csv"

		print("Extracting table from ", hrefs.string)
		page2 = requests.get(actual_url)
		second_level_page = BeautifulSoup(page2.content, 'html.parser')
		table = second_level_page.find_all('table')[0]
		rows = table.findAll("tr")

		with open(filename, "wt+", newline="") as f: 
			writer = csv.writer(f)
			for row in rows:
				csv_row = []
				for cell in row.findAll(["td", "th"]):
					csv_row.append(cell.get_text())
				writer.writerow(csv_row)

		print("CSV created > ", filename)




#table = soup.find_all('table')[0] 
#print(table.text.strip())

#-------------------------------------#
#    Write Table Content to CSV       #
#-------------------------------------#
#rows = table.findAll("tr")
#with open("editors.csv", "wt+", newline="") as f: 
#	writer = csv.writer(f)
#	for row in rows:
#		csv_row = []
#		for cell in row.findAll(["td", "th"]):
#			csv_row.append(cell.get_text())
#		writer.writerow(csv_row)


#--------------------------------------------------#
#    Ways to Find HTML TAGS and Pretty Print       #
#--------------------------------------------------#

#job_elems = results.find_all('tr', class_='data2')
#id = 0
#for job_elem in job_elems:
#	print(job_elem.text.strip())
    # Each job_elem is a new BeautifulSoup object.
    # You can use the same methods on it as you did before.
    #title_elem = job_elem.find('h2', class_='title')
    #company_elem = job_elem.find('div', class_='company')
    #location_elem = job_elem.find('div', class_='location')
    #meta = job_elem.find('div', class_='meta flex-col')
    #id += 1
    #print("<<Job", id, ">>")
    #if title_elem:
    #	print(title_elem.text.strip(), end=" ")
    #if company_elem:
    #	print(company_elem.text.strip(), end=" ")
    #if location_elem:
    #	print(location_elem.text.strip(), end=" ")
    #if meta:
    #	print(meta.text.strip(), end=" ")
    #print(end="\n\n")
#print(results.prettify())