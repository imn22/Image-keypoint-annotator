import os
import shutil
import csv

from flask import Flask, redirect, url_for, request, flash, session
from flask import render_template
from flask import send_file
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No files selected')
            return redirect('/')
        try:
            shutil.rmtree('./images')
            shutil.rmtree('./annotated_images')
        except:
            pass
        os.mkdir('./images')

        os.mkdir('./annotated_images')
        files = request.files.getlist("file")
        for f in files:
            f.save(os.path.join('./images', f.filename))
        for (dirpath, dirnames, filenames) in os.walk(app.config["IMAGES"]):
            files = filenames
            break
        app.config["FILES"] = files
        return redirect('/tagger', code=302)
    else:
        return render_template('index.html')


@app.route('/tagger')
def tagger():
    if (app.config["HEAD"] == len(app.config["FILES"])):
        return redirect(url_for('final'))
    directory = app.config["IMAGES"]
    image = app.config["FILES"][app.config["HEAD"]]
    labels = app.config["LABELS"]
    not_end = not(app.config["HEAD"] == len(app.config["FILES"]) - 1)
    print(not_end)
    return render_template('tagger.html', not_end=not_end, directory=directory, image=image, labels=labels, head=app.config["HEAD"] + 1, len=len(app.config["FILES"]))


@app.route('/next')
def next():
    image = app.config["FILES"][app.config["HEAD"]]

    # with open(app.config["OUT"],'a') as f:
    #     for label in app.config["LABELS"]:
            # f.write(image + "," +
            #         label["id"] + "," +
            #         label["name"] + "," +
            #         str(round(float(label["x"]))) + "," +
            #         str(round(float(label["y"]))) + "\n")
    coords = []
    with open(app.config["OUT"], 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for label in app.config["LABELS"]:
            coords.append(round(float(label["x"])))
            coords.append(round(float(label["y"])))
        writer.writerow([image, *coords])


    # Open the image and get its size
    img = Image.open(os.path.join('./images', app.config["FILES"][app.config["HEAD"]]))
    # Create a drawing object
    draw = ImageDraw.Draw(img)
    # Iterate over the labels and draw each point
    for i, label in enumerate(app.config["LABELS"]):
        # Split the line into x and y coordinates
        x, y = float(label["x"]), float(label["y"])
        # Draw a circle at the point
        # Draw a rectangle at the point
        draw.rectangle([(int(x) - 3, int(y) - 3), (int(x) + 3, int(y) + 3)], fill="red", outline="red")

        # Add the name above the point
        text = f"POI: {i + 1}"
        draw.text((int(x) , int(y) -28), text, fill="red", font=ImageFont.truetype("arial.ttf", 23))
    # Save the image with the same filename
    img.save(os.path.join('./annotated_images', image))

    app.config["HEAD"] = app.config["HEAD"] + 1
    app.config["LABELS"] = []
    # shutil.copyfile(os.path.join('./images', image), os.path.join('./annotated_images', image))
    return redirect(url_for('tagger'))


@app.route("/final")
def final():
    return render_template('final.html')


@app.route('/add/<id>')
def add(id):
    x = request.args.get("x")
    y = request.args.get("y")
    label_name = f"POI {int(id)}"
    app.config["LABELS"].append({"id":id, "name":label_name, "x":x,"y":y})
    return redirect(url_for('tagger'))


@app.route('/remove/<id>')
def remove(id):
    index = int(id) - 1
    del app.config["LABELS"][index]
    for label in app.config["LABELS"][index:]:
        a=int(label["id"])
        label["id"] = str(a - 1)
        label["name"] = f"POI {a - 1}"
    return redirect(url_for('tagger'))


@app.route('/clear')
def clear():
    app.config["LABELS"].clear()
    return redirect(url_for('tagger'))


@app.route('/rotate_left', methods=['POST'])
def rotate_left():
    angle = 90
    image_path = os.path.join('./images', app.config["FILES"][app.config["HEAD"]])
    with Image.open(image_path) as im:
        im_rotated = im.rotate(angle, expand=True)
        im_rotated.save(image_path)
    return redirect(url_for('tagger'))


@app.route('/rotate_right', methods=['POST'])
def rotate_right():
    angle = -90
    image_path = os.path.join('./images', app.config["FILES"][app.config["HEAD"]])
    with Image.open(image_path) as im:
        im_rotated = im.rotate(angle, expand=True)
        im_rotated.save(image_path)
    return redirect(url_for('tagger'))


@app.route('/label/<id>')
def label(id):
    name = f"POI {int(id)}"
    app.config["LABELS"][int(id) - 1]["name"] = name
    return redirect(url_for('tagger'))


@app.route('/image/<f>')
def images(f):
    images = app.config["IMAGES"]
    return send_file(images +'/'+f)


@app.route('/download')
def download():
    shutil.copyfile('out.csv', 'images/annotations.csv')

    return


if __name__ == "__main__":
    app.config["IMAGES"] = 'images'
    app.config["LABELS"] = []
    app.config["HEAD"] = 0
    app.config["OUT"] = "out.csv"
    with open("out.csv",'w') as f:
        f.write("image,x1,y1, x2,y2, x3,y3, x4,y4, x5,y5,x6,y6\n")
    app.run(debug="True")