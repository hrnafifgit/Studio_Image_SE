import time
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from core.base import ProcessingResult

def remove_background(image: np.ndarray, margin: int = 15, iterations: int = 5, sigma: float = 1.2) -> ProcessingResult:
    """
    عزل وقص الخلفية عبر خوارزمية GrabCut المتقدمة:
    تحديد العنصر الأساسي وتفريغ الخلفية لتصبح شفافة (BGRA) مع موازنة الهامش والتكرار والتنعيم
    """
    t0 = time.perf_counter()
    rows, cols = image.shape[:2]
    
    margin = max(3, min(min(rows, cols) // 4, int(margin)))
    rect = (margin, margin, cols - 2 * margin, rows - 2 * margin)
    
    mask = np.zeros((rows, cols), np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    iter_count = max(1, min(10, int(iterations)))
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, iter_count, cv2.GC_INIT_WITH_RECT)
    
    # 0 and 2 are background, 1 and 3 are foreground
    fg_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    
    # تنعيم الحواف (Feathering & Anti-aliasing)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    
    sig = max(0.1, float(sigma))
    k_val = max(3, int(round(sig * 4)) | 1)
    fg_mask = cv2.GaussianBlur(fg_mask, (k_val, k_val), sig)
    
    # دمج القناة الشفافة Alpha
    bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = fg_mask
    
    formula = f"GrabCut Energy Minimization: Iter={iter_count}, Margin={margin}px, σ={sig} | Foreground Segmentation"
    code = f"# Interactive Background Removal with GrabCut\nrect = ({margin}, {margin}, cols-{margin*2}, rows-{margin*2})\ncv2.grabCut(img, mask, rect, bgd, fgd, {iter_count}, cv2.GC_INIT_WITH_RECT)\nalpha = cv2.GaussianBlur(mask, ({k_val}, {k_val}), {sig})\nresult_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)\nresult_bgra[:, :, 3] = alpha"
    
    return ProcessingResult(bgra, formula, code, t0)

def replace_background(image: np.ndarray, bg_type: str = "color", bg_color: list = None, bg_image: np.ndarray = None) -> ProcessingResult:
    """
    تغيير واستبدال الخلفية:
    دمج العنصر المعزول مع خلفية بلون موحد، تدرج لوني، أو صورة خلفية جديدة
    """
    t0 = time.perf_counter()
    rows, cols = image.shape[:2]
    
    # استخراج القناع والـ BGR
    if image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3].astype(np.float32) / 255.0
    else:
        # إذا لم تكن مقصوصة مسبقاً نعزلها أولاً
        res_cut = remove_background(image)
        bgr = res_cut.image[:, :, :3]
        alpha = res_cut.image[:, :, 3].astype(np.float32) / 255.0
        
    alpha_3d = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)
    
    # 1. إنشاء الخلفية الجديدة
    if bg_type == "image" and bg_image is not None:
        bg_canvas = cv2.resize(bg_image[:, :, :3], (cols, rows), interpolation=cv2.INTER_AREA)
        bg_desc = "Scenic Custom Image Background"
    elif bg_type == "gradient":
        # تدرج لوني استوديو سينمائي
        bg_canvas = np.zeros((rows, cols, 3), dtype=np.uint8)
        c1 = np.array([24, 20, 15], dtype=np.float32)   # أزرق داكن في الأسفل
        c2 = np.array([120, 70, 30], dtype=np.float32)  # سماوي ناعم في الأعلى
        for y in range(rows):
            t = y / max(1, rows - 1)
            bg_canvas[y, :] = (c2 * (1.0 - t) + c1 * t).astype(np.uint8)
        bg_desc = "Studio Gradient (Deep Blue to Teal)"
    else: # Solid color
        if bg_color is None or len(bg_color) < 3:
            bg_color = [255, 255, 255] # White BGR
        bg_canvas = np.full((rows, cols, 3), bg_color[:3], dtype=np.uint8)
        bg_desc = f"Solid Studio Color: BGR{bg_color}"
        
    # 2. الدمج التراكمي: C = F * α + B * (1 - α)
    composite = (bgr.astype(np.float32) * alpha_3d + bg_canvas.astype(np.float32) * (1.0 - alpha_3d)).astype(np.uint8)
    
    formula = f"Alpha Compositing: C(x,y) = F(x,y)·α + B(x,y)·(1 - α) | {bg_desc}"
    code = f"# Alpha Matting Background Replacement\nalpha = mask[:,:,None] / 255.0\nresult = (foreground * alpha + background * (1.0 - alpha)).astype(np.uint8)"
    
    return ProcessingResult(composite, formula, code, t0)

