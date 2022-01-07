#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from flask import Flask,request,abort,render_template,send_file,flash
from werkzeug.utils import secure_filename
from datetime import datetime



app=Flask(__name__)

app.config['SECRET_KEY']='development'


PATH=os.path.join(app.root_path,'files')

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if "upload" in request.files:
            f=request.files['upload']

            secured_filename=os.path.join(PATH,secure_filename(f.filename))
            
            if os.path.exists(secured_filename):
                flash(f'File already exists : {secured_filename}')
                app.logger.log(f'File already exists : {secured_filename}')
                return redirect(url_for('.index'))

            f.save(secured_filename)

    tbody=[]
    for f in os.listdir(PATH):
        if f in ['.','..']:
            continue
        st=os.stat(os.path.join(PATH,f))
        ctime=datetime.fromtimestamp(st.st_ctime)
        tbody.append(  
                (
                    f,
                    st.st_size,
                    ctime.strftime('%F %T')
                ) 
            )

    return render_template('index.html',tbody=tbody )


@app.get('/files/<_file>')
def sendfile(_file):

    if _file not in  os.listdir(PATH)  or _file[0] == '.' :
        flash('File not found')
        return redirect(url_for('.index'))
    
    f=os.path.join(PATH,_file)

    return send_file(f)
    


@app.get('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path,'static'),'favicon.ico',mimetype='image/vnd.microsoft.icon')



if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.mkdir(PATH,mode=511)
    app.run(host='0.0.0.0',debug=True)
