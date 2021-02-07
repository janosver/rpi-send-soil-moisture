import time, board, busio, adafruit_ads1x15.ads1015 as ADS, json, datetime, requests
from adafruit_ads1x15.analog_in import AnalogIn

# Read configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
a0 = AnalogIn(ads, ADS.P0)
a1 = AnalogIn(ads, ADS.P1)
a2 = AnalogIn(ads, ADS.P2)
a3 = AnalogIn(ads, ADS.P3)


def send_to_api (sensor, voltage, moistureLevel):
    measurements = { 
        "device": config["device"],
        "dateTime": datetime.datetime.now().isoformat(),
        "sensor": sensor,
        "voltage": voltage,
        "moistureLevel": moistureLevel
    }
    try:
        # Send measurement to API
        resp = requests.post(config["rpi-measurements-api"]+'/soilmoisture', json=measurements)
        if resp.status_code != 200:
            return "["+datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")+"] Sensor {0} voltage={1:0.2f}v, Moisture Level={2:0.2f}% - ERROR sending data to API".format(sensor, voltage, moistureLevel)
        else: 
            return "["+datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")+"] Sensor {0} voltage={1:0.2f}v, Moisture Level={2:0.2f}% - Successfully sent to API".format(sensor, voltage, moistureLevel)
    except requests.exceptions.RequestException as e:
        return "["+datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")+"] Sensor {0} voltage={1:0.2f}v, Moisture Level={2:0.2f}% - ERROR connecting to API".format(sensor, voltage, moistureLevel)

print("Moisture level 0% (dry) to 100% (wet)")
print("Sensors from A0 to A3")
while True:
    # Calculate dryness percentage
    # ~1.4v = 100% (wet)
    # ~2.8v = 0% (dry)
    # <1.3v = sensor is not connected

    #Sensor 0
    if a0.voltage>1.3:
        a0pct = max(0, min( round((1-((a0.voltage-1.4)/1.4))*100,2), 100))   
        print(send_to_api("A0", round(a0.voltage,2), a0pct)) 
    else:
        a0pct = None        

    # Sensor 1
    if a1.voltage>1.3:
        a1pct = max(0, min( round((1-((a1.voltage-1.4)/1.4))*100,2), 100))
        print(send_to_api("A1", round(a1.voltage,2), a1pct))
    else:
        a1pct = None

    # Sensor 2
    if a2.voltage>1.3:
        a2pct = max(0, min( round((1-((a2.voltage-1.4)/1.4))*100,2), 100))
        print(send_to_api("A2", round(a2.voltage,2), a2pct))
    else:
        a2pct = None
    
    #Sensor 3
    if a3.voltage>1.3:
        a3pct = max(0, min( round((1-((a3.voltage-1.4)/1.4))*100,2), 100))
        print(send_to_api("A3", round(a3.voltage,2), a3pct))
    else:
        a3pct = None

    if a0pct is not None and a1pct is not None and a3pct is not None and a3pct is not None:
        print("["+datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")+"] Failed to retrieve data from any sensor")

    time.sleep(config["frequency"])