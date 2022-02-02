import requests as req, sys, pandas as pd, pytz
from PySide6 import QtGui
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PySide6.QtCore import QAbstractTableModel, Qt
#I seperated this to point out that this contains the UI elements. The PY file is generated from a .ui file using the pyside6-uic tool. 
from ui_main import Ui_Widget

#My API Key of course
api_key = '412e21305fa900bbca11c6434107bc57'
#Dictionary of states and their postal codes. For some reason if you want to use a State Code, you are required to use the US country code - it isn't implicit.
#Due to this we have to distinguish between a State Codes and Country Codes, by creating a dictionary set we get a dual purpose
#1) We get to validate state codes and return a properly formatted location
#2) We also can index the typed state to its state code and return the location still
states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

def get_location(location):
    #Checks for a String (City, State basically), Integer (Zip Code), or Tuple (Lat, Lon). Unlike with the get_weather_data function, we will check for a tuple and make an API call here. 
    #The reason for this is simple, it will let us use the Lat/Lon fields in the JSON data we get from get_weather data. This, in turn, lets us grab the closes City to those coords to display. 
    if type(location) == str:
        #Sorts out Country Codes vs State Codes, and reformats accordingly.
        loc_list = location.split(",")
        locStr = f'{location}'
        try:
            loc_list[1] = loc_list[1].strip()
            if (loc_list[1] in states.keys()) or (loc_list[1] in states.values()):
                stateNames = list(states.values())
                stateKeys = list(states.keys())
                stateCode = stateKeys[stateNames.index(loc_list[1])]
                if len(loc_list)<3:
                    locStr = f'{loc_list[0]},{stateCode},US'
                else:
                    loc_list[2] = loc_list[2].strip()
                    locStr = f'{loc_list[0]},{stateCode},{loc_list[2]}'
        except:
            pass
        geolocation_api = req.get(f'http://api.openweathermap.org/geo/1.0/direct?q={locStr}&appid={api_key}')
    elif type(location) == int:
        geolocation_api = req.get(f'http://api.openweathermap.org/geo/1.0/zip?zip={location}&appid={api_key}')
    elif type(location) == tuple:
        #This will attempt to convert the Tuple to a list and get the location in JSON. In case theres an error it aborts the function. 
        #It assumes the Tuple is set up in the order of (Lat,Lon), if it isn't then it will return the wrong location. 
        try:
            coord_location = list(location)
            geolocation_api = req.get(f'http://api.openweathermap.org/geo/1.0/reverse?lat={coord_location[0]}&lon={coord_location[1]}&appid={api_key}')
        except:
            return
    else:
        #Popup for invalid entry, return failure string.
        message = f'The input, {location}, was not valid. Please make sure you are entering a Zip Code or City, State, Country (where state is applicable). Check your input and try again.'
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec()
        return message
    geolocation_data = geolocation_api.json()
    if len(geolocation_data)<=0:
        #Popup for lack of location, and return failure string.
        message = f'Error: Location, {location} - was not found. Please check for typos and try again'
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec()
        return message
    #checks if there were multiple locations in the data, since this is only possible when providing it by Name (we don't care about tuples as that's only for function calls).
    #if there are multiple locations then output a message for the issue. If this was a downloaded app then I'd add a config for this (Don't remind me again type thing, or a togglable setting)
    elif len(geolocation_data)>1 and type(location) == str:
        message = f'There were total of {len(geolocation_data)} locations detected for the provided location: {location}. We will use the first location found. Please add a country and state to your query (where applicable)'
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec()
    return geolocation_data

def get_weather_data(location):
    #Attempts to convert location to an integer. Its a basic check for the Zipcode, and preventing any API call issues caused by floats or the like.
    #If it fails it will assume a string and move on. Dirty strings are fine since the API call will fail and return an error message.
    try:
        location = int(location)
    except:
        pass
    #Calls the get_location function with the given location. This lets us search for the coords of a given location. We use these coords in the API call later.
    geolocation_data = get_location(location)
    #This is will check that the returned output is JSON. In our case, this checks if the location check failed without having to complicate the returned content. 
    if type(geolocation_data) == str:
        return geolocation_data

    #The data structure for the JSON is ever so slightly different if you used a Zip instead of City, State. By checking for Int/Str we are basically checking for Zip/City, State. This makes sure we can grab the right data and return it
    if type(location) == str:
        onecall_api = req.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={geolocation_data[0]["lat"]}&lon={geolocation_data[0]["lon"]}&units=imperial&appid={api_key}')
    elif type(location) == int:
        onecall_api = req.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={geolocation_data["lat"]}&lon={geolocation_data["lon"]}&units=imperial&appid={api_key}')
    #return the JSON data. 
    return onecall_api.json()

