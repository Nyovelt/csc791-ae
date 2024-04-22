import matplotlib.pyplot as plt

# Data
llama3_8b = [0.32, 0.32, 0.36, 0.36, 0.32, 0.32, 0.32, 0.32, 0.36, 0.58]
rmse = [0.59, 0.41, 0.41, 0.41, 0.41, 0.41, 0.41, 0.41, 0.41, 0.41]
iterations = list(range(1, 11))

# Plot
plt.figure(figsize=(10, 5))
plt.plot(iterations, llama3_8b, marker='o', label='LLaMa3:8b')
plt.plot(iterations, rmse, marker='x', label='RMSE')
plt.title('Comparison between SMO algorithm using llama3:8b and SMO algorithm using RMSE in a single run')
plt.xlabel('Iterations')
plt.ylabel('RMSE value of the selected best row')
plt.legend()
plt.grid(True)
plt.savefig('llama3_8b_vs_rmse.png')
