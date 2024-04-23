import numpy as np
import matplotlib.pyplot as plt

# Define the RMSE values
llms = [0.54, 0.32, 0.47, 0.62, 0.41, 0.49, 0.45, 0.62, 0.61, 0.57]
rmse_new = [0.33, 0.32, 0.19, 0.39, 0.31, 0.32, 0.25, 0.32, 0.17, 0.4]

# Create a scatter plot with jitter
plt.figure(figsize=(10, 5))
# Adding jitter by adding small random noise to the x-coordinates
x_llms = np.random.normal(1, 0.05, size=len(llms))
x_rmse = np.random.normal(2, 0.05, size=len(rmse_new))

plt.scatter(x_llms, llms, color='blue', alpha=0.5, label='LLMs')
plt.scatter(x_rmse, rmse_new, color='red', alpha=0.5, label='RMSE')
plt.xticks([1, 2], ['LLMs', 'RMSE'])
plt.ylabel('RMSE Values')
plt.title('Scatter Plot with Jitter for SMO Algorithm Comparisons')
plt.legend()
plt.grid(True)
plt.savefig('llms_vs_rmse_10_run.png')
