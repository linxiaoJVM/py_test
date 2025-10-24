"""
功能：生成折线图
"""
# -- coding: utf-8 --

import matplotlib.pyplot as plt  # 为方便简介为plt
import numpy as np  # 画图过程中会使用numpy
import pandas as pd  # 画图过程中会使用pandas

# 查看 Matplotlib 可用绘图风格
print(plt.style.available)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文无法正常显示的问题
plt.rcParams['axes.unicode_minus'] = False  # 负号显示

# 折线图
# 去掉上方和右方的边框
# fig, ax = plt.subplots()
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# 设置图例中的字体和大小
font = {'family': 'SimSun',
        'serif': 'Times New Roman',
        'weight': 'normal',
        'size': 11}
plt.rc('font', **font)

# 数据
x = [i * 0.1 for i in range(1, 10)]  # 点的横坐标x
y1 = [1234, 2345, 2345, 4656, 4366, 5356, 5367, 6356, 6654]  # 线1的纵坐标
y2 = [234, 345, 456, 678, 789, 912, 945, 1111, 1234]  # 线2的纵坐标
y3 = [150, 224, 356, 451, 558, 490, 589, 723, 915]  # 线3的纵坐标
y4 = [45, 19, 25, 36, 83, 78, 34, 16, 24]  # 线4的纵坐标

# 点的形状	. 点	, 像素点	o 圆点	v 下三角点	^ 上三角点	< 左三角点
#			> 右三角点	1 下三叉点	 2 上三叉点	 3 左三叉点	 4 右三叉点
#			s 正方点	p 五角点	* 星形点	h 六边形点1	H 六边形点2
#			+ 加号点	x 乘号点	D 实心菱形点	d 瘦菱形点	_ 横线点
# 线条类型	- 实线	-- 虚线	-. 虚点线	: 点线
# 绘画出四条线，x 横坐标，y1 纵坐标，'s-' 点的形状，color 线条颜色，label 线条标签
plt.plot(x, y1, 's-', color='black', label='y1')
plt.plot(x, y2, '^-', color='red', label="y2")
plt.plot(x, y3, 'v-', color='yellow', label="y3")
plt.plot(x, y4, 'o-', color='green', label="y4")

# 设置横坐标
plt.xticks([x * 0.1 for x in range(1, 10)], fontsize=12)
plt.xlabel("横坐标", fontsize=15)  # 横坐标名字

# 设置纵坐标
plt.yscale('log')  # 设置纵坐标的缩放，写成m³格式
plt.yticks([1, 10, 100, 1000, 10000], fontsize=12)
plt.ylabel("Y", fontsize=15)  # 纵坐标名字

# loc 位置	best 0	upper right 1	upper left 2	lower left 3
# 			lower right 4	right 5	center left 6	center right 6
#			lower center 8	upper center 9	center 10
# 显示每条线的标签，loc 标签位置
plt.legend(loc="lower right")
plt.title("折线图")  # 图标题
# plt.savefig("demo.pdf", dpi=200)   #保存图片
plt.show()  # 显示图像
