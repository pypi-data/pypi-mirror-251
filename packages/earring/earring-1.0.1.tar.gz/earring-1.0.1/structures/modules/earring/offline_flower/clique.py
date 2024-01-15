



import earring.offline_flower.flask.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("offline_flower")
	def group ():
		pass

	'''
		./earring offline_flower start --port 43123
	'''
	import click
	@group.command ("start")
	@click.option ('--port', '-np', default = '43123')
	def search (port):		
		flask_start_dev.start (
			port = int (port)
		)
	
		return;

	return group




#



