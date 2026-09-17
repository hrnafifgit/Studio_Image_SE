import time
import cv2
import numpy as np
from core.base import ProcessingResult

def apply_negative(image: np.ndarray) -> ProcessingResult:
    """التحويل العكسي السالب (Negative Transform): s = (L - 1) - r"""
    t0 = time.perf_counter()
    # استخدام LUT بحجم 256
    lut = np.arange(255, -1, -1, dtype=np.uint8)
    res = cv2.LUT(image, lut)
    formula = "s = (L - 1) - r"
    code = "lut = np.arange(255, -1, -1, dtype=np.uint8)\nresult = cv2.LUT(img, lut)"
    return ProcessingResult(res, formula, code, t0)

def apply_log(image: np.ndarray, c: float = 1.0) -> ProcessingResult:
    """التحويل اللوغاريتمي المسرع بـ LUT: s = c * log(1 + r)"""
    t0 = time.perf_counter()
    # حساب c المعياري بحيث تتمدد القيم إلى [0, 255]
    c_norm = 255.0 / np.log(1.0 + 255.0) * float(c)
    lut = np.array([np.clip(c_norm * np.log(1.0 + r), 0, 255) for r in range(256)], dtype=np.uint8)
    res = cv2.LUT(image, lut)
    formula = "s = c · log(1 + r)"
    code = f"c = {c}\nc_norm = 255.0 / np.log(1.0 + 255.0) * c\nlut = np.array([np.clip(c_norm * np.log(1.0 + r), 0, 255) for r in range(256)], dtype=np.uint8)\nresult = cv2.LUT(img, lut)"
    return ProcessingResult(res, formula, code, t0)

def apply_gamma(image: np.ndarray, gamma: float = 1.0) -> ProcessingResult:
    """تصحيح قانون القوة وجاما المسرع بـ LUT: s = c * r^gamma"""
    t0 = time.perf_counter()
    inv_gamma = float(gamma)
    lut = np.array([np.clip(pow(i / 255.0, inv_gamma) * 255.0, 0, 255) for i in range(256)], dtype=np.uint8)
    res = cv2.LUT(image, lut)
    formula = "s = c · r^γ"
    code = f"gamma = {gamma}\nlut = np.array([np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255) for i in range(256)], dtype=np.uint8)\nresult = cv2.LUT(img, lut)"
    return ProcessingResult(res, formula, code, t0)

def apply_brightness_contrast(image: np.ndarray, brightness: int = 0, contrast: float = 1.0) -> ProcessingResult:
    """تعديل السطوع والتباين: g(x,y) = α * f(x,y) + β"""
    t0 = time.perf_counter()
    alpha = float(contrast)
    beta = int(brightness)
    lut = np.array([np.clip(alpha * i + beta, 0, 255) for i in range(256)], dtype=np.uint8)
    res = cv2.LUT(image, lut)
    formula = "g(x,y) = α · f(x,y) + β"
    code = f"alpha = {alpha}  # Contrast\nbeta = {beta}    # Brightness\nlut = np.array([np.clip(alpha * i + beta, 0, 255) for i in range(256)], dtype=np.uint8)\nresult = cv2.LUT(img, lut)"
    return ProcessingResult(res, formula, code, t0)

def apply_threshold(image: np.ndarray, threshold: int = 128, method: str = "binary") -> ProcessingResult:
    """تطبيق العتبة والتعتيب (Thresholding: Binary, Otsu, Trunc, ToZero)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if method == "otsu":
        _, res = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        formula = "s = 255 if r > T_otsu else 0"
        code = "gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n_, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)"
    elif method == "adaptive":
        res = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        formula = "s = 255 if r > T_local(x,y) else 0"
        code = "gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\nresult = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)"
    else:
        _, res = cv2.threshold(gray, int(threshold), 255, cv2.THRESH_BINARY)
        formula = f"s = 255 if r > {threshold} else 0"
        code = f"gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n_, result = cv2.threshold(gray, {threshold}, 255, cv2.THRESH_BINARY)"
    
    # إعادة إلى 3 قنوات للعرض المتناسق
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_histogram_equalization(image: np.ndarray, method: str = "global", clip_limit: float = 2.0) -> ProcessingResult:
    """تسوية الهيستوغرام الشاملة والموضعية CLAHE: s_k = (L-1) * CDF(r_k)"""
    t0 = time.perf_counter()
    if len(image.shape) == 2:
        if method == "clahe":
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            res = clahe.apply(image)
            formula = "CLAHE: Local CDF Equalization"
            code = f"clahe = cv2.createCLAHE(clipLimit={clip_limit}, tileGridSize=(8,8))\nresult = clahe.apply(gray)"
        else:
            res = cv2.equalizeHist(image)
            formula = "s_k = (L - 1) · ∑ p_r(r_j)"
            code = "result = cv2.equalizeHist(gray)"
        res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    else:
        # تحويل لـ YCrCb أو LAB لتسوية قناة الإضاءة دون تشويه الألوان
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        if method == "clahe":
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            ycrcb[:, :, 0] = clahe.apply(ycrcb[:, :, 0])
            formula = "CLAHE on Luminance Y Channel: Local CDF"
            code = f"ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)\nclahe = cv2.createCLAHE(clipLimit={clip_limit})\nycrcb[:,:,0] = clahe.apply(ycrcb[:,:,0])\nresult = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)"
        else:
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            formula = "s_k = (L - 1) · ∑ p_r(r_j) on Y Channel"
            code = "ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)\nycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0])\nresult = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)"
        res_bgr = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        
    return ProcessingResult(res_bgr, formula, code, t0)
