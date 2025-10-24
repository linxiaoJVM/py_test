# encoding:utf-8
'''
创建人：lin
创建时间：
'''
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
import matplotlib
font = FontProperties(fname=r"/System/Library/Fonts/.ttc", size=10)
a = [5.1, 5.3, 6.0, 6.5, 7.4, 8, 8.9]
# b = [26, 35, 50, 131, 322, 606, 913]
# c = [21, 29, 36, 94, 232, 415, 714]

plt.rcParams['font.sans-serif'] = ['Simsun']
# print(matplotlib.matplotlib_fname())

fmt = '%.2f'
yticks = mtick.FormatStrFormatter(fmt)
lx = [u'4', u'7', u'10', u'20', u'30', u'40', u'50']
x_indexes = np.arange(len(lx))
width = 0.2
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x_indexes, a, label=u'图像文件上链耗时', )
# ax1.plot(x_indexes, b, '*b--', label=u'MinBFT交易时延')
# ax1.plot(x_indexes, c, 'or-', label=u'本文TS-BFT交易时延')
ax1.yaxis.set_major_formatter(yticks)
ax1.legend(loc=1)
# ax1.set_ylim([0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00])
ax1.set_ylabel('平均耗时(s)', {'size': 10})
ax1.set_xlabel('节点数量', {'size': 10})

plt.legend(prop={'family': 'Simsun', 'size': 10}, loc="upper center")
plt.xticks(x_indexes, lx)
plt.yticks([0.00, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.00])

ax = plt.gca()
ax.spines['top'].set_color('none')
# ax.spines['bottom'].set_color('none')
# ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')

# plt.savefig('./Figure_7.png', dpi=200)
plt.show()
