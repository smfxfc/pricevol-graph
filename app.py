from flask import Flask, request, Response

app = Flask(__name__)

# simple webhook functionality. this will be used to invoke the bot to run
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.json)
        return "Webhook received! (POST REQUEST)"
    elif request.method == 'GET':
        print("Data received from Webhook is: ", request.json)
        return "Webhook received (GET request)!"

app.run(host='0.0.0.0', port=5000)