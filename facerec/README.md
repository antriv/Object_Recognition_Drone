# facerec

A simple face recognition command line application using Python and OpenCV.

## Install OpenCV-Python

- [Linux installation](http://docs.opencv.org/doc/tutorials/introduction/linux_install/linux_install.html#linux-installation)
- [Install OpenCV-Python in Fedora](http://docs.opencv.org/master/dd/dd5/tutorial_py_setup_in_fedora.html)
- [Install OpenCV in CentOS](http://superuser.com/questions/678568/install-opencv-in-centos/725799#725799)

Installation in OS X:

    $ brew tap homebrew/science;brew install opencv

## Add directory with OpenCV module to the PYTHONPATH

    $ export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages

Specify directory with OpenCV module. It may be different.

## Install python packages

Use **easy_install**:

    $ easy_install numpy; easy_install pillow; easy_install argparse

or **pip**:

    $ pip install numpy; pip install pillow; pip install argparse


## Installation

    $ curl https://raw.githubusercontent.com/shhavel/facerec/master/facerec>/usr/local/bin/facerec;chmod +x /usr/local/bin/facerec

Change path to `haarcascade_frontalface_alt2.xml` if needed, e.g. in OS X:

    $ sed -i '' s,/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml,/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml, /usr/local/bin/facedetect

## Usage

Enroll a new subject or update images of existing subject.
Requires subject code (name or identifier) and paths to image files.

    $ facerec enroll --subject "Ted Crilly" test/photos/ted1.gif \
        test/photos/ted2.jpg test/photos/ted3.jpg
    $ facerec enroll --subject "Dougal Mcguire" test/photos/dougal1.jpg \
        test/photos/dougal2.jpg test/photos/dougal3.gif

Get the identification of a subject given one image of him.
Returns subject code and confidence.

    $ facerec identify path/to/photo.jpg

Ignore specific subjects:

    $ facerec identify --ignore="s34,s46" path/to/photo.jpg

Identifi only from specific subjects:

    $ facerec identify --only="s12,s34" path/to/photo.jpg

Examples:

    $ facerec identify test/photos/photo1.jpg
    Subject 'Ted Crilly' is recognized with confidence 98.2978159334
    $ facerec identify test/photos/photo2.gif
    Subject 'Dougal Mcguire' is recognized with confidence 78.5389835475
    $ facerec identify test/photos/fridge.jpg
    Face was not detected in the original image
    $ facerec identify test/photos/larry.jpg
    Unable to recognize the face
    $ facerec identify --dry test/photos/photo2.gif
    Dougal Mcguire 78.5389835475

Get the codes of all enrolled subjects.

    $ facerec list

Show faces of all enrolled subjects.

    $ facerec showall --timeout 1

Show face of one enrolled subject.

    $ facerec show --subject "Dougal Mcguire" --timeout 1

Check if the subject with given code is entered.

    $ facerec check --subject "Dougal Mcguire"

Request to delete a subject by subject code.

    $ facerec delete --subject "Dougal Mcguire"

Compare two images

    $ facerec compare path/to/first_file.jpg path/to/second_file.jpg

Or compare few images that contain one face with other image

    $ facerec compare path/to/first_fileA.jpg path/to/first_fileB.jpg \
        path/to/second_file.jpg

Examples:

    $ facerec compare test/photos/dougal3.gif test/photos/photo2.gif
    Match with confidence '64.6777569774'
    $ facerec compare test/photos/dougal2.jpg test/photos/photo2.gif
    Not match
    $ facerec compare test/photos/dougal2.jpg test/photos/dougal3.gif \
        test/photos/photo2.gif
    Match with confidence '64.6777569774'

## Lisks

General infotmation about OpenCV

- http://docs.opencv.org/2.4/modules/contrib/doc/facerec/index.html
- http://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html

Face detection and face recognition using OpenCV and Python

- http://superuser.com/questions/420885/is-there-a-face-recognition-command-line-tool/794147#794147
- https://github.com/wavexx/facedetect
- http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/
- http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
- http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html
- https://realpython.com/blog/python/face-recognition-with-python/
- https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/

## Running tests

Install [bats](https://github.com/sstephenson/bats) (on Mac OS X just run `brew install bats`).

Run test suite:

    $ bats test
