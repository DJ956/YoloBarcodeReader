import os
import glob
import h5py
import random
import matplotlib.pyplot as plt

from PIL import Image
import scipy.misc
import scipy.ndimage
import numpy as np

import tensorflow.compat.v1 as tf

FLAGS = tf.app.flags.FLAGS

"""
Read h5 format data file
"""
def read_data(path):
	with h5py.File(path, "r") as hf:
		data = np.array(hf.get("data"))
		label = np.array(hf.get("label"))
		return data, label

"""
preprocess single image file
	(1)Read original image as YCbCr format(and grayscale as default)
	(2)Normalize
	(3)Apply image file with bicubic interpolation (bicubic:https://imagingsolution.blog.fc2.com/blog-entry-142.html)
"""
def preprocess(path, scale=3):
	image = imread(path, is_grayscale=True)
	label_ = modcrop(image, scale)

	#Normalize
	image = image / 255.
	label_ = label_ / 255.

	#縮小 1/3
	input_ = scipy.ndimage.interpolation.zoom(label_, (1./scale), prefilter=False)	
	#拡大
	input_ = scale.ndimage.interpolation.zoom(input_, (scale/1.), prefilter=False)	

	return input_, label_

"""
dataset: choose train dataset or test dataset
For train dataset, output data would be ['.../t1.bmp', '.../t2.bmp', ..., '.../t99.bmp']
"""
def prepare_data(sess, dataset):
	if FLAGS.is_train:
		filenames = os.listdir(dataset)
		data_dir = os.path.join(os.getcwd(), dataset)
		data = glob.glob(os.path.join(data_dir, "*.bmp"))
	else:
		data_dir = os.path.join(os.sep, (os.path.join(os.getcwd(), dataset)), "Set5")
		data = glob.glob(os.path.join(data_dir, "*.bmp"))

	return data

"""
Make input data as h5 file format
Depending on 'is_train' (flag value), savepath would be changed.
"""
def make_data(sess, data, label):
	if FLAGS.is_train:
		savepath = os.path.join(os.getcwd(), "checkpoint/train.h5")
	else:
		savepath = os.path.join(os.getcwd(), "checkpoint/test.h5")

	with h5py.File(savepath, "w") as hf:
		hf.create_dataset("data", data=data)
		hf.create_dataset("label", data=label)

"""
Read image using its path
Default value is gray_scale, and image is read YCbCr format as the paper said
"""
def imread(path, is_grayscale=True):
	if is_grayscale:
		return scipy.misc.imread(path, flatten=True, mode="YCbCr").astype(np.float)
	else:
		return scipy.misc.imread(path, mode="YCbCr").astype(np.float)

"""
To scale down and up the original image, first thing to do is to have remainder while scaling operation

We need to find modulo of height (and width) and scale factor.
Then, subtract the modulo from height (and width) of original image size
There would be no remainder even after scaling operation.
"""
def modcrop(image, scale=3):
	if len(image.shape) == 3:
		h, w, _ = image.shape
		h = h - np.mod(h, scale)
		w = w - np.mod(w, scale)
		image = image[0: h, 0: w, :]
	else:
		h, w = image.shape
		h = h - np.mod(h, scale)
		w = w - np.mod(w, scale)
		image = image[0:h, 0:w]
	return image

"""
Read image files and make their sub-images and saved them as a h5 file format
"""
def input_setup(sess, config):
	if config.is_train:
		data = prepare_data(sess, dataset="Train")
	else:
		data = prepare_data(sess, dataset="Test")
	#data は　*.bmpのファイルリスト

	sub_input_sequence = []
	sub_label_sequence = []
	padding = abs(config.image_size - config.label_size) / 2 # 6

	if config.is_train:
		for i in range(len(data)):
			#input_:正規化され、縮小拡大された画像データ label_:元の画像からmod減算された配列(*おそらく)
			input_, label_ = preprocess(data[i], config.scale)

			if len(input_.shape) == 3:
				h, w, _ = input_.shape
			else:
				h, w = input_.shape

			for x in range(0, h - config.image_size+1, config.stride):
				for y in range(0, w - config.image_size+1, config.stride):
					sub_input = input_[x:x+config.image_size, y:y+config.image_size] #[33 * 33]
					sub_label = label_[x+int(padding):x+int(padding)+config.label_size, y+int(padding):y+int(padding)+config.label_size] #[21 * 21]

					#Make channel value
					sub_input = sub_input.reshape([config.image_size, config.image_size, config.c_dim])
					sub_label = sub_label.reshape([config.label_size, config.label_size, config.c_dim])

					sub_input_sequence.append(sub_input)
					sub_label_sequence.append(sub_label)

	else:
		input_, label_ = preprocess(data[2], config.scale)

		if len(input_.shape) == 3:
			h, w, _ = input_.shape
		else:
			h, w = input_.shape

		# Numbers of sub-images in height and width of image are needed to compute merge operation.
		nx = ny = 0
		for x in range(0, h - config.image_size + 1, config.stride):
			nx += 1; ny = 0
			for y in range(0, w - config.image_size + 1, config.stride):
				ny += 1
				sub_input = input_[x:x+config.image_size, y:y+config.image_size] #[33 * 33]
				sub_label = label_[x+int(padding):x+int(padding)+config.label_size, y+int(padding):y+int(padding)+config.label_size] # [21 * 21]

				sub_input = sub_input.reshape([config.image_size, config.image_size, 1])
				sub_label = sub_input.reshape([config.image_size, config.image_size, 1])

				sub_input_sequence.append(sub_input)
				sub_label_sequence.append(sub_label)

	"""
	len(sub_input_sequence) : the number of sub_input (33 x 33 x ch) in one image
	(sub_input_sequence[0]).shape : (33, 33, 1)
	"""
	
	#Make list to numpy array. With this transform
	arrdata = np.asarray(sub_input_sequence) # [?, 33, 33, 1]
	arrlabel = np.asarray(sub_label_sequence) # [?, 21, 21, 1]

	#h5フォーマットの形式でデータ保存
	make_data(sess, arrdata, arrlabel)	

	if not config.is_train:
		return nx, ny

def imsave(image, path):
	return scipy.misc.imsave(path, image)

def merge(images, size):
	h, w = images.shape[1], images.shape[2]
	img = np.zeros((h*size[0], w*size[1]), 1)
	for idx, image in enumerate(images):
		i = idx % size[1]
		j = idx // size[1]
		img[j*h:j*h+h, i*w:i*w+w, :] = image

	return img
