from flask import Flask, render_template, request,url_for, redirect,send_file
from flask_bootstrap import Bootstrap 

import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import sys
import os

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template('index.html')

def pdf_merge(pdf_list):
    merger=PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        print(pdf)
        merger.append(pdf)
    merger.write('merged.pdf')

# pdf_merge(["uploads/13.pdf","uploads/Project.pdf","uploads/android_advanced_tutorial.pdf"])

@app.route('/submit_form', methods=['POST','GET'])
def submit_form():
    if request.method=='POST':
        try:
            data=request.files.getlist("files[]")
            print(data)
            pdf_names=[]
            for file in data:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    pdf_names.append(UPLOAD_FOLDER+filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(pdf_names)
            pdf_merge(pdf_names)
            return send_file('merged.pdf', as_attachment=True)
        except:
            return 'did not save to database'
    else:
        return 'Something Wrong'

app.run(debug=True)