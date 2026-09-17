import time
import cv2
import numpy as np
from scipy.signal import wiener
from core.base import ProcessingResult

def apply_gaussian_blur(image: np.ndarray, ksize: int = 5, sigma: float = 1.4) -> ProcessingResult:
    """مرشح جاوس التنعيمي القابل للفصل O(2K): G(x,y) = G(x) * G(y)"""
    t0 = time.perf_counter()
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    sig = float(sigma)
    res = cv2.GaussianBlur(image, (k, k), sig)
    formula = "G(x,y) = [ 1 / (2πσ²) ] · e^{-(x²+y²)/(2σ²)}"
    code = f"# Separable 1D Gaussian Convolution O(2K)\nresult = cv2.GaussianBlur(img, ({k}, {k}), {sig})"
    return ProcessingResult(res, formula, code, t0)

def apply_box_blur(image: np.ndarray, ksize: int = 5) -> ProcessingResult:
    """مرشح الصندوق والمتوسط الحسابي: g(x,y) = (1/K²) * ∑ f(x+s, y+t)"""
    t0 = time.perf_counter()
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    res = cv2.blur(image, (k, k))
    formula = "g(x,y) = (1 / K²) · ∑ ∑ f(x-s, y-t)"
    code = f"# Box/Mean Filtering\nresult = cv2.blur(img, ({k}, {k}))"
    return ProcessingResult(res, formula, code, t0)

def apply_median_filter(image: np.ndarray, ksize: int = 5) -> ProcessingResult:
    """مرشح الوسيط لإزالة الضوضاء النبضية (Salt & Pepper): g(x,y) = median{f(s,t)}"""
    t0 = time.perf_counter()
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    res = cv2.medianBlur(image, k)
    formula = "g(x,y) = median { f(s, t) | (s,t) ∈ W }"
    code = f"# Non-linear Median Filter\nresult = cv2.medianBlur(img, {k})"
    return ProcessingResult(res, formula, code, t0)

def apply_wiener_filter(image: np.ndarray, ksize: int = 5) -> ProcessingResult:
    """مرشح وينر التكيفي الأمثل لتقليل متوسط مربع الخطأ (Minimum Mean Square Error)"""
    t0 = time.perf_counter()
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    
    if len(image.shape) == 2:
        gray = image.astype(np.float64)
        filtered = wiener(gray, (k, k))
        res = np.clip(filtered, 0, 255).astype(np.uint8)
        res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    else:
        # تطبيق وينر على كل قناة لونية
        channels = cv2.split(image.astype(np.float64))
        filtered_channels = [np.clip(wiener(ch, (k, k)), 0, 255).astype(np.uint8) for ch in channels]
        res_bgr = cv2.merge(filtered_channels)

    formula = "H(u,v) = H*(u,v) / [ |H(u,v)|² + S_η(u,v) / S_f(u,v) ]"
    code = f"from scipy.signal import wiener\n# Adaptive MMSE Wiener Filter\nresult = wiener(img, ({k}, {k}))"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_bilateral_filter(image: np.ndarray, d: int = 9, sigma_color: float = 75.0, sigma_space: float = 75.0) -> ProcessingResult:
    """المرشح الثنائي (Bilateral Filter) لحفظ الحواف أثناء التنعيم"""
    t0 = time.perf_counter()
    res = cv2.bilateralFilter(image, int(d), float(sigma_color), float(sigma_space))
    formula = "BF[I]_p = (1/W_p) ∑_q G_σs(||p-q||) · G_σr(|I_p - I_q|) · I_q"
    code = f"# Edge-Preserving Bilateral Smoothing\nresult = cv2.bilateralFilter(img, {d}, {sigma_color}, {sigma_space})"
    return ProcessingResult(res, formula, code, t0)

def apply_custom_kernel(image: np.ndarray, kernel_matrix: list) -> ProcessingResult:
    """تطبيق مصفوفة التواء مخصصة (Custom 2D Convolution Kernel)"""
    t0 = time.perf_counter()
    k = np.array(kernel_matrix, dtype=np.float32)
    res = cv2.filter2D(image, -1, k)
    formula = "g(x,y) = f(x,y) * K = ∑ ∑ K(s,t) · f(x-s, y-t)"
    code = f"kernel = np.array({kernel_matrix}, dtype=np.float32)\nresult = cv2.filter2D(img, -1, kernel)"
    return ProcessingResult(res, formula, code, t0)
