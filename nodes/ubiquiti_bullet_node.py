#!/usr/bin/env python

'''
Val Schmidt
Center for Coastal and Ocean Mapping
University of New Hampshire
Copyright 2021

ToDo:
Remove hard-coded password and accept on command line.
Test with a third radio.
Quotes or other nonalpha-numeric characters in the radio's hostname will break this.

'''

import rospy
import ubiquiti.UbiquitiWifi as ubwf
from ubiquiti.msg import UbiquitiRadio

rospy.init_node('ubiquiti')
    
def run():
    U = ubwf.UbiquitiWifi(ipaddr='192.168.101.45')
    U.username = 'field'
    U.passwd = 'Chas3ocean!'
    U.getAirOSVersion()
    
    
    rate = rospy.Rate(0.5)    
    pubs = {}
    while not rospy.is_shutdown():
        
        try:

            U.getstatus()
        except:
            rospy.LOGINFO('Failed to get status from Ubiquiti Radio.')
    
        if U.statusraw is not None:

            hostname = U.status['host']['hostname'].replace(' ','')
                
            if hostname not in pubs.keys():
                pubs[hostname] = rospy.Publisher('/ubiquiti/' + 
                            hostname, UbiquitiRadio,queue_size=10)
                
            M = UbiquitiRadio()
            M.header.stamp = rospy.Time.now()
            # Local radio information
            M.local_hostname = U.status['host']['hostname']
            M.local_uptime = U.status['host']['uptime']
            #M.local_temperature = U.status['host']['temperature']
            M.local_frequency = U.status['interfaces'][2]['wireless']['frequency']
            #M.local_distance = U.status['wireless']['distance']
            M.local_selfnoisedB = U.status['interfaces'][2]['wireless']['noisef']
            M.local_txpower = U.status['interfaces'][2]['wireless']['txpower']
            #M.local_channelbw = U.status['wireless']['chanbw']
            M.local_tx_throughput = U.status['interfaces'][2]['wireless']['utilization']['tx_busy']
            M.local_rx_throughput = U.status['interfaces'][2]['wireless']['utilization']['rx_busy']   
            # Distant radio information
            #M.remote_hostname = station['remote']['hostname']
            M.remote_uplink_capacity = U.status['interfaces'][2]['wireless']['txrate']
            M.remote_downlink_capacity = U.status['interfaces'][2]['wireless']['rxrate']
            #M.remote_signal = station['remote']['signal']
            M.remote_rssi = U.status['interfaces'][2]['wireless']['rssi']
            #M.remote_noisefloor = station['remote']['noisefloor']
            #M.remote_distance = station['remote']['distance']
            #M.remote_temperature = station['remote']['temperature']
            #M.remote_uptime = station['remote']['uptime']
            #M.remote_tx_throughput = station['remote']['tx_throughput']
            #M.remote_rx_throughput = station['remote']['rx_throughput']
            #M.remote_tx_power = station['remote']['tx_power']
            
            M.raw_status = U.statusraw       
            pubs[hostname].publish(M)
        rate.sleep()
 
 
if __name__=='__main__':

    try:
        run()
    except rospy.ROSInterruptException:
        pass
