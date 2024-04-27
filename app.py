from flask import request, Response, Flask
from flask_sock import Sock
import requests
import json
import websocket

with open("config.json") as f:
    config = json.load(f)

app = Flask('__main__')
app.config['SERVER_NAME'] = f'{config.get("domain")}'
socket = Sock(app)
ref = config.get("redirection")

@app.route('/', subdomain=config.get("subdomain")) 
def home():
    page = ""
    for name in ref.keys():
        page+=f"<a href=http://{name}.{config.get('domain')}>{name}</a>\n"
    return page

methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
def register(subdomain, data):
    protocole = data.get("protocole")
    domain = data.get("domain")
    have_ws = data.get("websocket")

    if have_ws:
        @socket.route("/ws", subdomain=subdomain)
        def handle_connect(ws):

            def on_message(sws, message):
                ws.send(message)

            def on_error(sws, error):
                print(error)

            def on_close(sws, close_status_code, close_msg):
                ws.close()

            def on_open(sws):
                print("Server connected")

            print('Client connected')
            # Ouvrir une connexion WebSocket avec le serveur distant
            ws_url = f"ws://{domain}/ws"
            sws = websocket.WebSocketApp(ws_url,
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            
            sws.run_forever()
            while True:
                try:
                    client_data = ws.recv()
                    sws.send(client_data)
                except Exception:
                    sws.close()
                    ws.close()
                    break

    @app.route('/', defaults={'path': ''}, methods=methods, subdomain=subdomain, endpoint=subdomain) 
    @app.route('/<path:path>', methods=methods, subdomain=subdomain, endpoint=subdomain)
    @app.route('/static/<path:path>', methods=methods, subdomain=subdomain, endpoint=subdomain)
    def redirect_to_API_HOST(path):

        def parse_arg(args):
            if args:
                formated = "?"
                for key, val in args.items():
                    formated+=f"{key}={val}&"
                return formated
            else:
                return ""
            
        def fix_hearders(initial_headers):
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', 'Host']
            headers = [
            (k,v) for k,v in initial_headers.items()
            if k.lower() not in excluded_headers
        ]
            return headers

        res = requests.request(method=request.method, url=f'{protocole}{domain}/{path}{parse_arg(request.args)}',
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True,
            headers={"User-Agent":request.headers.get("User-Agent")}
        )
        print(f"\n\nInitial request : \nurl : {request.url}\nargs : {request.args}\ncookies : {request.cookies}")
        print(f"Redirected to :\nurl : {protocole}{domain}/{path}{parse_arg(request.args)}\nresponse code : {res.status_code}")
            
        response = Response(res.content, res.status_code, fix_hearders(res.headers))

        for key, cookie in res.cookies.get_dict().items():
            response.set_cookie(key, cookie)
            print(f"cookies set : {key}:{cookie}")
        return response

if __name__ == '__main__':
    for sub, data in ref.items():
        register(sub, data)
    app.run(host=config.get("ip"), port=config.get("port"), debug=True)
