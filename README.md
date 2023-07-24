# IMAGE ANNOTATOR

Image Annotator is a Flask-based web application that allows users to tag points of interest (POI) in a set of images. Users can upload a set of images, one or multiple, to the application and then annotate each image by clicking on points of interest on it. The application will save the images with their POIs marked in red points and labeled with their corresponding POI number.

# Installation

1. Install the required dependencies using the following command: pip install -r requirements.txt.
2. Run the application with python app.py.
3. Open your web browser and go to http://localhost:5000.


# Usage
The Image Annotator allows users to:

1. Upload a set of images to be annotated. (Multiple images can be uploaded at once).
2. Annotate each image by clicking on points of interest on the image. POIs are marked with red circles and labeled with their corresponding POI number.
3. Save the annotated images to a folder 'annotated_images'.
4. Save the annotations as a csv file 'annotations.csv'
