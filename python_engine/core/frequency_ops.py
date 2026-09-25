import time
import cv2
import numpy as np
from core.base import ProcessingResult

def get_fft_spectrum(image: np.ndarray) -> ProcessingResult:
    """تحويل فورييه السريع وعرض طيف الترددات اللوغاريتمي: D(u,v) = c * log(1 + |F(u,v)|)"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2D Fast Fourier Transform
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    
    # Magnitude Spectrum with Log scaling
    magnitude_spectrum = 20 * np.log(np.abs(dft_shift) + 1.0)
    norm_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
    res = np.uint8(norm_spectrum)
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    
    formula = "F(u,v) = ∬ f(x,y) · e^{-j2π(ux+vy)} dx dy\nD(u,v) = c · log(1 + |F(u,v)|)"
    code = "# 2D-FFT Magnitude Spectrum\ndft = np.fft.fft2(gray)\ndft_shift = np.fft.fftshift(dft)\nspectrum = 20 * np.log(np.abs(dft_shift) + 1.0)\nresult = cv2.normalize(spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_frequency_filter(image: np.ndarray, filter_type: str = "lowpass", cutoff: float = 30.0, filter_model: str = "gaussian", order: int = 2) -> ProcessingResult:
    """تطبيق المرشحات في مجال التردد: G(u,v) = H(u,v) * F(u,v) ثم التحويل العكسي IFFT"""
    t0 = time.perf_counter()
    gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, cols = gray.shape
    crow, ccol = rows // 2, cols // 2
    
    # 2D-FFT
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    
    # شبكة المسافات من المركز D(u,v)
    u = np.arange(rows)
    v = np.arange(cols)
    U, V = np.meshgrid(u, v, indexing='ij')
    D = np.sqrt((U - crow)**2 + (V - ccol)**2)
    D0 = max(1.0, float(cutoff))
    
    # حساب قناع الترشيح H(u,v)
    if filter_model.lower() == "ideal":
        H = np.zeros((rows, cols), dtype=np.float32)
        H[D <= D0] = 1.0
    elif filter_model.lower() == "butterworth":
        n = int(order)
        H = 1.0 / (1.0 + (D / D0)**(2 * n))
    else: # Gaussian
        H = np.exp(-(D**2) / (2 * (D0**2)))
        
    if filter_type.lower() == "highpass":
        H = 1.0 - H
        
    # الترشيح: ضرب المصفوفات في مجال التردد
    filtered_shift = dft_shift * H
    
    # التحويل العكسي Inverse FFT
    f_ishift = np.fft.ifftshift(filtered_shift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    res = np.clip(img_back, 0, 255).astype(np.uint8)
    res_bgr = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    
    formula = f"G(u,v) = H(u,v) · F(u,v) | {filter_model.capitalize()} {filter_type.capitalize()} (D0={D0})"
    code = f"# Frequency Domain Filtering ({filter_model} {filter_type})\ndft = np.fft.fftshift(np.fft.fft2(gray))\nfiltered = dft * H\nresult = np.abs(np.fft.ifft2(np.fft.ifftshift(filtered))).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

def apply_notch_filter(image: np.ndarray, notches: list = None, d0: float = 18.0) -> ProcessingResult:
    """
    مرشح الرفض النقطي في مجال التردد (2D-FFT Notch Reject Filter):
    لإزالة التشويش النمطي والخطوط المتكررة (Periodic Noise & Moiré Patterns)
    H_NR(u,v) = ∏ [1 - exp(-0.5 · (D_k · D_{-k} / D0²))]
    """
    t0 = time.perf_counter()
    rows, cols = image.shape[:2]
    crow, ccol = rows // 2, cols // 2
    d0 = max(2.0, float(d0))
    
    # شبكة الإحداثيات
    u = np.arange(rows)
    v = np.arange(cols)
    U, V = np.meshgrid(u, v, indexing='ij')
    
    # افتراضياً، إذا لم تُحدد نقاط نستخدم نقاط تداخل دوري شائعة
    if not notches:
        notches = [{"u": crow - 35, "v": ccol + 45}]
        
    H = np.ones((rows, cols), dtype=np.float32)
    
    for notch in notches:
        if isinstance(notch, dict):
            uk = float(notch.get("u", crow - 30))
            vk = float(notch.get("v", ccol + 30))
        elif isinstance(notch, (list, tuple)) and len(notch) >= 2:
            uk, vk = float(notch[0]), float(notch[1])
        else:
            continue
            
        # المسافة للنقطة المتناظرة طردياً وعكسياً حول المركز (Symmetric Conjugate)
        D1 = np.sqrt((U - uk)**2 + (V - vk)**2)
        u_sym = 2 * crow - uk
        v_sym = 2 * ccol - vk
        D2 = np.sqrt((U - u_sym)**2 + (V - v_sym)**2)
        
        # دالة الرفض الغاوسية المزدوجة
        H_k = (1.0 - np.exp(-0.5 * (D1**2) / (d0**2))) * (1.0 - np.exp(-0.5 * (D2**2) / (d0**2)))
        H *= H_k
        
    # تطبيق المرشح على القنوات اللونية
    channels = cv2.split(image)
    filtered_channels = []
    for ch in channels:
        dft = np.fft.fft2(ch.astype(np.float32))
        dft_shift = np.fft.fftshift(dft)
        filtered_shift = dft_shift * H
        f_ishift = np.fft.ifftshift(filtered_shift)
        img_back = np.real(np.fft.ifft2(f_ishift))
        filtered_channels.append(np.clip(img_back, 0, 255).astype(np.uint8))
        
    res_bgr = cv2.merge(filtered_channels)
    
    notch_count = len(notches)
    formula = f"Notch Reject: H(u,v) = ∏ [1 - e^{{-D_k²/(2D₀²)}}] · [1 - e^{{-D_{{-k}}²/(2D₀²)}}] | ({notch_count} Notches, D₀={d0}px)"
    code = f"# 2D-FFT Notch Reject Filter ({notch_count} frequency pairs)\ndft = np.fft.fftshift(np.fft.fft2(channel))\nfiltered = dft * H_notch\nresult = np.real(np.fft.ifft2(np.fft.ifftshift(filtered))).astype(np.uint8)"
    return ProcessingResult(res_bgr, formula, code, t0)