def render_text_overlay(image: np.ndarray, text: str, x: int = 50, y: int = 50, font_size: int = 36, color_bgr: list = None, font_family: str = "tahoma") -> ProcessingResult:
    """
    الكتابة على الصور بخطوط TrueType واضحة مع دعم العربية والإنجليزية والظل
    """
    t0 = time.perf_counter()
    if color_bgr is None or len(color_bgr) < 3:
        color_bgr = [255, 255, 255]
        
    # تحويل الصورة إلى PIL Image للتعامل مع النصوص والخطوط
    is_bgra = (image.shape[2] == 4)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA if is_bgra else cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)
    
    # اختيار مسار الخط
    font_size = max(10, min(200, int(font_size)))
    font_paths = {
        "tahoma": r"C:\Windows\Fonts\tahoma.ttf",
        "arial": r"C:\Windows\Fonts\arial.ttf",
        "segoe": r"C:\Windows\Fonts\seguihis.ttf",
        "impact": r"C:\Windows\Fonts\impact.ttf"
    }
    font_file = font_paths.get(font_family.lower(), font_paths["tahoma"])
    if not os.path.exists(font_file):
        font_file = font_paths["arial"]
        
    try:
        font = ImageFont.truetype(font_file, font_size)
    except Exception:
        font = ImageFont.load_default()
        
    # رسم الظل (Drop Shadow)
    shadow_color = (15, 15, 15, 180) if is_bgra else (15, 15, 15)
    text_color = (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]), 255) if is_bgra else (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0]))
    
    pos = (int(x), int(y))
    draw.text((pos[0] + 2, pos[1] + 2), text, font=font, fill=shadow_color)
    draw.text(pos, text, font=font, fill=text_color)
    
    # إعادة التحويل لمصفوفة NumPy
    arr_out = np.array(pil_img)
    res = cv2.cvtColor(arr_out, cv2.COLOR_RGBA2BGRA if is_bgra else cv2.COLOR_RGB2BGR)
    
    formula = f"Raster Typography: Text='{text}' | Font={font_family} ({font_size}px) @ ({x}, {y})"
    code = f"# PIL Text Rasterization\nfont = ImageFont.truetype('{font_file}', {font_size})\ndraw.text(({x}, {y}), '{text}', font=font, fill={text_color})"
    
    return ProcessingResult(res, formula, code, t0)

