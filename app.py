from flask import Flask, render_template, request
import random
import requests

app = Flask(__name__)
api_key="1e4fab47686917a1d937476d67e1c60d"



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["GET", "POST", "HEAD"])
def dashboard():
    if request.method == "HEAD":
        return '', 200
    return render_template("dashboard.html")

@app.route("/calculator", methods=["GET", "POST", "HEAD"])
def calculator():
    result = None
    if request.method == "POST":
        try:    
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            op = request.form["operation"]
            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op == "*":
                result = num1 * num2
            elif op == "/" and num2 != 0:
                result = num1 / num2
            else:
                result = "Error"
        except:
            result = "Invalid Input"
    return render_template("calculator.html", result=result)

@app.route("/currency", methods=["GET", "POST", "HEAD"])
def currency():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_curr = request.form["from_currency"]
            to_curr = request.form["to_currency"]
            url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
            res = requests.get(url).json()
            rate = res["rates"].get(to_curr)
            if rate:
                result = round(amount * rate, 2)
            else:
                result = "Invalid currency"
        except:
            result = "Error"
    return render_template("converter.html", result=result)

@app.route("/rps", methods=["GET", "POST", "HEAD"])
def rps():
    result = None
    if request.method == "POST":
        user = request.form["choice"]
        comp = random.choice(["rock", "paper", "scissors"])
        if user == comp:
            result = "Draw"
        elif (user == "rock" and comp == "scissors") or \
             (user == "scissors" and comp == "paper") or \
             (user == "paper" and comp == "rock"):
            result = "You Win!"
        else:
            result = "Computer Wins!"
        result = f"You: {user}, Computer: {comp}. {result}"
    return render_template("rps.html", result=result)

@app.route("/guess", methods=["GET", "POST", "HEAD"])
def guess():
    result = None
    if request.method == "POST":
        try:
            user_guess = int(request.form["guess"])
            number = random.randint(1, 100)
            if user_guess == number:
                result = "Correct!"
            elif user_guess < number:
                result = f"Too Low! (Number was {number})"
            else:
                result = f"Too High! (Number was {number})"
        except:
            result = "Invalid input"
    return render_template("guess.html", result=result)

@app.route("/register", methods=["GET", "POST", "HEAD"])
def register():
    msg = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        msg = f"Welcome {name}! Registered successfully."
    return render_template("register.html", msg=msg)

@app.route("/weather", methods=["GET", "POST", "HEAD"])
def weather():
    weather_data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()
                if data.get("cod") == 200:
                    weather_data = {
                        "city": data["name"],
                        "temp": data["main"]["temp"],
                        "desc": data["weather"][0]["description"].title(),
                        "icon": data["weather"][0]["icon"],
                    }
                else:
                    error = data.get("message", "City not found")
            except Exception as e:
                error = "Error fetching weather"
        else:
            error = "Please enter a city name"
    return render_template("weather.html", weather=weather_data, error=error)




if __name__ == "__main__":
    app.run(debug=True)
