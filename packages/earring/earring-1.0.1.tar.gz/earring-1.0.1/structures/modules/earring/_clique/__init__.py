




from earring._clique.group import clique as clique_group

from earring.offline_flower.clique import clique as offline_flower_clique
from earring.online_flower.clique import clique as online_flower_clique


from earring.modules.vibes.clique import clique as vibes_clique

def clique ():

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("example")
	def example_command ():	
		print ("example")

	group.add_command (example_command)

	group.add_command (offline_flower_clique ())
	group.add_command (online_flower_clique ())
	
	group.add_command (vibes_clique ())
	
	
	group ()




#