def composite_overlay_image(base_image: np.ndarray, overlay_image: np.ndarray, x: int = 50, y: int = 50, scale: float = 1.0, opacity: float = 1.0) -> ProcessingResult:
    """
    إضافة صورة على صورة (Picture-in-Picture / Watermark / Dual Layer Overlay)
    مع إمكانية التحكم بالموضع والحجم والشفافية
    """
    t0 = time.perf_counter()
    rows, cols = base_image.shape[:2]
    is_base_bgra = (base_image.shape[2] == 4)
    
    base = base_image.copy()
    if not is_base_bgra:
        base = cv2.cvtColor(base, cv2.COLOR_BGR2BGRA)
        
    # تغيير حجم الصورة المراد إضافتها
    scale = max(0.05, min(5.0, float(scale)))
    ow = max(1, int(round(overlay_image.shape[1] * scale)))
    oh = max(1, int(round(overlay_image.shape[0] * scale)))
    overlay_resized = cv2.resize(overlay_image, (ow, oh), interpolation=cv2.INTER_AREA)
    
    if overlay_resized.shape[2] == 3:
        overlay_resized = cv2.cvtColor(overlay_resized, cv2.COLOR_BGR2BGRA)
        
    opacity = max(0.0, min(1.0, float(opacity)))
    
    # حساب حدود التقاطع (Bounding Box Intersection)
    x = int(x)
    y = int(y)
    
    x1_base = max(0, x)
    y1_base = max(0, y)
    x2_base = min(cols, x + ow)
    y2_base = min(rows, y + oh)
    
    x1_over = max(0, -x)
    y1_over = max(0, -y)
    x2_over = x1_over + (x2_base - x1_base)
    y2_over = y1_over + (y2_base - y1_base)
    
    if x2_base > x1_base and y2_base > y1_base:
        over_crop = overlay_resized[y1_over:y2_over, x1_over:x2_over]
        base_crop = base[y1_base:y2_base, x1_base:x2_base]
        
        alpha_over = (over_crop[:, :, 3].astype(np.float32) / 255.0) * opacity
        alpha_base = base_crop[:, :, 3].astype(np.float32) / 255.0
        
        # Porter-Duff 'Source Over' compositing
        alpha_out = alpha_over + alpha_base * (1.0 - alpha_over)
        safe_alpha_out = np.where(alpha_out > 0, alpha_out, 1.0)
        
        for c in range(3):
            base_crop[:, :, c] = np.clip(
                (over_crop[:, :, c].astype(np.float32) * alpha_over +
                 base_crop[:, :, c].astype(np.float32) * alpha_base * (1.0 - alpha_over)) / safe_alpha_out,
                0, 255
            ).astype(np.uint8)
            
        base_crop[:, :, 3] = np.clip(alpha_out * 255.0, 0, 255).astype(np.uint8)
        base[y1_base:y2_base, x1_base:x2_base] = base_crop
        
    out = base if is_base_bgra else cv2.cvtColor(base, cv2.COLOR_BGRA2BGR)
    formula = f"Porter-Duff Compositing: α_out = α_A + α_B(1-α_A) | Scale={scale:.2f}x, Opacity={opacity*100:.0f}%"
    code = f"# Picture-in-Picture Image Overlay\noverlay = cv2.resize(watermark, (int(w*{scale}), int(h*{scale})))\nroi = base[{y}:{y+oh}, {x}:{x+ow}]\ncomposite = cv2.addWeighted(overlay, {opacity}, roi, 1.0 - {opacity}, 0)"
    
    return ProcessingResult(out, formula, code, t0)

