import time
import cv2
import numpy as np
from core.base import ProcessingResult

def apply_rotation(image: np.ndarray, angle: float = 45.0, scale: float = 1.0) -> ProcessingResult:
    """تدوير الصورة مع تغيير المقياس (Affine Rotation)"""
    t0 = time.perf_counter()
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, float(angle), float(scale))
    res = cv2.warpAffine(image, m, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    formula = "x' = x·cos(θ) - y·sin(θ) + tx\ny' = x·sin(θ) + y·cos(θ) + ty"
    code = f"# 2D Affine Rotation\ncenter = (w // 2, h // 2)\nM = cv2.getRotationMatrix2D(center, {angle}, {scale})\nresult = cv2.warpAffine(img, M, (w, h))"
    return ProcessingResult(res, formula, code, t0)

def apply_resize(image: np.ndarray, scale_factor: float = 0.5, interpolation: str = "bicubic") -> ProcessingResult:
    """تغيير حجم الصورة بالاستيفاء الرياضي (Nearest, Bilinear, Bicubic, Lanczos)"""
    t0 = time.perf_counter()
    interp_map = {
        "nearest": cv2.INTER_NEAREST,
        "bilinear": cv2.INTER_LINEAR,
        "bicubic": cv2.INTER_CUBIC,
        "lanczos": cv2.INTER_LANCZOS4
    }
    flag = interp_map.get(interpolation.lower(), cv2.INTER_CUBIC)
    h, w = image.shape[:2]
    sf = float(scale_factor)
    new_w, new_h = max(10, int(w * sf)), max(10, int(h * sf))
    res = cv2.resize(image, (new_w, new_h), interpolation=flag)
    formula = f"f(x, y) Interpolation Mode: {interpolation.capitalize()}"
    code = f"# Interpolated Resizing\nresult = cv2.resize(img, ({new_w}, {new_h}), interpolation=cv2.INTER_{interpolation.upper()})"
    return ProcessingResult(res, formula, code, t0)

def apply_flip(image: np.ndarray, mode: str = "horizontal") -> ProcessingResult:
    """انعكاس الصورة (Flip): أفقي أو رأسي"""
    t0 = time.perf_counter()
    code_val = 1 if mode.lower() == "horizontal" else 0
    res = cv2.flip(image, code_val)
    formula = "x' = -x + W (Horizontal) | y' = -y + H (Vertical)"
    code = f"result = cv2.flip(img, {code_val})"
    return ProcessingResult(res, formula, code, t0)

def apply_crop(image: np.ndarray, x: int = 0, y: int = 0, width: int = 100, height: int = 100) -> ProcessingResult:
    """قص الصورة (Image Cropping / ROI Slicing)"""
    t0 = time.perf_counter()
    h, w = image.shape[:2]
    
    x = max(0, min(int(x), w - 1))
    y = max(0, min(int(y), h - 1))
    width = max(10, min(int(width), w - x))
    height = max(10, min(int(height), h - y))
    
    cropped = image[y:y+height, x:x+width].copy()
    formula = f"ROI = I[y:{y+height}, x:{x+width}] (Dimensions: {width}×{height} px)"
    code = f"# Sub-matrix Cropping\ncropped = img[{y}:{y+height}, {x}:{x+width}]"
    return ProcessingResult(cropped, formula, code, t0)
