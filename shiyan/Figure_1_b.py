# encoding:utf-8
'''
创建人：Moss
创建时间：
'''
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
import matplotlib
font = FontProperties(fname=r"/System/Library/Fonts/.ttc", size=10)
a = [47, 84, 107, 230, 595, 1084, 1713]
b = [28, 44, 58, 144, 329, 657, 946]
c = [26, 35, 49, 101, 217, 408, 797]

plt.rcParams['font.sans-serif'] = ['Simsun']
# print(matplotlib.matplotlib_fname())

fmt = '%d'
yticks = mtick.FormatStrFormatter(fmt)
lx = [u'4', u'7', u'10', u'20', u'30', u'40', u'50']
x_indexes = np.arange(len(lx))
width = 0.2
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x_indexes, a, '+g-.', label=u'PBFT交易时延(f=10%)')
ax1.plot(x_indexes, b, '*b--', label=u'MinBFT交易时延(f=10%)')
ax1.plot(x_indexes, c, 'or-', label=u'本文TS-BFT交易时延(f=10%)')
ax1.yaxis.set_major_formatter(yticks)
ax1.legend(loc=1)
ax1.set_ylim([0, 2000])
ax1.set_ylabel('平均交易交易时延(ms)', {'size': 10})
plt.legend(prop={'family': 'Simsun', 'size': 10}, loc="best")
plt.xticks(x_indexes, lx)
ax1.set_xlabel('节点数量(恶意节点比例为10%)', {'size': 10})
plt.savefig('./Figure_1_b.png', dpi=200)
# plt.show()
