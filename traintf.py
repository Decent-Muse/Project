import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd

data_file = "new.xls"
epochs = 100
#reading data

dfile = xlrd.open_workbook(data_file, encoding_override="utf-8")
sheet = dfile.sheet_by_index(0)
data = np.asarray([sheet.row_values(i)for i in range(1, sheet.nrows)])
n_samples = sheet.nrows - 1

#creating placeholders

BARCODE =tf.placeholder(tf.float32,name="BARCODE")
CREATED_STAMP =tf.placeholder(tf.float32,name="CREATED_STAMP")

#creating weight and bias, initialized to 0

w =tf.Variable(0.0,name="BARCODE")
b =tf.Variable(0.0,name="CREATED_STAMP")

Y_pred = BARCODE * w + b

loss = tf.square(CREATED_STAMP-Y_pred, name="loss")

opt = tf.train.GradientDescentOptimizer(learning_rate = 0.001).minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in range(epochs):
        for x, y in data:
            sess.run(opt, feed_dict={BARCODE: x, CREATED_STAMP: y})

    w_value, b_value = sess.run([w, b])
