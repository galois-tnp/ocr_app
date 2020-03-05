from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Configuration import fl_Dict,sales,debt,assets,netWorth,pbit,capEmp,qrCA,cfa
import fnmatch,re
from word_count import word_count


############## Function for PBIT computation ############

def pbit_tot(arr):
    text3=arr
    pbit_tot = 0
    for i in text3:
        istring=i.split(' ')
        cntstr=len(fnmatch.filter(istring,'20??'))
        if(cntstr>1):break
    for k in text3:
        k=k.replace("|","")
        k=k.replace("_","")
        k=k.replace("=","")
        k=k.replace("—-","")
        if(k.split(" ")[0].isalpha()==False):
            k=k.replace(k.split(" ")[0],"")
        for l in range(0,len(pbit['PBIT'])):
            if(word_count(k.lower())==word_count(pbit['PBIT'][l].lower())):
                print("k identifier"+" "+k)
                print("pbit"+" "+pbit['PBIT'][l])
                if(k.lower().find(pbit['PBIT'][l].lower())!=-1):
                    bal_str=k.lower().replace(pbit['PBIT'][l].lower(),"")
                    bal_str=bal_str.replace("|","")
                    bal_lst=bal_str.split(" ")

                    bal_lst1=[]
                    for j in range(0,len(bal_lst)):
                        if(bal_lst[j] !=''):bal_lst1.append(bal_lst[j])
                    bal_lst=bal_lst1
                    print(bal_lst)
                    if(len(bal_lst)>cntstr):
                        for m in range(0,((len(bal_lst))-cntstr)):
                            bal_lst.pop(0)
                    if(len(bal_lst)!=0):
                        str_ng=bal_lst[0].replace(",","")
                        str_ng=str_ng.replace(".","")
                        if((str_ng.isdigit()==True or str_ng.isdigit()==True) and (pbit['PBIT'][l].lower()=="Profit before tax") and word_count(k.lower())==word_count("Profit before tax")):
                            pbit_tot=float(bal_lst[0].replace(",",""))
                            print ("hh %s" %total_assets)
                            break
                        if(str_ng.isdigit()==True or str_ng.isdigit()==True):

                            pbit_tot=pbit_tot+ float(bal_lst[0].replace(",",""))
                            print ("gg %s" %pbit_tot)
                        elif(bal_lst[0]=="-"):
                            pbit_tot=pbit_tot+ float(bal_lst[0].replace("-","0"))
                            print ("kk %s" %pbit_tot)
                        elif(bal_lst[0].find("(")!=-1):
                            pbit1=bal_lst[0].replace("(","")
                            pbit1=pbit1.replace(")","")
                            pbit_tot=pbit_tot - float(pbit1)
                            print ("kk %s" %pbit_tot)
        if(k.lower().find("Profit before tax")!=-1 and word_count(k.lower())==word_count("Profit before tax")):
            break
    return pbit_tot


########################################################################################################################
