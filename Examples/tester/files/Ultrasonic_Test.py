from basehat import UltrasonicSensor
import time
import cmdgui

def Ultrasonic_Test():
        result = ['Ultrasonic_Test']

        ultrasonicstage = cmdgui.stage(title = 'Ultrasonic Test',width = 60, height = 15)
        cmdgui.setstage(ultrasonicstage)

        cmdgui.writeline(ultrasonicstage,'Ultrasonic will Read for 5s, wave your hand over it!',1)

        zerovalue = False

        pin = 5

        # Initializing the sensor so the function within the class can be used
        ultra = UltrasonicSensor(pin)

        for i in range(10):

            readval = ultra.getDist

            if (readval == 0):
                zerovalue = True

            cmdgui.writeline(ultrasonicstage,'Distance: '+ str(readval),3)
            
            time.sleep(0.25)

        if zerovalue:
                cmdgui.writeline(ultrasonicstage,'ERROR: zero value detected',5)
                result.append('FAILED')
        else:
                cmdgui.writeline(ultrasonicstage,'Non-zero values returned, good!',5)
                result.append('PASSED')
        cmdgui.writeline(ultrasonicstage,str(result[0]+": " + result[1]),6)
        time.sleep(1)
        return(result)
