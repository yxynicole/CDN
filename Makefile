all: 
		echo 'python3 http/server.py "$$@"' > httpserver && chmod +x httpserver
		echo 'python3 dns/server.py "$$@"' > dnsserver && chmod +x dnsserver
clean:
		rm -f httpserver dnsserver
