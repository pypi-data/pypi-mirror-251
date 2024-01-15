import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

def resize_and_average_images(image1_path, image2_path):
    # Read images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Resize image2 to match the size of image1
    height, width, _ = image1.shape
    image2 = cv2.resize(image2, (width, height))

    # Calculate the average of pixel values
    averaged_image = np.mean([image1, image2], axis=0).astype(np.uint8)

    return averaged_image

def main():
    if len(sys.argv) != 3:
        print("Usage: resize_and_average <image1_path> <image2_path>")
        sys.exit(1)

    # File paths for two images
    image_path1 = sys.argv[1]
    image_path2 = sys.argv[2]

    # Resize images and calculate the average
    result_image = resize_and_average_images(image_path1, image_path2)

    # Display the result using Matplotlib
    plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