def blend_two_images(image1: np.ndarray, image2: np.ndarray, alpha: float = 0.5, mode: str = "linear") -> ProcessingResult:
    """
    دمج صورتين معاً (DIP Two-Image Blending):
    g(x,y) = (1 - alpha) * f0(x,y) + alpha * f1(x,y)
    يدعم الأنماط:
    - linear (Alpha Blending cv2.addWeighted)
    - addition (جمع البكسلات مع تشبع)
    - subtraction (طرح الصورتين لكشف الفروقات)
    - multiply (ضرب البكسلات)
    - screen (عكس الضرب للإنارة)
    """
    t0 = time.perf_counter()
    rows, cols = image1.shape[:2]
    
    # تحجيم الصورة الثانية لتطابق أبعاد الصورة الأولى تماماً
    img2_resized = cv2.resize(image2, (cols, rows), interpolation=cv2.INTER_LINEAR)
    
    # التأكد من توافق القنوات
    if len(image1.shape) == 3 and image1.shape[2] == 4:
        img1 = image1[:, :, :3]
    else:
        img1 = image1.copy()
        
    if len(img2_resized.shape) == 3 and img2_resized.shape[2] == 4:
        img2 = img2_resized[:, :, :3]
    elif len(img2_resized.shape) == 2:
        img2 = cv2.cvtColor(img2_resized, cv2.COLOR_GRAY2BGR)
    else:
        img2 = img2_resized.copy()
        
    if len(img1.shape) == 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        
    alpha = max(0.0, min(1.0, float(alpha)))
    beta = 1.0 - alpha
    
    if mode == "addition":
        out = cv2.add(cv2.multiply(img1, np.array([beta])), cv2.multiply(img2, np.array([alpha])))
        formula = f"Image Addition: g(x,y) = clip({beta:.2f}·f₁(x,y) + {alpha:.2f}·f₂(x,y), 0, 255)"
        code = f"# DIP Linear Addition\nres = cv2.addWeighted(img1, {beta:.2f}, img2, {alpha:.2f}, 0.0)"
    elif mode == "subtraction":
        out = cv2.absdiff(img1, img2)
        formula = "Image Difference / Subtraction: g(x,y) = |f₁(x,y) - f₂(x,y)|"
        code = "# DIP Image Subtraction\nres = cv2.absdiff(img1, img2)"
    elif mode == "multiply":
        f1 = img1.astype(np.float32) / 255.0
        f2 = img2.astype(np.float32) / 255.0
        out_f = (1.0 - alpha) * f1 + alpha * (f1 * f2)
        out = np.clip(out_f * 255.0, 0, 255).astype(np.uint8)
        formula = f"Multiply Blending: g = (1-α)·f₁ + α·(f₁ · f₂) | α={alpha:.2f}"
        code = f"# Multiply Blending\nres = np.clip((1.0-{alpha:.2f})*f1 + {alpha:.2f}*(f1*f2), 0, 1) * 255"
    elif mode == "screen":
        f1 = img1.astype(np.float32) / 255.0
        f2 = img2.astype(np.float32) / 255.0
        scr = 1.0 - (1.0 - f1) * (1.0 - f2)
        out_f = (1.0 - alpha) * f1 + alpha * scr
        out = np.clip(out_f * 255.0, 0, 255).astype(np.uint8)
        formula = f"Screen Blending: g = 1 - (1-f₁)(1-f₂) | α={alpha:.2f}"
        code = f"# Screen Blending\nres = (1.0 - (1.0 - f1) * (1.0 - f2)) * 255"
    else: # linear
        out = cv2.addWeighted(img1, beta, img2, alpha, 0.0)
        formula = f"Linear Blend: g(x,y) = (1 - α)·f₁(x,y) + α·f₂(x,y) | α={alpha:.2f} ({int(alpha*100)}%)"
        code = f"# Classical DIP Linear Image Blending\nalpha = {alpha:.2f}\nres = cv2.addWeighted(img1, 1.0 - alpha, img2, alpha, 0.0)"
        
    return ProcessingResult(out, formula, code, t0)

