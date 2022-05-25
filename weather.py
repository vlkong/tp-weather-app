import json
import os
import urllib.parse

import requests

from taipy import Gui

city  = ""
weather_icons = ""
forecast = None

# weather service
ws_endpoint = "http://api.weatherstack.com/current"
ws_apikey = os.environ.get("WEATHERSTACK_API_KEY", None)

def get_ws_url(ws_endpoint, ws_api_key, city_string):
    f = {'access_key': ws_apikey,
         'query': city_string}
    return f"{ws_endpoint}?{urllib.parse.urlencode(f)}"

page_no_ws = """
# Weather forecast

For the `Weather forecast` demo to work, you need to register a free api on [Weatherstack](https://weatherstack.com/)

Please follow the steps:

- signup on [https://weatherstack.com/signup/free](https://weatherstack.com/signup/free)
- grab your api key
- set environment variable `WEATHERSTACK_API_KEY=your_key` or edit `weather.py` and change line

    ```
    ws_apikey = os.environ.get("WEATHERSTACK_API_KEY", None)
    ``` 
  
    to replace the default value (`None`) with your api key.
"""

page = """
<center><h1>Weather forecast</h1></center>
<|part|
<|layout|columns=1 50px|class_name=centered_elements|
  <|{city}|input|class_name=input_tf|>
  <|Search|button|on_action=submit_query|class_name=input_button|>
|>
<|layout|columns=1fr|class_name=centered_temp|
  <|{str(forecast["current"]["temperature"])+"°C" if forecast else ""}|label|class_name=weather_temp|>
  
  <|{weather_icons}|image|width=100px|height=100px|class_name=weather_icon|>
|>
|>
"""

def submit_query(state, *args):
    search_city = state.city
 
    url=get_ws_url(ws_endpoint, ws_apikey, search_city)
    r = requests.get(url)
    state.forecast = json.loads(r.content)
    state.weather_icons = state.forecast["current"]["weather_icons"][0]


if __name__ == "__main__":
    if ws_apikey:
        display_page = page
    else:
        display_page = page_no_ws
    Gui(page=display_page, css_file="style").run(dark_mode=True)
    
    
    ''' Example query result:
    {
   "request":{
      "type":"City",
      "query":"Lambersart, France",
      "language":"en",
      "unit":"m"
   },
   "location":{
      "name":"Lambersart",
      "country":"France",
      "region":"Nord-Pas-de-Calais",
      "lat":"50.650",
      "lon":"3.033",
      "timezone_id":"Europe\/Paris",
      "localtime":"2022-05-23 20:54",
      "localtime_epoch":1653339240,
      "utc_offset":"2.0"
   },
   "current":{
      "observation_time":"06:54 PM",
      "temperature":14,
      "weather_code":122,
      "weather_icons":[
         "https:\/\/assets.weatherstack.com\/images\/wsymbols01_png_64\/wsymbol_0004_black_low_cloud.png"
      ],
      "weather_descriptions":[
         "Overcast"
      ],
      "wind_speed":24,
      "wind_degree":240,
      "wind_dir":"WSW",
      "pressure":1002,
      "precip":1.1,
      "humidity":94,
      "cloudcover":75,
      "feelslike":12,
      "uv_index":4,
      "visibility":10,
      "is_day":"yes"
   }
    '''