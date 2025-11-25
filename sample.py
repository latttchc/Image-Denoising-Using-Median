import cv2
import numpy as np
import matplotlib.pyplot as plt
# from google.colab.patches import cv2_imshow
from skimage.util import random_noise
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# 'PSNR' or 'SSIM'
IMAGE_TASK = 'PSNR'
 
# Load and preprocess the image
image_path = cv2.imread("dataset/Lena-image.png")
image_gray = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
 
# Define the noise levels
noise_levels = [0.01 * (2 ** i) for i in range(11)]  # [0.01, 0.02, ..., 10.24]
metric_values = []
 
# Iterate through each noise level
for noise_amount in noise_levels:
    # Add salt-and-pepper noise
    image_sp = random_noise(image_gray, mode="s&p", amount=noise_amount)
    image_sp = (255 * image_sp).astype("uint8")
 
    # Apply median filter
    recovered_image = cv2.medianBlur(image_sp, 3)  # Using a 3x3 kernel
 
    match IMAGE_TASK:
        case 'PSNR':
            # Calculate PSNR
            value = psnr(image_gray, recovered_image)
            metric_values.append(value)

            # Display results
            print(f"Noise amount: {noise_amount}, PSNR value: {value:.2f} dB")
            plt.imshow(recovered_image)
        case 'SSIM':
            # Calculate SSIM
            value = ssim(image_gray, recovered_image, data_range=255)
            metric_values.append(value)

            # Display results
            print(f"Noise amount: {noise_amount}, SSIM value: {value:.2f} dB")
            plt.imshow(recovered_image, cmap='gray')

match IMAGE_TASK:
    case 'PSNR':
        # Plot the metric values against the noise levels
        plt.figure(figsize=(10, 5))
        
        # Plotting PSNR vs Noise Amount
        plt.subplot(1, 2, 1)
        plt.plot(noise_levels, metric_values, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.xlabel("Noise Amount (log scale)")
        plt.ylabel("PSNR (dB)")
        plt.title("PSNR vs. Noise Amount")
        plt.grid(True)
        
        # Adding a table to display the Noise Amount and PSNR Values
        plt.subplot(1, 2, 2)
        table_data = [[f"{amount:.2f}", f"{psnr:.2f}"] for amount, psnr in zip(noise_levels, metric_values)]
        column_labels = ["Noise Amount", "PSNR (dB)"]
        plt.axis('tight')
        plt.axis('off')
        plt.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
        
        plt.tight_layout()
        plt.show()
    
    case 'SSIM':
        # Plot the metric values against the noise levels
        plt.figure(figsize=(10, 5))
        
        # Plotting SSIM vs Noise Amount
        plt.subplot(1, 2, 1)
        plt.plot(noise_levels, metric_values, marker='o', linestyle='-', color='b')
        plt.xscale('log')
        plt.xlabel("Noise Amount (log scale)")
        plt.ylabel("SSIM (dB)")
        plt.title("SSIM vs. Noise Amount")
        plt.grid(True)
        
        # Adding a table to display the Noise Amount and SSIM Values
        plt.subplot(1, 2, 2)
        table_data = [[f"{amount:.2f}", f"{ssim:.2f}"] for amount, ssim in zip(noise_levels, metric_values)]
        column_labels = ["Noise Amount", "SSIM (dB)"]
        plt.axis('tight')
        plt.axis('off')
        plt.table(cellText=table_data, colLabels=column_labels, cellLoc='center', loc='center')
        
        plt.tight_layout()
        plt.show()
