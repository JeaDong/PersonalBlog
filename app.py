from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'It is my PersonalBlog!'

if __name__ == '__main__':
    app.run(debug=True)