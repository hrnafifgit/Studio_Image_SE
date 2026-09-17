import time
import cv2
import numpy as np
from core.base import ProcessingResult

def apply_sobel(image: np.ndarray, ksize: int = 3) -> ProcessingResult:
    """كاشف سوبل للانحدار المشتق الأول: |∇f| = √(Gx² + Gy²)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=k)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=k)
    mag = np.sqrt(grad_x**2 + grad_y**2)
    res = np.clip(mag, 0, 255).astype(np.uint8)
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    formula = "|∇f| = √(G_x² + G_y²)\nθ = arctan(G_y / G_x)"
    code = f"gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\ngx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize={k})\ngy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize={k})\nmag = np.sqrt(gx**2 + gy**2)\nresult = np.clip(mag, 0, 255).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_prewitt(image: np.ndarray) -> ProcessingResult:
    """كاشف بريويت للحواف (Prewitt Operator)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    gx = cv2.filter2D(gray, cv2.CV_32F, kernelx)
    gy = cv2.filter2D(gray, cv2.CV_32F, kernely)
    mag = np.sqrt(gx**2 + gy**2)
    res = np.clip(mag, 0, 255).astype(np.uint8)
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    formula = "Prewitt: G_x = [-1 0 1]^T * [1 1 1], G_y = [1 1 1]^T * [-1 0 1]"
    code = "kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])\nkernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])\ngx = cv2.filter2D(gray, -1, kernelx)\ngy = cv2.filter2D(gray, -1, kernely)\nresult = np.clip(np.sqrt(gx**2 + gy**2), 0, 255).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_laplacian(image: np.ndarray, ksize: int = 3) -> ProcessingResult:
    """كاشف لابلاسيان للمشتقة المكانية الثانية: ∇²f = ∂²f/∂x² + ∂²f/∂y²"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=k)
    res = np.clip(np.abs(lap), 0, 255).astype(np.uint8)
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    formula = "∇²f = (∂²f / ∂x²) + (∂²f / ∂y²)"
    code = f"gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\nlap = cv2.Laplacian(gray, cv2.CV_64F, ksize={k})\nresult = np.clip(np.abs(lap), 0, 255).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_canny(image: np.ndarray, t1: int = 50, t2: int = 150, sigma: float = 1.4) -> ProcessingResult:
    """خوارزمية كاني متعددة المراحل (التنعيم، التدرج، قمع غير النهايات العظمى NMS، العتبة المزدوجة)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # تنعيم جاوس
    blurred = cv2.GaussianBlur(gray, (5, 5), float(sigma))
    # كشف كاني
    edges = cv2.Canny(blurred, int(t1), int(t2))
    res_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    formula = "Canny: 1. Gauss Blur → 2. |∇f| & θ → 3. NMS → 4. Hysteresis(T1, T2)"
    code = f"# Multi-stage Optimal Canny Detector\nblurred = cv2.GaussianBlur(gray, (5, 5), {sigma})\nedges = cv2.Canny(blurred, {t1}, {t2})"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_unsharp_mask(image: np.ndarray, sigma: float = 1.5, strength: float = 1.5) -> ProcessingResult:
    """قناع عدم الوضوح والتعزيز العالي (Unsharp Masking & High-Boost): g = f + k * (f - f_blur)"""
    t0 = time.perf_counter()
    blurred = cv2.GaussianBlur(image, (0, 0), float(sigma))
    mask = cv2.subtract(image, blurred)
    res = cv2.addWeighted(image, 1.0, mask, float(strength), 0)
    formula = "g(x,y) = f(x,y) + k · [ f(x,y) - f_smooth(x,y) ]"
    code = f"blurred = cv2.GaussianBlur(img, (0, 0), {sigma})\nmask = cv2.subtract(img, blurred)\nresult = cv2.addWeighted(img, 1.0, mask, {strength}, 0)"
    return ProcessingResult(res, formula, code, t0)
