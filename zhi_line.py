"""
功能：生成直方图
"""
# -- coding: utf-8 --

import matplotlib.pyplot as plt
import numpy as np

# 折线图
# 去掉上方和右方的边框
# fig, ax = plt.subplots()
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# 设置图例中的字体和大小
font = {'family': 'serif',
        'serif': 'Times New Roman',
        'weight': 'normal',
        'size': 15}
plt.rc('font', **font)

# 横坐标标签
labels=  ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9']
# 数据
y1 = [1234, 2345, 2345, 4656, 4366, 5356, 5367, 6356, 6654] # 柱体1的纵坐标
y2 = [234, 345, 456, 678, 789, 912, 945, 1111, 1234]  # 柱体2的纵坐标
y3 = [150, 224, 356, 451, 558, 490, 589, 723, 915]  # 柱体3的纵坐标
y4 = [45, 19, 25, 36, 83, 78, 34, 16, 24]  # 柱体4的纵坐标


# 横坐标位置（相对位置）
x = np.arange(len(labels))
# 柱体宽度
width = 0.2


#绘制柱体 x-width*1.5 柱体相对中央的偏移 y1 纵坐标 width 柱体宽度 color 柱体颜色 edgecolor 柱体边缘颜色 hatch 填充线条类型 label 柱体标签
# hatch 填充线条类型: {'/', '', '|', '-', '+', 'x', 'o', 'O', '.', '*'} 连续多个表示密度
plt.bar(x - width * 1.5, y1, width, color='r', edgecolor='black', hatch='|||', label='feat')
plt.bar(x - width * 0.5, y2, width, color='g', edgecolor='black', hatch='\\\\\\\\\\', label='key')
plt.bar(x + width * 0.5, y3, width, color='b', edgecolor='black', hatch='/', label='soc')
plt.bar(x + width * 1.5, y4, width, color='w', edgecolor='black', hatch='---', label='ksg')

# 显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置
plt.xticks(x, labels)
plt.xlabel("X", fontsize=15)  # 横坐标名字

plt.yscale('log')  # 设置纵坐标的缩放，写成m³格式
plt.yticks([1,10, 100, 1000, 10000], fontsize=12)
plt.ylabel('Y')

# loc 位置	best 0	upper right 1	upper left 2	lower left 3
# 			lower right 4	right 5	center left 6	center right 6
#			lower center 8	upper center 9	center 10
# 显示每条线的标签，loc 标签位置
plt.legend(loc="upper right")
plt.title("Histogram")   # 图标题
# plt.savefig("demo.pdf", dpi=300)  # 保存图片
plt.show()   # 显示图像
