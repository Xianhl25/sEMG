import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from matplotlib import rcParams
config = {
    "font.family":'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
bound_gaussian_sigma = 42

data_file = r"D:\GitHub\sEMG\data\processed\SLO_BFlh_0.csv"

data_df = pd.read_csv(data_file)

x = data_df['X']
mean = data_df['Mean']
mean_smooth = gaussian_filter1d(data_df['Mean'], sigma=9)
upper_bound = data_df['Mean + Std Dev']
upper_bound_smooth = gaussian_filter1d(data_df['Mean + Std Dev'], sigma=bound_gaussian_sigma)
lower_bound = data_df['Mean - Std Dev']
lower_bound_smooth = gaussian_filter1d(data_df['Mean - Std Dev'], sigma=bound_gaussian_sigma)

# 绘制误差带图
fig, ax = plt.subplots(figsize=(6, 4))
plt.plot(x, mean_smooth, color='#5D5D60', label='Mean', linewidth=3.0, linestyle='--')
plt.fill_between(x, lower_bound_smooth, upper_bound_smooth, color='#5D5D60', alpha=0.2)

# 配置
plt.title("Muscle Activation ", fontsize=14)
plt.xlabel("Gait Phase (%)", fontsize=12)
# plt.ylabel("RMS of VAS", fontsize=12)
plt.ylabel("RMS of GAS", fontsize=12)
# plt.ylabel("RMS of BF", fontsize=12)
plt.legend(fontsize=12)
# plt.grid(alpha=0.5)
plt.tight_layout()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.show()