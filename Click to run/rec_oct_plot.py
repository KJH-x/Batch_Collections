import os
import sys
os.chdir(sys.path[0])
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 设置rcParams
rcParams = {
    'figure.figsize': [12, 7],
    'figure.dpi': 100,
    'axes.labelsize': 'medium',
    'axes.linewidth': 1,
    'axes.grid': True,
    'axes.grid.which': 'major',
    'axes.grid.axis': 'both',
    'axes.edgecolor': 'black',
    'grid.alpha': 0.8,
    'axes.spines.left': True,
    'axes.spines.bottom': True,
    'axes.spines.right': True,
    'axes.spines.top': True,
    'xtick.major.size': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.size': 0.5,
    'ytick.major.width': 0.5,
    'xtick.minor.size': 0,
    'ytick.minor.size': 0,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'xtick.color': '#000',
    'ytick.color': '#000',
    'lines.linewidth': 0.5,
    'lines.color': '#000',
    'font.size': 10,
    'savefig.transparent': True,
}

# 使用rcParams设置
plt.rcParams.update(rcParams)

# 绘制图表
fig, ax = plt.subplots()

# 设置坐标轴范围
ax.set_xlim(1, 22)
ax.set_ylim(1, 16)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置刻度
ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=0.1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(base=0.1))

# 添加网格
ax.grid(True, which='both', linestyle='-', linewidth=0.5, color='#000', alpha=0.2)

# 调整图的上方、右侧、左侧和下方留白
plt.subplots_adjust(top=0.85, right=0.99, left=0.04, bottom=0.04)

# 保存为PNG格式
plt.savefig('custom_plot.png', dpi=1400, transparent=True)

plt.show()
