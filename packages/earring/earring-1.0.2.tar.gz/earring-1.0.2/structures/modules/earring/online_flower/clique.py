



import earring.offline_flower.flask.start_dev as flask_start_dev

def clique ():
	import click
	@click.group ("online_flower")
	def group ():
		pass

	'''
		./earring online_flower start --port 43123
	'''
	import click
	@group.command ("start")
	@click.option ('--port', '-p', default = '55500')
	def search (port):		
		flask_start_dev.start (
			port = int (port)
		)
	
		return;

	return group




#



