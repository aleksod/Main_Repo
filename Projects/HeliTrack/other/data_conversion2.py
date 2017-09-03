training_folder = "/Users/aleksod/Documents/Metis/Main_Repo/Projects/HeliTrack/other/raw_data/train"
testing_folder = "/Users/aleksod/Documents/Metis/Main_Repo/Projects/HeliTrack/other/raw_data/test"
holdout_folder = "/Users/aleksod/Documents/Metis/Main_Repo/Projects/HeliTrack/other/raw_data/holdout"

writer_path = '../data/train.record' #'../data/train.record' #'../data/train.record'

filepath = training_folder

'''Append the path to TensorFlow object detection scripts'''
import sys, os

# Create a hi module in your home directory.
home_dir = os.path.expanduser("/Users/aleksod/Documents/Metis/models")

# # Add the home directory to sys.path
sys.path.append(home_dir)

import numpy as np
import cv2
import imutils

import pandas as pd
from scipy import ndimage
import gc

'''Create label number for each of the ten classes'''
classes_labels = {
    "Car":              1,
    "Truck":            2,
    "Tractor-Trailer":  3,
    "Bus":              4,
    "Container":        5,
    "Boat":             6,
    "Plane":            7,
    "Helicopter":       8,
    "Person":           9,
    "Cyclist":          10,
    "DCR":              11
}

import tensorflow as tf

from object_detection.utils import dataset_util

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
# FLAGS = flags.FLAGS


def create_tf_example(example, filename, image_format, xmins, ymins, xmaxs, ymaxs, classes_text, classes, width, height):
    # TODO(user): Populate the following variables from your example.
    # height = None # Image height
    # width = None # Image width
    # filename = None # Filename of the image. Empty if image is not from file
    encoded_image_data = example #None # Encoded image bytes
    # image_format = None # b'jpeg' or b'png'
    #
    # xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    # xmaxs = [] # List of normalized right x coordinates in bounding box
    #          # (1 per box)
    # ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    # ymaxs = [] # List of normalized bottom y coordinates in bounding box
    #          # (1 per box)
    # classes_text = [] # List of string class name of bounding box (1 per box)
    # classes = [] # List of integer class id of bounding box (1 per box)

    # print(dataset_util.bytes_feature(b'test'))
    tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(bytes(filename,'utf8')),
      'image/source_id': dataset_util.bytes_feature(bytes(filename,'utf8')),
      'image/encoded': dataset_util.bytes_feature((encoded_image_data)), #.tobytes()),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature([bytes(i,'utf8') for i in classes_text]),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(writer_path)

    # TODO(user): Write code to read in your dataset to examples variable
    extensions = [".mpg"] #e.g. only iterate through videos

    # print(filepath)
    # print("Does this file exist?", os.path.isfile(filepath))
    # print(os.walk(filepath))

    for subdir, dirs, files in os.walk(filepath):
        for filename in files:
            ext = os.path.splitext(filename)[-1].lower()
            if ext in extensions:

                video_name = os.path.join(subdir, filename)
                print("Now working on {}".format(video_name))
                print("Does this file exist?", os.path.isfile(video_name))

                '''Extracting frames from a video'''

                vidcap = cv2.VideoCapture(video_name)
                success,image = vidcap.read()
                count = 0
                success = True
                while success:
                    if count == 0:
                        width = max(image.shape)
                        height = min(image.shape)
                    success,image = vidcap.read()
                    print('Read a new frame: ', success, '\t filepath:', "temp/frame%d.jpg" % count)
                    cv2.imwrite("temp/frame%d.jpg" % count, image)     # save frame as JPEG file
                    count += 1

                # cap = cv2.VideoCapture(video_name)
                # print(cap)
                # count = 0
                # while True:
                #     success,image = cap.read()
                #     if success == True:
                #         if count == 0:
                #             width = image.shape[1]
                #             height = image.shape[0]
                #         success,image = cap.read()
                #         # print("Extracting frame #{}".format(count))
                #         cv2.imwrite("temp/frame%d.jpg" % count, image)     # save frame as JPEG file
                #         count += 1
                #         if cv2.waitKey(10) == 27:                     # exit if Escape is hit
                #             print("Finished the video file")
                #             break

                vidcap.release()

                df = pd.read_csv(video_name.replace(extensions[0], '.csv'))
                ind = df[df.ObjectType.isnull()].index
                df = df.query('index not in @ind')

                '''Walk down each frame mentioned in the CSV and mark rectangles with objects for model training'''

                for index,frame in enumerate(df.Frame.unique()): # Perform operation for each frame
                    print('frame:', frame)
                    df2 = df[df.Frame == frame]
                    filename = "temp/frame%d.jpg" % frame
                    image_format = b'jpg'

                    df3x = df2.iloc[:,[1,3,5,7]]
                    df3y = df2.iloc[:,[2,4,6,8]]

                    xmins_abs = list(df3x.apply(lambda x: min(x), axis=1))
                    ymins_abs = list(df3y.apply(lambda y: min(y), axis=1))
                    xmaxs_abs = list(df3x.apply(lambda x: max(x), axis=1))
                    ymaxs_abs = list(df3y.apply(lambda y: max(y), axis=1))

                    xmins = [x/width  for x in xmins_abs]
                    ymins = [y/height for y in ymins_abs]
                    xmaxs = [x/width  for x in xmaxs_abs]
                    ymaxs = [y/height for y in ymaxs_abs]

                    classes_text = list(df2.iloc[:,9])
                    print(classes_text)
                    classes  = [classes_labels[x] for x in classes_text]
                    classes_text

                    del df2, df3x, df3y
                    gc.collect()

                    with open(filename, "rb") as imageFile:
                        f = imageFile.read()
                        img = bytes(f)

                    tf_example = create_tf_example(img, filename, image_format, xmins, ymins, xmaxs, ymaxs, classes_text, classes, width, height)
                    writer.write(tf_example.SerializeToString())

                    # for example in examples:
                    #     tf_example = create_tf_example(example)
                    #     writer.write(tf_example.SerializeToString())

    writer.close()


if __name__ == '__main__':
    tf.app.run()
