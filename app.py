from curses import flash
from dbm import dumb
import os
import zipfile
from flask import Flask, redirect, render_template, request, send_file, url_for
from main import pdf_to_img

app=Flask(__name__)

UPLOAD_FOLDER='static/uploads'
OUTPUT_FOLDER='static/outputs'

app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['OUTPUT_FOLDER']=OUTPUT_FOLDER

@app.route('/')
def home():
    return render_template('index.html')    

@app.route('/download-all')
def download_all():
   zip_path='static/outputs/converted_images.zip'
   
   # Remove old zip if exists
   if os.path.exists(zip_path):
        os.remove(zip_path)
    
   # Make sure folder exists
   if not os.path.exists('static/outputs') or not os.listdir('static/outputs'):
        flash("No images found to download.", "error")
        return redirect(url_for('home'))

   with zipfile.ZipFile(zip_path,'w') as zipf:
    for image in os.listdir('static/outputs'):
        zipf.write(os.path.join('static/outputs',image),arcname=image)
   return send_file(zip_path,as_attachment=True)

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