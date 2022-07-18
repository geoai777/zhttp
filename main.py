from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from os.path import isfile, split, join as pjoin

from freq import SensorData
from render import RenderGames

from json import dumps
from datetime import datetime

import logging

class H(BaseHTTPRequestHandler):
    def _set_response(self, data_type: str="html"):
        self.send_response(200)
        if data_type == "json":
            self.send_header('Content-type', 'text/json')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.debug('started')

        # Here we generate data and send it to client.
        if 'data' in self.path:
            self._set_response("json")
            sd = SensorData()
            html_ready = (dumps(
                [
                    sd.gpu_freq(),
                    sd.cpu_freq(),
                    sd.get_thermal()
                ], indent=4
            ))
        elif 'time' in self.path:
            self._set_response("json")
            html_ready = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        else:
            self._set_response()
            template_path = pjoin('html', 'template.html')
            style_path = pjoin('html', 'style.css')
            rg = RenderGames()
            body = ""
            html_ready = rg.merge_template(template_path, style_path, 'System stats')

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

