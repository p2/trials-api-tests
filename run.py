#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# documentation: https://clinicaltrials.gov/ct2/resources/download

import sys
import time
import random
import requests
import xml.etree.ElementTree as ET


_base_ctgov = 'https://clinicaltrials.gov/ct2/show/'


def get_trial_nct(nct):
	url = _base_ctgov + nct
	res = requests.get(url, {'resultsxml': 'true'})
	if res.status_code < 400:
		return ET.fromstring(res.text)
	return None

def compare_countries(trial):
	nct = trial.find('id_info/nct_id').text
	has_countries = set([c.text for c in trial.findall('location_countries/country')])
	wants_countries = set([c.text for c in trial.findall('location/facility/address/country')])
	if has_countries != wants_countries:
		if wants_countries < has_countries:
			print("--->  {} `location/facility` is missing countries, needs {} but has only {}"
				.format(nct, has_countries, wants_countries))
		else:
			print("<---  {} `location_countries` is missing countries, has {} but in facilities found {}"
				.format(nct, has_countries, wants_countries))
	else:
		print("      {} `location/facility` and `location_countries` are in sync".format(nct))

def rand_nct():
	return 'NCT{:08}'.format(random.randrange(1, 2999999))


def main(argv):
	if True:
		t = get_trial_nct('NCT02895360')
		print("-->  location data")
		for l in t.findall('location'):
			ET.dump(l)
		print("---  ^")
		compare_countries(t)
		return
	
	i = 0
	while i < 1000:
		nct = rand_nct()
		t = get_trial_nct(nct)
		if t is not None:
			i += 1
			compare_countries(t)
			time.sleep(1)


if '__main__' == __name__:
	main(sys.argv)

{
	"facility": {
		"name": str,
		"address": {
			"street": str,
			"city": str,
			"zip": str,
			"country": str
		},
		"location": "{lat}, {lon}",
		"status": str,
		"contact": [
			{
				"use": str,
				"name": str,
				"phone": str,
				"email": str
			}
		]
	}
}
