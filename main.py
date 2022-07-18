from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from os.path import isfile, split, join as pjoin

from freq import SensorData
from render import RenderGames

import logging

class H(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.debug('started')
        self._set_response()

        # Here we generate data and send it to client.
        if 'data' in self.path:
            print('Get data')
        template_path = pjoin('html', 'template.html')
        style_path = pjoin('html', 'style.css')
        sd = SensorData()
        rg = RenderGames()
        body = ""
        for l in [sd.gpu_freq(), sd.cpu_freq(), sd.get_thermal()]:
            body += rg.render_list(l)
            html_ready = rg.merge_template(template_path, style_path, body, 'System stats')


        self.wfile.write(bytes(html_ready, "UTF-8"))


def main():
    logging.basicConfig(
            level=logging.DEBUG,
            format="[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
    )
    host = '192.168.10.250'
    port = 8080

    try:
        httpd = HTTPServer((host, port), H)
        logging.info(f'HTTP server started on {host}:{port}')
        httpd.serve_forever()

    except KeyboardInterrupt:
        logging.info('Keyboard interrput, server stopped')
        httpd.socket.close()

if __name__ == '__main__':
    main()

