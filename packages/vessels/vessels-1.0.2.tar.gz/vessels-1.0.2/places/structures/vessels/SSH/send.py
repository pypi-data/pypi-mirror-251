
'''
	import vessels.SSH.send as SSH_send
	
	from os.path import dirname, join, normpath
	import pathlib
	import sys

	this_directory = pathlib.Path (__file__).parent.resolve ()
	from_directory = normpath (join (this_directory, "../platform"))
	
	SSH_send.splendidly ({
		"private key": "/online ellipsis/vegan/DO/vegan/RSA.private",
		
		"from": {
			"directory": from_directory,
			"exclude": []
		},
		
		"to": {
			"address": "164.92.112.195",
			"directory": "/platform"
		},
		
		"return script": "yes"
	})
'''
import os

def splendidly (parameters):
	private_key = parameters ["private key"]

	from_directory = parameters ["from"] ["directory"]
	
	exclude_script = ""
	if ("exclude" in parameters ["from"]):
		exclude_ = parameters ["from"] ["exclude"]
		
		for exclusion in exclude_:
			exclude_script += f'--exclude "{ exclusion }"'

	to_directory = parameters ["to"] ["directory"]
	to_address = parameters ["to"] ["address"]

	script = " ".join ([
		"rsync",
		"-r",
		"-a",
		"--info=progress2",
		"-v",
		"--delete",
		"--delete-excluded",
		"--progress",
		"--human-readable",
		"--mkpath",
		
		exclude_script,
		
		f"""
			-e "ssh -o StrictHostKeyChecking=no -i '{ private_key }'"
		""".strip (),
		
		f'{ from_directory }/',
		f"root@{ to_address }:{ to_directory }"
	])

	print (script);

	if (
		"return script" in parameters and 
		parameters ["return script"] == "yes"
	):
		return script
	
	

	os.system (script)
	
	