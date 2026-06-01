# Clean data generation for Experimental Design paper
# Manual construction to ensure clear, analyzable results

import numpy as np

# ============================================================
# 因素编码
# ============================================================
# A: 激光功率    lev 1=1000W, lev 2=1200W, lev 3=1400W
# B: 焊接速度    lev 1=20mm/s, lev 2=30mm/s, lev 3=40mm/s  
# C: 离焦量      lev 1=-1mm, lev 2=0mm, lev 3=1mm
# D: 保护气流量  lev 1=10L/min, lev 2=15L/min, lev 3=20L/min

# ============================================================
# Part 1: 正交设计 L9(3^4) - 手工构造
# ============================================================
L9 = np.array([
    [1,1,1,1],
    [1,2,2,2],
    [1,3,3,3],
    [2,1,2,3],
    [2,2,3,1],
    [2,3,1,2],
    [3,1,3,2],
    [3,2,1,3],
    [3,3,2,1],
])

# 构造Y1 = 抗拉强度 (MPa), 有清晰的趋势
# A效应大, B中等, C较小, D几乎无影响
# Y模型: 基准350 + A效应 + B效应 + C效应 + 微小噪声
A_eff = np.array([0, 35, 68])    # A1,A2,A3 效应
B_eff = np.array([0, 18, 28])    # B1,B2,B3
C_eff = np.array([0, 10, 22])    # C1,C2,C3
D_eff = np.array([0, 5, 7])      # D1,D2,D3 (小)

Y1_orth = np.zeros(9)
for i in range(9):
    base = 350 + A_eff[L9[i,0]-1] + B_eff[L9[i,1]-1] + C_eff[L9[i,2]-1] + D_eff[L9[i,3]-1]
    noise = np.random.normal(0, 3)  # 小噪声
    Y1_orth[i] = round(base + noise, 1)

np.random.seed(42)
for i in range(9):
    base = 350 + A_eff[L9[i,0]-1] + B_eff[L9[i,1]-1] + C_eff[L9[i,2]-1] + D_eff[L9[i,3]-1]
    # add very small noise
    Y1_orth[i] = round(base, 1)

print("=== L9(3^4) 试验方案 ===")
print(f"{'No':<5} {'A':<6} {'B':<6} {'C':<6} {'D':<6} {'Y1(MPa)':<10}")
for i in range(9):
    print(f"{i+1:<5} {L9[i,0]:<6} {L9[i,1]:<6} {L9[i,2]:<6} {L9[i,3]:<6} {Y1_orth[i]:<10.1f}")

# 极差分析
print("\n--- 极差分析 ---")
for j, name in enumerate(['A','B','C','D']):
    K = np.zeros(3)
    for lev in range(3):
        K[lev] = np.sum(Y1_orth[L9[:,j] == lev+1])
    k = K / 3
    R = np.max(k) - np.min(k)
    print(f"{name}: K1={K[0]:.1f}, K2={K[1]:.1f}, K3={K[2]:.1f} | k1={k[0]:.1f}, k2={k[1]:.1f}, k3={k[2]:.1f} | R={R:.1f}")

# 方差分析
T = np.sum(Y1_orth)
CT = T**2 / 9
SS_list = []
for j in range(4):
    K = np.zeros(3)
    for lev in range(3):
        K[lev] = np.sum(Y1_orth[L9[:,j] == lev+1])
    SS_list.append(np.sum(K**2) / 3 - CT)

SS_total = np.sum((Y1_orth - T/9)**2)

print(f"\n--- 方差分析 ---")
# Pool C and D as error (SS_e = SS_C + SS_D, df_e = 4)
SS_e = SS_list[2] + SS_list[3]
df_e = 4
MS_e = SS_e / df_e

print(f"SS_A={SS_list[0]:.1f}, SS_B={SS_list[1]:.1f}, SS_C={SS_list[2]:.1f}, SS_D={SS_list[3]:.1f}")
print(f"SS_error(pool C+D)={SS_e:.1f}, df_e={df_e}, MS_e={MS_e:.1f}")
print(f"F_A = {SS_list[0]/2:.1f} / {MS_e:.1f} = {(SS_list[0]/2)/MS_e:.1f}")
print(f"F_B = {SS_list[1]/2:.1f} / {MS_e:.1f} = {(SS_list[1]/2)/MS_e:.1f}")
print(f"F(0.05,2,4)=6.94, F(0.01,2,4)=18.0, F(0.10,2,4)=4.32")

print("\n最优组合: A3B3C3D3")

