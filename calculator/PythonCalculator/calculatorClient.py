import zeep
from zeep import Client

from flask import Flask, render_template, request

app = Flask(__name__)

c = zeep.Client("http://localhost:8000/?wsdl")


@app.route("/")
def main():
    return render_template("app.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    num1 = request.form["num1"]
    num2 = request.form["num2"]
    operation = request.form["operation"]
    if operation == "add":

        result = str(c.service.Add(num1, num2))
        return render_template("app.html", result=result)

    elif operation == "subtract":
        result = str(c.service.Subtract(num1, num2))
        return render_template("app.html", result=result)

    elif operation == "multiply":
        result = str(c.service.Multiply(num1, num2))
        return render_template("app.html", result=result)

    elif operation == "divide":
        result = str(c.service.Div(num1, num2))
        return render_template("app.html", result=result)
    else:
        return render_template("app.html")


if __name__ == "__main__":
    app.run(debug=True)
