#Made by gabriel asher (github gaasher)

import pandas as pd
import os
import shutil
import json
import argparse
from copy import deepcopy

IPFS_URL = 'ipfs://QmdfDmrWZb5UM7obpnsJeDDuHoAzoR7n5SCZk6fAKX5hfD' #CID to folder with keggy images
BASE_NAME = "Keggy #" #keggy image names

BASE_JSON = { #base metadata format as directed by opensea
    "name": BASE_NAME,
    "description": '',
    "image": IPFS_URL,
    "attributes": [],
}

#Function which takes paths to image folder, metadata folder, and json_folder and 
#ensures that they are all properly formatted and contain the correct files. Also creates json_folder
def validate_paths(images_path: str, metadata_path: str, json_path: str):
    #Check and create json folder
    if json_path is not None and os.path.exists(json_path):
        try:
            shutil.rmtree(json_path)
            print('Directory %s succesfully removed', json_path)

        except OSError as error:
            print(error)
            print('Directory %s cannot be removed', json_path)
            return False
    os.mkdir(json_path)
    print("JSON Directory created....")

    #Check images folder
    if images_path is not None:
        for file in os.listdir(images_path):
            if not str(file).endswith(".png"):
                print(str(file))
                print("Invalid file detected in directory: %s", images_path)
                return False
    else:
        print("Invalid images path directory %s", images_path)
        return False
    
    #Check metadata folder
    if metadata_path is not None:
        if not os.path.exists(metadata_path + "metadata.csv"): #ensure etadata csv exists
            print("No metadata file in directory %s", metadata_path)
            return False
    else:
        print("Invalid metadata folder %s", metadata_path)
        return False

    return True

#Takes path to metadata, retrieves and formats dataframe, and returns dataframe
def retrieve_attr_df(metadata_path: str):
    df = pd.read_csv(metadata_path + "metadata.csv")
    row_names = df['Unnamed: 0'].to_list()
    df.index = row_names
    df = df.drop('Unnamed: 0', axis= 1)

    return df

def main():
    #Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--images_path", type=str) #images folder
    parser.add_argument("--metadata_path", type=str) #metadata folder
    parser.add_argument("--json_path", type=str) #json folder
    args = parser.parse_args()

    images_path = args.images_path
    metadata_path = args.metadata_path
    json_path = args.json_path

    #Ensure valid paths
    if not validate_paths(images_path, metadata_path, json_path):
        return None
    
    #retrieve pandas df
    df = retrieve_attr_df(metadata_path)

    #loop over cols in dataframe
    for idx, col in df.iteritems():
        itemname = str(idx)
        #populate json
        item_json = deepcopy(BASE_JSON) #create copy of base json struct
        
        item_json['name'] = item_json['name'] + itemname #json name

        item_json['image'] = item_json['image'] + "/" + itemname + ".png"

        at_dict = dict(col)

        if at_dict["Description"] == "None":
            item_json['description'] = "A normal Keggy performing his daily duties"
        else:
            item_json['description'] = at_dict["Description"]

        #populate attribute list in json
        for attr in at_dict:
            if attr != "ItemName" and attr != "Description":
                item_json['attributes'].append({'trait_type': attr, 'value': at_dict[attr]})

        #dump json into json folder
        item_json_path = os.path.join(json_path, itemname+".json")
        with open(item_json_path, "w") as f:
            json.dump(item_json, f, indent= 4)

if __name__ == "__main__":
    main()
    #sample code for running (off of images created in `keggy_collection_and_csv.py``):
    #python .\keggy_metadata.py --images_path "test1/single_images/" --metadata_path "test1/metadata/" --json_path "test1/jsons/" "