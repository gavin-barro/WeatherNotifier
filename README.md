# WeatherNotifier

This Python script is a weather alert system that uses the OpenWeatherMap API to fetch short-term weather forecasts and sends an SMS notification via Twilio if rain is expected. The user is prompted to input their phone number and (optionally) geographic coordinates (latitude and longitude). If invalid coordinates are provided, the script defaults to the coordinates of Harrisonburg, Virginia.

At its core, the script makes an HTTP GET request to the OpenWeatherMap 5-day forecast endpoint (https://api.openweathermap.org/data/2.5/forecast). It requests a limited number (cnt=4) of upcoming forecast entries for a specified location, using the API key stored in an .env file for authentication. The response contains weather data such as condition codes and descriptions for each forecasted time interval.

The script then parses the weather condition codes from the response to determine if rain is expected. Weather codes below 600 (as per OpenWeatherMap's classification) generally indicate rain, drizzle, or thunderstorms. If any of these codes are detected in the forecast, a message is composed using a corresponding emoji to visually represent the weather condition (🌧️ for rain, ⛈️ for thunderstorms, etc.).

If rain is predicted, the script uses the Twilio API to send an SMS alert to the user's phone number. Twilio credentials and the sender phone number are also securely loaded from environment variables. The SMS message includes the weather description and a reminder to bring an umbrella, enhancing user preparedness for inclement weather.