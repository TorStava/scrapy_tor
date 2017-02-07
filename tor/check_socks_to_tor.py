import socks # SocksiPy module
import socket
import urllib.request
import stem.process
from stem.util import term

TOR_SOCKS_PORT = 9150

def set_socks_proxy():
	try:
		# Set socks proxy
		socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', TOR_SOCKS_PORT)
		socket.socket = socks.socksocket

		# Perform DNS resolution through the socket 
		def getaddrinfo(*args):
			return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
		socket.getaddrinfo = getaddrinfo
	except:
		raise Exception("Socks proxy is incorrect")

# Uses urllib to fetch a site using SocksiPy for Tor over the TOR_SOCKS_PORT
def query(url):
	try:
		return urllib.request.urlopen(url).read()
	except:
		return "Unable to reach %s " % url

# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.
def launch_tor():
	print(term.format("Starting Tor:\n", term.Attr.BOLD))
	def print_bootstrap_lines(line):
		if "Bootstrapped " in line:
			print(term.format(line, term.Color.BLUE))
	return stem.process.launch_tor_with_config(
		config={
			'SocksPort': str(TOR_SOCKS_PORT),
			'ExitNodes': '{ru}', # tor proxy exit node in the country Russia
		},
		init_msg_handler = print_bootstrap_lines,
	)

def check_endpoint():
	print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
	print(term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE))

def kill_tor(p):
	p.kill()

if __name__ == '__main__':
	set_socks_proxy()
	#process = launch_tor()
	#check_endpoint()
	#kill_tor(process)
	# https://www.atagar.com/echo.php
	print(query("http://icanhazip.com/"))