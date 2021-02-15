import numpy as np
import matplotlib.pyplot as plt
import sys

import pyzed.sl as sl
import pyrealsense2 as rs

import PIL as Image
from PIL import Image as im

from args import *
import Jetson.GPIO as GPIO

#import cv2
buttonOneOldState = True
buttonTwoOldState = True
buttonOneNewState = True
buttonTwoNewState = True

buttonOnePressed = False
buttonTwoPressed = False

buttonOneReleased = False
buttonTwoReleased = False


def detectButtonsState():
	"""
	Function to detect the change of buttons satate
	And detect When each button is pressed or released
	"""
	# Defineing global buttons' variables 
	global buttonOneOldState, buttonTwoOldState, buttonOneNewState, buttonTwoNewState
	global buttonOnePressed, buttonOneReleased, buttonTwoReleased, buttonTwoPressed
	
	buttonOneOldState = buttonOneNewState
	buttonTwoOldState = buttonTwoNewState

	buttonOneNewState = GPIO.input(inputPin1)
	buttonTwoNewState = GPIO.input(inputPin2)
	
	if buttonOneNewState==1 and buttonOneOldState==0:
		buttonOneReleased = True
	elif buttonOneNewState==0 and buttonOneOldState==1:
		buttonOnePressed = True

	if buttonTwoNewState==1 and buttonTwoOldState==0:
		buttonTwoReleased = True
	elif buttonTwoNewState==0 and buttonTwoOldState==1:
		buttonTwoPressed = True

def collectRealsense(pipeline, image_index):
	"""
	Function to Collect and save images using realsense camera
	"""
	i = image_index
	frames = pipeline.wait_for_frames()
	depth_frame = frames.get_depth_frame()
	color_frame = frames.get_color_frame()
	fisheye_frame = frames.get_fisheye_frame()
	infrared_frame = frames.get_infrared_frame() 

	while not depth_frame or not color_frame:
		frames = pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()
		#infrared_frame = frames.get_infrared_frame()

	rgb = np.asanyarray(color_frame.get_data())
	depth = np.asanyarray(depth_frame.get_data())
	#infrared = np.asanyarray(infrared_frame.get_data())


	str_rgb = "dataset/rs/image/{}.jpg".format(i)
	str_depth = "dataset/rs/depth/{}.jpg".format(i)

	data_rgb = im.fromarray(rgb)
	data_depth = im.fromarray(depth)
	data_depth.mode = 'I'

	data_rgb.save(str_rgb)
	#data_rgb.show()
	data_depth.point(lambda i:i*(1./256)).convert('L').save(str_depth)
	print("Saved RS images!")


def collectZed(zed, runtime_parameters, image_index):
	"""
	Function to Collect and save images using Zed camera
	"""
	i = image_index
	image_z_l = sl.Mat()
	image_z_r = sl.Mat()
	depth_z = sl.Mat()

	if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
		# A new image is available if grab() returns SUCCESS
		zed.retrieve_image(image_z_l, sl.VIEW.LEFT)
		zed.retrieve_image(image_z_r, sl.VIEW.RIGHT)
		zed.retrieve_measure(depth_z, sl.MEASURE.DEPTH)
		img_z_l = image_z_l.get_data()
		img_z_r = image_z_r.get_data()
		dpth_z = depth_z.get_data()
		str_rgb_l = "dataset/z/image_l/{}.jpg".format(i)
		str_rgb_r = "dataset/z/image_r/{}.jpg".format(i)
		str_depth = "dataset/z/depth/{}.jpg".format(i)

		data_img_z_l = im.fromarray(img_z_l)
		data_img_z_l = data_img_z_l.convert('RGB')
		data_img_z_r = im.fromarray(img_z_r)
		data_img_z_r = data_img_z_r.convert('RGB')
		data_depth_z = im.fromarray(dpth_z)
		data_depth_z.mode = 'I'

		data_img_z_l.save(str_rgb_l)
		data_img_z_r.save(str_rgb_r)
		data_depth_z.point(lambda i:i*(1./256)).convert('L').save(str_depth)

		print("Saved Zed images!")

