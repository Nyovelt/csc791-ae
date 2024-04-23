import numpy as np
import matplotlib.pyplot as plt

# Define the RMSE values
llms = [0.52, 0.44, 0.43, 0.45, 0.32]
rmse_new = [0.22, 0.21, 0.28, 0.17, 0.29]

# Create a scatter plot with jitter
plt.figure(figsize=(10, 5))
# Adding jitter by adding small random noise to the x-coordinates
x_llms = np.random.normal(1, 0.05, size=len(llms))
x_rmse = np.random.normal(2, 0.05, size=len(rmse_new))

plt.scatter(x_llms, llms, color='blue', alpha=0.5, label='LLMs')
plt.scatter(x_rmse, rmse_new, color='red', alpha=0.5, label='RMSE')
plt.xticks([1, 2], ['LLMs', 'RMSE'])
plt.ylabel('RMSE Values')
plt.title('Scatter Plot with Jitter for SMO Algorithm Comparisons (Wine Quality)')
plt.legend()
plt.grid(True)
plt.savefig('llms_vs_rmse_5_run_wine.png')
