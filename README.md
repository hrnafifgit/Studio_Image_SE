# VisionCraft - Digital Image Processing (DIP) Studio

![CI Workflow](https://github.com/hrnafifgit/Studio_Image_SE/actions/workflows/ci.yml/badge.svg)
![Laravel](https://img.shields.io/badge/Laravel-11-FF2D20?style=flat&logo=laravel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=flat&logo=git&logoColor=white)

---

## 📝 وصف مختصر

يواجه الطلاب والباحثون صعوبة في الوصول لأدوات خفيفة وسهلة لتطبيق خوارزميات معالجة الصور الرقمية (DIP) والرياضيات التطبيقية دون الحاجة لتثبيت برامج ثقيلة أو كتابة أكواد تفصيلية لكل تجربة. يقدم مشروع **VisionCraft** حلاً متكاملاً عبر تطبيق ويب تفاعلي يوفر واجهة معالجة سهلة، مدعومة بمحرك بايثون سريع ينفذ العمليات النقطية، المرشحات المكانية، كشف الحواف، والتحويلات الترددية والمورفولوجية بدقة عالية ومباشرة عبر المتصفح.

---

## 👥 أعضاء الفريق

- **أحمد القاضي**
- **أمجد الفضلي**
- **شعيب جازم**
- **هارون العفيف**

---

## 🛠️ التقنيات المتوقعة

- **Laravel:** بناء بوابة التطبيق (API Gateway) وخدمة واجهات الويب والـ Routing.
- **Python (Flask, OpenCV, NumPy, SciPy):** محرك معالجة الصور الرقمية والخوارزميات المتقدمة.
- **MySQL:** إدارة وبناء قواعد البيانات.
- **Git & GitHub:** التحكم في الإصدارات وإدارة العمل الجماعي.

---

## 📄 وثائق المشروع

- [وثيقة المتطلبات (SRS)](docs/SRS.md)
- [سجل توثيق استخدام الذكاء الاصطناعي (AI Usage Log)](AI_LOG.md)

---

## 🔄 طريقة العمل

يتبع الفريق أفضل ممارسات هندسة البرمجيات والعمل الجماعي؛ حيث يتم استخدام **GitHub Issues** لإدارة وتوزيع المهام ومتابعة إنجازها، ويقوم كل عضو بالعمل على فروع مخصصة (**Branches**) لكل ميزة أو إصلاح، ثم تقديم طلبات الدمج (**Pull Requests**) للمراجعة المتبادلة والتدقيق قبل الدمج في الفرع الرئيسي (`main`).

---

## 🚀 طريقة التشغيل في بيئة التطوير (Development)

### 1. تشغيل محرك بايثون (Python Engine)

```bash
cd python_engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/server.py
```

> يعمل المحرك على المنفذ `5001` (`http://127.0.0.1:5001`)
> مشرف المشروع :
# لعنة الله على الظالمين
### 2. تشغيل سيرفر لارافل (Laravel Server)

```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan serve
```

> تعمل الواجهة على المنفذ `8000` (`http://127.0.0.1:8000`).