#Since we commonly need to convert a UNIX time code to UTC then localize it for the timezone, I created a function to handle that. It returns an unformatted time, which we format on at the function call depending on the need.
def localizeTime(unixTime, timezone):
   localTime = pytz.utc.localize(datetime.utcfromtimestamp(unixTime))
   return localTime.astimezone(pytz.timezone(timezone))

#Creates a description of the Wind Speed based on numbers from https://www.weather.gov/pqr/wind
def windSpeedDescription(windSpeed):
    if windSpeed < 1:
        return "Calm winds"
    elif 1 <= windSpeed < 4:
        return "Light Air"
    elif 4 <= windSpeed < 8:
        return "Light Breeze"
    elif 8 <= windSpeed < 13:
        return "Gentle Breeze"
    elif 13 <= windSpeed < 19:
        return "Moderate Breeze"
    elif 19 <= windSpeed < 25:
        return "Fresh Breeze"
    elif 25 <= windSpeed < 32:
        return "Strong Breeze"
    elif 32 <= windSpeed < 39:
        return "Near Gale"
    elif 39 <= windSpeed < 47:
        return "Gale"
    elif 47 <= windSpeed < 55:
        return "Strong Gale"
    elif 55 <= windSpeed < 64:
        return "Whole Gale"
    elif 64 <= windSpeed <= 75:
        return "Storm Force"
    elif 75 < windSpeed:
        return "Hurricane Force"
    else:
        return "Wind Error"
#Sets a TableModel Class. This is neccessary to work with a TableView in QT. The reason it is neccessary is because QAbstractTableModel and its subclasses don't do anything inherently in the QT library. 
#You have to manually sub-class it and define what it does. In this case it combines QT and Pandas to allow me to easily and dynamically define tables for the TableViews in my UI files. 
#This was easily the hardest part of the project. 
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        #This identifies the data table from the Coloumn and Index headers in the DataFrame.
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        #Gets the number of rows
        return self._data.shape[0]

    def columnCount(self, index):
        #Gets the number of columns
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        #This checks the headerData to get the defined Headers. This identified in the DataFrame.
        #Column is the Column Headers of course, while Index is the Row Headers. By using DataFrames it provides readability and simplicity.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

