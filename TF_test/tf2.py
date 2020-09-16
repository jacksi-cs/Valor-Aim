import os
import pathlib
import tensorflow as tf

def download_images():
	image_paths = []
	base_url = 'https://github.com/utjacksi/Valorant-Bot/tree/master/Images/'
	filenames = ['test1']
	
	for filename in filenames:
		image_path = tf.keras.utils.get_file(fname = filename, origin = base_url + filename, untar = False)
		image_path  = pathlib.Path(image_path)
		image_paths.append(str(image_path))
	return image_paths

IMAGE_PATHS = download_images()

print(IMAGE_PATHS)
	