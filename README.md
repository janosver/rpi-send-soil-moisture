# rpi-send-soil-moisture
Send soil measurements measurements from a Raspberry Pi to [rpi-measurements-api](https://github.com/janosver/rpi-measurements-api)


# Configuration

Create a `config.json` file with the below contents
```
{
    "device":"<name of your device which is taking the measurements>",
    "rpi-measurements-api":"http://<url to the API>:<port - optional>",
    "frequency" : <seconds>
}
```

With the `frequency` parameter you can define how often a reading should be attempted. So if it set to 300 it will attempt a reading every 5 minutes. After each reading the measurements is attempted to be sent to the API and logged in the console.

Example
```
{
    "device":"raspberrypizero",
    "rpi-measurements-api":"http://raspberrypi:8650",
    "frequency" : 300
}
```

# Running the script
```
python3 rpi-send-soil-moisture.py
```

The script will run continuously until it is terminated.