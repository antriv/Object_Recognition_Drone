# Object Recognition Drone

This project is an ongoing work under Anusua Trivedi, Data Scientist Sr. at Microsoft. Anusua is a mentor to Isha Chakraborty & Neelagreev Griddalur, who are the main contributors to this project.

The Object Recognition Drone is a platform that allows one to perform object recognition using a drone. This software implements the Microsoft Computer Vision API and the Microsoft Bing Speech API and combines it with the Node Javascript file to access a Web Interface for full control of the drone functionalities. By invoking the server.js, you can fly your drone and have it recognize objects in real-time. 

For more information on Microsoft Computer Vision APIs and the Microsoft Bing Speech APIs, see the Microsoft Computer Vision API Documentation and Microsoft Bing Speech APIs on docs.microsoft.com. 

Inspiration for this project came from Lukas Biewald’s article at https://www.oreilly.com/ideas/how-to-build-an-autonomous-voice-controlled-face-recognizing-drone-for-200. 

If you run into any problems, feel free to contact Isha Chakraborty at ishachak@gmail.com or Neelagreev Griddalur at neelagreev@griddalur.xyz

LinkedIns: 

https://www.linkedin.com/in/ishachakraborty/

https://www.linkedin.com/in/neelagreevgriddalur/



# Source Code

Clone the sources: git clone https://github.com/Object_Recognition_Drone

# The Project
This is a Node.js and Python application to demonstrate the uses and integrations of the Computer Vision APIs and Bing Speech APIs. 

# Dependencies
This repository contains all of the necessary files and dependencies excluding node.js and Python needed to build this project and use it yourself. A drone is needed for recreating this project, a Parrot AR Drone 2.0 Power Edition Quadricopter is recommended for best compatibility. 

To install Node.js, https://nodejs.org/en/ 

To install node-ar drone libraries, run “npm install git://github.com/felixge/node-ar-drone.git”

Run “pip install git+https://github.com/westparkcom/Python-Bing-TTS.git”

Install ffmpeg 


# Running the Project 

Note: This specific drone only supports 2.4 GHz networks.

Turn the Drone on and connect to its network.

Run the command, “./start.sh” to run the shell file and follow the instructions present on your terminal window by entering the credentials of your desired network and reconnect to it after completion. 

In the same terminal window, run “node server.js”  and navigate to “localhost:3001” in your browser window. 
Open a second terminal window In the window, run “./object_detect.sh” to take the picture. This will run the ComputerVision.py file to identify the object. 

If you want to run the facial recognition, run "./startfacerec.sh" to take the picture. This will run the OpenCV code and the bat files to identify the person. This can only be done once you "enroll" the subject, details of how to do that can be found in the README.md file in the facerec folder. 



