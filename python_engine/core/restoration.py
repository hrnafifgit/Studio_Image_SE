import time
import cv2
import numpy as np
from core.base import ProcessingResult

def _make_motion_psf(rows: int, cols: int, length: int = 15, angle: float = 45.0) -> np.ndarray:
    """توليد مصفوفة دالة التشتت النقطي للاهتزاز الحركي (Point Spread Function - PSF)"""
    psf = np.zeros((rows, cols), dtype=np.float32)
    crow, ccol = rows // 2, cols // 2
    
    rad = np.deg2rad(angle)
    dx = np.cos(rad)
    dy = np.sin(rad)
    
    half_len = length / 2.0
    steps = int(max(length * 2, 10))
    for t in np.linspace(-half_len, half_len, steps):
        r = int(round(crow + t * dy))
        c = int(round(ccol + t * dx))
        if 0 <= r < rows and 0 <= c < cols:
            psf[r, c] += 1.0
            
    total = np.sum(psf)
    if total > 0:
        psf /= total
    else:
        psf[crow, ccol] = 1.0
    return psf

def apply_motion_deblur(image: np.ndarray, length: int = 15, angle: float = 45.0, snr: float = 0.01) -> ProcessingResult:
    """
    استعادة حدة الصور المشوهة بالاهتزاز الحركي عبر ترشيح وينر العكسي:
    G(u,v) = [H*(u,v) / (|H(u,v)|² + K)] · F(u,v)
    """
    t0 = time.perf_counter()
    rows, cols = image.shape[:2]
    
    length = max(1, min(100, int(length)))
    angle = float(angle)
    k_snr = max(1e-5, min(1.0, float(snr)))
    
    # 1. إنشاء PSF متمركزة وتحويلها إلى أصل الترددات (0,0)
    psf = _make_motion_psf(rows, cols, length, angle)
    psf_shifted = np.fft.ifftshift(psf)
    
    # 2. تحويل فورييه للـ PSF
    H = np.fft.fft2(psf_shifted)
    H_conj = np.conj(H)
    H_mag_sq = np.abs(H) ** 2
    
    # 3. مرشح وينر الترددي (Wiener Deconvolution Filter)
    W = H_conj / (H_mag_sq + k_snr)
    
    # 4. التطبيق على القنوات اللونية
    channels = cv2.split(image)
    deblurred_channels = []
    
    for ch in channels:
        F = np.fft.fft2(ch.astype(np.float32))
        res_freq = F * W
        restored = np.real(np.fft.ifft2(res_freq))
        restored = np.clip(restored, 0, 255).astype(np.uint8)
        deblurred_channels.append(restored)
        
    res_bgr = cv2.merge(deblurred_channels)
    
    formula = f"Wiener Deconvolution: W(u,v) = H*(u,v) / [|H(u,v)|² + K] | (L={length}px, θ={angle}°, K={k_snr})"
    code = f"# Motion Deblur with Wiener Filter\npsf = make_motion_psf(img.shape, length={length}, angle={angle})\nH = np.fft.fft2(np.fft.ifftshift(psf))\nW = np.conj(H) / (np.abs(H)**2 + {k_snr})\nrestored = np.real(np.fft.ifft2(np.fft.fft2(channel) * W))"
    
    return ProcessingResult(res_bgr, formula, code, t0)
