#!/usr/bin/env python
import numpy as np
import argparse, cv2, sys, os, math
from PIL import Image
from time import sleep

# CV compatibility stubs
if 'IMREAD_GRAYSCALE' not in dir(cv2):
    cv2.IMREAD_GRAYSCALE = 0L

# Profiles
PROFILES = {
    'HAAR_FRONTALFACE_ALT2': 'haarcascade_frontalface_alt2.xml'
    'HAAR_PROFILEFACE': 'haarcascade_profileface.xml'
    'HAAR_EYE': 'haarcascade_eye.xml'
}
CV2_FLAGS = cv2.CV_HAAR_DO_CANNY_PRUNING | cv2.CV_HAAR_FIND_BIGGEST_OBJECT
THRESHOLD = {'min': 4, 'max': 100}
subjects_directory = None

# Support functions
def error(msg):
    sys.stderr.write("{0}: error: {1}\n".format(os.path.basename(sys.argv[0]), msg))

def fatal(msg):
    error(msg)
    sys.exit(1)

def check_profiles():
    for k, v in PROFILES.iteritems():
        if not os.path.exists(v):
            fatal("cannot load {0} from {1}".format(k, v))

faceCascade = None
def detect_faces(image_path):
    global faceCascade
    faceCascade = faceCascade or cv2.CascadeClassifier(PROFILES['HAAR_FRONTALFACE_ALT2'])
    # Read the image and convert to grayscale
    image_pil = Image.open(image_path).convert('L')
    # Convert the image format into numpy array
    image = np.array(image_pil, 'uint8')
    # Detect the face in the image
    side = math.sqrt(image.size)
    minlen = int(side / 20)
    maxlen = int(side / 2)
    faces = faceCascade.detectMultiScale(image, 1.1, 4, CV2_FLAGS, (minlen, minlen), (maxlen, maxlen))
    return faces, image

# Enroll a new subject or update images of existing subject
def enroll(args):
    directory = os.path.join(subjects_directory, args.subject)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except OSError, e:
                fatal(e)

    for image_path in args.files:
        if not os.path.exists(image_path):
            fatal("File not found: '{0}'".format(image_path))
    face_number = 0
    for image_path in args.files:
        faces, image = detect_faces(image_path)
        # If face is detected, write the face image to the subject directory
        if len(faces):
            (x, y, w, h) = faces[len(faces) - 1]
            face_number += 1
            face_path = os.path.join(directory, str(face_number) + ".jpg")
            cv2.imwrite(face_path, image[y: y + h, x: x + w])
            if args.debug:
                cv2.imshow(args.subject, image[y: y + h, x: x + w])
                cv2.waitKey(50)
    if face_number:
        print("Enrolled subject: '{0}', number of faces: {1}".format(args.subject, face_number))
        return 0
    else:
        print("No faces detected for subject '{0}'".format(args.subject))
        return 2

# Identify subject by image
def identify(args):
    for image_path in args.files:
        if not os.path.exists(image_path):
            fatal("File not found: '{0}'".format(image_path))
    if not args.only is None:
        only = args.only.split(',')
    if not args.ignore is None:
        ignore = args.ignore.split(',')
    images = []
    labels = []
    all_subjects = {}
    subject_number = 0
    for subject in os.listdir(subjects_directory):
        if not subject.startswith('.') and (args.only is None or subject in only) and (args.ignore is None or subject not in ignore):
            subject_number += 1
            all_subjects[subject_number] = subject
            directory = os.path.join(subjects_directory, subject)
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                image_pil = Image.open(file_path)
                image = np.array(image_pil, 'uint8')
                images.append(image)
                labels.append(subject_number)
                if args.debug:
                    cv2.imshow(subject, image)
                    cv2.waitKey(50)

    if not len(labels):
        fatal("Unable to identify with empty storage. Enroll few subjects first.")

    recognizer = cv2.createLBPHFaceRecognizer()
    recognizer.train(images, np.array(labels))

    predict_faces = []
    for image_path in args.files:
        faces, image = detect_faces(image_path)
        if len(faces):
            (x, y, w, h) = faces[len(faces) - 1]
            predict_faces.append(image[y: y + h, x: x + w])

    if len(predict_faces):
        predictions = []
        for predict_face in predict_faces:
            nbr_predicted, conf = recognizer.predict(predict_face)
            if nbr_predicted and THRESHOLD['min'] < conf and conf < THRESHOLD['max']:
                predictions.append((nbr_predicted, conf))
        if len(predictions):
            sorted_predictions = sorted(predictions, key=lambda p: -p[1])
            if args.all:
                printed_nbrs = []
                for nbr_predicted, conf in sorted_predictions:
                    if not nbr_predicted in printed_nbrs:
                        printed_nbrs.append(nbr_predicted)
                        if args.dry:
                            print "{0} {1}".format(all_subjects[nbr_predicted], conf)
                        else:
                            print "Subject '{0}' is recognized with confidence this is 1 {1}".format(all_subjects[nbr_predicted], conf)

            else:
                nbr_predicted, conf = sorted_predictions[0]
                if args.dry:
                    print "{0} {1}".format(all_subjects[nbr_predicted], conf)
                else:
                    print "Subject '{0}' is recognized with confidence this is 2 {1}".format(all_subjects[nbr_predicted], conf)
        else:
            print("Unable to recognize the face")
            return 2
    else:
        print("Face was not detected in the original image")
        return 2

