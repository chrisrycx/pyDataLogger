'''
Dyacon TPH-1 Sensor
- Platform: Windows
- Connection: USB-RS485
- Interface: DataBear Sensor Interface V0.1(?)

'''

import datetime
import minimalmodbus as mm

class dyaconTPH:
    #Inherit from "modbus sensor class"?
    def __init__(self,name,settings):
        '''
        Create a new Dyacon TPH sensor
        Inputs
            - Name for sensor
            - settings['serialnum'] = Serial Number
            - settings['port'] = Serial com port
            - settings['address'] = Sensor modbus address
        '''
        self.name = name
        self.sn = settings['serialnumber']
        self.port = settings['port']
        self.address = settings['address']
        self.frequency = settings['measurement']

        #Serial settings
        self.rs = 'RS485'
        self.duplex = 'half'
        self.resistors = 1
        self.bias = 1

        #Define characteristics of this sensor
        self.sensor_type = 'polled'
        self.maxfrequency = 1  #Maximum frequency in seconds the sensor can be polled

        #Define measurements
        airT = {'name':'airT','register':210,'regtype':'float'}
        rh = {'name':'rh','register':212,'regtype':'float'}
        bp = {'name':'bp','register':214,'regtype':'float'}
        self.measurements = [airT,rh,bp]

        #Setup measurement
        self.comm = mm.Instrument(self.port,self.address)
        self.comm.serial.timeout = 0.3

        #Initialize data structure
        self.data = {'airT':[],'rh':[],'bp':[]} #Empty data dictionary

    def measure(self,measuretime,lastmeasure):
        '''
        Read in data using modbus
        '''
        for measure in self.measurements:
            dt = datetime.datetime.now()
            val = self.comm.read_float(measure['register'])

            #Output results for testing
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S %f')
            print('Measure {}: {}, value= {}'.format(measure['name'],timestamp,val))

            self.data[measure['name']].append((dt,val))

    def getdata(self,name,startdt,enddt):
        '''
        Return a list of values such that
        startdt <= timestamps < enddt
        - Inputs: datetime objects
        '''
        output = []
        data = self.data[name]
        for val in data:
            if (val[0]>=startdt) and (val[0]<enddt):
                output.append(val)
        return output


    def cleardata(self,name,startdt,enddt):
        '''
        Clear data values for a particular measurement
        Loop through values and remove. Note: This is probably
        inefficient if the data structure is large.
        '''
        savedata = []
        data = self.data[name]
        for val in data:
            if (val[0]<startdt) and (val[0]>=enddt):
                savedata.append(val)

        self.data[name] = savedata