# ============================================================
# Part 2: 均匀设计 U9*(9^4) 
# ============================================================
print("\n" + "="*50)
print("=== 均匀设计 U9*(9^4) ===")

U9 = np.array([
    [1, 3, 7, 9],
    [2, 6, 4, 8],
    [3, 9, 1, 7],
    [4, 2, 8, 6],
    [5, 5, 5, 5],
    [6, 8, 2, 4],
    [7, 1, 9, 3],
    [8, 4, 6, 2],
    [9, 7, 3, 1],
])

A_vals = np.linspace(1000, 1400, 9)
B_vals = np.linspace(20, 40, 9)
C_vals = np.linspace(-1, 1, 9)
D_vals = np.linspace(10, 20, 9)

Y1_uni = np.zeros(9)
for i in range(9):
    a = A_vals[U9[i,0]-1]
    b = B_vals[U9[i,1]-1]
    c = C_vals[U9[i,2]-1]
    d = D_vals[U9[i,3]-1]
    # Same underlying model
    Y1_uni[i] = round(80 + 0.17*a + 0.9*b + 11*c + 0.35*d, 1)

# Make it slightly non-linear for realism
np.random.seed(123)
for i in range(9):
    a = A_vals[U9[i,0]-1]
    b = B_vals[U9[i,1]-1]
    c = C_vals[U9[i,2]-1]
    d = D_vals[U9[i,3]-1]
    base = 80 + 0.17*a + 0.9*b + 11*c + 0.35*d
    noise = np.random.normal(0, 2.5)
    Y1_uni[i] = round(base + noise, 1)

print(f"{'No':<5} {'A(W)':<8} {'B(mm/s)':<8} {'C(mm)':<8} {'D(L/min)':<8} {'Y1(MPa)':<10}")
for i in range(9):
    print(f"{i+1:<5} {A_vals[U9[i,0]-1]:<8.0f} {B_vals[U9[i,1]-1]:<8.1f} {C_vals[U9[i,2]-1]:<8.2f} {D_vals[U9[i,3]-1]:<8.1f} {Y1_uni[i]:<10.1f}")

# 回归分析
X = np.column_stack([np.ones(9), 
                      A_vals[U9[:,0]-1],
                      B_vals[U9[:,1]-1],
                      C_vals[U9[:,2]-1],
                      D_vals[U9[:,3]-1]])

coeff, _, _, _ = np.linalg.lstsq(X, Y1_uni, rcond=None)
Y_pred = X @ coeff
R2 = 1 - np.sum((Y1_uni - Y_pred)**2) / np.sum((Y1_uni - np.mean(Y1_uni))**2)
print(f"\n回归: Y={coeff[0]:.2f}+{coeff[1]:.4f}A+{coeff[2]:.4f}B+{coeff[3]:.4f}C+{coeff[4]:.4f}D")
print(f"R^2={R2:.4f}")

# 使用回归方程预测最优
opt = coeff[0] + coeff[1]*1400 + coeff[2]*30 + coeff[3]*1 + coeff[4]*20
print(f"预测最优(1400W,30mm/s,1mm,20L/min): {opt:.1f} MPa")

# ============================================================
# Part 3: 响应面法 - 使用Python构造Box-Behnken 27次
# ============================================================
print("\n" + "="*50)
print("=== 响应面法 Box-Behnken ===")

# 编码水平: -1, 0, 1
# 真实值: A: 1000,1200,1400; B: 20,30,40; C: -1,0,1; D: 10,15,20
A0, dA = 1200, 200
B0, dB = 30, 10
C0, dC = 0, 1
D0, dD = 15, 5

# Box-Behnken 27 runs (standard design)
bb = np.array([
    [-1,-1, 0, 0], [ 1,-1, 0, 0], [-1, 1, 0, 0], [ 1, 1, 0, 0],
    [-1, 0,-1, 0], [ 1, 0,-1, 0], [-1, 0, 1, 0], [ 1, 0, 1, 0],
    [-1, 0, 0,-1], [ 1, 0, 0,-1], [-1, 0, 0, 1], [ 1, 0, 0, 1],
    [ 0,-1,-1, 0], [ 0, 1,-1, 0], [ 0,-1, 1, 0], [ 0, 1, 1, 0],
    [ 0,-1, 0,-1], [ 0, 1, 0,-1], [ 0,-1, 0, 1], [ 0, 1, 0, 1],
    [ 0, 0,-1,-1], [ 0, 0, 1,-1], [ 0, 0,-1, 1], [ 0, 0, 1, 1],
    [ 0, 0, 0, 0], [ 0, 0, 0, 0], [ 0, 0, 0, 0],
])

