import zipfile

from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
from ipywidgets import interact
from numpy import asarray
from IPython.display import display


# loading the face detection classifier
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')
#Function list 

def load_from_zip(zip_file):
    #importing zip file 
    new_zip = zipfile.ZipFile(zip_file, mode='r', allowZip64=True)
    #extracting data from zip file to current directory
    ims = new_zip.extractall()
    #creating a list of names of items in the zip file
    extracted_ims = new_zip.namelist()
    images = []
    for i in extracted_ims: 
        images.append(i)
    return images

def find_words(img): 
    '''Method of finding words in document. Img goes in in as an array
    
    It displays the Image and displays the text'''
    
    new_img = Image.open(img)
    input_strs = pytesseract.image_to_string(new_img.convert('L')).replace('-\n','')
    return input_strs
   
def find_faces(img): 
    '''Method of finding faces from an image. input is a string img input'''
   
    input_img = cv.imread(img)
    faces = (face_cascade.detectMultiScale(np.array(input_img),1.35,4))
    if faces == (): 
        return None
    else:
        faces.tolist()
        RGB_img = Image.open(img).convert('RGB')
        drawing=ImageDraw.Draw(RGB_img) 

    # For each item in faces, lets surround it with a red box
    list_of_faces = []
    for x,y,w,h in faces:
    #Cropping the rectangle out of the image and appending to a list 
        n = RGB_img.crop((x,y,(x+w),(y+h)))
        list_of_faces.append(n)
    return list_of_faces


def contact_sheet(lists):
    # create a contact sheet
    first_image=lists[0]
    new_size = (200,200)
    resized_image = first_image.resize(new_size)
    contact_sheet=Image.new(first_image.mode, (int(resized_image.width*4),int(resized_image.height*2)))
    x=0
    y=0

    for img in lists:
    # Pasting images into the contact sheet and resize all the images for better display
        new_img = img.resize(new_size)
        contact_sheet.paste(new_img, (x, y))
        if x+resized_image.width == contact_sheet.width:
            x=0
            y=y+resized_image.height
        else:
            x=x+resized_image.width

    # resize and display the contact sheet
    contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
    display(contact_sheet)
    
img_list = load_from_zip('small_img.zip')
big_img_list = load_from_zip('images.zip')


#Small zip file 
print('Small Zip File')
for i in img_list: 
    words = find_words(i)
    if 'Christopher' in words:
        print('results found in file {}'.format(i))
        x = find_faces(i)
        if x == None: 
            print('But no faces in that file!')
        else:
            contact_sheet(x)
    else:
        print('Word not present in file {} image'.format(i))
        
        
#Large zip file
print('Large Zip File')
for i in big_img_list: 
    words = find_words(i)
    if 'Mark' in words:
        print('results found in file {}'.format(i))
        x = find_faces(i)
        if x == None: 
            print('But no faces in that file!')
        else:
            contact_sheet(x)
    else:
        print('Word not present in file {} image'.format(i))
