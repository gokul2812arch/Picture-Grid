try:
    from Tkinter import *
    from Tkinter import filedialog
    import tkFileDialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog
from tkinter import Tk,Frame,Button,StringVar,Label,DoubleVar,IntVar,Entry,OptionMenu,BooleanVar,Checkbutton
from tkinter import filedialog
from tkinter.messagebox import showerror
import os
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from math import ceil
import math 


global hItem
global vItem
global png_list
global jpg_list
global width_1_image
global height_1_image
global annotation
global annotation_scale
global start_number
global step_number
global prefix
global suffix

# grid size 
hItem = 3
vItem = 5

# output file name
file_output_name = 'combined'

# image with annotation name 
annotation_file_name = 'combined_A'

# annotation 
annotation_scale = 1 
start_number = 1
step_number = 1
# suffix / prefix for annotation 
prefix = "Picture"
suffix = "."







def commbine_pictures_jpg():

	# get size of i image 
	im = Image.open(jpg_list[0])
	width_1_image, height_1_image = im.size 

	# number of images to load 
	total_number_of_images = len(jpg_list)
	print(len(jpg_list),"----length of all pictures present")

	number_of_immages = vItem * hItem
	print(number_of_immages, "----number of pictures in grid")

	number_of_images_to_get = number_of_immages - 1
	step_integer = math.floor(total_number_of_images / (number_of_images_to_get))
	print(step_integer, "------step value")

	list_images_new = []

	l = 0 
	for i in range(number_of_images_to_get):
		list_images_new.append(jpg_list[l])
		l = l + step_integer

	list_images_new.append(jpg_list[-1])
	print("a")
	print("a")
	print("a")

	print(list_images_new)

	# create the master image large size 
	new_image = Image.new("RGB", (vItem*width_1_image, hItem*height_1_image))
	i = 0 
	for y in range(hItem):
		if i>=len(list_images_new):
			break
		y *= height_1_image
		for x in range(vItem):
			x *= width_1_image
			im2 = Image.open(list_images_new[i])
			width_2_image, height_2_image = im2.size 
			new_image.paste(im2, (x,y,x+width_2_image,y+height_2_image))
			print("paste", x,y)
			i +=1

	new_image.save(file_output_name +'.jpg')

	txt_height = annotation_scale * 0.05 * height_1_image 
	im3 = new_image
	draw = ImageDraw.Draw(im3)
	font = ImageFont.truetype("arial.ttf", int(txt_height))
	i=0
	for y in range(hItem):
		if i>=len(list_images_new):
			break
		y *= height_1_image
		for x in range(vItem):
			x *= width_1_image
			im4 = Image.open(list_images_new[i])
			width_4_image, height_4_image = im4.size 
			if i + start_number == 0:
				text_to_draw = prefix + str(0) + suffix 
			else:
				text_to_draw = prefix + str(i*step_number + start_number) + suffix
			draw.text((x+(int(width_4_image/10)), y+height_4_image-int(txt_height*1.1)),str(text_to_draw),font=font,fill=(0,0,0))
			i +=1
	im3.save(annotation_file_name +'.jpg')



#get png file names
def import_dir_png(folder):
	png_list = []
	for file in os.listdir(folder):
		if file.endswith('.png'):
			png_list.append(os.path.join(folder, file))

			# sort file names in ascending order 
			# sort(key=lambda f: int(re.sub('\D', '', f)))  # for python 3 
			# sort(key=lambda f: int(filter(str.isdigit, f)))    # for python 2    
			# credits https://stackoverflow.com/questions/33159106/sort-filenames-in-directory-in-ascending-order
			png_list.sort(key=lambda f: int(re.sub('\D', '', f)))   

	return (png_list)

#get png file names
def import_dir_jpg(folder):
	jpg_list = []
	for file in os.listdir(folder):
		if file.endswith('.jpg'):
			jpg_list.append(os.path.join(folder, file)) 

			# sort file names in ascending order 
			# sort(key=lambda f: int(re.sub('\D', '', f)))  # for python 3 
			# sort(key=lambda f: int(filter(str.isdigit, f)))    # for python 2    
			# credits https://stackoverflow.com/questions/33159106/sort-filenames-in-directory-in-ascending-order
			jpg_list.sort(key=lambda f: int(re.sub('\D', '', f)))  
	return (jpg_list)

def browse_folder():
	global png_list
	global jpg_list
	global folderPath

	folderPath = filedialog.askdirectory()
	print(folderPath,"-----folder path")

	#get png files
	png_list = import_dir_png(folderPath + "/")
	print("searching for png files")
	

	if len(png_list)<1:
		print("no png files in the folder")
	else:
		print(png_list)

	jpg_list = import_dir_jpg(folderPath + "/")
	print("searching for jpg files")

	if len(jpg_list)<1:
		print("no jpg files in the folder")
	else:
		print(jpg_list)


browse_folder()
commbine_pictures_jpg()
