



def scan_file (path):
	with open (path, mode = 'r') as selector:
		return selector.read ()

def build_scan_string (path):
	contents = scan_file (path)
	contents += '''
		
try:
	______unions ["checks"] = checks;	
	______unions ["checks FOUND"] = True;
except Exception as E:
	print (E)
	______unions ["checks FOUND"] = False;
		'''

	return contents


import unions.functions.exceptions as bs_exceptions

import json
import time
from time import sleep, perf_counter as pc


def start (FIND):
	# path = {}
	
	FINDINGS = []
	stats = {
		"passes": 0,
		"alarms": 0
	}

	path_E = ""

	try:
		CONTENTS = build_scan_string (FIND)
		
		______unions = {}
		exec (
			CONTENTS, 
			{ 
				'______unions': ______unions,
				'__file__': FIND
			}
		)
		

		if (______unions ["checks FOUND"] == False):
			return {
				"empty": True,
				"parsed": True
			}

		
		checks = ______unions ['checks']		

		
		for check in checks:
			try:
				TIME_START = pc ()
				checks [ check ] ()
				TIME_END = pc ()
				TIME_elapsed = TIME_END - TIME_START

				FINDINGS.append ({
					"check": check,
					"passed": True,
					"elapsed": [ TIME_elapsed, "seconds" ]
				})
				
				stats ["passes"] += 1
				
			except Exception as E:				
				FINDINGS.append ({
					"check": check,
					"passed": False,
					"exception": repr (E),
					"exception trace": bs_exceptions.find_trace (E)
				})
				
				stats ["alarms"] += 1
		
		
		return {
			"empty": False,
			"parsed": True,
						
			"stats": stats,			
			"checks": FINDINGS
		}
		
	except Exception as E:		
		path_E = E;

	return {
		"parsed": False,
		"alarm": "An exception occurred while scanning the path.",
		"exception": repr (path_E),
		"exception trace": bs_exceptions.find_trace (path_E)
	}