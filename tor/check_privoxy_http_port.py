import requests

# privoxy proxy port
proxy_port = 8118

# generate http session
s = requests.Session()
s.proxies = {
	"http": "http://127.0.0.1:%d" % proxy_port
}

# make http request
#r = s.get("http://www.google.com")
r = s.get("https://www.atagar.com/echo.php")
print(r.text)