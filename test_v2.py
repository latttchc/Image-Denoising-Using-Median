import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from skimage.util import random_noise
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import pandas as pd
import config

IMAGE_TASK = config.TASK_NAME
IMAGE_NAME = config.FILE_NAME

if not os.path.exists("dataset"):
    os.makedirs("dataset")
    print("Created dataset folder. Please place image files in the folder.")
    exit()

if not os.path.exists("results"):
    os.makedirs("results")
    print("Created results folder.")

# Check if image file exists
image_file_path = f"dataset/{IMAGE_NAME}.png"
if not os.path.exists(image_file_path):
    print(f"Error: {image_file_path} not found.")
    print("Please place the image file in the dataset folder.")
    exit()


# noise of MSE
def mse(basic_image, noise_image):
    return np.mean((noise_image - basic_image) ** 2)

# Load and preprocess the image
image_path = cv2.imread(f"dataset/{IMAGE_NAME}.png")
image_gray = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
 
# Define the noise levels
noise_levels = [0.01 * (2 ** i) for i in range(11)]  # [0.01, 0.02, ..., 10.24]
filter_methods = ['median', 'gaussian', 'bilateral']
noise_types = ['salt_pepper', 'gaussian']
results = []
sp_image = []
ga_image = []

if config.OUTPUT_IMAGE:
    for noise_amount in noise_levels:
        sp_noisy = random_noise(image_gray, mode='s&p', amount=noise_amount)
        sp_image.append(sp_noisy)
        ga_noisy = random_noise(image_gray, mode='gaussian', var=noise_amount)
        ga_image.append(ga_noisy)
    # Output noise image 
    fig, axes = plt.subplots(2, 11, figsize=(22, 4))

    for i, img in enumerate(sp_image[:11]):
        axes[0,i].imshow(img, cmap='gray')
        axes[0,i].axis('off')
        axes[0,i].set_title(f"S&P\n{noise_levels[i]:.3f}")

    for i, img in enumerate(ga_image[:11]):
        axes[1,i].imshow(img, cmap='gray')
        axes[1,i].axis('off')
        axes[1,i].set_title(f"Gauss\n{noise_levels[i]:.3f}")

    plt.suptitle("Noise Comparision: Salt & Pepper vs Gaussian", fontsize=14)
    plt.tight_layout()
    if config.SAVE_RESULT:
        plt.savefig(f"results/{IMAGE_NAME}-noises.png")
    plt.show()

for noise_type in noise_types:
    for method in filter_methods:
        for noise_amount in noise_levels:
            if noise_type == 'salt_pepper':
                noisy_image = random_noise(image_gray, mode='s&p', amount=noise_amount)
            elif noise_type == 'gaussian':
                noisy_image = random_noise(image_gray, mode='gaussian', var=noise_amount)
            else:
                continue

            noisy_image = (255 * noisy_image).astype('uint8')
            if method == 'median':
                recovered = cv2.medianBlur(noisy_image, 3)
            elif method == 'gaussian':
                recovered = cv2.GaussianBlur(noisy_image, (3, 3), 0)
            elif method == 'bilateral':
                recovered = cv2.bilateralFilter(noisy_image, 5, 75, 75)

            match IMAGE_TASK:
                case 'PSNR':
                    value = psnr(image_gray, recovered)
                case 'SSIM':
                    value = ssim(image_gray, recovered, data_range=255)
                case 'MSE':
                    value = mse(image_gray, recovered)

            results.append({
                'noise_type': noise_type,
                'noise_amount': noise_amount,
                'filter': method,
                'value': value
            })

            print(f"Noise: {noise_type}, Amount: {noise_amount:.3f}, Filter: {method}, {IMAGE_TASK}: {value:.2f} dB")


df = pd.DataFrame(results)

# Graph plot
for noise_type in noise_types:
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 2, figure=fig, width_ratios=[1, 1], height_ratios=[1,1.5,1])

    ax_graph = fig.add_subplot(gs[1, 0])
    for method in filter_methods:
        sub_df = df[(df['noise_type'] == noise_type) & (df['filter'] == method)]
        ax_graph.plot(sub_df['noise_amount'], sub_df['value'], marker='o', label=method)
    ax_graph.set_xscale('log')
    ax_graph.set_xlabel("Noise Amount (log scale)")
    ax_graph.set_ylabel(f"{IMAGE_TASK} (dB)")
    ax_graph.set_title(f"{IMAGE_TASK} Comparison for {noise_type.title()} Noise")
    ax_graph.legend()
    ax_graph.grid(True)

    for i, method in enumerate(filter_methods):
        ax_table = fig.add_subplot(gs[i, 1])
        sub_df = df[(df['noise_type'] == noise_type) & (df['filter'] == method)]
        table_data = sub_df[['noise_amount', 'value']].round(3).values.tolist()
        table_header = ["Noise Amount", f"{IMAGE_TASK} (dB)"]
        ax_table.axis('off')
        if table_data:
            ax_table.table(cellText=table_data, colLabels=table_header, cellLoc='center', loc='center')
        ax_table.set_title(f"{method.title()} Filter")

    plt.suptitle(f"{noise_type.title()} Noise Analysis", fontsize=14)
    plt.tight_layout()
    if config.SAVE_RESULT:
        plt.savefig(f"results/{IMAGE_TASK}_{noise_type}_analysis.png")
    plt.show()

