
'''
	python3 insurance.proc.py "modules/vibes/proposal/status_1.py"
'''

from os.path import dirname, join, normpath
import pathlib
import sys
import os

import earring.modules.vibes.proposal.start as start_proposal_vibes

import shutil


def erase_directory (directory_path):
	try:
		shutil.rmtree (directory_path)
	except Exception:
		pass;

def check_1 ():
	seed = "4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8"

	this_directory = pathlib.Path (__file__).parent.resolve ()
	_status_temporary_directory = normpath (join (this_directory, "_status_temporary/1"))
	
	erase_directory (_status_temporary_directory)
	os.mkdir (_status_temporary_directory)

	start_proposal_vibes.decisively (
		seed = seed,
		
		proceeds_proposal_popularity_vibe = normpath (join (_status_temporary_directory, "proposal_vibe.popularity")),
		
		proceeds_proposal_essence_vibe = normpath (join (_status_temporary_directory, "proposal_vibe.essence")),
		proceeds_seed_path = normpath (join (_status_temporary_directory, "proposal.seed"))
	)
	
	#erase_directory (_status_temporary_directory)

	return;
	
checks = {
	'check 1': check_1
}