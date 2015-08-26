import os
import requests
import xml.etree.ElementTree as ET
from string import index

def get_filenames(file_id):
	RESULTS = []

	base_path = os.path.dirname(os.path.abspath(__file__))
	files_path = os.path.join(base_path, 'static/files')
	files = os.listdir(files_path)

	for f in files:
		try:
			p = f.index('.')
			item_name = f[:p]
		except:
			pass

		try:
			i = f.index('_')
			item_name = f[:i]
		except:
			pass
		
		if item_name == file_id:
			RESULTS.append(f)

	return RESULTS

def get_metadata(file_id):
	RESULTS = {}

	r = requests.get("http://walter.mit.edu/rest-dlf/record/mit01" + file_id + "?view=full")
	metadata = r.content

	record = ET.fromstring(metadata).find('record')

	try:
		title = record.find("./datafield[@tag='245']/*[@code='a']").text
		title = title.rstrip('/ ')
		RESULTS['Title'] = title
	except:
		RESULTS['Error'] = 'Item not found.'

	try:
		author = record.find("./datafield[@tag='245']/*[@code='c']").text
		author = author.rstrip('. ')
		RESULTS['Author'] = author
	except:
		pass
		

	## Workaround searching for Python 2.6
		# fields = record.findall("./datafield")
		# for field in fields:
		# 	if field.attrib.get('tag') == '245':
		# 		titleElements = field.getchildren()
		# 		for item in titleElements:
		# 			if item.attrib.get('code') == 'a':
		# 				title = item.text
		# 			if item.attrib.get('code') == 'c':
		# 				author = item.text

	return RESULTS