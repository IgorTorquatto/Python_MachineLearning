import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf

x = tf.constant(4, shape=(1,1), dtype=tf.float32)
print(x)

#rank 2
y = tf.constant([[1,2,3],[4,5,6]])
print(y)