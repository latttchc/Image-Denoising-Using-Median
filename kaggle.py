import kagglehub

# Download latest version
path = kagglehub.dataset_download("pallavii02/lena-imagedataset")

print("Path to dataset files:", path)