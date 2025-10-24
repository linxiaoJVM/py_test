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
# a = [6710, 5150, 4251, 1321, 317, 106, 41]
# b = [8400, 6600, 5040, 2500, 420, 198, 78]
# c = [9720, 8534, 7020, 4160, 1140, 307, 103]

a = [6542, 5029, 3859, 989, 263, 51, 24]
b = [8391, 6600, 4800, 2160, 333, 180, 63]
c = [9541, 8120, 6827, 4059, 991, 283, 70]

plt.rcParams['font.sans-serif'] = ['Simsun']
# print(matplotlib.matplotlib_fname())

fmt = '%d'
yticks = mtick.FormatStrFormatter(fmt)
lx = [u'4', u'7', u'10', u'20', u'30', u'40', u'50']
x_indexes = np.arange(len(lx))
width = 0.15
fig = plt.figure()
ax1 = fig.add_subplot(111)
# ax1.plot(x_indexes, a, '*g-.', label=u'PBFT方案吞吐量(f=10%)')
# ax1.plot(x_indexes, b, '*b--', label=u'MinBFT方案吞吐量(f=10%)')
# ax1.plot(x_indexes, c, 'or-', label=u'本文TS-BFT方案吞吐量(f=10%)')
ax1.bar(x_indexes-width, a, width=width, alpha=0.8,
        label=u'PBFT方案吞吐量(f=10%)', edgecolor="black", hatch='///')
ax1.bar(x_indexes, b, width=width, alpha=0.8,
        label=u'MinBFT方案吞吐量(f=10%)', edgecolor="black", hatch='oo')
ax1.bar(x_indexes+width, c, width=width, alpha=0.8,
        label=u'本文TS-BFT方案吞吐量(f=10%)', edgecolor="black", hatch='**')

ax1.yaxis.set_major_formatter(yticks)
ax1.legend(loc=1)
ax1.set_ylim([0, 10000])
ax1.set_ylabel('平均交易吞吐量(TPS)', {'size': 10})
plt.legend(prop={'family': 'Simsun', 'size': 10}, loc="best")
plt.xticks(x_indexes, lx)
ax1.set_xlabel('节点数量(恶意节点比例为10%)', {'size': 10})
plt.savefig('./Figure_2_b.png', dpi=200)
# plt.show()
