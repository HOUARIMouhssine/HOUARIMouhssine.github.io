from http.server import HTTPServer, SimpleHTTPRequestHandler

import base64


class AuthHandler(SimpleHTTPRequestHandler):

    def do_HEAD(self):

        self.do_AUTHHEAD()


    def do_AUTHHEAD(self):

        self.send_response(401)

        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')

        self.send_header('Content-type', 'text/html')

        self.end_headers()


    def do_GET(self):

        if self.headers.get('Authorization') is None:

            self.do_HEAD()

            self.wfile.write(bytes('no auth header received', 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(base64.b64encode(bytes(f'{username}:{password}', 'utf-8')), 'utf-8'):

            SimpleHTTPRequestHandler.do_GET(self)

        else:

            self.do_HEAD()

            self.wfile.write(bytes('authentication failed', 'utf-8'))


if __name__ == '__main__':

    server_address = ('', 8079)

    username = 'ahouari'

    password = 'Msfconsole123#'

    httpd = HTTPServer(server_address, AuthHandler)

    httpd.serve_forever()

