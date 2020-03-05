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

############### Function for word count ###############

def word_count(string):
    return len(re.findall("[a-zA-Z_]+", string))

######################################################
