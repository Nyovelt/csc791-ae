import numpy as np
import matplotlib.pyplot as plt

# RMSE values for each model
rmse_chatgpt = [0.38, 0.45, 0.59, 0.39, 0.4]
rmse_llama2 = [0.63, 0.8, 0.77, 0.77, 0.56, 0.92, 0.33, 0.28, 0.77, 0.62, 0.38, 0.59, 0.87, 0.35, 0.76, 0.77, 0.59, 0.49, 0.59, 0.91]
rmse_llama38b = [0.54, 0.32, 0.47, 0.62, 0.41, 0.49, 0.45, 0.62, 0.61, 0.57]

# Calculate averages
avg_rmse_chatgpt = np.mean(rmse_chatgpt)
avg_rmse_llama2 = np.mean(rmse_llama2)
avg_rmse_llama38b = np.mean(rmse_llama38b)

# Cost per run
cost_chatgpt = 3.0
cost_llama2 = 0.2
cost_llama38b = 0.1

# Average RMSE and cost per run for each model
avg_rmse = [avg_rmse_chatgpt, avg_rmse_llama2, avg_rmse_llama38b]
cost_per_run = [cost_chatgpt, cost_llama2, cost_llama38b]
release_dates = ["Aug 22, 2023", "Feb 2023", "Apr 18, 2024"]  # Updated release dates for each model

plt.figure(figsize=(10, 6))

# Scatter plot with RMSE on y-axis and cost on x-axis
plt.scatter(cost_per_run, avg_rmse, s=[100, 100, 100], alpha=0.5)  # Adjusted marker size for clarity
for i, txt in enumerate(["ChatGPT-3.5 Turbo", "LLaMa2:13b", "LLaMa3:8b"]):
    plt.annotate(f"{txt} ({release_dates[i]})", (cost_per_run[i], avg_rmse[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.ylabel('Average RMSE (lower is better)')
plt.xlabel('Cost per Run ($)')
plt.title('Cost-Performance Considerations for Various Large Language Models with Release Dates')
plt.grid(True)
plt.savefig('cost_performance.png')
