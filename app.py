from flask import Flask,render_template, url_for, flash, redirect, request, Blueprint,session,jsonify,send_file
from werkzeug import secure_filename
import os, glob
from image_process import pdf_split,image_conversion,OCR_read1,OCR_read2
from net_worth import net_worth
from pbit_tot import pbit_tot
from total_assets import total_assets
from total_curr_liab import total_curr_liab
from total_liab import total_debt
from word_count import word_count
from forms import ImageForm,Financial_RiskForm,Financial_RiskForm1
from io import BytesIO
import pandas as pd
import subprocess
from Configuration import fl_Dict,sales,debt,assets,netWorth,pbit,capEmp,qrCA,cfa
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

        #filename.close()
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

        for i in page_num_lst:
            filename= "split-page%s.pdf" % i
            filename1= "split-page%s.png" % i
            image_conversion(upload_folder,filename,i)
            OCR_read1(upload_folder,filename,i)
            #page_num_lst = ','.join(page_num_lst1)
        return redirect(url_for('FinancialRisk', page_num_lst=page_num_lst),code=307)

    return render_template('OCR_Process.html',form=form)






@app.route('/financialrisk<page_num_lst>', methods = ['GET', 'POST'])
def FinancialRisk(page_num_lst):
            upload_folder = "C:/Project Spreading tool/OCR_APP/tmp/"
            networth_comp=0
            pbit_comp=0
            assets_comp=0
            liab_comp=0
            curr_liab_comp=0
            page_num_lst = page_num_lst.replace("[","")
            page_num_lst = page_num_lst.replace("]","")
            page_num_lst = page_num_lst.replace("'","")
            page_num_lst = page_num_lst.replace("'","")
            page_num_lst = page_num_lst.replace(" ","")
            page_num_lst = page_num_lst.split(",")
            print(page_num_lst)
            for i in page_num_lst:
                #filename= "split-page%s.pdf" % i
                #filename1= "split-page%s.png" % i
                #filename= "split-page8.pdf"
                filename1= "split-page%s-grayscale.png" % i
                #OCR_read1(upload_folder,filename,i)
                data_arr = OCR_read2(upload_folder,filename1,i)
                networth_comp=networth_comp+net_worth(data_arr)
                liab_comp=liab_comp+total_debt(data_arr)
                curr_liab_comp=curr_liab_comp+total_curr_liab(data_arr)
                assets_comp=assets_comp+total_assets(data_arr)
                pbit_comp=pbit_comp+pbit_tot(data_arr)
                try:
                    gear_ratio=liab_comp/networth_comp
                except:gear_ratio=0
                try:
                    roce=pbit_comp/(assets_comp-curr_liab_comp)
                except:roce=0
                print(networth_comp)
                print(liab_comp)
                print(curr_liab_comp)
                print(pbit_comp)
                print(assets_comp)
                form1=Financial_RiskForm1(tot_debt = liab_comp,
                net_equity = networth_comp,
                gearing = gear_ratio,
                pb_it = pbit_comp,
                tot_assets = assets_comp,
                cap_emp = (assets_comp-curr_liab_comp),
                curr_liab = curr_liab_comp,
                roce = roce)
            return render_template('fr.html', form = form1)





if __name__ == '__main__':
   app.run(debug = True)
