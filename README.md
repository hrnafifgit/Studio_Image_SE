# 🐝 VisionCraft - Digital Image Processing (DIP) Studio & AR Mirror

![CI Workflow](https://github.com/hrnafifgit/Studio_Image_SE/actions/workflows/ci.yml/badge.svg)
![Laravel](https://img.shields.io/badge/Laravel-11-FF2D20?style=flat&logo=laravel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=flat&logo=opencv&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=flat&logo=git&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

---

## 📖 وصف المشروع (Project Description)
يواجه الطلاب والباحثون صعوبة في الوصول لأدوات خفيفة وسهلة لتطبيق خوارزميات معالجة الصور الرقمية (DIP) والرياضيات التطبيقية دون الحاجة لتثبيت برامج ثقيلة أو كتابة أكواد تفصيلية لكل تجربة.

يقدم مشروع **VisionCraft DIP Studio** حلاً متكاملاً عبر استوديو ويب تفاعلي متقدم يحاكي برنامج أدوبي فوتوشوب (Photoshop Pro)، مخصص لحسابات ومعالجة الصور الرقمية وتطبيقات الواقع المعزز (AR Mirror). تم تصميم النظام وبناؤه وفق أفضل ممارسات **هندسة البرمجيات (Software Engineering Best Practices)**.

---

## 👥 أعضاء الفريق (Team Members)
- **أحمد القاضي**
- **أمجد الفضلي**
- **شعيب جازم**
- **هارون العفيف**

---

## 🌟 أبرز مميزات النظام (Key Features)
* **واجهة فوتوشوب احترافية:** مقارنة الشاشة المقسمة (Before/After Slider)، إدارة الطبقات (Layers)، والتراجع/الإعادة غير المحدود (Undo/Redo Memento Pattern).
* **معمارية خدمات مصغرة ثنائية النواة:** واجهة وبوابة خلفية قوية مبنية بـ **Laravel 11** متصلة بمحرك علمي حسابي فائق السرعة عبر **Python (Flask, OpenCV, NumPy, SciPy)**.
* **قدرات خارقة لمعالجة الصور:**
  - تفريغ وعزل الخلفيات الذكي عبر خوارزمية **GrabCut**.
  - إزالة التغبيش الحركي واستعادة الصور عبر **Wiener Deconvolution**.
  - فلتر حجب الترددات التفاعلي **2D-FFT Notch Reject** للقضاء على تموجات المواريه (Moiré).
  - فرشاة المعالجة الانتقائية (Selective Processing Brush).
  - استخراج لوحات الألوان الذكية (K-Means Palette) والمكبر الرقمي للبكسلات (7x7 Pixel Loupe).
  - بث الإطارات اللحظية عبر **WebSocket** لمرآة الواقع المعزز (AR Try-On).

---

## 📜 سياسات المستودع والمجتمع (Community Standards & Governance)

| الوثيقة | الوصف والرابط |
| :--- | :--- |
| **رخصة الاستخدام (License)** | مرخص بالكامل تحت رخصة مفتوحة المصدر: [MIT License](LICENSE) |
| **ميثاق السلوك (Code of Conduct)** | قواعد السلوك والتعاون الأكاديمي بين أفراد الفريق: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **سياسة الأمان (Security Policy)** | تعليمات الإبلاغ عن الثغرات وحماية النظام: [SECURITY.md](SECURITY.md) |
| **دليل المساهمة (Contributing)** | إرشادات كتابة الكود ومراجعة طلبات السحب (PR): [CONTRIBUTING.md](CONTRIBUTING.md) |
| **دليل سير عمل الطلاب (Git Workflow)** | دليل إدارة الفروع والمهام: [GIT_WORKFLOW_STUDENTS_GUIDE.txt](GIT_WORKFLOW_STUDENTS_GUIDE.txt) |
| **وثيقة المتطلبات (SRS)** | مواصفات ومتطلبات النظام: [docs/SRS.md](docs/SRS.md) |
| **سجل استخدام الذكاء الاصطناعي** | توثيق استخدام أدوات الذكاء الاصطناعي: [AI_LOG.md](AI_LOG.md) |
| **تقرير معمارية الـ API (PDF Report)** | التقرير الأكاديمي الشامل المعتمد: [docs/VisionCraft_API_Architecture_Report.pdf](docs/VisionCraft_API_Architecture_Report.pdf) |

---

## 🛠️ متطلبات التشغيل (Prerequisites)

- **PHP 8.2+** و **Composer** (يفضل استخدام Laravel Herd أو بيئة متوافقة).
- **Python 3.10+** مع تثبيت البيئة الوهمية (venv).
- **Node.js & NPM** (لتطوير وبناء الواجهة إن لزم الأمر).
- **MySQL 8.0+** لقواعد البيانات.

---

## 🚀 طريقة التشغيل في بيئة التطوير (Quick Start)

لكي يعمل النظام بشكل متكامل، يتم تشغيل الخدمتين معاً:

### 1. تشغيل محرك بايثون العلمي (Python DIP Engine)
افتح نافذة موجه أوامر (Terminal) وانتقل لمجلد الخدمة المصغرة:
```bash
cd python_engine
python -m venv venv
venv\Scripts\activate       # على أنظمة لينكس/ماك: source venv/bin/activate
pip install -r requirements.txt
python app/server.py        # أو تشغيل python run.py
```
> يعمل المحرك على المنفذ `5001` (`http://127.0.0.1:5001`).

### 2. تشغيل سيرفر لارافل (Laravel API Gateway & Frontend)
افتح نافذة موجه أوامر أخرى في المسار الرئيسي للمشروع:
```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan serve
```
> سيتم تشغيل واجهة الموقع على المنفذ `8000` (`http://127.0.0.1:8000`).  
> يقوم لارافل بخدمة الواجهة وتمرير طلبات المعالجة (`/api/process`) مباشرة إلى محرك بايثون.

---

## 👥 آلية العمل الجماعي (Team Workflow & Scrum)

- **الفروع (Branches):** يجب على كل عضو إنشاء فرع منفصل لكل مهمة (مثل: `feature/ui-improvements` أو `fix/grabcut-mask`).
- **قوالب المشاكل (Issue Templates):** استخدم قوالب GitHub المجهزة مسبقاً (`.github/ISSUE_TEMPLATE`) لتسجيل المهام أو الأخطاء.
- **طلبات السحب (Pull Requests):** لا تقم بالدمج مباشرة إلى الـ `main`. افتح PR ليتم فحصه آلياً عبر GitHub Actions ومراجعته من الزملاء.

---

## 📁 هيكلية المشروع (Architecture Tree)

```text
/
├── app/Http/Controllers/ImageProcessingController.php  <-- المتحكم الوسيط لنقل الطلبات إلى بايثون
├── docs/VisionCraft_API_Architecture_Report.pdf        <-- التقرير الهندسي الشامل للـ API (11 صفحة)
├── public/                                             <-- أصول الواجهة (JavaScript, CSS, Assets)
├── python_engine/                                      <-- الخدمة المصغرة لمحرك بايثون
│   ├── app/server.py                                   <-- خادم Flask و Socket.IO
│   ├── core/                                           <-- خوارزميات معالجة الصور الرقمية (DIP)
│   └── requirements.txt                                <-- حزم بايثون (OpenCV, NumPy, SciPy...)
├── resources/views/welcome.blade.php                   <-- واجهة استوديو الفوتوشوب التفاعلية
├── routes/api.php                                      <-- مسارات الـ API العامة (/api/process)
├── CODE_OF_CONDUCT.md                                  <-- ميثاق قواعد السلوك
├── CONTRIBUTING.md                                     <-- دليل المساهمة
├── LICENSE                                             <-- رخصة الاستخدام (MIT)
└── SECURITY.md                                         <-- سياسة الأمان وحماية النظام
```
