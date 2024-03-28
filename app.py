from flask import request, Response, Flask
import requests
import json

with open("config.json") as f:
    config = json.load(f)

app = Flask('__main__')
app.config['SERVER_NAME'] = f"{config.get('ip')}:{config.get('port')}"

ref = config.get("redirection")

@app.route('/') 
def home():
    page = ""
    for name in ref.keys():
        page+=f"<a href=http://{name}.{app.config['SERVER_NAME']}>{name}</a>\n"
    return page

methods = ["GET", "POST", "HEAD", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]
def register(subdomain, sitename):
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

        res = requests.request(method=request.method, url=f'{sitename}/{path}{parse_arg(request.args)}',
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True,
            headers={"User-Agent":request.headers.get("User-Agent")}
        )
        print(f"\n\nInitial request : \nurl : {request.url}\nargs : {request.args}\ncookies : {request.cookies}")
        print(f"Redirected to :\nurl : {sitename}/{path}{parse_arg(request.args)}\nresponse code : {res.status_code}")
            
        response = Response(res.content, res.status_code, fix_hearders(res.headers))

        for key, cookie in res.cookies.get_dict().items():
            response.set_cookie(key, cookie)
            print(f"cookies set : {key}:{cookie}")
        return response

if __name__ == '__main__':
    for sub, site in ref.items():
        register(sub, site)
    app.run(host=config.get("ip"), port=config.get("port"))
