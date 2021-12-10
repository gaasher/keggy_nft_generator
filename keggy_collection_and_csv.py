#Made by Gabriel Asher (github gaasher)

import os
import shutil
from random import random
import pandas as pd
import argparse

from gen_d_nft import generate_single_image


#generate collection of n keggy images and save them to specified folder. Additionally
#keep their attribute data in a unified csv file 
def generate_collection_images(outpath: str, num_images: int, collection_name: str):
    attribute_table = {} #contains each image and image attributes
    
    #ensure correct path to dir
    if outpath is not None:
        if os.path.exists(outpath):
            try:
                shutil.rmtree(outpath)
                print('Directory %s succesfully removed', outpath)

            except OSError as error:
                print(error)
                print('Directory %s cannot be removed', outpath)
                return None

        os.mkdir(outpath)
        images_outpath = outpath + "single_images/"
        os.mkdir(images_outpath)
    
        #generate num_images images
        for i in range(1, num_images + 1):    
            img, temp_at = generate_single_image()
            itemname = str(i) #zero pad
            itemid = itemname +".png"
            img.save(images_outpath + itemid)

            temp_at['ItemName'] = itemname

            for trait in temp_at: #populate dict mapping itemname -> attributes which each -> trait value
                if itemname not in attribute_table:
                    attribute_table[itemname] = {}
                attribute_table[itemname][trait] = temp_at[trait]
        
        attribute_table = pd.DataFrame(attribute_table) #turn attribute table dict to pandas dataframe
        print("Generated %d images, image metadata moved to dataframe", num_images)

    return attribute_table


def main():
    #take args from console
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", type=str)
    parser.add_argument("--collection_path", type=str)
    parser.add_argument("-n", type=int)
    args = parser.parse_args()

    collection = args.collection
    outpath = args.collection_path
    num_images = args.n

    #create attribute table 
    at = generate_collection_images(outpath, num_images, collection)
    print("Saving metadata to csv file:")
    
    #save attribute table in new metadata folder
    if outpath is not None:
        metadatapath = outpath + "metadata/"
        if os.path.exists(metadatapath):
            for sub in os.listdir(metadatapath): #remove metadata and any other files previously existing
                os.remove(str(sub))
            try:
                os.rmdir(metadatapath)
                print('Directory %s succesfully removed', metadatapath)

            except OSError as error:
                print(error)
                print('Directory %s cannot be removed', metadatapath)
                return None
        os.mkdir(metadatapath)
    
    print("Saving metadata to csv.....")
    at.to_csv(metadatapath + "metadata.csv") #save df as csv

    print("Metadata saved")



if __name__ == "__main__":
    main()

    #sample terminal input: 'python .\keggy_collection_and_csv.py --collection "test_images" --collection_path "test1/" -n 100'
