from flask import Flask, render_template
from waitress import serve

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # For development
    app.run(debug=True)
    # For production
    #print("Starting the Waitress server on http://127.0.0.1:5000/")
    #serve(app, host='127.0.0.1', port=5000)