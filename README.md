# استوديو المعالجة الرقمية للصور (VisionCraft - DIP Photoshop Studio) 🐝🎨

برنامج متكامل لمعالجة الصور الرقمية الرياضية (Digital Image Processing) عبر واجهة ويب احترافية شبيهة بالفوتوشوب مدعومة بمحرك خوارزميات بايثون الرياضي (OpenCV, NumPy, SciPy).

## 🌟 المميزات والعمليات المضمنة:
1. **العمليات النقطية (Point Operations):**
   - السطوع والتباين (Brightness / Contrast).
   - تحويلات السجل والـ Gamma والعتبة (Thresholding).
   - موازنة الهستوجرام العالمي والمحلي (Global / CLAHE Histogram Equalization).
2. **المرشحات المكانية (Spatial Filtering):**
   - Gaussian Blur, Box Blur, Median, Wiener Filter, Bilateral Filter.
   - تطبيق مصفوفة نواة مخصصة (Custom Convolution Kernel).
3. **كشف الحواف (Edge Detection):**
   - Canny, Sobel, Prewitt, Laplacian, Unsharp Masking.
4. **العمليات المورفولوجية (Morphological Operations):**
   - التآكل (Erosion)، التمدد (Dilation)، الفتح (Opening)، الإغلاق (Closing).
   - التدرج المورفولوجي، Top-hat / Black-hat، واستخراج الهياكل (Skeleton).
5. **معالجة الترددات (Frequency Domain):**
   - تحويل فورييه السريع (FFT Spectrum).
   - فلاتر التردد المنخفض والعالي (Ideal, Butterworth, Gaussian).
   - مرشح الشق (Notch Filter).
6. **فضاءات الألوان واستعادة الصور:**
   - تحويلات Grayscale, HSV, LAB.
   - عزل القنوات اللونية، تجزئة K-Means، واستخراج الباليتات.
   - إزالة الضبابية الحركية (Motion Deblur - Wiener).
7. **التركيب والطبقات (Layers & Composition):**
   - إزالة الخلفية وتغييرها، إضافة نصوص وصور مدمجة.

---

## 🚀 طريقة التشغيل:

### 1. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

### 2. تشغيل البرنامج:
```bash
python run.py
```
سيفتح المتصفح تلقائياً على الرابط: `http://127.0.0.1:5001`