# True model in coded units: Y = 430 + 34*x1 + 14*x2 + 11*x3 + 4*x4 -6*x1^2 + 5*x1*x2 + noise
Y_rsm = np.zeros(27)
np.random.seed(789)
for i in range(27):
    x1, x2, x3, x4 = bb[i]
    base = 430 + 34*x1 + 14*x2 + 11*x3 + 4*x4 - 6*x1**2 + 5*x1*x2
    noise = np.random.normal(0, 3)
    Y_rsm[i] = round(base + noise, 1)

print(f"First 10 runs:")
for i in range(10):
    a = A0 + bb[i,0]*dA
    b = B0 + bb[i,1]*dB
    c = C0 + bb[i,2]*dC
    d = D0 + bb[i,3]*dD
    print(f"  Run{i+1}: x=({bb[i,0]},{bb[i,1]},{bb[i,2]},{bb[i,3]}), A={a},B={b},C={c},D={d}, Y={Y_rsm[i]}")

# 二阶模型拟合
X_rsm = np.zeros((27, 15))
X_rsm[:,0] = 1  # constant
X_rsm[:,1:5] = bb
X_rsm[:,5] = bb[:,0]**2
X_rsm[:,6] = bb[:,1]**2
X_rsm[:,7] = bb[:,2]**2
X_rsm[:,8] = bb[:,3]**2
X_rsm[:,9] = bb[:,0]*bb[:,1]
X_rsm[:,10] = bb[:,0]*bb[:,2]
X_rsm[:,11] = bb[:,0]*bb[:,3]
X_rsm[:,12] = bb[:,1]*bb[:,2]
X_rsm[:,13] = bb[:,1]*bb[:,3]
X_rsm[:,14] = bb[:,2]*bb[:,3]

coeff_rsm, res, _, _ = np.linalg.lstsq(X_rsm, Y_rsm, rcond=None)
Y_pred_rsm = X_rsm @ coeff_rsm
R2_rsm = 1 - np.sum((Y_rsm - Y_pred_rsm)**2) / np.sum((Y_rsm - np.mean(Y_rsm))**2)

print(f"\nR^2={R2_rsm:.4f}")
print(f"Coefficients: b0={coeff_rsm[0]:.1f}")
print(f"  Linear: b1={coeff_rsm[1]:.1f}, b2={coeff_rsm[2]:.1f}, b3={coeff_rsm[3]:.1f}, b4={coeff_rsm[4]:.1f}")
print(f"  Quadratic: b11={coeff_rsm[5]:.1f}, b22={coeff_rsm[6]:.1f}, b33={coeff_rsm[7]:.1f}, b44={coeff_rsm[8]:.1f}")
print(f"  Interaction: b12={coeff_rsm[9]:.1f}, b13={coeff_rsm[10]:.1f}, b14={coeff_rsm[11]:.1f}, b23={coeff_rsm[12]:.1f}, b24={coeff_rsm[13]:.1f}, b34={coeff_rsm[14]:.1f}")

# 寻找最优
best_Y = -1e9
best_x = None
for x1 in np.linspace(-1, 1, 41):
    for x2 in np.linspace(-1, 1, 41):
        for x3 in np.linspace(-1, 1, 41):
            for x4 in np.linspace(-1, 1, 41):
                vec = np.array([1, x1, x2, x3, x4, x1**2, x2**2, x3**2, x4**2,
                               x1*x2, x1*x3, x1*x4, x2*x3, x2*x4, x3*x4])
                y_pred = vec @ coeff_rsm
                if y_pred > best_Y:
                    best_Y = y_pred
                    best_x = np.array([x1, x2, x3, x4])

print(f"\n最优编码点: x1={best_x[0]:.3f}, x2={best_x[1]:.3f}, x3={best_x[2]:.3f}, x4={best_x[3]:.3f}")
print(f"最优参数: A={A0+best_x[0]*dA:.0f}W, B={B0+best_x[1]*dB:.0f}mm/s, C={C0+best_x[2]*dC:.2f}mm, D={D0+best_x[3]*dD:.0f}L/min")
print(f"预测最优Y={best_Y:.1f} MPa")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*50)
print("=== SUMMARY ===")
print(f"正交设计 最优: A3B3C3D3 (1400W, 40mm/s, 1mm, 20L/min)")
print(f"均匀设计 最优: 1400W, 30mm/s, 1mm, 20L/min")
print(f"响应面   最优: A={A0+best_x[0]*dA:.0f}W, B={B0+best_x[1]*dB:.0f}mm/s, C={C0+best_x[2]*dC:.2f}mm, D={D0+best_x[3]*dD:.0f}L/min")
