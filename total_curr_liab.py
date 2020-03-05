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


############## Function for total current liabilities computation ############

def total_curr_liab(arr):
    text3=arr
    total_curr_liab = 0
    for i in text3:
        istring=i.split(' ')
        cntstr=len(fnmatch.filter(istring,'20??'))
        if(cntstr>1):break
    for n in range(0,len(text3)):
        if (text3[n].find("Current liabilities")!=-1):
            for p in range(n,len(text3)):
                k=text3[p]
                k=k.replace("|","")
                k=k.replace("_","")
                k=k.replace("=","")
                if(k.split(" ")[0].isalpha()==False):
                    k=k.replace(k.split(" ")[0],"")
                for l in range(0,len(capEmp['Capital Employed'])):
                    print
                    if(word_count(k.lower())==word_count(capEmp['Capital Employed'][l].lower())):
                       print("k identifier"+" "+k)
                       print("debt"+" "+capEmp['Capital Employed'][l])
                       if(k.lower().find(capEmp['Capital Employed'][l].lower())!=-1):
                           bal_str=k.lower().replace(capEmp['Capital Employed'][l].lower(),"")
                           bal_str=bal_str.replace("|","")
                           bal_lst=bal_str.split(" ")
                           print(bal_lst)
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
                               if((str_ng.isdigit()==True or str_ng.isdigit()==True) and (capEmp['Capital Employed'][l].lower()=="total current liabilities") and word_count(k.lower())==word_count("total current liabilities")):
                                   total_curr_liab=float(bal_lst[0].replace(",",""))
                                   print ("hh %s" %total_curr_liab)
                                   break
                               if(str_ng.isdigit()==True or str_ng.isdigit()==True):
                                   total_curr_liab=total_curr_liab+ float(bal_lst[0].replace(",",""))
                                   print ("gg %s" %total_curr_liab)
                               elif(bal_lst[0]=="-"):
                                   total_curr_liab=total_curr_liab+ float(bal_lst[0].replace("-","0"))
                                   print ("kk %s" %total_curr_liab)
                if(k.lower().find("total current liabilities")!=-1 and word_count(k.lower())==word_count("total current liabilities")):
                    break
    return total_curr_liab

########################################################################################################################