#Defines the main UI class
class ui_main(QMainWindow):
    #Initalizes the UI from the ui_main file, and sets any connections.
    def __init__(self):
        super(ui_main, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        #Uses the IP address to get location data for the default info on the form.
        try:
            ip_data = req.get("https://ipinfo.io/json").json()
            location = f'{ip_data["city"]},{ip_data["region"]},{ip_data["country"]}'
            weather_data = get_weather_data(location)
            if weather_data == str:
                raise Exception(weather_data)
            else:
                self.displayData(weather_data)
        except:
            location = "Las Vegas, CA"
            weather_data = get_weather_data(location)
            self.displayData(weather_data)
        
        #Connects specific events
        self.ui.pushButtonEnterLoc.clicked.connect(self.loc_prompt)
        self.ui.pushButtonQuit.clicked.connect(self.exit)
     
    #Prompts the user to enter a new location when the "Enter New Location" button is clicked.
    def loc_prompt(self, s):
        popup = QInputDialog(self)
        popup.setWindowTitle("New Location")
        popup.setLabelText("Please enter location (Postal codes are supported in US only):")
        popup.exec()

        weather_data = get_weather_data(popup.textValue())
        #This is a redundancy check for if the returned data from the function is a string (all would be failure strings). If they are it stops the function, otherwise it calls displayData.
        if weather_data == str:
            return
        self.displayData(weather_data)

    #calls each display function, passing the raw json data through each time. By seperating the functions it keeps the logic clear, and isolates the variables.
    def displayData(self, json):
       self.displayCurrent(json)
       self.displayMin(json)
       self.displayHourly(json)
       self.displayDaily(json)
       self.displayWeatherAlert(json)

    #Processes and Displays "Current" information, and general info. This is stuff like the current time, location, current weather, etc.
    def displayCurrent(self, json):
        current = json["current"]
        loc_name = get_location((json["lat"],json["lon"]))
        self.ui.labelCurTime.setText(localizeTime(current["dt"],json["timezone"]).strftime("%b %d, %H:%M"))
        if loc_name[0]["country"] == "US":
            labelLocMsg = f'{loc_name[0]["name"]}, {loc_name[0]["state"]}'
        else:
            labelLocMsg = f'{loc_name[0]["name"]}, {loc_name[0]["country"]}'
        self.ui.labelLoc.setText(labelLocMsg)
        self.ui.labelCurTemp.setText(f'{current["temp"]:.0f}\N{DEGREE SIGN}F')
        self.ui.labelFeelsLike.setText(f'Feels like {current["feels_like"]:.0f}\N{DEGREE SIGN}F. {current["weather"][0]["description"].title()}. {windSpeedDescription(current["wind_speed"])}')
        self.ui.labelHumidity.setText(f'Humidity: {current["humidity"]:.0f}%')
        self.ui.labelWind.setText(f'Wind Speed: {current["wind_speed"]}mph')
        
        picture = QtGui.QPixmap()
        picture.loadFromData(req.get(f'http://openweathermap.org/img/wn/{current["weather"][0]["icon"]}@2x.png').content)
        self.ui.labelImg.setPixmap(picture)
    #Processes and Displays the Minutely information. This (for some reason) is only the Precpitation. This forecasts 1hr (60min)
    def displayMin(self, json):
        minutely = json["minutely"]
        tableMin = self.ui.tableViewMin
        minuteData = []

        for x in minutely:
            dt, precip = x
            minuteTime = localizeTime(x[dt], json["timezone"]).strftime("%H:%M")
            minuteData.append([minuteTime,f'{x[precip]:.0%}'])

        minuteFrame = pd.DataFrame(
            minuteData,
            columns = ['DT','Precip']
            )

        tableMin.model = TableModel(minuteFrame)
        tableMin.setModel(tableMin.model)
    
    #Processes and Displays the Hourly information. This forecasts 48hrs
    def displayHourly(self, json):
        #Display: Time, Temp, Feels Like, Humidity, Precip
        hourly = json["hourly"]
        tableHourly = self.ui.tableViewHourly
        hourlyData = []
        for x in hourly:
            
            time = localizeTime(x["dt"], json["timezone"]).strftime("%b %d, %H:%M")
            temp = f'{x["temp"]:.0f}\N{DEGREE SIGN}F'
            feelsLike = f'{x["feels_like"]:.0f}\N{DEGREE SIGN}F'
            precip = f'{x["pop"]:.0%}'
            humidity = f'{x["humidity"]:.0f}%'
            hourlyData.append([time, temp, feelsLike, humidity, precip])
        hourlyFrame = pd.DataFrame(
            hourlyData,
            columns=['Time','Temp','Feels Like', 'Humidity', 'Precip']
            )
        tableHourly.model = TableModel(hourlyFrame)
        tableHourly.setModel(tableHourly.model)
    #Processes and Displays the Daily information. This forecasts 7 days
    def displayDaily(self, json):
        #Display: Date, High, Low, Weather and Precip, Humidity, Wind, (Depending on what fits)
        daily = json["daily"]
        tableDaily = self.ui.tableViewDaily
        dailyData = []
        for x in daily:
            date = localizeTime(x["dt"],json["timezone"]).strftime("%b %d, %H:%M")
            high = f'{x["temp"]["max"]:.0f}\N{DEGREE SIGN}F. Feels like {x["feels_like"]["day"]:.0f}\N{DEGREE SIGN}F'
            low = f'{x["temp"]["min"]:.0f}\N{DEGREE SIGN}F. Feels like {x["feels_like"]["night"]:.0f}\N{DEGREE SIGN}F'
            weatherPrecip = f'{x["pop"]:.0%} chance of {x["weather"][0]["description"].capitalize()}'
            humidity = f'{x["humidity"]:.0f}%'
            wind = f'{windSpeedDescription(x["wind_speed"])} with wind speeds of {x["wind_speed"]}mph.'
            dailyData.append([date,high,low,weatherPrecip,humidity,wind])
        dailyFrame = pd.DataFrame(
            dailyData,
            columns=['Date','High','Low','Weather','Humidity','Wind']
            )
        tableDaily.model = TableModel(dailyFrame)
        tableDaily.setModel(tableDaily.model)

    #Processes and Displays the Weather Alert information. This will display any current weather alerts that are affecting the area. 
    def displayWeatherAlert(self, json):
        #Display Sender, Event, Start, End, Description from weather alerts. This SHOULD work, but it's hard to test the API against weather alerts as even historical data doesn't contain this field.
        alertsData = []
        tableAlerts = self.ui.tableWeatherAlerts
        try:
            alerts = json["alerts"]
            for x in alerts:
                sender, event, start, end, description, *alertsExtra = x.values()
                start_time = localizeTime(start, json["timezone"]).strftime("%a %d, %H:%M")
                end_time = localizeTime(end, json["timezone"]).strftime("%a %d, %H:%M")
                alertsData.append([sender,event,start_time,end_time,description])
        except:
            pass
        alertsFrame = pd.DataFrame(
            alertsData,
            columns=['Source', 'Event', 'Start Time', 'End Time', 'Message']
            )
        tableAlerts.model = TableModel(alertsFrame)
        tableAlerts.setModel(tableAlerts.model)
    #Defines exit function
    def exit(self, s):
        app.exit()

#As long as it is the main file, launch the application/UI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ui_main()
    window.show()

    sys.exit(app.exec())