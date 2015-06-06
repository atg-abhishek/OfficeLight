# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 15:50:56 2015

@author: Abhishek Gupta

This is the backend data parser for OfficeLight

extending the code from https://github.com/bcimontreal/bci_workshop
"""

import socket
import numpy as np
import array
import struct
import matplotlib.pyplot as plt
import time
import pprint
from datetime import datetime

from mules_utils import mules_parse_header, mules_parse_data

if __name__ == "__main__":
    
    plt.close("all")
    
    # 1 Configuration for the TCP/IP Client

    mules_ip = '127.0.0.1'
    mules_port = 30000
    BUFFER_SIZE = 5000000
    
    client_cnx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_cnx.connect((mules_ip, mules_port))
    #data = client_cnx.recv(BUFFER_SIZE)
    #conn, addr = client_cnx.accept()
    
    # 2 Request of Header
    i=0
    j=0
    result = []
    measure_unit = "Amplitude"
    loc_esi_id = "Muse-0CCD"
    direction = "P"
    print ('Use a keyboard interrupt to stop')
    try:  
        #needs to be True for infinite pinging 
        #also remove all the other prints
        #in the while loop let the condition be based on an hour from the current time and then 
        #send all of the data in the end at once
        while i<100:    
            print('Header request')
            command = 'H'
            client_cnx.send(command)
            
            nBytes_4B = array.array('B',client_cnx.recv(4) )
            nBytes = struct.unpack('i',nBytes_4B[::-1])[0]
            #nBytes equals to number of bytes to read from the connection
            #[0] is used to get an int32 rather than turple
            package = client_cnx.recv(nBytes)
            #edit and obtain parameters from the package
            dev_name, dev_hardware, fs, data_format, nCh = mules_parse_header(package)
            
            # 3 Request of channel names
            print('Channel names request')
            command = 'N'
            client_cnx.send(command)
            
            nBytes_4B = array.array('B',client_cnx.recv(4)) 
            nBytes = struct.unpack('i',nBytes_4B[::-1])[0]
            package = client_cnx.recv(nBytes)
            cur_time_init = str(datetime.now())
            ch_labels = package.split(',')
            
            # 4 Flush old data from the Server data
            print('Flushing Server data')
            command = 'F'
            client_cnx.send(command)
        
            # 5 Pause script 5 seconds to gather data 
#            print('Wait 5 seconds');
            # getting data in 0.05 second intervals
            time.sleep(0.05);
            
            # 6 Request EEG data since the last flush (5 seconds)
            print('EEG data request');
            command = 'R';
            client_cnx.send(command)
            nBytes_4B = array.array('B',client_cnx.recv(4)) 
            nBytes = struct.unpack('i',nBytes_4B[::-1])[0]
        
            eeg_package = '';
            while len(eeg_package) < nBytes:
                eeg_package += client_cnx.recv(1)
            
            eeg_data = mules_parse_data(eeg_package, data_format)
            
            # 7 Plot EEG data
            n_samples = eeg_data.shape[0];
            if n_samples!=1:
                time_vec = np.arange(n_samples)/fs
                avg_value = time_vec.mean()
                j=j+1
                sub_result = {'measure unit' : measure_unit, 'loc_esi_id' : loc_esi_id, 'direction' : direction, 'value' : avg_value, 'tstamp' : cur_time_init}
#                pprint.pprint(sub_result)                
                result.append(sub_result) 
#            print ('nsamples '+str(n_samples))
            #pprint.pprint(time_vec)           
#            plt.ion()    
#            plt.plot(time_vec,eeg_data); 
#            plt.xlabel('Time [s]');
#            plt.ylabel('Amplitude');
            #plt.show()
#            print ('i '+str(i))
            i=i+1
            
        
#        print ("j value " + str(j))
        pprint.pprint(result)
    except KeyboardInterrupt:
        
        # 8 Close connection with Server
        client_cnx.close()
        print('Connection closed.')