import os
import requests
import xml.etree.ElementTree as ET
from string import index

def get_filetypes(file_id):
	RESULTS = []

	base_path = os.path.dirname(os.path.abspath(__file__))
	files_path = os.path.join(base_path, 'static/files')
	files = os.listdir(files_path)

	for file in files:
		i = file.index('.')
		file_name = file[:i]
		file_type = file[i+1:]
		
		if file_name == file_id:
			RESULTS.append(file_type)

	return RESULTS

def get_metadata(file_id):
	RESULTS = {}

	r = requests.get("http://walter.mit.edu/rest-dlf/record/mit01" + file_id + "?view=full")
	metadata = r.content

	record = ET.fromstring(metadata).find('record')
	title = record.find("./datafield[@tag='245']/*[@code='a']").text
	author = record.find("./datafield[@tag='245']/*[@code='c']").text	

	title = title.rstrip('/ ')
	author = author.rstrip('. ')

	RESULTS['title'] = title
	RESULTS['author'] = author

	return RESULTS
