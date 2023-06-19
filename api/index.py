from flask import Flask, request, render_template
from CustomClass import CustomClass

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    url = request.form['url']
    custom_obj = CustomClass()
    result = custom_obj.process_url(url)
    return result

if __name__ == '__main__':
    app.run()
