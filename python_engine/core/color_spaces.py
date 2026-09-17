import time
import cv2
import numpy as np
from core.base import ProcessingResult

def convert_color_space(image: np.ndarray, target: str = "gray") -> ProcessingResult:
    """التحويل بين فضاءات الألوان: RGB, Grayscale, HSV, LAB, YCrCb"""
    t0 = time.perf_counter()
    target = target.lower()
    
    if target == "gray":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        res = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        formula = "Y = 0.299·R + 0.587·G + 0.114·B"
        code = "result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)"
    elif target == "hsv":
        res = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        formula = "HSV: Hue (0-179°), Saturation (0-255), Value (0-255)"
        code = "result = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)"
    elif target == "lab":
        res = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        formula = "CIE L*a*b*: L*(Lightness), a*(Green-Red), b*(Blue-Yellow)"
        code = "result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)"
    elif target == "ycrcb":
        res = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        formula = "YCrCb: Y(Luminance), Cr(Red Chrominance), Cb(Blue Chrominance)"
        code = "result = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)"
    else:
        res = image.copy()
        formula = "RGB / BGR Color Model"
        code = "# Unchanged BGR"

    return ProcessingResult(res, formula, code, t0)

def isolate_channel(image: np.ndarray, channel: str = "r") -> ProcessingResult:
    """عزل قناة لونية واحدة: Red, Green, Blue"""
    t0 = time.perf_counter()
    b, g, r = cv2.split(image)
    zeros = np.zeros_like(b)
    
    ch = channel.lower()
    if ch in ["r", "red"]:
        res = cv2.merge([zeros, zeros, r])
        formula = "Isolate Red: [0, 0, R]"
        code = "b, g, r = cv2.split(img)\nzeros = np.zeros_like(b)\nresult = cv2.merge([zeros, zeros, r])"
    elif ch in ["g", "green"]:
        res = cv2.merge([zeros, g, zeros])
        formula = "Isolate Green: [0, G, 0]"
        code = "b, g, r = cv2.split(img)\nzeros = np.zeros_like(b)\nresult = cv2.merge([zeros, g, zeros])"
    elif ch in ["b", "blue"]:
        res = cv2.merge([b, zeros, zeros])
        formula = "Isolate Blue: [B, 0, 0]"
        code = "b, g, r = cv2.split(img)\nzeros = np.zeros_like(b)\nresult = cv2.merge([b, zeros, zeros])"
    else:
        res = image.copy()
        formula = "RGB Full Spectrum"
        code = "result = img"

    return ProcessingResult(res, formula, code, t0)

def apply_kmeans_segmentation(image: np.ndarray, k: int = 4) -> ProcessingResult:
    """التكميم اللوني وتقطيع الصورة عبر خوارزمية K-Means Clustering"""
    t0 = time.perf_counter()
    k_clusters = max(2, min(16, int(k)))
    
    # تحويل الصورة إلى متجه ثنائي الأبعاد
    pixel_vals = image.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    _, labels, centers = cv2.kmeans(pixel_vals, k_clusters, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    res = segmented_data.reshape(image.shape)
    
    formula = f"K-Means Clustering (K={k_clusters}): argmin_S ∑ ∑ ||x - μ_i||²"
    code = f"# K-Means Color Quantization\npixels = img.reshape((-1, 3)).astype(np.float32)\ncriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)\n_, labels, centers = cv2.kmeans(pixels, {k_clusters}, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)\nresult = np.uint8(centers)[labels.flatten()].reshape(img.shape)"
    return ProcessingResult(res, formula, code, t0)

def apply_color_splash(image: np.ndarray, target_bgr: list = None, tolerance: float = 24.0) -> ProcessingResult:
    """
    عزل الألوان الذكي (Color Splash / Selective Color Slicing):
    تحويل الصورة بالكامل إلى أبيض وأسود عالي التباين مع إبقاء اللون المختار فقط بتدرجاته الطبيعية
    """
    t0 = time.perf_counter()
    if target_bgr is None or len(target_bgr) < 3:
        target_bgr = [0, 0, 220] # أحمر افتراضي
        
    target_pixel = np.uint8([[target_bgr]])
    target_hsv = cv2.cvtColor(target_pixel, cv2.COLOR_BGR2HSV)[0, 0]
    target_hue = int(target_hsv[0])
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_channel = hsv[:, :, 0].astype(np.int16)
    s_channel = hsv[:, :, 1]
    
    # حساب المسافة الدائرية على حلقة اللون (Circular Hue Distance 0-180)
    diff = np.abs(h_channel - target_hue)
    circular_diff = np.minimum(diff, 180 - diff)
    
    # القناع: فرق اللون أقل من التسامح، وتشبع لوني ملحوظ
    tol = int(max(5, min(80, tolerance)))
    mask = ((circular_diff <= tol) & (s_channel >= 35)).astype(np.uint8) * 255
    
    # تنعيم حواف القناع لمنع التسنن
    mask = cv2.GaussianBlur(mask, (5, 5), 1.0)
    mask_3d = np.repeat(mask[:, :, np.newaxis] / 255.0, 3, axis=2)
    
    # الصورة الرمادية الأساسية
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    # الدمج الموزون
    res = (image.astype(np.float32) * mask_3d + gray_bgr.astype(np.float32) * (1.0 - mask_3d)).astype(np.uint8)
    
    hex_color = "#{:02x}{:02x}{:02x}".format(int(target_bgr[2]), int(target_bgr[1]), int(target_bgr[0]))
    formula = f"HSV Slicing: Keep Color if |H - H₀| ≤ ΔH ({tol}°) & S ≥ 35 | Target: {hex_color}"
    code = f"# Selective Color Slicing (Color Splash)\nhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)\nmask = (np.abs(hsv[:,:,0] - {target_hue}) <= {tol}) & (hsv[:,:,1] >= 35)\ngray = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)\nresult = np.where(mask[:,:,None], img, gray)"
    return ProcessingResult(res, formula, code, t0)

def extract_color_palette(image: np.ndarray, k: int = 6) -> list:
    """استخراج أهم الألوان المهيمنة في الصورة عبر K-Means Clustering مع أكواد الـ HEX"""
    k = max(3, min(12, int(k)))
    # تصغير الصورة لتسريع التجميع اللوني الفوري
    small = cv2.resize(image, (120, 120), interpolation=cv2.INTER_AREA)
    pixels = small.reshape((-1, 3)).astype(np.float32)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    
    centers = np.uint8(centers)
    counts = np.bincount(labels.flatten())
    total = len(labels.flatten())
    
    palette = []
    # فرز الألوان من الأكثر انتشاراً إلى الأقل
    indices = np.argsort(-counts)
    for idx in indices:
        b, g, r = int(centers[idx][0]), int(centers[idx][1]), int(centers[idx][2])
        hex_code = "#{:02X}{:02X}{:02X}".format(r, g, b)
        percent = round(float(counts[idx]) / total * 100, 1)
        palette.append({
            "hex": hex_code,
            "rgb": [r, g, b],
            "bgr": [b, g, r],
            "percent": percent
        })
    return palette

