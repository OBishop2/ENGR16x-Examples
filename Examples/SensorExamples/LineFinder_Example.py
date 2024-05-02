from basehat import LineFinder
import time

def main():

    # set the pin to be used
    # if sensor is plugged into port D5, pin1 should be 5
    # make sure to only plug in Ultrasonic Sensor to digital ports of the Grove BaseHAT (D5, D16, D18, D22, D24, D26)
    pin = 5

    # Initializing the sensor so the function within the class can be used
    lineFinder = LineFinder(pin)

    print('Detecting infrared...')

    try: 
        while True:
            try: 
                # update and read the values of the lineFinder
                curValue = lineFinder.valueL

                # print values
                print("IR valueL: {}".format(curValue))

                time.sleep(0.5)

            except IOError:
                print ("\nError occurred while attempting to read values.")

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting...")
        break

if __name__ == '__main__':
    main()