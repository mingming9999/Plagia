from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    f = open("demofile2.txt", "a")
    f.write("Now the file has more content!")
    f.close()

    return "Hello, World!"
    
if __name__ == "__main__":
    app.run(debug=True)