def fit_image_to_box(img: np.ndarray, box_w: int, box_h: int) -> np.ndarray:
    """
    ملاءمة وقص الصورة هندسياً لملء أبعاد الخانة (Cover Crop) مع الحفاظ على النسبة
    """
    if img is None or img.size == 0 or box_w <= 0 or box_h <= 0:
        return np.zeros((max(1, box_h), max(1, box_w), 3), dtype=np.uint8)
    
    # تحويل للقنوات الثلاث إذا كانت صورة رمادية أو BGRA
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
    ih, iw = img.shape[:2]
    scale = max(box_w / max(1, iw), box_h / max(1, ih))
    nw, nh = max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))
    
    interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC
    resized = cv2.resize(img, (nw, nh), interpolation=interp)
    
    # اقتصاص من المنتصف Center-crop
    x1 = max(0, (nw - box_w) // 2)
    y1 = max(0, (nh - box_h) // 2)
    x2 = min(nw, x1 + box_w)
    y2 = min(nh, y1 + box_h)
    
    cropped = resized[y1:y2, x1:x2]
    # التأكد من مطابقة المقاس النهائي بالضبط
    if cropped.shape[1] != box_w or cropped.shape[0] != box_h:
        cropped = cv2.resize(cropped, (box_w, box_h), interpolation=cv2.INTER_LINEAR)
    return cropped

def generate_photo_collage(images: list, template: str = "grid_2x2", border_size: int = 10, border_color: list = None, canvas_w: int = 1200, canvas_h: int = 1200) -> ProcessingResult:
    """
    توليد كولاج وشبكات دمج الصور الرقمية (DIP Multi-Image Collage)
    - side_by_side: صورتين جنباً إلى جنب (1:1 أفقي)
    - top_bottom: صورتين فوق وتحت (1:1 رأسي)
    - three_one_left: 3 صور (واحدة كبيرة في اليسار + اثنتين في اليمين)
    - three_columns: 3 صور متساوية في 3 أعمدة
    - grid_2x2: 4 صور في شبكة مربعة 2x2
    - four_header: 4 صور (واحدة بانورامية في الأعلى + 3 بالأعمدة تحت)
    """
    t0 = time.perf_counter()
    if border_color is None or len(border_color) < 3:
        border_color = [255, 255, 255] # أبيض افتراضي
        
    border = max(0, min(60, int(border_size)))
    canvas = np.full((canvas_h, canvas_w, 3), border_color[:3], dtype=np.uint8)
    
    # التأكد من وجود صور صالحة
    valid_imgs = [im for im in images if im is not None and im.size > 0]
    if not valid_imgs:
        valid_imgs = [np.full((400, 400, 3), 180, dtype=np.uint8)]
        
    num_imgs = len(valid_imgs)
    
    # حساب الإحداثيات لكل قالب
    boxes = [] # [(x, y, w, h)]
    
    if template == "side_by_side":
        # صورتين جنباً إلى جنب
        w_slot = (canvas_w - 3 * border) // 2
        h_slot = canvas_h - 2 * border
        boxes.append((border, border, w_slot, h_slot))
        boxes.append((border * 2 + w_slot, border, canvas_w - (border * 2 + w_slot) - border, h_slot))
        desc = "2-Image Horizontal Split (1:1 Side by Side)"
        
    elif template == "top_bottom":
        # صورتين رأسياً
        w_slot = canvas_w - 2 * border
        h_slot = (canvas_h - 3 * border) // 2
        boxes.append((border, border, w_slot, h_slot))
        boxes.append((border, border * 2 + h_slot, w_slot, canvas_h - (border * 2 + h_slot) - border))
        desc = "2-Image Vertical Split (Top & Bottom)"
        
    elif template == "three_one_left":
        # 3 صور: 1 يسار كبيرة، و 2 يمين
        w_left = (canvas_w - 3 * border) * 6 // 10
        w_right = canvas_w - 3 * border - w_left
        h_all = canvas_h - 2 * border
        h_half = (canvas_h - 3 * border) // 2
        
        boxes.append((border, border, w_left, h_all))
        boxes.append((border * 2 + w_left, border, w_right, h_half))
        boxes.append((border * 2 + w_left, border * 2 + h_half, w_right, canvas_h - (border * 2 + h_half) - border))
        desc = "3-Image Featured Left (1 Large + 2 Stacked)"
        
    elif template == "three_columns":
        # 3 صور أعمدة متساوية
        w_slot = (canvas_w - 4 * border) // 3
        h_slot = canvas_h - 2 * border
        for i in range(3):
            x = border + i * (w_slot + border)
            w = w_slot if i < 2 else (canvas_w - x - border)
            boxes.append((x, border, w, h_slot))
        desc = "3-Image Tri-Column Strip"
        
    elif template == "four_header":
        # 4 صور: واحدة بانورامية عليا و3 بالأسفل
        h_top = (canvas_h - 3 * border) * 55 // 100
        h_bot = canvas_h - 3 * border - h_top
        boxes.append((border, border, canvas_w - 2 * border, h_top))
        
        w_col = (canvas_w - 4 * border) // 3
        y_bot = border * 2 + h_top
        for i in range(3):
            x = border + i * (w_col + border)
            w = w_col if i < 2 else (canvas_w - x - border)
            boxes.append((x, y_bot, w, h_bot))
        desc = "4-Image Panoramic Header + 3 Columns"
        
    else: # grid_2x2
        # 4 صور شبكة 2x2
        w_slot = (canvas_w - 3 * border) // 2
        h_slot = (canvas_h - 3 * border) // 2
        w2 = canvas_w - (border * 2 + w_slot) - border
        h2 = canvas_h - (border * 2 + h_slot) - border
        
        boxes.append((border, border, w_slot, h_slot))
        boxes.append((border * 2 + w_slot, border, w2, h_slot))
        boxes.append((border, border * 2 + h_slot, w_slot, h2))
        boxes.append((border * 2 + w_slot, border * 2 + h_slot, w2, h2))
        desc = "4-Image Classic Quad Grid (2×2)"

    # تركيب الصور داخل الخانات
    for i, (bx, by, bw, bh) in enumerate(boxes):
        src_img = valid_imgs[i % num_imgs]
        fitted = fit_image_to_box(src_img, bw, bh)
        canvas[by:by+bh, bx:bx+bw] = fitted

    formula = f"Collage Assembly: {desc} | Slots={len(boxes)} | Gap={border}px"
    code = f"# DIP Multi-Image Grid Assembly\ncanvas = np.full(({canvas_h}, {canvas_w}, 3), {border_color[:3]}, dtype=np.uint8)\n# Render {len(boxes)} image slots with smart aspect-fill"
    
    return ProcessingResult(canvas, formula, code, t0)


def cut_background_by_threshold(image: np.ndarray, t1: int = 50, t2: int = 150, sigma: float = 1.4, mode: str = "band", invert: bool = False) -> ProcessingResult:
    """
    عزل وقص الخلفية بالاعتماد على العتبة والمعايير (T1, T2, Gaussian Sigma):
    - وضع النطاق (Band): عزل العناصر التي تقع كثافتها اللونية بين العتبتين T1 و T2
    - وضع الحواف (Edge Contours): تحديد حدود العنصر بحواف كاني وملء الجسم وعزل الخلفية
    """
    t0 = time.perf_counter()
    rows, cols = image.shape[:2]
    
    # 1. القناة الرمادية
    if len(image.shape) == 2:
        gray = image
    elif image.shape[2] == 4:
        gray = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2GRAY)
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # 2. تنعيم جاوس بمعامل السيجما (Gaussian Smoothing)
    k_val = max(3, int(round(float(sigma) * 4)) | 1)
    blurred = cv2.GaussianBlur(gray, (k_val, k_val), float(sigma))
    
    low = min(int(t1), int(t2))
    high = max(int(t1), int(t2))
    
    if mode == "edges":
        # عزل الخلفية عبر حواف كاني وملء الكنتور
        edges = cv2.Canny(blurred, low, high)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # ملء الكنتورات المغلقة
        mask = np.zeros((rows, cols), dtype=np.uint8)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cv2.drawContours(mask, contours, -1, 255, -1)
        else:
            mask = cv2.inRange(blurred, low, high)
    else:
        # وضع العتبة المزدوجة (Dual Thresholding Mask)
        mask = cv2.inRange(blurred, low, high)
        
    if invert:
        mask = cv2.bitwise_not(mask)
        
    # تنعيم حواف القناع للقص الاحترافي (Feathering)
    mask = cv2.GaussianBlur(mask, (3, 3), 0.8)
    
    # إنشاء صورة BGRA شفافة
    if len(image.shape) == 2:
        bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 4:
        bgr = image[:, :, :3]
    else:
        bgr = image
        
    bgra = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = mask
    
    formula = f"Alpha(x,y) = 255 if {low} ≤ G_σ(x,y) ≤ {high} else 0 | (σ = {sigma})"
    code = f"# Threshold Background Cutout\nblurred = cv2.GaussianBlur(gray, (5, 5), {sigma})\nmask = cv2.inRange(blurred, {low}, {high})\nresult_bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)\nresult_bgra[:, :, 3] = mask"
    
    return ProcessingResult(bgra, formula, code, t0)



