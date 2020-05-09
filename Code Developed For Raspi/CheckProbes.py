from w1thermsensor import W1ThermSensor, SensorNotReadyError, NoSensorFoundError
for sensor in W1ThermSensor.get_available_sensors():
    print(sensor.get_temperature())