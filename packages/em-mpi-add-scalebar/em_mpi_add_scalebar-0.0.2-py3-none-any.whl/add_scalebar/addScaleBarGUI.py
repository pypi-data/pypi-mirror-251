#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:21:32 2024

@author: vega
"""
import os
import glob
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.exposure import equalize_adapthist
import aicsimageio
from aicsimageio import AICSImage
from microfilm.microplot import microshow
import mrcfile

import argparse
from gooey import Gooey, GooeyParser
from wx.core import wx

is_dark = wx.SystemSettings.GetAppearance().IsUsingDarkBackground()

bg_color = '#343434' if is_dark else '#eeeeee'
wbg_color = '#262626' if is_dark else '#ffffff'
fg_color = '#eeeeee' if is_dark else '#000000'

item_default = {
    'error_color': '#ea7878',
    'label_color': fg_color,
    'help_color': fg_color,
    'description_color': fg_color,
    'full_width': False,
    'external_validator': {
        'cmd': '',
    }
}

#from message import display_message
def addScale(rMeth,imDir,inFile,outFile,convert_8bit,auto_bright_contrast,add_sb,sb_color):
    #sb_color = 'white'  # Scale bar color
    #sb_length = 20
    #f_stat.insert(0,'Running...')
    if rMeth[0] == '1':
        rDir = os.path.join(os.path.split(imDir)[0],'ImagesWithScaleBar')
        if os.path.exists(rDir):
            print('Folder exists: '+rDir )
        else:
            print('Created new folder: ' +rDir)
            os.mkdir(rDir)
       
    # Get list of images in directory and sub folders

    imageInitList = glob.glob(os.path.join(imDir, '**/*' + inFile),
                      recursive=True)
    imageExc = glob.glob(os.path.join(imDir, '**/*' + outFile),
                          recursive=True)
    checkIm = np.setdiff1d(np.array(imageInitList),np.array(imageExc))
    imList = list(checkIm)
    print(imageInitList)
    # 1 . Load each image
    for im in imList:
        #Check if readable (tif)
        sb_unit = 'um'
        try:
            img_info = AICSImage(im)
            image_file = cv.imreadmulti(im)
            image_sb = image_file[1][0]
            im_name = os.path.split(im)[1][:-4]
            pixel_size = np.around(img_info.physical_pixel_sizes.Y, 3)
            sb_font = 10#np.round(image_sb.shape[0]*0.0025)
            sb_length = np.uint(np.round((image_sb.shape[0]*pixel_size)*0.10))
        

        except:
            #Otherise assume mrc file
            image_sb = mrcfile.read(im)
            img_info = mrcfile.open(im)
            im_name = os.path.split(im)[1][:-4]
            pixel_size = np.around(img_info.voxel_size.y, 3)/10000 #MRC files read in 10^4 micron 
            sb_font = 10#np.round(image_sb.shape[0]*0.0025)
            sb_length = np.uint(np.round((image_sb.shape[0]*pixel_size)*0.10))
        if sb_length ==0:
            pixel_size = np.around(img_info.voxel_size.y, 3)/10
            sb_length = np.uint(np.around((image_sb.shape[0]*pixel_size)*0.10,-2))
            sb_unit = 'nm'
        # 2b Contrast, value doesn't seem to be used in original code
        if auto_bright_contrast:
            image_sb = equalize_adapthist(image_sb)  # amount contrast here?
        if convert_8bit:
            image_sb = np.uint8(image_sb*255)
        if add_sb:
            # Figure out how this translates to multicolor,ztack, or timelapse
            
            fig = plt.figure()
            microim = microshow(
                images=[image_sb], unit=sb_unit, scalebar_size_in_units=sb_length,
                scalebar_unit_per_pix=pixel_size, scalebar_font_size=sb_font,
                scalebar_color=sb_color)
            # Save new image
            if rMeth[0] == '2':
                subFolder = 'ImagesWithScaleBar'
                rDir = os.path.join(os.path.split(im)[0],subFolder)
                if os.path.exists(rDir):
                    print('Folder exists')
                else:
                    print('Created new folder')
                    os.mkdir(rDir)
            elif rMeth[0] == '3':
                rDir = os.path.split(im)[0]

            plt.savefig(os.path.join(rDir, im_name+outFile),
                            bbox_inches='tight', pad_inches=0, dpi=600)
            plt.close()
            print(im_name+' finished')
    #f_stat.insert(0,'Finished') 

@Gooey(program_name='Add Scale Bar',
        terminal_panel_color=bg_color,
        terminal_font_color=fg_color,
        body_bg_color=bg_color,
        header_bg_color=wbg_color,
        footer_bg_color=bg_color,
        sidebar_bg_color=bg_color)
def main():
    settings_msg = 'Progam adds scale bar to all images within folder'
    parser = GooeyParser(description=settings_msg)

    group1 = parser.add_argument_group('Input Parameters')
    group1.add_argument('Input_location', help="location of images to process", widget='DirChooser')
    group1.add_argument('Input_file_extenstion', action='store',default='.tif')
    group1.add_argument('Output_method', help="select how processed images are saved", widget='Dropdown'
                        ,default = "1.[Default] Save in Subfolder in Parent Folder"
                        ,choices=["1.[Default] Save in Subfolder in Parent Folder","2. Save in Subfolder","3. Save in Same Folder"])
    group1.add_argument('Output_file_extenstion', action='store',default='.scalebar.tif')

    # group2 = parser.add_argument_group('Function Options')
    group1.add_argument('--Convert_to_8_bit', default =True, action='store_true')
    group1.add_argument('--Auto_Contrast_Enhance', default =True, action='store_true')
    group1.add_argument('--Add_Scale_Bar', default =True, action='store_true')
    group1.add_argument('Font_color', widget='Dropdown',default='black'
                        ,choices=['black','white','yellow','red'])
    args=parser.parse_args()
    print(args)
    addScale(args.Output_method,args.Input_location,args.Input_file_extenstion,
             args.Output_file_extenstion,args.Convert_to_8_bit,
             args.Auto_Contrast_Enhance,args.Add_Scale_Bar,args.Font_color)
   #display_message()
    
#fun(arg)
if __name__ == '__main__':
    main()
    
   