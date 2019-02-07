from flask import Flask,render_template, url_for, flash, redirect, request, Blueprint,session,jsonify,send_file
from werkzeug import secure_filename
import os, glob
from image_process import pdf_split,image_conversion,OCR_read
from forms import ImageForm,ConfigurationForm
from io import BytesIO
import pandas as pd
import subprocess
from Configuration import fl_Dict
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sp!#54rama'


@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    pgs = 0
    upload_folder = "C:/Project Spreading tool/OCR_APP/tmp/"
    for the_file in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(upload_folder, filename))
        pgs = pdf_split(upload_folder,filename)
        #image_conversion(upload_folder,filename)
        return redirect(url_for('OCR_Process'))
    return render_template('main.html')

@app.route('/OCR_Process', methods = ['GET', 'POST'])
def OCR_Process():
    form=ImageForm()
    if form.validate_on_submit():
        page_num= form.pageNum.data
        page_num_lst=[]
        j=""
        for i in page_num:
            if(i!=","):
                j=j+i
            else:
                page_num_lst.append(j)
                j=""
        page_num_lst.append(j)
        print(page_num_lst)
        upload_folder = "C:/Project Spreading tool/OCR_APP/tmp/"
        ind=1
        datfram=[]
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        for i in page_num_lst:
            filename= "split-page%s.pdf" % i
            filename1= "split-page%s.png" % i
            image_conversion(upload_folder,filename,i)
            data_frame = OCR_read(upload_folder,filename1,i)
            datfram.append(data_frame)
            datfram[ind-1].to_excel(writer, sheet_name='Sheet%s'%ind)
            ind=ind+1
        writer.save()
        output.seek(0)
        return send_file(output, attachment_filename='OCR_output.xlsx', as_attachment=True)
    return render_template('OCR_Process.html', form = form)

@app.route('/OCR_Process1', methods = ['GET', 'POST'])
def OCR_Process():
    form=ImageForm()
    if form.validate_on_submit():
        page_num= form.pageNum.data
        page_num_lst=[]
        j=""
        for i in page_num:
            if(i!=","):
                j=j+i
            else:
                page_num_lst.append(j)
                j=""
        page_num_lst.append(j)
        print(page_num_lst)
        upload_folder = "C:/Project Spreading tool/OCR_APP/tmp/"
        ind=1
        datfram=[]
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        for i in page_num_lst:
            filename= "split-page%s.pdf" % i
            filename1= "split-page%s.png" % i
            image_conversion(upload_folder,filename,i)
            data_frame = OCR_read(upload_folder,filename1,i)
            datfram.append(data_frame)
            datfram[ind-1].to_excel(writer, sheet_name='Sheet%s'%ind)
            ind=ind+1
        writer.save()
        output.seek(0)
        return send_file(output, attachment_filename='OCR_output.xlsx', as_attachment=True)
    return render_template('OCR_Process.html', form = form)

@app.route('/configurations', methods = ['GET', 'POST'])
def Configurations():
    form=ConfigurationForm()
    if form.validate_on_submit():
        bal_sheet= form.bal_sheet.data
        profit_loss= form.profit_loss.data
        #bal_sheet_lst=[]
        #profit_loss_lst=[]
        j=""
        k=""
        for i in bal_sheet:
            if(i!=","):
                j=j+i
            else:
                fl_Dict["Balance Sheet"].append(j)
                j=""
        fl_Dict["Balance Sheet"].append(j)
        print(fl_Dict["Balance Sheet"])
        for l in profit_loss:
            if(l!=","):
                k=k+l
            else:
                fl_Dict["Profit and Loss"].append(k)
                k=""
        fl_Dict["Profit and Loss"].append(k)
    return render_template('configurations.html', form = form)


if __name__ == '__main__':
   app.run(debug = True)
