# coding: utf-8
'''
创建人：Moss
创建时间：
'''
import pandas as pd
from pandas import DataFrame, np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

a = [15, 14.55, 14.02, 14.01, 13.67]
b = [12.13, 12.03, 11.88, 11.78, 11.69]
c = [8.87, 8.73, 8.63, 8.59, 8.43]
d = [5.33, 5.28, 5.23, 5.18, 5.13]
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
plt.legend(prop={'family': 'SimHei', 'size': 14}, loc="upper right")
plt.xticks(x_indexes, lx)
plt.ylim([0, 22.5])
plt.xlabel(r'节点数', {'size': 16})
plt.ylabel(r'平均交易确认时间开销($s$)', {'size': 16})
plt.savefig('./Figure_4.pdf')
plt.show()
