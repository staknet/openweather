from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not bool(city.strip()):
        city = "New Delhi"

    weather_data, bg_image = get_current_weather(city)

    if not weather_data['cod'] == 200:
        return render_template("city-not-found.html", bg_image = bg_image)
        
    return render_template(
        "weather.html",
        title = weather_data["name"],
        status = weather_data["weather"][0]["description"].capitalize(),
        icon = f'https://openweathermap.org/img/wn/{weather_data["weather"][0]["icon"]}.png',
        temp = f"{weather_data['main']['temp']:.1f}",
        feels_like = f"{weather_data['main']['feels_like']:.1f}",
        local_time = weather_data['local_time'],
        bg_image = bg_image
        
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000) 
