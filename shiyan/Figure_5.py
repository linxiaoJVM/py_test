# coding: utf-8
'''
创建人：Moss
创建时间：
'''
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
a = [15.5667, 38.2532, 69.3024, 93.9931, 114.0267]  # time cost PBFT
b = [16, 34, 64, 86, 103]  #
c = [14.46, 28.96, 44.81, 58.01, 73.03]  # TS-BFT
f = [332, 691, 1120, 1335, 1477]  # Throughput PBFT
g = [432, 791, 1220, 1435, 1677]  # MinBFT
h = [501, 853, 1368, 1713, 1873]  # 本章提出方案 (Proposed) TS-BFT
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
ax2.set_ylim([0, 150])
ax2.set_ylabel('共识交易确认时延 ($s$)', {'size': 16})
plt.legend(prop={'family': 'SimHei', 'size': 13}, loc="upper right")
plt.xticks(x_indexes, lx)
ax1.set_xlabel('节点数量', {'size': 16})
plt.savefig('./Figure_5.pdf')
plt.show()
# exit()
