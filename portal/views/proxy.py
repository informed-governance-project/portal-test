import http.client
from urllib.parse import urlencode

from flask import Blueprint
from flask import request
from flask import Response
from werkzeug.datastructures import Headers


# proxy_bp: blueprint doing the reverse proxy job
proxy_bp = Blueprint("proxy_bp", __name__, url_prefix="/")
# based on permissions users will be proxied to the appropirate Web service.


def check_login():
    pass


proxy_bp.before_request(check_login)


def iterform(multidict):
    for key in multidict.keys():
        for value in multidict.getlist(key):
            yield (key.encode("utf8"), value.encode("utf8"))


def parse_host_port(h):
    """Parses strings in the form host[:port]"""
    host_port = h.split(":", 1)
    if len(host_port) == 1:
        return (h, 80)
    else:
        host_port[1] = int(host_port[1])
        return host_port


@proxy_bp.route("/<host>/", methods=["GET", "POST"])
@proxy_bp.route("/<host>/<path:file>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_request(host, file=""):
    """The route which is actually doing the job of a reverse proxy."""
    hostname, port = parse_host_port(host)

    # Whitelist a few headers to pass on
    request_headers = {}
    for h in ["Cookie", "Referer", "X-Csrf-Token"]:
        if h in request.headers:
            request_headers[h] = request.headers[h]

    if request.query_string:
        path = f"/{file}?{request.query_string}"
    else:
        path = "/" + file

    if request.method == "POST":
        form_data = list(iterform(request.form))
        form_data_str = urlencode(form_data)
        request_headers["Content-Length"] = str(len(form_data_str))
    else:
        form_data = None

    conn = http.client.HTTPConnection(hostname, port)
    conn.request(request.method, path, body=form_data, headers=request_headers)
    resp = conn.getresponse()

    # Clean up response headers for forwarding
    response_headers = Headers()
    for key, value in resp.getheaders():
        if key in ["content-length", "connection", "content-type"]:
            continue

        if key == "set-cookie":
            cookies = value.split(",")
            [response_headers.add(key, c) for c in cookies]
        else:
            response_headers.add(key, value)

    # Prepare the contents
    contents = resp.read()

    flask_response = Response(
        response=contents,
        status=resp.status,
        headers=response_headers,
        content_type=resp.getheader("content-type"),
    )
    return flask_response
