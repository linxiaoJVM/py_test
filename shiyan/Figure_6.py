# coding: utf-8
'''
创建人：Moss
创建时间：
'''
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
a = [25, 67, 94, 126, 153]  # PBFT
b = [21, 60, 85, 106, 123]  # MinBFT
c = [17.49, 33, 64.81, 78.01, 97.03]  # 本章提出方案 TS-BFT
f = [320, 553, 778, 913, 1034]  # PBFT
g = [400, 653, 978, 1313, 1634]  # MinBFT
h = [432, 779, 1210, 1635, 1957]  # 本章提出方案 (Proposed) TS-BFT
plt.rcParams['font.sans-serif'] = ['SimHei']

fmt = '%d'
yticks = mtick.FormatStrFormatter(fmt)
lx = [u'20', u'40', u'60', u'80', u'100']
x_indexes = np.arange(len(lx))
width = 0.15
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x_indexes, f, 'vg-.', label=u'PBFT交易吞吐量')
ax1.plot(x_indexes, g, 'ob--', label=u'MinBFT交易吞吐量')
ax1.plot(x_indexes, h, '*r-', label=u'TS-BFT交易吞吐量')
ax1.yaxis.set_major_formatter(yticks)
ax1.legend(loc=1)
ax1.set_ylim([0, 3000])
ax1.set_ylabel('共识平均交易吞吐量', {'size': 16})
plt.legend(prop={'family': 'SimHei', 'size': 13}, loc="upper left")
ax2 = ax1.twinx()  # this is the important function
ax2.bar(x_indexes-width, a, width=width, alpha=0.5,
        label=u'PBFT交易时延', edgecolor="k", hatch='///')
ax2.bar(x_indexes, b, width=width, alpha=0.5,
        label=u'MinBFT交易时延', edgecolor="k", hatch='oo')
ax2.bar(x_indexes+width, c, width=width, alpha=0.5,
        label=u'TS-BFT交易时延', edgecolor="k", hatch='**')
ax2.legend(loc=2)
ax2.set_ylim([0, 200])
ax2.set_ylabel('共识交易确认时延 ($s$)', {'size': 16})
plt.legend(prop={'family': 'SimHei', 'size': 13}, loc="upper right")
plt.xticks(x_indexes, lx)
ax1.set_xlabel('节点数量', {'size': 16})
# plt.savefig('./Figure_6.pdf')
plt.show()
# exit()
