import os
import pathlib
import tensorflow as tf

def download_images():
	image_paths = []
	image_path = "C:\Users\Jack\Desktop\Tensorflow\workspace\training_demo\images\test"
	image_path = pathlib.Path(image_path)
	image_paths.append(str(image_path))
	