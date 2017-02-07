import io
import pycurl
import stem.process
from stem.util import term

TOR_SOCKS_PORT = 9150

# Uses pycurl to fetch a site using the proxy on the SOCKS_PORT
def query(url):
	output = io.BytesIO()

	query = pycurl.Curl()
	query.setopt(pycurl.URL, url)
	query.setopt(pycurl.PROXY, 'localhost')
	query.setopt(pycurl.PROXYPORT, TOR_SOCKS_PORT)
	query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
	query.setopt(pycurl.WRITEFUNCTION, output.write)

	try:
		query.perform()
		return output.getvalue().decode('utf8')
	except pycurl.error as e:
		return "Unable to reach %s (%s)" % (url, e)

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

def kill_tor(p):
	p.kill()

def check_endpoint():
	print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
	#https://www.atagar.com/echo.php
	print(term.format(query("http://ip.cn/"), term.Color.BLUE))


if __name__ == '__main__':
	#process = launch_tor()
	check_endpoint()
	#kill_tor(process)