# VisionCraft - Digital Image Processing (DIP) Studio

![CI Workflow](https://github.com/hrnafifgit/Studio_Image_SE/actions/workflows/ci.yml/badge.svg)
![Laravel](https://img.shields.io/badge/Laravel-11-FF2D20?style=flat&logo=laravel&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-5C3EE8?style=flat&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue)

تم بناء وهيكلة هذا المشروع ليتبع أفضل ممارسات هندسة البرمجيات (Software Engineering Best Practices) وفق معمارية الخدمات المصغرة (Microservices Architecture) المكونة من:

1. **الواجهة الأمامية ومعالجة المسارات (Laravel 11)**: يقوم بخدمة الواجهة الأمامية ويوفر نقطة اتصال وسيطة (API Proxy).
2. **محرك معالجة الصور (Python Flask)**: يعمل كخدمة مصغرة (Microservice) لمعالجة الصور بخوارزميات متقدمة.

## 🛠️ متطلبات التشغيل (للفريق)

- PHP 8.2+ و Composer (يفضل استخدام Laravel Herd على الويندوز).
- Python 3.10+
- بيئة وهمية (Virtual Environment) لبايثون.
- Node.js & NPM (لتطوير الواجهة الأمامية إن لزم الأمر).

## 🚀 طريقة التشغيل في بيئة التطوير (Development)

لكي يعمل النظام بشكل متكامل، يجب تشغيل الخدمتين معاً:

### 1. تشغيل محرك بايثون (Python Engine)
افتح نافذة موجه أوامر (Terminal) جديدة، وانتقل لمجلد المشروع، ثم نفذ:
```bash
cd python_engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/server.py
```
> سيتم تشغيل المحرك على المنفذ `5001` (`http://127.0.0.1:5001`).

### 2. تشغيل سيرفر لارافل (Laravel Server)
افتح نافذة موجه أوامر (Terminal) أخرى في المسار الرئيسي للمشروع، ونفذ:
```bash
composer install
cp .env.example .env
php artisan key:generate
php artisan serve
```
> سيتم تشغيل واجهة الموقع على المنفذ `8000` (`http://127.0.0.1:8000`).
> لارافل سيقوم بتمرير جميع طلبات المعالجة (`/api/process`) إلى محرك بايثون خلف الكواليس.

## 👥 آلية العمل الجماعي (Team Workflow)

- **الفروع (Branches):** يجب على كل عضو في الفريق (4 أعضاء) إنشاء فرع خاص بمهمته قبل البدء بالتطوير (مثال: `feature/ui-improvements` أو `fix/image-crop`).
- **لوحة المهام (Kanban):** يُفضل استخدام Trello أو GitHub Projects لتتبع المهام (To Do, In Progress, Review, Done).
- **الدمج (Merge):** لا تقم بالدمج مباشرة إلى الـ `main`. قم بعمل Pull Request (PR) ليقوم زميل آخر بمراجعة الكود.

## 📁 هيكلة المشروع (Architecture)

```text
/
├── app/Http/Controllers/ImageProcessingController.php  <-- المتحكم الخاص بربط لارافل مع بايثون
├── public/                  <-- ملفات الـ Assets (js, css, images)
├── python_engine/           <-- مجلد الخدمة المصغرة (Python Microservice)
│   ├── app/server.py        <-- ملف التشغيل للخدمة المصغرة
│   ├── core/                <-- خوارزميات معالجة الصور
│   └── requirements.txt
├── resources/views/         <-- واجهات Blade (مثل welcome.blade.php)
├── routes/
│   ├── api.php              <-- مسارات الـ API التي تنادي ImageProcessingController
│   └── web.php              <-- مسار الويب الرئيسي
└── ...
```