# Get all subjects codes.
def list(args):
    empty = True
    for subject in os.listdir(subjects_directory):
        if not subject.startswith('.'):
            print subject
            empty = False
    if empty:
        print "No subjects"
        return 2
    else:
        return 0

# Show all subjects images.
def showall(args):
    empty = True
    for subject in os.listdir(subjects_directory):
        if not subject.startswith('.'):
            empty = False
            directory = os.path.join(subjects_directory, subject)
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                image_pil = Image.open(file_path)
                image = np.array(image_pil, 'uint8')
                cv2.imshow(subject, image)
                if args.timeout:
                    sleep(args.timeout)
                #cv2.waitKey(50)
                cv2.destroyAllWindows()
    if empty:
        print "No subjects"
        return 2
    else:
        return 0

# Show subject
def show(args):
    directory = os.path.join(subjects_directory, args.subject)
    if os.path.exists(directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            image_pil = Image.open(file_path)
            image = np.array(image_pil, 'uint8')
            cv2.imshow(args.subject, image)
            if args.timeout:
                sleep(args.timeout)
            #cv2.waitKey(50)
            cv2.destroyAllWindows()
        return 0
    else:
        print("No entry found")
        return 2

# Check if subject exists
def check(args):
    directory = os.path.join(subjects_directory, args.subject)
    if os.path.exists(directory):
        print("Subject '{0}' exists".format(args.subject))
        return 0
    else:
        print("No entry found")
        return 2

# Delete subject
def delete(args):
    directory = os.path.join(subjects_directory, args.subject)
    if os.path.exists(directory):
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except OSError, e:
                fatal(e)
        try:
            os.removedirs(directory)
        except OSError, e:
            fatal(e)
        print("Subject '{0}' deleted".format(args.subject))
        return 0
    else:
        print("No entry found")
        return 2

# Compare two images
def compare(args):
    for file in args.first_files:
        if not os.path.exists(file):
          fatal("File not found: '{0}'".format(file))
    if not os.path.exists(args.second_file):
        fatal("File not found: '{0}'".format(args.second_file))

    faceCascade = cv2.CascadeClassifier(PROFILES['HAAR_FRONTALFACE_ALT2'])


    face_number = 0
    first_faces = []
    for image_path in args.first_files:
        faces, image = detect_faces(image_path)
        if len(faces):
            (x, y, w, h) = faces[len(faces) - 1]
            face_number += 1
            first_face = image[y: y + h, x: x + w]
            first_faces.append(first_face)
            if args.debug:
                cv2.imshow("First face", first_face)
                cv2.waitKey(50)
    if not face_number:
        print("Face was not detected in the first files")
        return 2

    image_pil = Image.open(args.second_file).convert('L')
    image = np.array(image_pil, 'uint8')
    side = math.sqrt(image.size)
    minlen = int(side / 20)
    maxlen = int(side / 2)
    faces = faceCascade.detectMultiScale(image, 1.1, 4, CV2_FLAGS, (minlen, minlen), (maxlen, maxlen))
    if len(faces):
        (x, y, w, h) = faces[len(faces) - 1]
        second_face = image[y: y + h, x: x + w]
        if args.debug:
            cv2.imshow("Second face", second_face)
            cv2.waitKey(50)
    else:
        print("Face was not detected in the second file")
        return 2

    recognizer = cv2.createLBPHFaceRecognizer()
    recognizer.train(first_faces, np.array([1] * len(first_faces)))

    nbr_predicted, conf = recognizer.predict(second_face)
    if nbr_predicted and THRESHOLD['min'] < conf and conf < THRESHOLD['max']:
        print "Match with confidence '{0}'".format(conf)
        return 0
    else:
        print("Not match")
        return 2

def __main__():
    parser = argparse.ArgumentParser(description='A simple face recognizer')
    subparsers = parser.add_subparsers()

    parser_enroll = subparsers.add_parser('enroll', help='Enroll a new subject or update images of existing subject')
    parser_enroll.add_argument('--subject', '-s', help="subject code (name or identifier)", required=True)
    parser_enroll.add_argument('files', type=str, nargs='+', help='paths to image files')
    parser_enroll.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_enroll.add_argument('--debug', '-d', action="store_true", help='show faces of subjects')
    parser_enroll.set_defaults(func=enroll)

    parser_identify = subparsers.add_parser('identify', help='Get the identification of a subject given image of him')
    parser_identify.add_argument('files', type=str, nargs='+', help='paths to image files')
    parser_identify.add_argument('--only', '--within', type=str, help='identify only from specific subjects (comma separated list of codes)')
    parser_identify.add_argument('--ignore', '--exclude', type=str, help='ignore specific subjects (comma separated list of codes)')
    parser_identify.add_argument('--dry', action="store_true", help='output only subject and confidence number divided with space')
    parser_identify.add_argument('--all', action="store_true", help='return all possible identifications')
    parser_identify.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_identify.add_argument('--debug', '-d', action="store_true", help='show faces of subjects')
    parser_identify.set_defaults(func=identify)

    parser_list = subparsers.add_parser('list', help='Get the codes of all enrolled subjects')
    parser_list.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_list.set_defaults(func=list)

    parser_showall = subparsers.add_parser('showall', help='Show faces of all enrolled subjects')
    parser_showall.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_showall.add_argument('--timeout', '-t', help="timeout in seconds between displays of faces", type=int, required=False)
    parser_showall.set_defaults(func=showall)

    parser_show = subparsers.add_parser('show', help='Show face of one enrolled subject')
    parser_show.add_argument('--subject', '-s', help="subject code (name or identifier)", required=True)
    parser_show.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_show.add_argument('--timeout', '-t', help="timeout in seconds between displays of faces", type=int, required=False)
    parser_show.set_defaults(func=show)

    parser_check = subparsers.add_parser('check', help='Check if the subject with given code is entered')
    parser_check.add_argument('--subject', '-s', help="subject code (name or identifier)", required=True)
    parser_check.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_check.set_defaults(func=check)

    parser_delete = subparsers.add_parser('delete', help='Delete a subject by subject code')
    parser_delete.add_argument('--subject', '-s', help="subject code (name or identifier)", required=True)
    parser_delete.add_argument('--storage', help="directory for keeping faces images", required=False)
    parser_delete.set_defaults(func=delete)

    parser_compare = subparsers.add_parser('compare', help='Compare similarity of two images')
    parser_compare.add_argument('first_files', type=str, nargs='+', help='images set with same face')
    parser_compare.add_argument('second_file', help='comparable image')
    parser_compare.add_argument('--debug', '-d', action="store_true", help='show faces')
    parser_compare.set_defaults(func=compare)

    args = parser.parse_args()

    global subjects_directory
    if getattr(args, 'storage', None) is not None:
        subjects_directory = args.storage
        if not os.path.exists(subjects_directory):
            os.makedirs(subjects_directory)
    else:
        subjects_directory = os.path.join(os.curdir, "subjects")

    check_profiles()
    return args.func(args)

if __name__ == '__main__':
    sys.exit(__main__())
