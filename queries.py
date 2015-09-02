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

	r = requests.get("http://library.mit.edu/rest-dlf/record/mit01" + file_id + "?view=full")
	metadata = r.content

	record = ET.fromstring(metadata).find('record')

	## Searching in Python 2.7
	# try:
	# 	title = record.find("./datafield[@tag='245']/*[@code='a']").text
	# 	title = title.rstrip('/ ')
	# 	RESULTS['Title'] = title
	# except:
	# 	RESULTS['Error'] = 'Item not found.'

	# try:
	# 	author = record.find("./datafield[@tag='245']/*[@code='c']").text
	# 	author = author.rstrip('. ')
	# 	RESULTS['Author'] = author
	# except:
	# 	pass
		

	# Workaround searching for Python 2.6
	# try:
	fields = record.findall("./datafield")
	for field in fields:
			title = get_field_value(field, '245', 'a')
			subtitle = get_field_value(field, '245', 'b')
			if title:
				title = title.rstrip('/ ')
				if subtitle:
					title += subtitle
				RESULTS['Title'] = title

			author = get_field_value(field, '100', 'a')
			if author:
				author = author.rstrip('. ')
				RESULTS['Author'] = author

			edition = get_field_value(field, '250', 'a')
			if edition:
				RESULTS['Edition'] = edition

			# pub_info = get_field_value(field, '260',)

			series = get_field_value(field, '830', 'a')
			series_num = get_field_value(field, '830', 'v')
			if series:
				if series_num:
					series += series_num
				RESULTS['Series'] = series

			isbn = get_field_value(field, '020', 'a')
			if isbn:
				RESULTS['ISBN'] = isbn

			issn = get_field_value(field, '022', 'a')
			if issn:
				RESULTS['ISSN'] = issn
			
	# except:
	# 	RESULTS['Error'] = 'Item not found.'

	return RESULTS

def get_field_value(parent, marc_field, subcode):
	if parent.attrib.get('tag') == marc_field:
		fieldElements = parent.getchildren()
		for item in fieldElements:
			if item.attrib.get('code') == subcode:
				field_value = item.text
				return field_value
	else:
		return False
