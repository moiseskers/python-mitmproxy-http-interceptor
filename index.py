import os
import logging
from mitmproxy import http

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

TARGET_HOST = os.getenv('TARGET_HOST', 'workingapi.com')
FALLBACK_HOST = os.getenv('FALLBACK_HOST', 'localhost')
FALLBACK_PORT = int(os.getenv('FALLBACK_PORT', 3000))

def request(flow: http.HTTPFlow) -> None:
    logging.debug(f"Request - Host: {flow.request.pretty_host}, Path: {flow.request.path}, Scheme: {flow.request.scheme}")

    if flow.request.pretty_host == TARGET_HOST:
        logging.info(f"Intercepting request to {TARGET_HOST} and redirecting to {FALLBACK_HOST}:{FALLBACK_PORT}")
        flow.request.host = FALLBACK_HOST
        flow.request.port = FALLBACK_PORT
        flow.request.scheme = "http"

def response(flow: http.HTTPFlow) -> None:
    logging.debug(f"Response - Host: {flow.request.host}, Path: {flow.request.path}, Status Code: {flow.response.status_code}")

    # Add a custom header to the response
    flow.response.headers["X-Custom-Header"] = "Intercepted by mitmproxy"

    if flow.request.host == FALLBACK_HOST and flow.response.status_code != 200:
        logging.info(f"Fallback to {TARGET_HOST} for request path: {flow.request.path}")
        flow.request.host = TARGET_HOST
        flow.request.port = 443
        flow.request.scheme = "https"
        flow.resume()  # Continue with the request to TARGET_HOST
