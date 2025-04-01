from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("base.html", title="home", content_colour="red")

@app.route("/photography/gallery")
def photo_gallery():
    return render_template("photography/gallery.html", title="gallery", content_colour="purple")

@app.route("/photography/equipment")
def photo_equipment():
    return render_template("photography/equipment.html", title="equipment", content_colour="purple")

@app.route("/cubing/progress")
def cubing_progress():
    return render_template("cubing/progress.html", title="progress", content_colour="blue")

@app.route("/services/minecraft")
def serv_minecraft():
    return render_template("services/minecraft.html", title="minecraft", content_colour="teal")

@app.route("/other/hmmmmmmmm")
def other_hmmmmmmmm():
    return render_template("other/hmmmmmmmm.html", title="hmmmmmmmm", content_colour="green")
