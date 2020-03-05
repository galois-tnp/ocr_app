from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
# import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Configuration import fl_Dict,sales,debt,assets,netWorth,pbit,capEmp,qrCA,cfa
import fnmatch,re
from word_count import word_count


############## Function for Networth computation ############

def net_worth(arr):
    text3=arr
    net_worth = 0
    for i in text3:
        istring=i.split(' ')
        cntstr=len(fnmatch.filter(istring,'20??'))
        if(cntstr>1):break
    for k in text3:
        k=k.replace("|","")
        k=k.replace("_","")
        k=k.replace("=","")
        if(k.split(" ")[0].isalpha()==False):
            k=k.replace(k.split(" ")[0],"")
        for l in range(0,len(netWorth['Networth'])):
            if(word_count(k.lower())==word_count(netWorth['Networth'][l].lower())):
                print("k identifier"+" "+k)
                print("networt"+" "+netWorth['Networth'][l])
                if(k.lower().find(netWorth['Networth'][l].lower())!=-1):
                    bal_str=k.lower().replace(netWorth['Networth'][l].lower(),"")
                    bal_str=bal_str.replace("|","")
                    bal_lst=bal_str.split(" ")
                    bal_lst1=[]
                    for j in range(0,len(bal_lst)):
                        if(bal_lst[j] !=''):bal_lst1.append(bal_lst[j])
                    bal_lst=bal_lst1
                    if(len(bal_lst)>cntstr):
                        for m in range(0,((len(bal_lst))-cntstr)):
                            bal_lst.pop(0)
                    if(len(bal_lst)!=0):
                        str_ng=bal_lst[0].replace(",","")
                        str_ng=str_ng.replace(".","")
                        if((str_ng.isdigit()==True or str_ng.isdigit()==True) and (netWorth['Networth'][l].lower()=="total equity") and word_count(k.lower())==word_count("total equity")):
                            net_worth=float(bal_lst[0].replace(",",""))
                            print ("hh %s" %net_worth)
                            break
                        if(str_ng.isdigit()==True or str_ng.isdigit()==True):
                            net_worth=net_worth+ float(bal_lst[0].replace(",",""))
                            print ("gg %s" %net_worth)
                        elif(bal_lst[0]=="-"):
                            net_worth=net_worth+ float(bal_lst[0].replace("-","0"))
                            print ("kk %s" %net_worth)
        if(k.lower().find("total equity")!=-1 and word_count(k.lower())==word_count("total equity")):
            break
    return net_worth

##################################################################
