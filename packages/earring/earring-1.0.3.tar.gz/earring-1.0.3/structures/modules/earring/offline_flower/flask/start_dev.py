

import earring.offline_flower.flask as offline_flower_flask

def start (
	port
):
	print ('starting')
	
	app = offline_flower_flask.build ()
	app.run (port = port)

	return;