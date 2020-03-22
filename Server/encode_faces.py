# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

def member(list, str):
	for i in list:
		if str == i:
			return True
	return False

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-f", "--file-exists", type=int, required=True,
	help="1 file exists, 0 file does not exist")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# opening already encoded names or creating new one
print("[INFO] unserializing encodings...")

if args["file_exists"] == 1:
	f = open(args["encodings"], "rb")
	data = pickle.load(f)
	f.close()
	knownEncodings = data["encodings"]
	knownNames = data["names"]
	knownPaths = data["paths"]
else:
	knownEncodings = []
	knownNames = []
	knownPaths = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	if member(knownPaths, imagePath):
		print("[INFO] image already encoded...")
		continue
	else:
		knownPaths.append(imagePath)

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames, "paths": knownPaths}
f = open(args["encodings"], "wb")
pickle.dump(data, f)
f.close()
print("[INFO] encoding complete!")
