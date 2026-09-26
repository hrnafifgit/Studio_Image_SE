import os
import cv2
import numpy as np

out_dir = os.path.abspath("g:/haroonalafif/universty/level four/project/imageprocessingmalek/web/samples")
os.makedirs(out_dir, exist_ok=True)

# 1. Standard Benchmark Image (Rich with geometric shapes, text, gradients, and concentric rings)
h, w = 600, 800
img1 = np.zeros((h, w, 3), dtype=np.uint8)

# Smooth gradient background
for y in range(h):
    for x in range(w):
        img1[y, x] = [int(x / w * 140), int(y / h * 120), int((x + y) / (w + h) * 180)]

# Concentric geometric rings
cv2.circle(img1, (w // 4, h // 2), 120, (255, 255, 255), 2)
cv2.circle(img1, (w // 4, h // 2), 80, (0, 229, 255), 3)
cv2.circle(img1, (w // 4, h // 2), 40, (124, 77, 255), 4)

# Polygon and sharp edges
pts = np.array([[w * 3 // 4, h // 4], [w * 7 // 8, h // 2], [w * 3 // 4, h * 3 // 4], [w * 5 // 8, h // 2]], np.int32)
cv2.fillPoly(img1, [pts], (220, 180, 50))
cv2.polylines(img1, [pts], True, (255, 255, 255), 3)

# Contrast grid
for i in range(5):
    val = int(i * 50)
    cv2.rectangle(img1, (100 + i * 50, h - 120), (145 + i * 50, h - 60), (val, val, val), -1)
    cv2.rectangle(img1, (100 + i * 50, h - 120), (145 + i * 50, h - 60), (255, 255, 255), 1)

cv2.putText(img1, "VisionCraft DSP Benchmark", (w // 2 - 180, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
cv2.putText(img1, "Standard 8-bit RGB Test Field", (w // 2 - 150, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 229, 255), 1)

cv2.imwrite(os.path.join(out_dir, "benchmark.png"), img1)

# 2. Low Contrast Image (for Equalization / Gamma demonstration)
img2 = (img1.astype(np.float32) * 0.25 + 90).astype(np.uint8)
cv2.imwrite(os.path.join(out_dir, "low_contrast.png"), img2)

# 3. Salt & Pepper + Gaussian Noise Image (for Wiener / Median / Gaussian demonstration)
img3 = img1.copy()
# Salt and Pepper noise
num_noise = int(0.04 * h * w)
for _ in range(num_noise):
    y = np.random.randint(0, h)
    x = np.random.randint(0, w)
    img3[y, x] = [255, 255, 255] if np.random.rand() > 0.5 else [0, 0, 0]

# Add mild gaussian noise
gauss = np.random.normal(0, 15, img3.shape)
img3 = np.clip(img3.astype(np.float32) + gauss, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(out_dir, "noisy.png"), img3)

print("Sample benchmark images generated in web/samples/")
