import time
import cv2
import numpy as np
from core.base import ProcessingResult

def _get_structuring_element(shape_name: str, ksize: int) -> np.ndarray:
    shape_map = {
        "rect": cv2.MORPH_RECT,
        "ellipse": cv2.MORPH_ELLIPSE,
        "cross": cv2.MORPH_CROSS
    }
    s = shape_map.get(shape_name.lower(), cv2.MORPH_RECT)
    k = int(ksize)
    if k % 2 == 0:
        k += 1
    return cv2.getStructuringElement(s, (k, k))

def apply_erosion(image: np.ndarray, ksize: int = 5, shape: str = "rect", iterations: int = 1) -> ProcessingResult:
    """التآكل المورفولوجي: A ⊖ B = { z | (B)_z ⊆ A }"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element(shape, ksize)
    res = cv2.erode(image, kernel, iterations=int(iterations))
    formula = "A ⊖ B = { z | (B)_z ⊆ A }"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_{shape.upper()}, ({ksize}, {ksize}))\nresult = cv2.erode(img, kernel, iterations={iterations})"
    return ProcessingResult(res, formula, code, t0)

def apply_dilation(image: np.ndarray, ksize: int = 5, shape: str = "rect", iterations: int = 1) -> ProcessingResult:
    """التمدد المورفولوجي: A ⊕ B = { z | (B̂)_z ∩ A ≠ ∅ }"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element(shape, ksize)
    res = cv2.dilate(image, kernel, iterations=int(iterations))
    formula = "A ⊕ B = { z | (B̂)_z ∩ A ≠ ∅ }"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_{shape.upper()}, ({ksize}, {ksize}))\nresult = cv2.dilate(img, kernel, iterations={iterations})"
    return ProcessingResult(res, formula, code, t0)

def apply_opening(image: np.ndarray, ksize: int = 5, shape: str = "rect") -> ProcessingResult:
    """الفتح المورفولوجي (تآكل ثم تمدد): A ∘ B = (A ⊖ B) ⊕ B"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element(shape, ksize)
    res = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    formula = "A ∘ B = (A ⊖ B) ⊕ B"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_{shape.upper()}, ({ksize}, {ksize}))\nresult = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)"
    return ProcessingResult(res, formula, code, t0)

def apply_closing(image: np.ndarray, ksize: int = 5, shape: str = "rect") -> ProcessingResult:
    """الإغلاق المورفولوجي (تمدد ثم تآكل): A • B = (A ⊕ B) ⊖ B"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element(shape, ksize)
    res = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    formula = "A • B = (A ⊕ B) ⊖ B"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_{shape.upper()}, ({ksize}, {ksize}))\nresult = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)"
    return ProcessingResult(res, formula, code, t0)

def apply_morphological_gradient(image: np.ndarray, ksize: int = 3) -> ProcessingResult:
    """التدرج المورفولوجي: G(A) = (A ⊕ B) - (A ⊖ B)"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element("rect", ksize)
    res = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    formula = "Grad(A) = (A ⊕ B) - (A ⊖ B)"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ({ksize}, {ksize}))\nresult = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)"
    return ProcessingResult(res, formula, code, t0)

def apply_tophat_blackhat(image: np.ndarray, ksize: int = 9, mode: str = "tophat") -> ProcessingResult:
    """قبعة الرأس وقبعة القاع: TopHat = A - (A ∘ B) | BlackHat = (A • B) - A"""
    t0 = time.perf_counter()
    kernel = _get_structuring_element("rect", ksize)
    op = cv2.MORPH_TOPHAT if mode.lower() == "tophat" else cv2.MORPH_BLACKHAT
    res = cv2.morphologyEx(image, op, kernel)
    formula = "TopHat = A - (A ∘ B)" if mode.lower() == "tophat" else "BlackHat = (A • B) - A"
    code = f"kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ({ksize}, {ksize}))\nresult = cv2.morphologyEx(img, cv2.MORPH_{mode.upper()}, kernel)"
    return ProcessingResult(res, formula, code, t0)

def apply_skeleton(image: np.ndarray) -> ProcessingResult:
    """استخراج الهيكل العظمي وتنحيف الخطوط (Morphological Skeletonization)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    skeleton = np.zeros(binary.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    img_copy = binary.copy()
    while True:
        eroded = cv2.erode(img_copy, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img_copy, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        img_copy = eroded.copy()
        if cv2.countNonZero(img_copy) == 0:
            break

    res_bgr = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
    formula = "S(A) = ⋃_k [ (A ⊖ kB) - (A ⊖ kB) ∘ B ]"
    code = "# Iterative Morphological Skeletonization\nelement = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))\n# repeat: eroded = erode(), temp = subtract(), bitwise_or(skel, temp)"
    return ProcessingResult(res_bgr, formula, code, t0)
