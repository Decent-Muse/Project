import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt

#parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50

#training data

busy = open('BUSY7246fb6.csv','r');
for line in busy:
	cols = line.split('|')
	if len(cols) >= 2:
		print(cols[4])
		
p = os.system("python3 main.py > file.csv");
