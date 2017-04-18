#!/bin/bash

connectDrone()
{ #Gathers information about user's desired network.
    printf "\nEnter desired network information (NOTE: Password is visible)-->"
    printf "\nSSID: "
    read SSID
    printf "Password: "
    read password
    printf "Desired IP on Network: "
    read ipAddress
    printf "\n\nCONNECTING..\n\n"
    ./connect_drone/connect "$SSID" -p "$password" -a "$ipAddress" -d "192.168.1.1"
    printf "\n\nCONNECTED! \n**CONNECT BACK TO NETWORK**\n\n"
}

printf "\nObject Recognizing Drone \n(c) Neel Griddalur and Isha Chakraborty\n\n"

#Gets preliminary information from user regarding drone state
printf "\nWelcome! Are you connected to the drone's created access point (y/n)> "
read connectedBool
if [ $connectedBool == 'y' ]
then
    connectDrone
else
    printf "\nConnect to Drone Access Point!\n"
fi
