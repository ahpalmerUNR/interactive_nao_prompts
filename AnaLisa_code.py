#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: ahpalmerUNR
# @Date:   2018-07-25 13:43:18
# @Last Modified by:   ahpalmerUNR
# @Last Modified time: 2018-07-25 16:49:01

import Tkinter as Tk 
from PIL import Image, ImageTk
import os
import time
import datetime
from threading import Timer
import csv
from naoqi import ALProxy

next_step = False 
positive = 1
negative = 3
neutral = 2

conditionSayings = [
		# condition 1 - POSITIVE
		[
			("You are really good at this"),
			("You are doing really well"),
			("You are really mastering this"),
		   #("You are amazing"),
			("You did really well"),
		   #("You are inspired today"),
			#"You are on fire"),
		   #("You are the best")
		],
		# condition 2 neutral is empty
		[
			("You can continue to the next image"),
			("You are halfway through"),
			("You can move on now"),
			("You are done now"),
			#(""),
			#(""),
			#(""),
			#("")
		],
		# condition 3 - NEGATIVE
		[
			("You are really bad at this"),
			("You are doing terrible"),
			("You just dont get this"),
			("You did really badly"),
			#("You need some practice"),
			#("You are not so good at this"),
			#("Boy, you just don't get it"),
			#("This is not great performance")
		]
	]

def robotWelcome():
	# Welcome script
	# motion.goToPosture("Stand", 1.0)

	# animatedTts.setBodyLanguageMode(2)
	# time.sleep(1)
	# animatedTts.say("^start(animations/Stand/Hello) Hello! ")
	# animatedTts.say("^start(animations/Stand/Gestures/Enthusiastic_3)Nice to meet you!")
	# animatedTts.say("My^wait(animations/Stand/Gestures/Me_1)name is Taylor")

	# tts.say("Thank you for spending a bit of time with me")
	# animatedTts.say("Let me walk ^start(animations/Stand/Gestures/You_1)you through the task")
	# tts.say("There will be a total of eight images")
	# tts.say("You will have thirty seconds to count the number of things wrong in each image")
	# animatedTts.say("Please^start(animations/Stand/Gestures/Please_1) answer as quickly and acurately as possible")
	# animatedTts.say("you will need to enter ^start(animations/Stand/Gestures/Enthusiastic_4)a nonzero numerical value")
	# time.sleep(3)
	# tts.say("After you finish each task, I will check your answers")
	# tts.say("Now let's get started.")
	# time.sleep(1)
	pass

def loadImage(tk_root,label,image_name):
	display_image = ImageTk.PhotoImage(Image.open(image_name))
	label.configure(image=display_image)
	label.image = display_image
	
	tk_root.update_idletasks()
	tk_root.update()

def move_Forward():
	global next_step
	next_step = True

def getAnswer(tk_root,label):
	global  next_step
	next_step = False
	value = 0
	label.configure(text = "How many mistakes were in the image?", image = "")
	label.pack()
	answer = Tk.Entry(tk_root)
	answer.pack()
	next_b = Tk.Button(tk_root, text = "Enter", command = move_Forward)
	next_b.pack()
	# print(next_b)
	while not next_step:
		
		tk_root.update_idletasks()
		tk_root.update()
	# print(answer)	
	# answer.grid_remove()
	# next_b.grid_remove()
	value = answer.get()
	answer.destroy()
	next_b.destroy()
	return value


if __name__ == "__main__":
	totalSubtasks = 8
	subtaskTime = 2     # seconds to perform task
	waitTime = 5     # MINIMUM wait period time between subtasks

	itteration = 0

	image_files = []
	for x in os.listdir(os.getcwd()+"/images"):
		image_files.append(os.getcwd()+"/images/"+ str(x))


	#Connection Info to NAO
	ip = "localhost" 
	port = 9559

	pos_neg_neut_order = [positive,positive,neutral,negative,negative,positive,positive,neutral]

	#initiate robot communication
	tts = ALProxy("ALTextToSpeech", "192.168.1.138", 9559)
	motion = ALProxy("ALRobotPosture", "192.168.1.138", 9559)
	animatedTts = ALProxy("ALAnimatedSpeech", "192.168.1.138", 9559)


	#setting up window
	root = Tk.Tk()
	root.title("HRI Study")
	root.geometry("620x375+650+352")
	root.configure(background="gray")
	main_label = Tk.Label(root)
	main_label.pack(side = "top",fill = 'both', expand = 'yes')
	main_label.configure(text = "Thank you for participating. \n Test will begin shortly.")
	# main_label.text = "Thank you for participating. \n Test will begin shortly."
	root.update_idletasks()
	root.update()
	time.sleep(5)
	#Perform Robot Welcome
	robotWelcome()
	time_start = time.time()
	for x in  image_files:
		itteration += 1
		print(x)
		loadImage(root,main_label,x)		

		time.sleep(1)

		answer = getAnswer(root,main_label)
		print(answer,itteration)

		#putting saying stuff here

	time.sleep(1)

	

	# START INTERACTION

	

	# app = HRISubtask(root, outputFile, scriptReader, task, subtaskTime)
	




	# #closing script
	# tts.say("I will rip out your intestines. Flesh is yummy. Give me your bones.")
	# time.sleep(7)
	# tts.say("Where are the bones you owe me?")
	# time.sleep(10)
	# tts.say("I am waiting for flesh. Provide your flesh.")
	# tts.say("Thank you for your time.")
	# time.sleep(.5)
	# tts.say("The experiment is now complete.")
	# time.sleep(1)
	# animatedTts.say("Please^start(animations/Sit/Gestures/Please_1) call the experimenter back to the room.")
	# tts.say("Good bye")
	time.sleep(5)