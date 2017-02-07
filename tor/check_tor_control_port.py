import getpass
import sys

import stem
import stem.connection
from stem.control import Controller

CONTROL_PORT = 9151

if __name__ == '__main__':
	# connect tor control socket
	try:
		controller = Controller.from_port(port=CONTROL_PORT)
	except stem.SocketError as e:
		print("Unable to connect to tor on port %d: %s" % (CONTROL_PORT, e))
		sys.exit(1)

	# authenticate tor control socket
	try:
		controller.authenticate()
	except stem.connection.MissingPassword:
		pw = getpass.getpass("Tor ControllerPort Password: ")
		try:
			controller.authenticate(password=pw)
		except stem.connection.PasswordAuthFailed:
			print("Unable to authenticate, password is incorrect")
			sys.exit(1)
	except stem.connection.AuthenticationFailure as e:
		print("Unable to authenticate: %s" % e)
		sys.exit(1)
	except Exception as e:
		print("Wrong")
		sys.exit(1)

	print("Tor is running version %s" % controller.get_version())
	controller.close()