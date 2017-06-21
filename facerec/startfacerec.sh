#!/bin/bash
cd /Users/neelgriddalur/Documents/Microsoft\ AI\ Project/2\ -\ Face\ Recog\ Drone/FaceRecognitionTesting/facerec/
brew tap homebrew/science
brew install opencv
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
pip install numpy
pip install pillow
pip install argparse
curl https://raw.githubusercontent.com/shhavel/facerec/master/facerec>/usr/local/bin/facerec;chmod +x /usr/local/bin/facerec
sed -i '' s,/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml,/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml, /usr/local/bin/facerec
