import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import os
import sys
os.chdir(sys.path[0])

# 设置rcParams
rcParams = {
    'figure.figsize': [12, 7],
    'figure.dpi': 140,
    'axes.labelsize': 'medium',
    'axes.linewidth': 2,
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
    'lines.linewidth': 1,
    'lines.color': '#000',
    'font.size': 10,
    'savefig.transparent': True,
}

# 使用rcParams设置
plt.rcParams.update(rcParams)

# 绘制图表
fig, ax = plt.subplots()

# 设置坐标轴范围
ax.set_xlim(0.01, 10.1)
ax.set_ylim(0.01, 10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置对数坐标轴
ax.set_xscale('log')
ax.set_yscale('log')

# 设置刻度
ax.xaxis.set_major_locator(ticker.FixedLocator([0.01, 0.1, 1, 10]))
ax.yaxis.set_major_locator(ticker.FixedLocator([0.01, 0.1, 1, 10]))

# 设置刻度标签
ax.set_xticklabels(['0.01', '0.1', '1', '10'])
ax.set_yticklabels(['0.01', '0.1', '1', '10'])

# 添加网格
ax.grid(True, which='both', linestyle='-', linewidth=0.5,
        color='#444654', alpha=1.0)
plt.subplots_adjust(top=0.85, right=0.99, left=0.04, bottom=0.04)
ax.tick_params(axis='both', which='major', pad=10)
# 保存为PNG格式
plt.savefig('log_log.grid.png', dpi=330, transparent=True)
plt.savefig('log_log.grid.svg', format='svg', transparent=True)
# plt.show()
