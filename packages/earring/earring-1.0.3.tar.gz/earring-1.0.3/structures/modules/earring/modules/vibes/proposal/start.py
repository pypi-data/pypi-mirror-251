


'''
	seed = "4986888b11358bf3d541b41eea5daece1c6eff64130a45fc8b9ca48f3e0e02463c99c5aedc8a847686d669b7d547c18fe448fc5111ca88f4e8"

	import earring.modules.vibes.proposal.start as start_proposal_vibes
	start_proposal_vibes.decisively (
		seed = seed,
		
		proceeds_proposal_popularity_vibe = "",
		proceeds_proposal_essence_vibe = "",		
		proceeds_seed_path = ""
	)
'''

import earring.modules.ED448.private.creator as ED448_private_key_creator
import earring.modules.ED448.public.creator as ED448_public_key_creator
	
import os
def write_seed (path, seed_string):
	if (os.path.exists (path)):
		raise Exception (f"The path for the seed_string is not available. '{ path }'");
	
	#f = open (path, 'wb')
		
	f = open (path, 'w')

	f.write (seed_string)
	f.close ()
	
	return True	
	
def decisively (
	seed = "",
	
	#format = "PEM",
	format = "DER",
	#format = "raw",
	#format = "bytes",
	
	proceeds_proposal_popularity_vibe = "",
	proceeds_proposal_essence_vibe = "",	
	
	proceeds_seed_path = ""
):	
	private_key = ED448_private_key_creator.create (
		seed, 
		format, 
		proceeds_proposal_essence_vibe
	)
	
	#private_key_instance = private_key ["instance"]
	#private_key_string = private_key ["string"]
	
	public_key = ED448_public_key_creator.create (
		private_key_path = proceeds_proposal_essence_vibe,
		public_key_path = proceeds_proposal_popularity_vibe,
		
		public_key_format = format
	)
	#public_key_instance = public_key ["instance"]
	#public_key_string = public_key ["string"]
	
	write_seed (proceeds_seed_path, seed)