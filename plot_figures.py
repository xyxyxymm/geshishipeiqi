# -*- coding: utf-8 -*-
# Plotting script for: 基于正交设计、均匀设计与响应面法的激光焊接工艺参数优化
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# ============================================================
# Chinese font setup for Windows
# ============================================================
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

output_dir = r'C:\Users\xuyyy\Desktop\实验设计\figures'
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# Figure 1: 正交试验 因素-指标趋势图
# ============================================================
factors = ['A-激光功率', 'B-焊接速度', 'C-离焦量', 'D-保护气流量']
level_data = {
    'A': {'label': '激光功率 (W)', 'x': [1000, 1200, 1400], 'k': [380.0, 415.0, 448.0], 'R': 68.0},
    'B': {'label': '焊接速度 (mm/s)', 'x': [20, 30, 40], 'k': [399.0, 417.0, 427.0], 'R': 28.0},
    'C': {'label': '离焦量 (mm)', 'x': [-1, 0, 1], 'k': [403.7, 413.7, 425.7], 'R': 22.0},
    'D': {'label': '保护气流量 (L/min)', 'x': [10, 15, 20], 'k': [410.3, 415.3, 417.3], 'R': 7.0},
}

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
axes = axes.flatten()

for idx, (key, d) in enumerate(level_data.items()):
    ax = axes[idx]
    ax.plot(d['x'], d['k'], 'o-', color='#2c7fb8', linewidth=2.5, markersize=10,
            markerfacecolor='white', markeredgewidth=2, markeredgecolor='#2c7fb8')
    ax.set_xlabel(d['label'], fontsize=12)
    ax.set_ylabel('抗拉强度均值 / MPa', fontsize=12)
    ax.set_title(f'{key}  (极差 R={d["R"]:.0f})', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.tick_params(labelsize=10)

fig.suptitle('图1  正交试验因素-指标趋势图', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig1_orthogonal_trend.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 1 saved.')

# ============================================================
# Figure 2: 极差对比 - 因素主次排序
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
names = ['A\n激光功率', 'B\n焊接速度', 'C\n离焦量', 'D\n保护气流量']
R_vals = [68.0, 28.0, 22.0, 7.0]
colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
bars = ax.bar(names, R_vals, color=colors, width=0.6, edgecolor='white', linewidth=1.2)
for bar, val in zip(bars, R_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{val:.0f}', ha='center', va='bottom', fontsize=13, fontweight='bold')
ax.set_ylabel('极差 R', fontsize=13)
ax.set_title('图2  各因素极差对比（极差越大影响越大）', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.tick_params(labelsize=11)
ax.set_ylim(0, 80)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig2_range_comparison.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 2 saved.')

# ============================================================
# Figure 3: 方差分析 SS 贡献饼图
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# Pie chart of SS
ss_labels = ['A-激光功率\n6938.0', 'B-焊接速度\n1208.0', 'C-离焦量\n728.0', 'D-保护气流量\n78.0']
ss_vals = [6938.0, 1208.0, 728.0, 78.0]
pie_colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3']
explode = (0.05, 0.02, 0.02, 0.02)

wedges, texts, autotexts = ax1.pie(ss_vals, explode=explode, labels=ss_labels,
                                     colors=pie_colors, autopct='%1.1f%%',
                                     startangle=90, textprops={'fontsize': 9})
for at in autotexts:
    at.set_fontweight('bold')
ax1.set_title('各因素偏差平方和SS占比', fontsize=12, fontweight='bold')

# Bar chart of F-values
f_labels = ['A-激光功率', 'B-焊接速度']
f_vals = [17.22, 3.00]
bar_colors = ['#e41a1c', '#377eb8']
bars = ax2.bar(f_labels, f_vals, color=bar_colors, width=0.5)
ax2.axhline(y=6.94, color='red', linestyle='--', linewidth=1.5, label='F(0.05,2,4)=6.94')
ax2.axhline(y=4.32, color='orange', linestyle=':', linewidth=1.5, label='F(0.10,2,4)=4.32')

for bar, val in zip(bars, f_vals):
    sig = '**' if val > 6.94 else ''
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'F={val:.2f}{sig}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax2.set_ylabel('F值', fontsize=12)
ax2.set_title('方差分析显著性检验', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9, loc='upper left')
ax2.grid(axis='y', alpha=0.2)
ax2.set_ylim(0, 22)

fig.suptitle('图3  正交试验方差分析', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig3_anova.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 3 saved.')

# ============================================================
# Figure 4: 均匀设计 实际值vs预测值
# ============================================================
A_uni = np.array([1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400])
B_uni = np.array([25.0, 32.5, 40.0, 22.5, 30.0, 37.5, 20.0, 27.5, 35.0])
C_uni = np.array([0.50, -0.25, -1.00, 0.75, 0.00, -0.75, 1.00, 0.25, -0.50])
D_uni = np.array([20.0, 18.8, 17.5, 16.2, 15.0, 13.8, 12.5, 11.2, 10.0])
Y_uni = np.array([282.3, 294.1, 298.8, 305.9, 314.8, 326.9, 328.3, 339.9, 350.7])

# Predicted from regression: Y=0.06+0.2257A+0.254B+0.1404C+2.4815D
Y_pred_uni = 0.06 + 0.2257*A_uni + 0.2540*B_uni + 0.1404*C_uni + 2.4815*D_uni

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(Y_uni, Y_pred_uni, s=80, c='#2c7fb8', edgecolors='white', linewidth=1.2, zorder=3)
min_val = min(Y_uni.min(), Y_pred_uni.min()) - 5
max_val = max(Y_uni.max(), Y_pred_uni.max()) + 5
ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=1.5, label='y=x')
for i in range(9):
    ax.annotate(f'{i+1}', (Y_uni[i], Y_pred_uni[i]), textcoords="offset points",
                xytext=(5, 5), fontsize=9, color='gray')
ax.set_xlabel('实测抗拉强度 / MPa', fontsize=13)
ax.set_ylabel('预测抗拉强度 / MPa', fontsize=13)
ax.set_title('图4  均匀设计回归模型 实测值 vs 预测值\n(R^2=0.9951)', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(alpha=0.3, linestyle='--')
ax.set_aspect('equal')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig4_uniform_pred_vs_actual.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 4 saved.')

# ============================================================
# Figure 5+6: 响应面 3D图 & 等高线图 (AxB interaction)
# ============================================================
from matplotlib import cm

# Coefficients from BBD model
coeff = np.array([430.7, 34.5, 13.6, 10.4, 4.6, -5.8, -1.8, -1.2, 1.0,
                   5.2, 0.3, -1.1, -0.7, -1.2, -0.6])

def predict_rsm(x1, x2, x3=0, x4=0):
    """Predict Y from coded variables using BBD model"""
    return (coeff[0] + coeff[1]*x1 + coeff[2]*x2 + coeff[3]*x3 + coeff[4]*x4
            + coeff[5]*x1**2 + coeff[6]*x2**2 + coeff[7]*x3**2 + coeff[8]*x4**2
            + coeff[9]*x1*x2 + coeff[10]*x1*x3 + coeff[11]*x1*x4
            + coeff[12]*x2*x3 + coeff[13]*x2*x4 + coeff[14]*x3*x4)

# ----- 5a: 3D Surface for x1(A功率) vs x2(B速度), holding x3=0, x4=0 -----
x1_grid = np.linspace(-1, 1, 50)
x2_grid = np.linspace(-1, 1, 50)
X1, X2 = np.meshgrid(x1_grid, x2_grid)
Z = predict_rsm(X1, X2, 0, 0)

fig = plt.figure(figsize=(14, 6))

# 3D Surface
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X1, X2, Z, cmap=cm.coolwarm, alpha=0.85, linewidth=0,
                         antialiased=True, edgecolor='none')
ax1.set_xlabel('x1 (激光功率)', fontsize=11, labelpad=8)
ax1.set_ylabel('x2 (焊接速度)', fontsize=11, labelpad=8)
ax1.set_zlabel('抗拉强度 / MPa', fontsize=11, labelpad=8)
ax1.set_title('3D响应曲面 (x3=x4=0)', fontsize=12, fontweight='bold')
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)

# Contour
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contourf(X1, X2, Z, levels=20, cmap=cm.coolwarm, alpha=0.9)
cs = ax2.contour(X1, X2, Z, levels=12, colors='black', linewidths=0.5)
ax2.clabel(cs, inline=True, fontsize=8, fmt='%.0f')
ax2.set_xlabel('x1 (激光功率)', fontsize=12)
ax2.set_ylabel('x2 (焊接速度)', fontsize=12)
ax2.set_title('等高线图 (x3=x4=0)', fontsize=12, fontweight='bold')
# Mark optimal point
ax2.plot(1, 1, 'r*', markersize=18, markeredgecolor='white', markeredgewidth=1.5,
         label='最优点 (1,1)')
ax2.legend(fontsize=10, loc='lower right')
fig.colorbar(contour, ax=ax2, shrink=0.8)

# Decode ticks
A_ticks_coded = [-1, 0, 1]
A_ticks_actual = [1000, 1200, 1400]
B_ticks_coded = [-1, 0, 1]
B_ticks_actual = [20, 30, 40]

ax1.set_xticks(A_ticks_coded)
ax1.set_xticklabels([f'{a}' for a in A_ticks_actual])
ax1.set_yticks(B_ticks_coded)
ax1.set_yticklabels([f'{b}' for b in B_ticks_actual])

ax2.set_xticks(A_ticks_coded)
ax2.set_xticklabels([f'{a}W' for a in A_ticks_actual])
ax2.set_yticks(B_ticks_coded)
ax2.set_yticklabels([f'{b}mm/s' for b in B_ticks_actual])

fig.suptitle('图5  响应面法：激光功率(A)与焊接速度(B)的交互效应', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig5_response_surface_AB.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 5 saved.')

# ============================================================
# Figure 6: 等高线图 - 其他代表性交互 (x1*x3: 功率-离焦)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# A x C (x1*x3), holding x2=0, x4=0
X1c, X3c = np.meshgrid(x1_grid, x1_grid)  # x1 and x3 both on [-1,1]
Z_ac = predict_rsm(X1c, 0, X3c, 0)

ax = axes[0]
contour1 = ax.contourf(X1c, X3c, Z_ac, levels=20, cmap=cm.RdYlBu_r, alpha=0.9)
cs1 = ax.contour(X1c, X3c, Z_ac, levels=10, colors='black', linewidths=0.5)
ax.clabel(cs1, inline=True, fontsize=8, fmt='%.0f')
ax.set_xlabel('x1 (激光功率)', fontsize=12)
ax.set_ylabel('x3 (离焦量)', fontsize=12)
ax.set_title('功率(A) x 离焦(C) 等高线', fontsize=12, fontweight='bold')
fig.colorbar(contour1, ax=ax, shrink=0.8)

# B x C (x2*x3), holding x1=0, x4=0
Z_bc = predict_rsm(0, X1c, X3c, 0)

ax = axes[1]
contour2 = ax.contourf(X1c, X3c, Z_bc, levels=20, cmap=cm.RdYlBu_r, alpha=0.9)
cs2 = ax.contour(X1c, X3c, Z_bc, levels=10, colors='black', linewidths=0.5)
ax.clabel(cs2, inline=True, fontsize=8, fmt='%.0f')
ax.set_xlabel('x2 (焊接速度)', fontsize=12)
ax.set_ylabel('x3 (离焦量)', fontsize=12)
ax.set_title('速度(B) x 离焦(C) 等高线', fontsize=12, fontweight='bold')
fig.colorbar(contour2, ax=ax, shrink=0.8)

fig.suptitle('图6  响应面法：其他交互作用的等高线图', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig6_contour_AC_BC.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 6 saved.')

# ============================================================
# Figure 7: 三种方法 最优预测值 对比
# ============================================================
fig, ax = plt.subplots(figsize=(11, 6))

methods = ['正交设计\nL9(3^4)\n(9次试验)', '均匀设计\nU9*(9^4)\n(9次试验)', '响应面法\nBox-Behnken\n(27次试验)']
# Using normalized/comparable values - we compare the predicted optimum for
# the same parameter setting A=1400W,B=40mm/s,C=1mm,D=20L/min
#
# But uniform had different mapping. Let me use the prediction at the optimum
# for each method using its own model.
#
# Actually for fair comparison, let's use the prediction at the agreed optimal point

orth_opt = 475.1   # Engineering average
uni_opt = 373.4    # From linear regression at (1400,30,1,20) - different base
rsm_opt = 487.7    # From BBD model

# Note: uniform has different parameter range, re-calculate at the same grid
# For uniform design, predict at (1400, 40, 1, 20):
uni_recalc = 0.06 + 0.2257*1400 + 0.2540*40 + 0.1404*1 + 2.4815*20
# uni_recalc = 0.06 + 315.98 + 10.16 + 0.1404 + 49.63 = 375.97

# Let me present these as-is, with note about different model bases
vals = [orth_opt, uni_recalc, rsm_opt]
bar_colors = ['#e41a1c', '#4daf4a', '#377eb8']
bars = ax.bar(methods, vals, color=bar_colors, width=0.5, edgecolor='white', linewidth=1.5)

for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val:.1f} MPa', ha='center', va='bottom', fontsize=13, fontweight='bold')

# Add baseline
ax.axhline(y=np.mean(vals), color='gray', linestyle='--', linewidth=1, alpha=0.5, label='平均值')

ax.set_ylabel('预测最优抗拉强度 / MPa', fontsize=13)
ax.set_title('图7  三种方法在最优参数下的预测结果对比\n(A=1400W, B=40mm/s, C=+1mm, D=20L/min)', fontsize=13, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.2, linestyle='--')
ax.set_ylim(0, max(vals)*1.15)
ax.tick_params(labelsize=11)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig7_method_comparison.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 7 saved.')

# ============================================================
# Figure 8: 综合比较雷达图 (Spider/Radar chart)
# ============================================================
categories = ['试验次数少', '因素水平多', '计算简便', '交互考察能力', '非线性拟合', '全局寻优精度']
N = len(categories)

orth_scores = [9, 3, 9, 3, 2, 5]
uni_scores = [9, 9, 6, 6, 3, 5]
rsm_scores = [4, 3, 3, 9, 9, 9]

angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

orth_closed = orth_scores + orth_scores[:1]
uni_closed = uni_scores + uni_scores[:1]
rsm_closed = rsm_scores + rsm_scores[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
ax.fill(angles, orth_closed, alpha=0.15, color='#e41a1c')
ax.plot(angles, orth_closed, 'o-', color='#e41a1c', linewidth=2, markersize=7, label='正交设计')
ax.fill(angles, uni_closed, alpha=0.15, color='#4daf4a')
ax.plot(angles, uni_closed, 's-', color='#4daf4a', linewidth=2, markersize=7, label='均匀设计')
ax.fill(angles, rsm_closed, alpha=0.15, color='#377eb8')
ax.plot(angles, rsm_closed, 'D-', color='#377eb8', linewidth=2, markersize=7, label='响应面法')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8)
ax.set_title('图8  三种试验设计方法综合性能雷达图\n(1-10分, 分数越高越好)', fontsize=13, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig8_radar_comparison.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 8 saved.')

# ============================================================
# Figure 9: Prediction profile plot - effect of each factor
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Factor A (x1) effect at center of others
x_vals = np.linspace(-1, 1, 100)
for idx, (name, ax_i) in enumerate(zip(['A-激光功率', 'B-焊接速度', 'C-离焦量', 'D-保护气流量'], axes.flatten())):
    y_vals = np.zeros(100)
    for j, x in enumerate(x_vals):
        vec = np.zeros(4)
        vec[idx] = x
        y_vals[j] = predict_rsm(vec[0], vec[1], vec[2], vec[3])
    
    ax_i.plot(x_vals, y_vals, '-', color='#2c7fb8', linewidth=3)
    ax_i.fill_between(x_vals, y_vals, alpha=0.15, color='#2c7fb8')
    ax_i.axvline(x=1.0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax_i.set_xlabel(f'{name} (编码值)', fontsize=11)
    ax_i.set_ylabel('抗拉强度 / MPa', fontsize=11)
    ax_i.set_title(name, fontsize=12, fontweight='bold')
    ax_i.grid(alpha=0.2)
    ax_i.set_xlim(-1.2, 1.2)

fig.suptitle('图9  各因素对响应的边际效应曲线（其他因素固定为0水平）', fontsize=14, fontweight='bold')
plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig9_marginal_effects.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 9 saved.')

# ============================================================
# Figure 10: Summary flowchart / 论文方法框架图
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

# Title
ax.text(7, 7.5, '试验设计方法综合研究框架', ha='center', fontsize=16, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#2c7fb8', alpha=0.15))

# Problem
ax.text(7, 6.7, '问题: 四因素三水平激光焊接工艺参数优化\n因素A~D, 响应Y=抗拉强度', ha='center', fontsize=11,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

# Three branches
branches = [
    (2, 5.5, '正交试验设计\nL9(3^4)', '#e41a1c'),
    (7, 5.5, '均匀设计\nU9*(9^4)', '#4daf4a'),
    (12, 5.5, '响应面法\nBox-Behnken', '#377eb8'),
]

for x, y, title, color in branches:
    ax.text(x, y, title, ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.2, edgecolor=color))
    ax.plot([7, x], [6.3, y+0.5], color=color, linewidth=1.5, alpha=0.6)

# Method details
methods = [
    (2, 4.5, '极差分析\n方差分析\nF检验\n工程平均估计', '#e41a1c'),
    (7, 4.5, '均匀设计表\n多水平映射\n多元线性回归\nR^2=0.9951', '#4daf4a'),
    (12, 4.5, '二阶回归模型\n3D响应曲面\n交互效应分析\n网格搜索寻优\nR^2=0.9931', '#377eb8'),
]

for x, y, text, color in methods:
    ax.text(x, y, text, ha='center', fontsize=9, va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=color, alpha=0.8))

# Comparison
ax.text(7, 3.0, '三种方法综合比较', ha='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ff7f00', alpha=0.15))
ax.plot([2, 12], [3.8, 3.8], color='gray', linewidth=1, linestyle='--', alpha=0.5)
for x, _, _, _ in branches:
    ax.plot([x, x], [4.0, 3.5], color='gray', linewidth=1, alpha=0.5)
    ax.plot([x, 7], [3.5, 3.3], color='gray', linewidth=1, alpha=0.3)

# Conclusion
ax.text(7, 2.0, '结论: 综合最优参数 A=1400W, B=40mm/s, C=+1mm, D=20L/min', ha='center', fontsize=12,
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.4, edgecolor='green'))

ax.plot([7, 7], [3.3, 2.4], color='green', linewidth=2, alpha=0.6)

plt.tight_layout()
fig.savefig(os.path.join(output_dir, 'fig10_framework.png'), dpi=200, bbox_inches='tight')
plt.close()
print('Figure 10 saved.')

print(f'\nAll 10 figures saved to: {output_dir}')
print('Files:')
for f in sorted(os.listdir(output_dir)):
    size = os.path.getsize(os.path.join(output_dir, f)) / 1024
    print(f'  {f}  ({size:.0f} KB)')
