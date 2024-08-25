api_server:
fake_url: "https://workingapi.com"

middleware:
mitmproxy_urls:
- "https://localhost:8888"
- "http://localhost:8888"

fallback:
url: "http://localhost:3000"

handling_rules:
- condition: "If the API returns a 200 OK response"
  action: "Return the API's original response"
- condition: "If the API returns any other status code or fails to respond"
  action: "Redirect to the local mock server at https://localhost:3000/books"

objective: "Implement a network interceptor on a Linux system to manage API requests"

scenario:
description: "The system makes a request to an external API, such as https://workingapi.com"
uri: "https://workingapi.com/books"
response_handling:
- condition: "200 OK"
action: "Return the API's original response"
- condition: "Non-200 or no response"
action: "Redirect to local mock server at https://localhost:3000/books"

requirements:
environment: "Linux"
interceptor_behavior: "Seamlessly handle the request and redirection based on the API's response"

installation_steps:
- step: "Install Network Interceptor"
  commands:
    - "sudo pacman -S iptables"
    - "sudo pacman -S mitmproxy"

script_execution:
description: "Run the script"
command: "mitmproxy -s index.py --listen-port 8888 --target-host workingapi.com --fallback-host localhost --fallback-port 3000"

https_handling:
generate_certificate:
description: "Generate the certificate"
command: "mitmproxy --mode regular"
cert_location: "~/.mitmproxy"
install_certificate:
description: "Install the certificate system-wide"
commands:
- "sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /etc/ca-certificates/trust-source/anchors/mitmproxy-ca-cert.pem"
- "sudo update-ca-trust"

fake_dns_entry:
description: "Add a Fake DNS Entry for workingapi.com"
steps:
- "Edit the /etc/hosts file: sudo nano /etc/hosts"
- "Add the entry: 127.0.0.2 workingapi.com"

iptables_update:
http:
description: "Update iptables for HTTP"
command: "sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -d 127.0.0.2 -j REDIRECT --to-ports 3000"
https:
description: "Update iptables for HTTPS"
command: "sudo iptables -t nat -A OUTPUT -p tcp --dport 443 -d 127.0.0.2 -j REDIRECT --to-ports 8888"

