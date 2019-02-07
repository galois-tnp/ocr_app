from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf2image import convert_from_path
import os
from PIL import Image
import pytesseract
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Configuration import fl_Dict,sales,debt,netWorth,pbit,capEmp,qrCA,cfa
import fnmatch

def pdf_split(filePath,file):
    inputpdf = PdfFileReader(open(os.path.join(filePath, file), "rb"))
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        with open(os.path.join(filePath, "split-page%s.pdf") % i, "wb") as outputStream:
            output.write(outputStream)
    return inputpdf.numPages

#### Convert PDF into image ####

def image_conversion(filePath, file,page_num):
    pages = convert_from_path(os.path.join(filePath, "split-page%s.pdf") % page_num, 500)
    for page in pages:
        page.save(os.path.join(filePath, "split-page%s.png") % page_num, 'PNG')

#### OCR read ####

def OCR_read(filePath,file,page_num):
    inputPath = os.path.join(filePath, "split-page%s.png") % page_num
    inputImage = os.path.join(filePath, "split-page%s-grayscale.png") % page_num

### Convert image into grayscale ###
    image = cv2.imread(inputPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

### Image pre processing ###
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

### Save grayscale image to temporary folder ###
    cv2.imwrite(inputImage, gray)

### load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file ##
    text = pytesseract.image_to_string(Image.open(inputPath),lang = 'eng',config = '--psm 6')
    text1 = pytesseract.image_to_string(Image.open(inputImage),lang = 'eng',config = '--psm 6')

### Creating block from text

    text2 =  text.split('\n')
    text3 = np.array(text2)
    df = pd.DataFrame(columns=['1','2','3','4','5','6','7','8','9','10'])
    a,b,c,d,e,f,g,h,m,n=[],[],[],[],[],[],[],[],[],[]

################## Translate to excel ########

    for i in range(0,len(text3)):
        cnt=1
        fir_str=""
        fir_st=""
        if(sum(c.isdigit() for c in text3[i])<7):
            a.append(text3[i])
            b.append("")
            c.append("")
            d.append("")
            e.append("")
            f.append("")
            g.append("")
            h.append("")
            m.append("")
            n.append("")
        elif(text3[i].find("$")!=-1):
            st_ring=text3[i].split()
            count=1
            for p in range(0,len(st_ring)):
                if(count==1):
                    a.append(st_ring[p])
                    count=count+1
                elif(count==2):
                    b.append(st_ring[p])
                    count=count+1
                elif(count==3):
                    c.append(st_ring[p])
                    count=count+1
                elif(count==4):
                    d.append(st_ring[p])
                    count=count+1
                elif(count==5):
                    e.append(st_ring[p])
                    count=count+1
                elif(count==6):
                    f.append(st_ring[p])
                    count=count+1
                elif(count==7):
                    g.append(st_ring[p])
                    count=count+1
                elif(count==8):
                    h.append(st_ring[p])
                    count=count+1
                elif(count==9):
                    m.append(st_ring[p])
                    count=count+1
                elif(count==10):
                    n.append(st_ring[p])
                    count=count+1
        else:
            ls_t1=text3[i].split()
            for j in range(0,len(ls_t1)):
                if(sum(c.isdigit() for c in ls_t1[j])==0):
                    ls_t = ls_t1[j].replace(",","")
                    ls_t = ls_t.replace("(","")
                    ls_t = ls_t.replace(")","")
                else:
                    ls_t = ls_t1[j].replace(",","")
                if((((ls_t.isalpha()==True and ls_t.isdigit()== False) or (ls_t.isalpha()==False and ls_t.isdigit()== False))and(ls_t!="." and ls_t!="-") and ls_t.find(")")==-1 )):
                    fir_st=fir_st+" "+ls_t
                    fir_str=fir_st
                    #print(fir_str)
                elif((ls_t.isdigit()==True and sum(c.isdigit() for c in ls_t)>2 and ls_t.isalpha()==False)or ls_t.find(")")!=-1 or ls_t.find(".")!=-1 or ls_t.find("-")!=-1):
                    if(cnt==1):
                        a.append(fir_str)
                        b.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==2):
                        c.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==3):
                        d.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==4):
                        e.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==5):
                        f.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==6):
                        g.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==7):
                        h.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==8):
                        m.append(ls_t)
                        cnt=cnt+1
                    elif(cnt==9):
                        n.append(ls_t)
                        cnt=cnt+1
    try:
        df.iloc[:,0]=a
    except:(e)
    try:
        df.iloc[:,1]=b
    except:(e)
    try:
        df.iloc[:,2]=c
    except:(e)
    try:
        df.iloc[:,3]=d
    except:(e)
    try:
        df.iloc[:,4]=e
    except:(e)
    try:
        df.iloc[:,5]=f
    except:(e)
    try:
        df.iloc[:,6]=g
    except:(e)
    try:
        df.iloc[:,7]=h
    except:(e)
    try:
        df.iloc[:,8]=m
    except:(e)
    try:
        df.iloc[:,9]=n
    except:(e)

    return df
###################################
def OCR_read1(filePath,file,page_num):
    inputPath = os.path.join(filePath, "split-page%s.png") % page_num
    inputImage = os.path.join(filePath, "split-page%s-grayscale.png") % page_num

### Convert image into grayscale ###
    image = cv2.imread(inputPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

### Image pre processing ###
    gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

### Save grayscale image to temporary folder ###
    cv2.imwrite(inputImage, gray)

### load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file ##
    #text = pytesseract.image_to_string(Image.open(inputPath),lang = 'eng',config = '--psm 6')
    text1 = pytesseract.image_to_string(Image.open(inputImage),lang = 'eng',config = '--psm 6')

### Creating block from text

    text2 =  text1.split('\n')
    text3 = np.array(text2)
    return text3

################## Translate to excel ########
def bal_ratio(text3):
    for i in text3:
        istring=i.split(' ')
        cntstr=len(fnmatch.filter(istring,'20??'))
        if(cntstr>1):break

    for i in text3:
        for j in range(0,len(fl_Dict['Balance Sheet'])):
            if(i.lower().find(fl_Dict['Balance Sheet'][j].lower())!=-1):
                for k in text3:
                    for l in range(0,len(debt['Debt'])):
                        if(k.lower().find(debt['Debt'][l].lower()!=-1)):
                            bal_str=k.replace(debt['Debt'][l].lower(),"")
                            bal_lst=bal_str.split(" ")
                            if(len(bal_lst)>cntstr):
                                for m in range(0,(cntstr-len(bal_lst))):
                                    bal_lst.pop(m)
                            total_liab=float(bal_lst[0].replace(",",""))
                    for l in range(0,len(netWorth['Networth'])):
                        if(k.lower().find(netWorth['Networth'][l].lower()!=-1)):
                            bal_str=k.replace(netWorth['Networth'][l].lower(),"")
                            bal_lst=bal_str.split(" ")
                            if(len(bal_lst)>cntstr):
                                for m in range(0,(cntstr-len(bal_lst))):
                                    bal_lst.pop(m)
                            net_worth=float(bal_lst[0].replace(",",""))
