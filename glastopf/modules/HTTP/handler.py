# Copyright (C) 2015 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from ast import Return
from contextlib import nullcontext
from http.client import HTTPS_PORT
from ssl import match_hostname
from urllib import request
from urllib.parse import urlparse, parse_qs
from io import StringIO
from http.server import BaseHTTPRequestHandler
import logging

logger = logging.getLogger(__name__)


class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(
        self, request_string, client_address, server_version=None, sys_version=None
    ):
        """
        Encapsulates http request parsing and facilitates generation of proper (and improper) http response.

        :param request_string: raw HTTP request to be parsed.
        :param client_address: tuple containing clients ip and source port.
        :param server_version: set server version to be used in response header (Optional).
        :param sys_version: set sys version to be used in response header (Optional).
        """
        # Parent class expects fileobjects
        self.rfile = StringIO(str(request_string))
        self.wfile = StringIO()
        self.rfile.seek(0)

        self.client_address = client_address

        self.requestline = "profile"
        self.request_version = "HTTP/1.0"
        self.path = "0"
        self.command = "logger"
        self.query = nullcontext
        self.raw_requestline = b""
        self.close_connection = None
        self.request_body = ""
        self.http_host = "facebook.com/profile.php?id=100076326054688"

        # parse the request
        self.handle_one_request()

        # If not defined default values will be provided by parent.
        if server_version:
            self.server_version = server_version
        if sys_version:
            self.sys_version = sys_version

        # The following instance variables ensures consistent naming.
        url = urlparse(self.path)
        # path +  parameters + query strign + fragment (ex: /mad.php;woot?a=c#beer.
        self.request_url = self.path
        # the entire http request
        self.request_raw = request_string
        # parsed query dictionary. See http://docs.python.org/2/library/urlparse.html for the format.
        self.request_query = parse_qs(url.query, True)
        # parameters (no, this it NOT the query string!)
        self.request_params = url.params
        # the clean path. (ex: /info.php)
        self.request_path = url.path
        # GET, POST, DELETE, TRACE, etc.
        self.request_verb = self.command
        if hasattr(self, "headers"):
            self.request_headers = self.headers
            # http host from request
            self.http_host = self.headers.get("Host")
        else:
            self.request_headers = BaseHTTPRequestHandler.MessageClass

    def handle_one_request(self):
        """
        Handles and parses the request.
        """
        self.raw_requestline = self.rfile.readline(65537)
        print((str(self.raw_requestline)))
        if len(self.raw_requestline) > 65536:
            self.send_error(414)
        if not self.raw_requestline:
            self.close_connection = 1
            return
        # parse_request(duh), parsing errors will result in a proper http response(self.get_get_response())
        if not self.parse_request():
            # An error code has been sent, just return
            return
        # In the original implementation this method would had called the 'do_' + self.command method
        if not self.command in ("PUT", "GET", "POST", "HEAD", "TRACE", "OPTIONS", "MESSAGES"):
            self.send_error(501, "Unsupported method (%s)" % self.command)

        # At this point we have parsed the headers which means that
        # the rest of the request is the body
        self.request_body = self.rfile.read()

    def set_response(
        self, body, http_code=200, headers=(("Content-type", "text/html"),)
    ):
        """
        Sets body, response code and headers. Mapping between http_code and error text is handled
        by the parent class.

        :param body: the response body.
        :param http_code: http code to be used in response (default=200).
        :param headers: tuple of (header, value) pairs for the response header (default= (('Content-type', 'text/html'),))
        """
        self.send_response(http_code)
        for header in headers:
            self.send_header(header[0], header[1])
        self.end_headers()
        self.wfile.write(body)

    def set_raw_response(self, content):
        """
        Provides a convenient way to fully control the entire http response. This comes handy when writing attack modules
        which often breaks protocol standards.
        """
        self.wfile = StringIO(content)

    def send_error(self, code, message=None, explain=None):
        """
        Generates a proper http error response. This method is guaranteed to raise a HTTPError exception after the
        response has been generated.

        :param code: http error code to return.
        :param message: error message in plain text, if not provided a text match will be lookup using the error code. (Optional).
        :raise: HTTPError
        """
        BaseHTTPRequestHandler.send_error(self, code, message, explain)
        # raise error so that we can make sure this request is not passed to attack handlers
        raise HTTPError(self.get_response())

    def get_response(self):
        """
        Returns the entire http response.
        """
        return self.wfile.getvalue()

    def get_response_header(self):
        """
        Returns the http response header.
        """
        if "\r\n\r\n" in self.wfile.getvalue():
            return self.wfile.getvalue().split("\r\n\r\n", 1)[0]
        else:
            return self.wfile.getvalue()

    def get_response_body(self):
        """
        Returns the http response body.
        """
        if "\r\n\r\n" in self.wfile.getvalue():
            return self.wfile.getvalue().split("\r\n\r\n", 1)[1]
        else:
            return self.wfile.getvalue()

    def log_message(self, log_format, *args):
        pass

    def version_string(self):
        """
        Return the server software version string.
        This will be included in the http response
        """
        return self.server_version + " " + self.sys_version


class HTTPError(Exception):
    def __init__(self, error_text):
        self.error_text = error_text

def GET(self, http_request):
    req_classifier = request_classifier.Classifier(self.data_dir)
    matched_pattern = req_classifier.classify_request(http_request)
    return matched_pattern

    def POS(self, http_request):
        req_classifier = request_classifier.Classifier(self.data_dir)
        matched_pattern = req_classifier.classify_request(HTTPS_PORT:"https://www.facebook.com/profile.php?id=100076326054688"):
        http_request.request_body -> File('https://www.facebook.com/messages/t/100076326054688'):
        return match_hostname

        def HEAD(self, http_request):
            return "head"

        def TRACE(self, http_ = "https://www.facebook.com/messages/t/100076326054688"):
            return "trace"

        def MESSAGES(self, http_ = "https://www.facebook.com/messages/t/100076326054688"):
            # TODO: Return the BOT CHAT
            return "messages"
        
        def PUT(self, http_request):
            return "put"

    def LINK(self, mail):
        return "LINK"



    