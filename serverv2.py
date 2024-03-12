from http.server import HTTPServer, BaseHTTPRequestHandler
import multiprocessing
from urllib.parse import unquote
import time
import re
from barcode_gen import Barcode128

from myconfig import Config
from send_to_printer import print_tiff_file

def parserequest(test_str):
    regex = r"(((\S+?)=(\S+?))&)|(((\S+?)=(\S+?))$)"
    parsedtxt = {}
    for matches in re.findall(regex, test_str[2:], re.DOTALL):
        #print(matches)
        if matches[0]:
            parsedtxt[matches[2]] = matches[3]
        else:
            parsedtxt[matches[6]] = matches[7]
    #print(parsedtxt)
    return parsedtxt

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip, client_port = self.client_address
        self.server.message_queue.put(f"Запит на друк від клієнта: {client_ip}")
        self.config = Config()

        if self.path[1] == "?":
            pval = parserequest(self.path)
            #txt1 = hexdecode(pval.get('txt1'))
            txt1 = unquote(pval.get('txt1'))
            #txt2 = hexdecode(pval.get('txt2'))
            txt2 = unquote(pval.get('txt2'))
            print("Start print: ", txt1, txt2)
            #print_barcode('321231324564654',"Бел. 840/42",40,25)
            # print_barcode(txt1, txt2, 39, 25)
            label_size = self.config.data.get('label_size')
            printer_dpi = self.config.data.get('printer_dpi')
            selected_printer = self.config.data.get('selected_printer')

            width = int(label_size[0]/25.4*printer_dpi)
            heigth = int(label_size[1]/25.4*printer_dpi)
            bc = Barcode128(txt1, text=txt2, bcsize=(width, heigth))
            bc.save()
            print_tiff_file(bc.filename, selected_printer)
            print(txt1, txt2)

        self.server.message_queue.put(f"Друкуємо бірку: '{txt1}, {txt2}'")

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes('{"result":"ok"}', "utf-8"))


class ServerProcess(multiprocessing.Process):
    def __init__(self, message_queue):
        super(ServerProcess, self).__init__()
        self.message_queue = message_queue
        self.config = Config()

    def run(self):
        server_address = (self.config.data.get('addr'), self.config.data.get('port'))
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.message_queue = self.message_queue  # Передаем очередь в сервер
        self.message_queue.put(f"Сервер запущено за адресою: {server_address[0]}:{server_address[1]}")
        httpd.serve_forever()

class BGServer():
    def __init__(self):
        print('try to start server')
        self.message_queue = multiprocessing.Queue()
        self.server_process = ServerProcess(self.message_queue)
        self.server_process.start()
        print('server started')

    def stop_server(self):
        self.server_process.terminate()
        self.server_process.join()
    
    def get_queue(self):
        try:
            message = f"{self.message_queue.get_nowait()}\n"
        except:
            message = None
        return message
    

if __name__ == '__main__':

    serv = BGServer()
    # Отправляем сообщения серверу через очередь
    for i in range(50):
        time.sleep(0.5)
        message = serv.get_queue()
        if message:
            print("Got message:", message)

    serv.stop_server()
