from flask import Flask,redirect,request
try:
    from bowser import urlcheck # pylint: disable=import-error
except Exception:
    from bowser.bowser import urlcheck

from waitress import serve


app = Flask(__name__)



@app.route('/')
def redict_url():
    url = request.args['url']
    uchecker_result = urlcheck(url)
    return uchecker_result

def runbowser():
    serve(app=app,port=54422,threads=100)


if __name__ == "__main__":
    app.run(port=54422)
