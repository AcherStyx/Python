import matplotlib.pyplot as plt
import numpy as np
import math
import csv
import time
import random
import tensorflow as tf

# 从文件读取数据
with open('data.csv') as datafile:
    data = csv.reader(datafile)
    data = list(data)
# 字符串转浮点数
data = [[float(x) for x in row] for row in data]
# 拆分到xy变量中
x = []
y = []
for row in data:
    x.append(row[0])
    y.append(row[1])
x = np.array(x)
y = np.array(y)
print("[数据]", '\n', x, '\n', y)

# 设置值
print('[默认值]')
step = 0.01
n = len(x)
times = 1000
pick_n = 10  # 选取的数据的量
times_shuffle = 10  # 总计随机次数
again = 10  # 重复次数
print('下降次数:', times)
print('MBGD选取样本数:', pick_n)
print('MBGD随机次数:', times_shuffle)
print('重复次数:', again)

# 求偏导直接计算
print("[直接计算]")
starttime = time.time()
for iii in range(again):
    b = np.array([0.0, 0.0])
    b[1] = (n * sum(x * y) - sum(x) * sum(y)) / (n * sum(x * x) - sum(x) * sum(x))
    b[0] = sum(y) / n - b[1] * sum(x) / n
endtime = time.time()
print('运行时间: ', (endtime - starttime) * 1000 / again, 'ms a0: ', b[0], ' a1: ', b[1], sep='')
# 二乘法下的误差
current = 0
for i in range(0, len(x)):
    current += (y[i] - b[0] - b[1] * x[i]) ** 2
print('损失:', current)

# BGD
print("[BGD]")
starttime = time.time()
for iii in range(again):
    BGD_a = np.array([0.0, 0.0])
    for ii in range(times):
        change_0 = 0.0
        change_1 = 0.0
        for i in range(0, len(x)):
            change_0 += 2.0 * (BGD_a[1] * x[i] + BGD_a[0] - y[i])
            change_1 += 2.0 * x[i] * (BGD_a[1] * x[i] + BGD_a[0] - y[i])
        BGD_a[0] -= change_0 * step / n
        BGD_a[1] -= change_1 * step / n
endtime = time.time()
print('运行时间: ', (endtime - starttime) * 1000 / again, 'ms a0: ', BGD_a[0], ' a1: ', BGD_a[1], sep='')
# 二乘法下的误差
current = 0
for i in range(0, len(x)):
    current += (y[i] - BGD_a[0] - BGD_a[1] * x[i]) ** 2
print('损失:', current)

# SGD
print('[SGD]')
starttime = time.time()
for iii in range(again):
    SGD_a = np.array([0.0, 0.0])
    for i in range(times):
        i = random.randint(0, len(x) - 1)
        change_0 = 2.0 * (SGD_a[1] * x[i] + SGD_a[0] - y[i])
        change_1 = 2.0 * x[i] * (SGD_a[1] * x[i] + SGD_a[0] - y[i])
        SGD_a[0] -= change_0 * step
        SGD_a[1] -= change_1 * step
endtime = time.time()
print('运行时间: ', (endtime - starttime) * 1000 / again, 'ms a0: ', SGD_a[0], ' a1: ', SGD_a[1], sep='')
# 二乘法下的误差
current = 0
for i in range(0, len(x)):
    current += (y[i] - SGD_a[0] - SGD_a[1] * x[i]) ** 2
print('损失:', current)

# MBGD
print('[MBGD]')
starttime = time.time()
for iii in range(again):
    MBGD_a = np.array([0.0, 0.0])
    pick = list(range(len(x)))
    for ii in range(times):
        change_0 = 0
        change_1 = 0
        if ii % (times / times_shuffle) == 0:
            random.shuffle(pick)  # 随机调用的函数
        for i in pick[0:pick_n]:
            change_0 += 2.0 * (MBGD_a[1] * x[i] + MBGD_a[0] - y[i])
            change_1 += 2.0 * x[i] * (MBGD_a[1] * x[i] + MBGD_a[0] - y[i])
        MBGD_a[0] -= change_0 * step / pick_n
        MBGD_a[1] -= change_1 * step / pick_n
endtime = time.time()
print('运行时间: ', (endtime - starttime) * 1000 / again, 'ms a0: ', MBGD_a[0], ' a1: ', MBGD_a[1], sep='')
# 二乘法下的误差
current = 0
for i in range(0, len(x)):
    current += (y[i] - MBGD_a[0] - MBGD_a[1] * x[i]) ** 2
print('损失:', current)

# 使用Tensorflow
print('[Tensorflow]')
starttime = time.time()
batch_size = 5
w1 = tf.Variable(tf.zeros([1, 1], dtype=tf.float64), name='w1')
w2 = tf.Variable(tf.zeros([1, 1], dtype=tf.float64), name='w2')
tf_x = tf.placeholder(tf.float64, shape=(None, 1), name='x-input')
tf_y_ = tf.placeholder(tf.float64, shape=(None, 1), name='y-input')
tf_t = tf_x * w2
tf_y = tf_t + w1
loss = tf.reduce_mean(tf.square(tf_y_ - tf_y), name='loss')
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)
STEP = 5000
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for ii in range(STEP):
        # start=random.randint(0,len(x)-1)
        # end=random.randint(start,len(x)-1)
        # feed={tf_x:x[start:end].reshape([end-start,1]),tf_y_:y[start:end].reshape([end-start,1])}
        feed = {tf_x: x[:].reshape([len(x), 1]), tf_y_: y[:].reshape([len(x), 1])}
        sess.run(train_step, feed_dict=feed)
    TF_a = []
    TF_a.append(sess.run(w1, feed_dict=feed)[0][0])
    TF_a.append(sess.run(w2, feed_dict=feed)[0][0])
endtime = time.time()
print('运行时间: ', (endtime - starttime) * 1000 / again, 'ms a0: ', TF_a[0], ' a1: ', TF_a[1], sep='')
# 二乘法下的误差
current = 0
for i in range(0, len(x)):
    current += (y[i] - TF_a[0] - TF_a[1] * x[i]) ** 2
print('损失:', current)

# shuffle运行时间测试
print('[shuffle运行时间测试]')
starttime = time.time()
for ii in range(times):
    random.shuffle(pick)
endtime = time.time()
print('运行时间（', times, '次平均）: ', (endtime - starttime) * 1000 / times, sep='')

# 绘图
px = np.linspace(0, max(x), 100)
D_py = px * b[1] + b[0]
BGD_py = px * BGD_a[1] + BGD_a[0]
SGD_py = px * SGD_a[1] + SGD_a[0]
MBGD_py = px * MBGD_a[1] + MBGD_a[0]
TF_py = px * TF_a[1] + TF_a[0]
plt.plot(x, y, 'go', label='data')
plt.plot(px, D_py, 'r--', label='D', linewidth=5)
plt.plot(px, BGD_py, 'b--', label='BGD')
plt.plot(px, SGD_py, 'g--', label='SGD')
plt.plot(px, MBGD_py, 'y--', label='MBGD')
plt.plot(px, TF_py, 'b', label='Tensorflow')
plt.legend()
plt.show()