def main():
	# Defineing global buttons' variables 
	global buttonOnePressed, buttonOneReleased, buttonTwoReleased, buttonTwoPressed
	
	# Init the Realsense camera
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
	#pipeline.start(config)

	# Init Zed camera
	zed = sl.Camera()

	# Init the GPIO buttons
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(inputPin1, GPIO.IN)
	GPIO.setup(inputPin2, GPIO.IN)

	# Create a InitParameters object and set configuration parameters
	init_params = sl.InitParameters()
	init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
	init_params.camera_fps = 30  # Set fps at 30

	"""
	# Open the camera
	err = zed.open(init_params)
	if err != sl.ERROR_CODE.SUCCESS:
		print("No Zed Camera Connected")
		exit(1)
	"""

	image_z_l = sl.Mat()
	image_z_r = sl.Mat()
	depth_z = sl.Mat()
	runtime_parameters = sl.RuntimeParameters()

	i = 0

	try:
		while True:
			detectButtonsState()

			# ___________________________________________________________
			# What happens when press Button 1
			if buttonOnePressed:
				buttonOnePressed = False
				print("Btn 1 pressed!")

				collectRealsense(pipeline, i)
				collectZed(zed, runtime_parameters, i)
			# ___________________________________________________________
			# What happens when press Button 2
			if buttonTwoPressed:
				buttonTwoPressed = False
				print("Btn 2 pressed!")

			# ___________________________________________________________
			# What happens when release Button 1
			if buttonOneReleased:
				buttonOneReleased = False
				print("Btn 1 released!")

			# ___________________________________________________________
			# What happens when release Button 2
			if buttonTwoReleased:
				buttonTwoReleased = False
				print("Btn 2 released!")

			# ___________________________________________________________


			# Editing the log to change the image numbering
			f = open("img_num.log", "r+")
			i = int(f.read())
			f.close()

			f = open("img_num.log", "w")
			f.write(str(i+1))
			f.close()
			
			
			"""
			frames = pipeline.wait_for_frames()
			depth_frame = frames.get_depth_frame()
			color_frame = frames.get_color_frame()
			fisheye_frame = frames.get_fisheye_frame()
			infrared_frame = frames.get_infrared_frame() 

			while not depth_frame or not color_frame:
				frames = pipeline.wait_for_frames()
				depth_frame = frames.get_depth_frame()
				color_frame = frames.get_color_frame()
				#infrared_frame = frames.get_infrared_frame()

			rgb = np.asanyarray(color_frame.get_data())
			depth = np.asanyarray(depth_frame.get_data())
			#infrared = np.asanyarray(infrared_frame.get_data())


			str_rgb = "dataset/rs/image/{}.jpg".format(i)
			str_depth = "dataset/rs/depth/{}.jpg".format(i)

			data_rgb = im.fromarray(rgb)
			data_depth = im.fromarray(depth)
			data_depth.mode = 'I'

			data_rgb.save(str_rgb)
			#data_rgb.show()
			data_depth.point(lambda i:i*(1./256)).convert('L').save(str_depth)
			#str_infrared = "dataset/rs/infrared/{}.jpg".format(i)



			if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
				# A new image is available if grab() returns SUCCESS
				zed.retrieve_image(image_z_l, sl.VIEW.LEFT)
				zed.retrieve_image(image_z_r, sl.VIEW.RIGHT)
				zed.retrieve_measure(depth_z, sl.MEASURE.DEPTH)
				img_z_l = image_z_l.get_data()
				img_z_r = image_z_r.get_data()
				dpth_z = depth_z.get_data()
				str_rgb_l = "dataset/z/image_l/{}.jpg".format(i)
				str_rgb_r = "dataset/z/image_r/{}.jpg".format(i)
				str_depth = "dataset/z/depth/{}.jpg".format(i)

				data_img_z_l = im.fromarray(img_z_l)
				data_img_z_l = data_img_z_l.convert('RGB')
				data_img_z_r = im.fromarray(img_z_r)
				data_img_z_r = data_img_z_r.convert('RGB')
				data_depth_z = im.fromarray(dpth_z)
				data_depth_z.mode = 'I'

				data_img_z_l.save(str_rgb_l)
				data_img_z_r.save(str_rgb_r)
				data_depth_z.point(lambda i:i*(1./256)).convert('L').save(str_depth)
			"""

	finally:
		#pipeline.stop()
		pass


if __name__ == "__main__":
	main()

