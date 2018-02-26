'''
    Main function that gets a request from the app and the calls
    the app_handler function

'''
#flask and jsonify necessary to create and run server and convert dict to JSON
from flask import Flask
from flask import jsonify

#import handler code
import app_handler 

#create Flask app
app = Flask(__name__)

@app.route('/name/<username>')
def tiltify(username):
    whoseteam = username[:5]

    #rint(whoseteam)

    username = username[5:]
    
   # print(username)

    toSend = app_handler.app_handler(username, whoseteam)

    toSend = jsonify(toSend)

    return toSend


if __name__ == "__main__":
    app.run(host='', port=8080)
