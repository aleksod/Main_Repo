import xml.etree.cElementTree as ET
import pandas as pd
import os
import gc
import glob
import io
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

for directory in ["train", "test", "holdout"]:
    for subdir, dirs, files in os.walk('raw_data/{}/'.format(directory)):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext == ".csv":
                img_folder = os.path.join(subdir,file)[:-4]
                df = pd.read_csv(os.path.join(subdir,file))
                ind = df[df.ObjectType.isnull()].index
                df = df.query('index not in @ind')
                for frame in df.Frame.unique(): # Perform operation for each frame

                    image_filename = os.path.abspath(os.path.join(img_folder,'{:06}.png'.format(frame)))
                    im = Image.open(image_filename)
                    width, height = im.size

                    annotation1 = ET.Element("annotation")

                    folder = ET.SubElement(annotation1, "folder").text = "images"
                    filename = ET.SubElement(annotation1, "filename").text = '{:06}.png'.format(frame)
                    path = ET.SubElement(annotation1, "path").text = image_filename
                    source = ET.SubElement(annotation1, "source")

                    database = ET.SubElement(source, "database").text = "Unknown"

                    size = ET.SubElement(annotation1, "size")

                    width = ET.SubElement(size, "width").text = str(width)
                    height = ET.SubElement(size, "height").text = str(height)
                    depth = ET.SubElement(size, "depth").text = "3"

                    segmented = ET.SubElement(annotation1, "segmented").text = "0"

                    df2 = df[df.Frame == frame]
                    # For each object in the frame:
                    for obj in range(df2.shape[0]):

                        object1 = ET.SubElement(annotation1, "object")

                        name = ET.SubElement(object1, "name").text = str(df2.ObjectType.iloc[obj])
                        pose = ET.SubElement(object1, "pose").text = "Unspecified"
                        truncated = ET.SubElement(object1, "truncated").text = "Unspecified"
                        occluded = ET.SubElement(object1, "occluded").text = str(int(df2.Occlusion.iloc[obj]))
                        bndbox = ET.SubElement(object1, "bndbox")

                        xmin = ET.SubElement(bndbox, "xmin").text = str(min(df2.iloc[obj,[1,3,5,7]]))
                        ymin = ET.SubElement(bndbox, "ymin").text = str(min(df2.iloc[obj,[2,4,6,8]]))
                        xmax = ET.SubElement(bndbox, "xmax").text = str(max(df2.iloc[obj,[1,3,5,7]]))
                        ymax = ET.SubElement(bndbox, "ymax").text = str(max(df2.iloc[obj,[2,4,6,8]]))

                        difficult = ET.SubElement(object1, "difficult").text = str(int(df2.Ambiguous.iloc[obj]))

                    del df2
                    gc.collect()

                    tree = ET.ElementTree(annotation1)
                    tree.write(os.path.join(os.path.abspath(os.path.join(img_folder,'{:06}.xml'.format(frame)))))

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (os.path.join(path, root.find('filename').text),
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for directory in ['train', 'test', 'holdout']:
        dir_count = 0
        for subdirs, dirs, files in os.walk('raw_data/{}'.format(directory)):
            for d in dirs:
                image_path = os.path.join(os.getcwd(), 'raw_data/{}'.format(directory), d)
                if dir_count == 0:
                    xml_df = xml_to_csv(image_path)
                else:
                    xml_df = xml_df.append(xml_to_csv(image_path))
                dir_count +=1
        xml_df.to_csv('../data/{}_labels.csv'.format(directory), index=None)
        print('Successfully converted xml to csv in {} directory.'.format(directory))

main()
