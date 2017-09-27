import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd

data_file = "loc_vs_bar_main.xls"
epochs = 100
#reading data

dfile = xlrd.open_workbook(data_file, encoding_override="utf-8")
sheet = dfile.sheet_by_index(0)
data = np.asarray([sheet.row_values(i)for i in range(1, sheet.nrows)])
n_samples = sheet.nrows - 1

#creating placeholders

LOCATION =tf.placeholder(tf.float32,name="X")
BARCODE =tf.placeholder(tf.float32,name="Y")

#creating weight and bias, initialized to 0

w =tf.Variable(0.0,name="LOCATION")
b =tf.Variable(0.0,name="BARCODE")

Y_pred = LOCATION * w + b

loss = tf.square(BARCODE-Y_pred, name="loss")

opt = tf.train.GradientDescentOptimizer(learning_rate = 0.001).minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(epochs):
        for x, y in data:
            sess.run(opt, feed_dict={LOCATION: x, BARCODE: y})

    w_value, b_value = sess.run([w, b])
