import numpy as np
import matplotlib.pyplot as plt

# Data definitions
zero_shot = [0.54, 0.77, 0.17, 0.77, 0.69, 0.93, 0.44, 0.31, 0.71, 0.59]
four_shots = [0.38, 0.62, 0.34, 0.79, 0.31, 0.56, 0.41, 0.59, 0.38, 0.38, 0.81, 0.59, 0.62, 0.81, 0.38, 0.71, 0.33, 0.46, 0.34, 0.58]
eight_shots = [0.54, 0.32, 0.47, 0.62, 0.41, 0.49, 0.45, 0.62, 0.61, 0.57]

# Calculate averages
average_zero_shot = np.mean(zero_shot)
average_four_shots = np.mean(four_shots)
average_eight_shots = np.mean(eight_shots)

# Plot setup
plt.figure(figsize=(12, 6))

# Scatter points with jitter
x_zero = np.random.normal(1, 0.05, size=len(zero_shot))
x_four = np.random.normal(2, 0.05, size=len(four_shots))
x_eight = np.random.normal(3, 0.05, size=len(eight_shots))
plt.scatter(x_zero, zero_shot, alpha=0.5, label='0 Shot')
plt.scatter(x_four, four_shots, alpha=0.5, label='4 Shots')
plt.scatter(x_eight, eight_shots, alpha=0.5, label='8 Shots')

# Plotting averages
plt.scatter([1, 2, 3], [average_zero_shot, average_four_shots, average_eight_shots], color='red', marker='D', s=100, label='Average')

# Linear line connecting the averages
plt.plot([1, 2, 3], [average_zero_shot, average_four_shots, average_eight_shots], color='green', linestyle='-', marker='D', markersize=10, linewidth=2, label='Average Line')

plt.xticks([1, 2, 3], ['0 Shot', '4 Shots', '8 Shots'])
plt.ylabel('RMSE Values')
plt.title('RMSE Comparison for Different Few Shot Learning Settings')
plt.legend()
plt.grid(True)
plt.savefig('few_shots.png')
