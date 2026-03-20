from dbm import dumb
import os
from flask import Flask, render_template, request
from main import pdf_to_img

app=Flask(__name__)

UPLOAD_FOLDER='static/uploads'
OUTPUT_FOLDER='static/outputs'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['OUTPUT_FOLDER']=OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('index.html')    

@app.route('/convert',methods=["POST"])
def convert():
    file=request.files.get("pdf")
    image_type=request.form.get("format")
    
    if file and file.filename!="":
        os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
        file_path=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(file_path)
        output_images=pdf_to_img(file_path,image_type,app.config['OUTPUT_FOLDER'])
        return render_template('index.html',images=output_images)
    else:
        return render_template('index.html',error="No file uploaded")

if __name__=='__main__':
    app.run(debug=True)