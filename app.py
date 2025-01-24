from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_KEY = "2de59101f32a576ae4b6666324d010d8"

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None
    
    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            error = "Please enter a city name!"
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url)
                data = response.json()
                
                if data.get("cod") != 200:
                    error = data.get("message", "Unable to fetch weather data.")
                else:
                    weather_data = {
                        "city": city.capitalize(),
                        "temperature": data["main"]["temp"],
                        "weather": data["weather"][0]["description"].capitalize(),
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                    }
            except Exception as e:
                error = f"Error: {str(e)}"
    
    return render_template("index.html", weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
