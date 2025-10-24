# encoding: utf-8
'''
创建人：Moss
创建时间：
'''
import pandas as pd
from pandas import DataFrame, np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

a = [330, 463, 1324, 2162, 2702]
b = [543, 875, 1732, 2574, 3117]
c = [756, 1233, 2144, 2992, 3534]
d = [933, 1632, 2578, 3348, 3930]
lx = [u'20', u'40', u'60', u'80', u'100']
plt.rcParams['font.sans-serif'] = ['SimHei']
x_indexes = np.arange(len(lx))
width = 0.15
fmt = '%.2f'
yticks = mtick.FormatStrFormatter(fmt)
plt.bar(x_indexes-1.5*width, a, width=width, alpha=0.5,
        label=u's=0.2', edgecolor="k", hatch='///')
plt.bar(x_indexes-0.5*width, b, width=width, alpha=0.5,
        label=u's=0.3', edgecolor="k", hatch='oo')
plt.bar(x_indexes+0.5*width, c, width=width, alpha=0.5,
        label=u's=0.4', edgecolor="k", hatch='|||')
plt.bar(x_indexes+1.5*width, d, width=width, alpha=0.5,
        label=u's=0.5', edgecolor="k", hatch='**')
plt.legend(prop={'family': 'SimHei', 'size': 14}, loc="upper left")
plt.xticks(x_indexes, lx)
plt.ylim([0, 4000])
plt.xlabel(r'节点数', {'size': 16})
plt.ylabel(r'平均交易吞吐量', {'size': 16})
# plt.savefig('./Figure_3.pdf')
plt.show()
