# -*- coding: utf-8 -*-
"""
VisionCraft DIP Studio - Frontend Engineering & Complete System Manual Generator
Produces a publication-quality, comprehensive Arabic academic PDF on the user's Desktop.
Includes detailed AI Usage Log Entry for Ahmed Al-Qadi, deep explanations of all his code files,
and complete architectural analysis of all Markdown (.md) files in the repository.
"""

import os
import sys
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>التقرير الهندسي الشامل لمهندس الواجهات وتجربة المستخدم - VisionCraft DIP Studio</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Fira+Code:wght@400;500;600&display=swap');

    @page {
        size: A4;
        margin: 18mm 14mm 18mm 14mm;
        @bottom-left {
            content: "VisionCraft DIP Studio - الدليل الهندسي الشامل لمهندس الواجهات";
            font-family: 'Cairo', sans-serif;
            font-size: 8pt;
            color: #64748b;
        }
        @bottom-right {
            content: "صفحة " counter(page) " من " counter(pages);
            font-family: 'Cairo', sans-serif;
            font-size: 8pt;
            color: #64748b;
        }
    }

    * {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    body {
        font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
        font-size: 10pt;
        line-height: 1.65;
        color: #1e293b;
        background-color: #ffffff;
        margin: 0;
        padding: 0;
    }

    .page-break {
        page-break-before: always;
        break-before: page;
    }

    .no-break {
        page-break-inside: avoid;
        break-inside: avoid;
    }

    /* Cover Page */
    .cover-page {
        height: 100vh;
        max-height: 250mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        padding: 10mm 5mm 5mm 5mm;
        border: 2px solid #0284c7;
        border-radius: 8px;
        background: linear-gradient(180deg, #f8fafc 0%, #f0fdf4 100%);
        box-sizing: border-box;
    }

    .cover-header {
        font-size: 11pt;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.6;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 8px;
        width: 100%;
    }

    .cover-title-area {
        margin: 15px 0;
    }

    .cover-badge {
        display: inline-block;
        background: #0284c7;
        color: #ffffff;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 10pt;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }

    .cover-title {
        font-size: 22pt;
        font-weight: 900;
        color: #0f172a;
        margin: 0 0 8px 0;
        line-height: 1.3;
    }

    .cover-subtitle {
        font-size: 13pt;
        font-weight: 700;
        color: #0284c7;
        margin: 0 0 12px 0;
    }

    .cover-desc {
        font-size: 10pt;
        color: #475569;
        max-width: 580px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .cover-meta-box {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-right: 4px solid #0284c7;
        border-radius: 6px;
        padding: 14px 20px;
        text-align: right;
        width: 90%;
        margin: 10px auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }

    .cover-meta-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        font-size: 9.5pt;
    }

    .cover-meta-item strong {
        color: #0f172a;
    }

    .cover-footer {
        font-size: 9pt;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        padding-top: 8px;
        width: 100%;
    }

    /* Typography & Headers */
    h1 {
        font-size: 15.5pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 2px solid #0284c7;
        padding-bottom: 6px;
        margin: 20px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    h2 {
        font-size: 12pt;
        font-weight: 700;
        color: #0369a1;
        margin: 14px 0 8px 0;
        border-right: 3px solid #0284c7;
        padding-right: 8px;
    }

    h3 {
        font-size: 10.5pt;
        font-weight: 700;
        color: #1e293b;
        margin: 12px 0 6px 0;
    }

    p {
        margin: 0 0 8px 0;
        text-align: justify;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 14px 0;
        font-size: 8.5pt;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 8px;
        text-align: right;
    }

    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
    }

    tr:nth-child(even) td {
        background-color: #f8fafc;
    }

    /* Code Blocks */
    pre, code {
        font-family: 'Fira Code', Consolas, monospace;
        direction: ltr;
        text-align: left;
    }

    pre {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 9px 12px;
        border-radius: 6px;
        font-size: 8pt;
        line-height: 1.45;
        overflow-x: hidden;
        margin: 8px 0 12px 0;
        border: 1px solid #1e293b;
    }

    code.inline {
        background-color: #f1f5f9;
        color: #0284c7;
        padding: 2px 5px;
        border-radius: 4px;
        font-size: 8.5pt;
        border: 1px solid #e2e8f0;
    }

    /* Cards & Callouts */
    .callout {
        padding: 10px 14px;
        border-radius: 6px;
        margin: 10px 0;
        font-size: 9.5pt;
    }

    .callout-info {
        background-color: #f0f9ff;
        border-right: 4px solid #0284c7;
        color: #0369a1;
    }

    .callout-success {
        background-color: #f0fdf4;
        border-right: 4px solid #16a34a;
        color: #15803d;
    }

    .callout-warning {
        background-color: #fffbeb;
        border-right: 4px solid #d97706;
        color: #b45309;
    }

    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 7.5pt;
        font-weight: 700;
        color: #ffffff;
    }

    .badge-primary { background: #0284c7; }
    .badge-success { background: #16a34a; }
    .badge-purple { background: #9333ea; }
    .badge-orange { background: #ea580c; }

    .toc {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 18px;
        margin: 12px 0;
    }

    .toc-item {
        display: flex;
        justify-content: space-between;
        padding: 4px 0;
        border-bottom: 1px dashed #cbd5e1;
        font-size: 9pt;
    }

    .toc-item:last-child {
        border-bottom: none;
    }

    .feature-card {
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 10px;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
    <div class="cover-header">
        الجمهورية اليمنية — وزارة التعليم العالي والبحث العلمي<br>
        جامعة ذمار — كلية الحاسبات والمعلوماتية — قسم هندسة البرمجيات (Software Engineering)<br>
        مشروع تخرج المستوى الرابع (Graduation Project - Academic Year 2026)
    </div>

    <div class="cover-title-area">
        <span class="cover-badge">التقرير الفني الشامل لمهندس الواجهات والأنظمة والـ Git</span>
        <h1 class="cover-title">VisionCraft DIP Studio & AR Mirror</h1>
        <div class="cover-subtitle">دليل مهندس الواجهات وتجربة المستخدم وهندسة البرمجيات</div>
        <p class="cover-desc">
            مرجع هندسي تفصيلي يوثق كافة ملفات وكود الطالب أحمد القاضي، استوديو الواقع المعزز (AR Try-On)، سجل استخدام الذكاء الاصطناعي (AI Log Entry)، خريطة الملفات، تحليل ملفات الـ Markdown، ودليل سير العمل عبر Git & GitHub.
        </p>
    </div>

    <div class="cover-meta-box">
        <div class="cover-meta-grid">
            <div class="cover-meta-item"><strong>اسم الطالب (المطور):</strong> أحمد القاضي</div>
            <div class="cover-meta-item"><strong>الدور التخصصي:</strong> مهندس الواجهات وتجربة المستخدم (Frontend Lead)</div>
            <div class="cover-meta-item"><strong>اسم الفرع المخصص:</strong> <code class="inline">feature/frontend-studio</code></div>
            <div class="cover-meta-item"><strong>طلب الدمج الحالي:</strong> Pull Request #16 (Status: Open / Merged)</div>
            <div class="cover-meta-item"><strong>المستودع الرسمي:</strong> github.com/hrnafifgit/Studio_Image_SE</div>
            <div class="cover-meta-item"><strong>تاريخ التوثيق:</strong> 27 سبتمبر 2026م</div>
        </div>
    </div>

    <div class="cover-footer">
        مشروع معتمد لنيل درجة البكالوريوس في هندسة البرمجيات — جامعة ذمار — كلية الحاسبات والمعلوماتية
    </div>
</div>

<div class="page-break"></div>

<!-- TABLE OF CONTENTS -->
<h1>📋 فهرس محتويات الدليل الفني الشامل</h1>
<div class="toc">
    <div class="toc-item"><span>1. توثيق استخدام الذكاء الاصطناعي (AI Usage Entry - أحمد القاضي)</span><span>ص 3</span></div>
    <div class="toc-item"><span>2. شرح العمل المنفذ وكيف تم بناء المحرك والواجهة خطوة بخطوة</span><span>ص 4</span></div>
    <div class="toc-item"><span>3. خريطة ملفات أحمد القاضي في المشروع وأماكنها وأسمائها ووظيفتها</span><span>ص 5</span></div>
    <div class="toc-item"><span>4. ميزات وقدرات الواجهة واستوديو الواقع المعزز (AR Try-On Studio)</span><span>ص 7</span></div>
    <div class="toc-item"><span>5. خريطة الأكواد وأرقام الأسطر التفصيلية في Blade و App.js</span><span>ص 8</span></div>
    <div class="toc-item"><span>6. الأخطاء المكتشفة في الفرونت إند وكيف تم حلها برمجياً</span><span>ص 9</span></div>
    <div class="toc-item"><span>7. الشرح المعماري الشامل لكافة ملفات الـ Markdown (.md) في المشروع</span><span>ص 10</span></div>
    <div class="toc-item"><span>8. الدليل الكامل للعمل عبر Git و GitHub وتوثيق طلب الدمج PR #16</span><span>ص 12</span></div>
    <div class="toc-item"><span>9. الشرح المعماري لبقية ملفات المشروع (لارافل، بايثون، وقاعدة البيانات)</span><span>ص 14</span></div>
    <div class="toc-item"><span>10. بنك الأسئلة المتوقعة في مناقشة المشروع وإجاباتها النموذجية</span><span>ص 15</span></div>
</div>

<div class="page-break"></div>

<!-- SECTION 1: AI LOG ENTRY -->
<h1>1. توثيق استخدام الذكاء الاصطناعي (AI Usage Entry)</h1>
<p>
وفقاً لمعايير الشفافية والتفكير النقدي المعتمدة في قسم هندسة البرمجيات بجامعة ذمار، يوثق هذا القسم جلسة العصف الذهني واستخدام أداة الذكاء الاصطناعي الخاصة بالطالب أحمد القاضي:
</p>

<div class="callout callout-info no-break">
    <table style="margin:0; background:transparent;">
        <tr>
            <td style="width:25%; font-weight:bold; background:#e0f2fe;">التاريخ (Date):</td>
            <td>2026-09-20</td>
            <td style="width:20%; font-weight:bold; background:#e0f2fe;">اسم الطالب:</td>
            <td>أحمد القاضي</td>
        </tr>
        <tr>
            <td style="font-weight:bold; background:#e0f2fe;">الأداة المستخدمة:</td>
            <td>Antigravity AI (Google DeepMind)</td>
            <td style="font-weight:bold; background:#e0f2fe;">المسؤولية:</td>
            <td>تأسيس المعمارية ومحرك المعالجة والواجهات</td>
        </tr>
        <tr>
            <td style="font-weight:bold; background:#e0f2fe;">الغرض (Purpose):</td>
            <td colspan="3">تصميم هيكل خادم Python Flask وإعداد مسارات الـ API لمعالجة البكسلات وربطها مع Laravel.</td>
        </tr>
        <tr>
            <td style="font-weight:bold; background:#e0f2fe;">ملخص الطلب (Prompt):</td>
            <td colspan="3">"اقتراح هيكلية مجلدات ومسارات RESTful لميكروسيرفيس بايثون يتصل بـ Laravel على المنفذ 5001."</td>
        </tr>
    </table>
</div>

<h2>تحليل الاقتراحات والتفكير النقدي والقرارات الهندسية:</h2>
<table>
    <thead>
        <tr>
            <th>اقتراحات الذكاء الاصطناعي (AI Suggestions)</th>
            <th>القرار الهندسي (Decision)</th>
            <th>التعليل والمسوغ العلمي (Engineering Justification)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>الاقتراح 1:</strong> دمج بايثون داخل لارافل مباشرة باستخدام حزمة <code class="inline">php-python</code>.</td>
            <td><span class="badge badge-orange">مرفوض (Rejected)</span></td>
            <td>حزم استدعاء بايثون من داخل PHP غير مستقرة، تسبب بطء شديد (Overhead) عند تمرير المصفوفات الضخمة وتتعارض مع ملحقات OpenCV المكتوبة بلغة C++.</td>
        </tr>
        <tr>
            <td><strong>الاقتراح 2:</strong> تشغيل Flask كخدمة مصغرة مستقلة على المنفذ 5001 مع مسارات <code class="inline">/api/process</code> و <code class="inline">/api/health</code>.</td>
            <td><span class="badge badge-success">مقبول (Accepted)</span></td>
            <td>يحقق مبدأ فصل المسؤوليات (SoC)، خفيف جداً، يتيح معالجة مصفوفات NumPy بدون كتل زائدة، ويوفر سرعة استجابة فائقة.</td>
        </tr>
        <tr>
            <td><strong>الاقتراح 3:</strong> استخدام إطار عمل Django بدلاً من Flask.</td>
            <td><span class="badge badge-orange">مرفوض (Rejected)</span></td>
            <td>Django إطار ضخم يتضمن ميزات ثقيلة (ORM، لوحة إدارة، قوالب) لا نحتاجها إطلاقاً؛ لأن وظيفة بايثون هنا حسابية علمية بحتة (Microservice).</td>
        </tr>
    </tbody>
</table>

<div class="callout callout-success no-break">
    <strong>المراجعة البشرية والتنفيذ العملي (Human Review):</strong><br>
    قام الطالب <strong>أحمد القاضي</strong> باعتماد الهيكل المصغر، وأنشأ ملف الخادم <code class="inline">python_engine/app/server.py</code>، وقام بتهيئة CORS للسماح بالاتصال، وبرمج مسار فك تشفير سلاسل Base64 مع دعم EXIF Auto-Orientation لتصحيح صور الهواتف الذكية.
</div>

<div class="page-break"></div>

<!-- SECTION 2: WHAT WAS DONE STEP-BY-STEP -->
<h1>2. شرح العمل المنفذ وكيف تم البناء خطوة بخطوة</h1>
<p>
تم تنفيذ العمل عبر مراحل هندسية متتالية وفق منهجية هندسة البرمجيات:
</p>

<div class="feature-card no-break">
    <h3>المرحلة الأولى: تأسيس نواة خادم بايثون ومعالجة البكسلات (Python Microservice)</h3>
    <p>
    1. <strong>إنشاء خادم Flask:</strong> في <code class="inline">python_engine/app/server.py</code>، تم تجهيز السيرفر ليعمل على المنفذ 5001 مع دعم Flask-CORS و Socket.IO.<br>
    2. <strong>معالجة الصور الرقمية:</strong> كتابة دالة <code class="inline">decode_image_from_base64</code> التي تستقبل الصور بصيغة Base64، وتصحح اتجاه الصورة تلقائياً عبر EXIF Transpose، وتحولها إلى مصفوفات NumPy ثنائية وثلاثية الأبعاد صالحة لدوال OpenCV.<br>
    3. <strong>مسار المعالجة <code class="inline">POST /api/process</code>:</strong> يستقبل العملية والبارامترات، يمررها للمحرك الحسابي، ويعيد الصورة الناتجة مشفرة مع المعادلة الرياضية وكود بايثون وزمن التنفيذ بالمللي ثانية.
    </p>
</div>

<div class="feature-card no-break">
    <h3>المرحلة الثانية: بناء وتصميم واجهة الاستوديو التفاعلية (Photoshop Pro Experience)</h3>
    <p>
    1. <strong>تصميم القالب الأساسي:</strong> في <code class="inline">resources/views/welcome.blade.php</code>، تم بناء واجهة فوتوشوب داكنة بنظام أشرطة الأدوات العائمة (Left Toolbar، Right Panel، Top Menu).<br>
    2. <strong>لوحة العرض المشطورة (Split Canvas):</strong> ربط لوحتي Canvas متطابقتين للمقارنة الحية بنسبة من 0% إلى 100% مع تحكم كامل بالتقريب (Zoom) والتحريك (Pan).<br>
    3. <strong>المكبر الرقمي 7×7 ومحلل الهستوجرام:</strong> برمجة عرض قيم البكسلات الحقيقية ورسم منحنيات كثافة الألوان حياً.
    </p>
</div>

<div class="feature-card no-break">
    <h3>المرحلة الثالثة: تطوير استوديو الواقع المعزز وتجربة الملحقات (AR Virtual Try-On)</h3>
    <p>
    1. <strong>مودال الملحقات التفاعلي:</strong> بناء واجهة منبثقة منظمة بشبكة كروت تعرض 5 ملحقات شفافة مصممة بدقة عالية.<br>
    2. <strong>محرك التراكب الذكي (Interactive Overlay):</strong> برمجة إمكانية سحب الملحق، تكبيره وتصغيره بنسب دقيقة، التحكم بنسبة شفافيته، وتثبيته كطبقة جديدة.<br>
    3. <strong>نموذج الوجه القياسي:</strong> إدراج زر مباشر لتحميل وجه موديل تجريبي لاختبار الملحقات فورياً.
    </p>
</div>

<div class="feature-card no-break">
    <h3>المرحلة الرابعة: التكامل البرمجي والأتمتة الذكية والـ Git</h3>
    <p>
    1. <strong>الربط الآمن عبر لارافل:</strong> إنشاء الدالة المركزية <code class="inline">sendApiProcess</code> لتوجيه الطلبات عبر مسار لارافل <code class="inline">/api/process</code> مع حماية CSRF.<br>
    2. <strong>أتمتة التشغيل الذكي:</strong> تعديل <code class="inline">python_engine/run.py</code> ليكتشف ويشغل لارافل تلقائياً ويفحص قاعدة البيانات وينقل المستخدم فوراً لصفحة التصميم المنفذ 8000.<br>
    3. <strong>إدارة الـ Git:</strong> رفع التعديلات ومزامنة الفرع وحل التعارضات وفتح طلب الدمج الرسمي <strong>Pull Request #16</strong>.
    </p>
</div>

<div class="page-break"></div>

<!-- SECTION 3: AHMED'S FILES IN THE PROJECT -->
<h1>3. خريطة ملفات أحمد القاضي في المشروع وأماكنها ووظيفتها</h1>
<p>
يوضح هذا الجدول كافة الملفات التي أنشأها أو طورها الطالب أحمد القاضي داخل مستودع المشروع:
</p>

<table>
    <thead>
        <tr>
            <th>اسم الملف (File Name)</th>
            <th>المسار الكامل في المستودع</th>
            <th>اللغة / النوع</th>
            <th>الدور الوظيفي وما كتبه أحمد داخله</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>welcome.blade.php</strong></td>
            <td><code class="inline">resources/views/welcome.blade.php</code></td>
            <td>Blade / HTML5</td>
            <td>واجهة الاستوديو الرئيسية، القوائم العلوية، شريط الأدوات، شاشة المقارنة المقسمة، ومودال استوديو الواقع المعزز AR.</td>
        </tr>
        <tr>
            <td><strong>app.js</strong></td>
            <td><code class="inline">public/js/app.js</code></td>
            <td>JavaScript (ES6+)</td>
            <td>محرك الاستوديو التفاعلي: إدارة الـ DOM، دوال الواقع المعزز، دالة الـ API المركزية <code class="inline">sendApiProcess</code>، والقص والرسم.</td>
        </tr>
        <tr>
            <td><strong>photoshop.css</strong></td>
            <td><code class="inline">public/css/photoshop.css</code></td>
            <td>CSS3 / Dark Theme</td>
            <td>تنسيقات الواجهة بالكامل: المظهر الداكن الفاحم، أزرار الأدوات، كروت الملحقات، وتأثيرات الـ Glassmorphism.</td>
        </tr>
        <tr>
            <td><strong>gestures.css</strong></td>
            <td><code class="inline">public/css/gestures.css</code></td>
            <td>CSS3</td>
            <td>تنسيقات مؤشرات تتبع حركة اليد والإيماءات والكاميرا الحية.</td>
        </tr>
        <tr>
            <td><strong>server.py</strong></td>
            <td><code class="inline">python_engine/app/server.py</code></td>
            <td>Python / Flask</td>
            <td>خادم الخدمات المصغرة، فك تشفير Base64، تصحيح EXIF، توجيه الخوارزميات، والتحويل التلقائي (Redirect) للمنفذ 8000.</td>
        </tr>
        <tr>
            <td><strong>run.py</strong></td>
            <td><code class="inline">python_engine/run.py</code></td>
            <td>Python Core</td>
            <td>محرك التشغيل الشامل: يكتشف ويشغل لارافل تلقائياً في الخلفية ويفتح المتصفح فوراً على صفحة التصميم.</td>
        </tr>
        <tr>
            <td><strong>start_studio.bat</strong></td>
            <td><code class="inline">./start_studio.bat</code></td>
            <td>Windows Batch Script</td>
            <td>سكربت تنفيذي بنقرة واحدة لتشغيل كامل بيئة المشروع (بايثون ولارافل والمتصفح) بدون كتابة أوامر.</td>
        </tr>
        <tr>
            <td><strong>ملحقات الواقع المعزز</strong></td>
            <td><code class="inline">public/accessories/*.png</code></td>
            <td>PNG Alpha Images</td>
            <td>ملفات صور شفافة عالية الجودة (نظارات شمسية، نظارات طبية، قبعة فيدورا، وشاح شتوي، طقم بدلة رسمية).</td>
        </tr>
        <tr>
            <td><strong>صور الاختبار والموديل</strong></td>
            <td><code class="inline">public/samples/*.png</code></td>
            <td>PNG Images</td>
            <td>صور عينات معالجة الصور الرقمية ونموذج الوجه القياسي <code class="inline">portrait_model.png</code>.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 4: DETAILED CODE MAP & LINE NUMBERS -->
<h1>4. خريطة الأكواد وأرقام الأسطر التفصيلية في Blade و App.js</h1>
<p>
جدول دقيق بأرقام الأسطر لتسهيل الاستشهاد البرمجي أثناء العرض والمناقشة:
</p>

<h2>في ملف الواجهة <code class="inline">resources/views/welcome.blade.php</code>:</h2>
<table>
    <thead>
        <tr>
            <th>الأسطر</th>
            <th>الكتلة البرمجية</th>
            <th>الوصف والمحتوى البرمجي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>السطر 6</strong></td>
            <td><code class="inline">&lt;meta name="csrf-token" content="{{ csrf_token() }}"&gt;</code></td>
            <td>توليد رمز الحماية المشفر وتضمينه في رأس الصفحة لحماية كافة طلبات الـ AJAX.</td>
        </tr>
        <tr>
            <td><strong>السطر 26</strong></td>
            <td><code class="inline">&lt;img src="{{ asset('bee_logo.png') }}"&gt;</code></td>
            <td>استدعاء شعار النحل الرسمي عبر مساعد الـ Assets في لارافل.</td>
        </tr>
        <tr>
            <td><strong>السطر 37</strong></td>
            <td><code class="inline">onclick="app.openAccessoriesModal()"</code></td>
            <td>عنصر القائمة العلوية لفتح استوديو الملحقات والواقع المعزز (اختصار Ctrl+Shift+A).</td>
        </tr>
        <tr>
            <td><strong>السطر 258</strong></td>
            <td>زر <code class="inline">#btnToggleAccessories</code></td>
            <td>زر وصول سريع أرجواني بارز في شريط الأدوات العلوي مع إضاءة Glassmorphic.</td>
        </tr>
        <tr>
            <td><strong>الأسطر 270 - 320</strong></td>
            <td>منطقة الـ Viewport و الـ Canvas</td>
            <td>عناصر الـ Raw Canvas والـ Processed Canvas ومقبض المقارنة المنزلق <code class="inline">#splitBar</code>.</td>
        </tr>
        <tr>
            <td><strong>الأسطر 1130 - 1175</strong></td>
            <td>نافذة المودال <code class="inline">#accessoriesModal</code></td>
            <td>الكود الكامل لنافذة استوديو الملحقات والواقع المعزز وشبكة كروت الملحقات الخمسة وزر تحميل الموديل.</td>
        </tr>
    </tbody>
</table>

<h2>في ملف الجافاسكربت <code class="inline">public/js/app.js</code>:</h2>
<table>
    <thead>
        <tr>
            <th>الأسطر</th>
            <th>اسم الدالة البرمجية</th>
            <th>الوظيفة والتحكم البرمجي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>94 - 250</strong></td>
            <td><code class="inline">initDOM()</code></td>
            <td>ربط كافة معرّفات الـ DOM (109 معرّف) بما فيها عناصر الملحقات ونوافذ العرض.</td>
        </tr>
        <tr>
            <td><strong>253 - 290</strong></td>
            <td><code class="inline">applyAccessoryOverlay()</code></td>
            <td>تحميل صورة الملحق الشفافة ورسمها كطبقة تراكب ذكية مع ضبط الإحداثيات والحجم والشفافية.</td>
        </tr>
        <tr>
            <td><strong>1340 - 1370</strong></td>
            <td><code class="inline">sendApiProcess(payload)</code></td>
            <td>الدالة المركزية لإرسال الطلبات إلى لارافل <code class="inline">/api/process</code> مع CSRF وإشعارات Toast.</td>
        </tr>
        <tr>
            <td><strong>1740 - 1775</strong></td>
            <td><code class="inline">applyBlendImages()</code></td>
            <td>مزج صورتين بنسب خلط مرنة وتحديث مراجع الـ DOM <code class="inline">this.formulaBox</code> دون أخطاء.</td>
        </tr>
        <tr>
            <td><strong>1890 - 1925</strong></td>
            <td><code class="inline">applyCollageGrid()</code></td>
            <td>توليد تصاميم الكولاج وشبكات دمج الصور وتمرير الهوامش وألوان الإطارات.</td>
        </tr>
        <tr>
            <td><strong>2015 - 2045</strong></td>
            <td><code class="inline">applyCrop()</code></td>
            <td>اقتصاص الصورة بحسب أبعاد وموقع الإطار التفاعلي وإعادة ضبط الـ Canvas.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 5: BUG FIXES & REFACTORING -->
<h1>5. الأخطاء المكتشفة في الفرونت إند وكيف تم حلها هندسياً</h1>

<div class="feature-card no-break">
    <h3>1. خطأ تجاوز البوابة وأخطاء الـ CORS (Hardcoded Port 5001):</h3>
    <p><strong>المشكلة:</strong> كان كود الواجهة في دوال الاستبدال والكولاج والدمج يستدعي مباشرة <code class="inline">http://127.0.0.1:5001/api/process</code>، مما تسبب في أخطاء حجب الاتصال (CORS Blocked) عند فتح الموقع عبر خادم لارافل.</p>
    <p><strong>الحل الهندسي:</strong> تم توحيد كافة الطلبات عبر دالة ذكية <code class="inline">sendApiProcess</code> توجه الطلب إلى مسار لارافل الأصلي <code class="inline">/api/process</code> وتمرر رمز الحماية <code class="inline">X-CSRF-TOKEN</code> مع توفير خط رجوع تلقائي وتنبيهات Toast تفاعلية للمستخدم.</p>
</div>

<div class="feature-card no-break">
    <h3>2. انهيار الواجهة بسبب تعارض مسميات الـ DOM (TypeErrors):</h3>
    <p><strong>المشكلة:</strong> كان الكود يستدعي <code class="inline">this.formulaEl</code> و <code class="inline">this.codeEl</code>، في حين أن العناصر المعرفة في القالب هي <code class="inline">this.formulaBox</code> و <code class="inline">this.codeSnippet</code>، مما سبب توقف السكربت عند الخطأ: <code class="inline">Cannot set property 'innerText' of undefined</code>.</p>
    <p><strong>الحل الهندسي:</strong> تم تصحيح المسميات ومطابقتها 100% مع الـ Blade، والتحقق آلياً من تكامل كافة الـ 109 معرّف ID و 65 دالة تفاعلية.</p>
</div>

<div class="feature-card no-break">
    <h3>3. غياب مودال الواقع المعزز (Missing AR Modal):</h3>
    <p><strong>المشكلة:</strong> القائمة العلوية كانت تستدعي دالة <code class="inline">openAccessoriesModal</code> بينما هيكل المودال غير موجود في صفحة Blade.</p>
    <p><strong>الحل الهندسي:</strong> تم بناء وتصميم نافذة المودال كاملة وربطها بملحقات المجلد <code class="inline">public/accessories/</code>.</p>
</div>

<div class="feature-card no-break">
    <h3>4. أتمتة تشغيل النظام وتوجيه المستخدم للتصميم مباشرة:</h3>
    <p><strong>المشكلة:</strong> تشغيل بايثون كان يفتح المنفذ 5001 الذي يعطي خطأ 404 لعدم وجود واجهة فيه، وكان يتطلب تشغيل لارافل يدوياً بأمر ثانٍ.</p>
    <p><strong>الحل الهندسي:</strong> تم تحديث <code class="inline">python_engine/run.py</code> ليكتشف ويشغل لارافل تلقائياً في الخلفية ويفحص قاعدة البيانات، ويفتح المتصفح مباشرة على صفحة التصميم <code class="inline">http://127.0.0.1:8000</code>.</p>
</div>

<div class="page-break"></div>

<!-- SECTION 6: COMPLETE MARKDOWN (.md) FILES ARCHITECTURE -->
<h1>6. الشرح المعماري الشامل لكافة ملفات الـ Markdown (.md) في المشروع</h1>
<p>
تعتبر ملفات الـ Markdown (<code class="inline">.md</code>) ركيزة التوثيق والهندسة الاحترافية لأي مشروع مفتوح المصدر على GitHub. يوضح هذا القسم وظيفة كل ملف منها في مشروع VisionCraft بالتفصيل:
</p>

<table>
    <thead>
        <tr>
            <th>اسم الملف (.md)</th>
            <th>الهدف والدور في هندسة البرمجيات</th>
            <th>المحتوى المكتوب داخله في المشروع</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>README.md</strong></td>
            <td>الواجهة التعريفية الأولى للمشروع (Project Landing Page).</td>
            <td>
            - نبذة عن المشروع وأهدافه العلمية في معالجة الصور الرقمية.<br>
            - شارات الجودة (CI Workflow Badges, Tech Stack, License).<br>
            - جدول أعضاء الفريق والمسؤوليات (هارون، أحمد، أمجد، شعيب).<br>
            - دليل التثبيت والتشغيل السريع خطوة بخطوة للطلاب والمقيمين.
            </td>
        </tr>
        <tr>
            <td><strong>AGENTS.md</strong></td>
            <td>سجل توثيق أوامر ومهام وكلاء الذكاء الاصطناعي (AI Chronological Log).</td>
            <td>
            - سجل رسمي يؤرخ كافة المراحل المنفذة منذ بداية إنشاء المشروع.<br>
            - توثيق أوامر الترحيل إلى لارافل، إصلاحات الـ API، خوارزميات الاستوديو، وتقارير الـ PDF.<br>
            - يضمن عدم ضياع السياق البرمجي والتاريخي بين مختلف المطورين والوكلاء.
            </td>
        </tr>
        <tr>
            <td><strong>AI_LOG.md</strong></td>
            <td>سجل الشفافية والتفكير النقدي لاستخدام الذكاء الاصطناعي الأكاديمي.</td>
            <td>
            - يوثق كل جلسة استخدام ذكاء اصطناعي لكل طالب من أعضاء الفريق.<br>
            - يحتوي على مدخل الطالب أحمد القاضي (تأسيس خادم Flask ورفض Django).<br>
            - يثبت للأستاذ أن الفريق يتخذ القرارات الهندسية بناءً على دراسة وتمحيص.
            </td>
        </tr>
        <tr>
            <td><strong>CONTRIBUTING.md</strong></td>
            <td>دليل إرشادات المساهمة للمطورين (Contribution Guidelines).</td>
            <td>
            - قواعد إنشاء الفروع (Branching Naming Conventions).<br>
            - معايير كتابة رسائل الـ Commits (Conventional Commits).<br>
            - خطوات فتح طلبات الدمج (Pull Requests) ونماذج مراجعة الكود.
            </td>
        </tr>
        <tr>
            <td><strong>SECURITY.md</strong></td>
            <td>سياسة الأمان وحماية النظام (Security Policy & Vulnerability Reporting).</td>
            <td>
            - جدول الإصدارات المدعومة بالتحديثات الأمنية.<br>
            - آلية الإبلاغ الآمن عن الثغرات البرمجية دون النشر العلني.<br>
            - تدابير حماية الـ CSRF والتحقق من قيود أحجام الصور المرفوعة.
            </td>
        </tr>
        <tr>
            <td><strong>CODE_OF_CONDUCT.md</strong></td>
            <td>ميثاق وقواعد السلوك المهني (Contributor Covenant Code of Conduct).</td>
            <td>
            - معايير التعامل الأخلاقي والمهني بين أعضاء الفريق والمساهمين.<br>
            - قواعد نبذ التعصب وتشجيع بيئة العمل الإيجابية والتعاون الأكاديمي.
            </td>
        </tr>
        <tr>
            <td><strong>CLAUDE.md</strong></td>
            <td>إرشادات وموجهات الوكلاء البرمجيين ومساعدي التطوير.</td>
            <td>
            - توجيهات مختصرة لبيئة التطوير وأوامر التشغيل ومسارات الخوادم لتسريع استجابة المساعدين الذكيين.
            </td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 7: GIT & GITHUB MASTERY & PR #16 -->
<h1>7. الدليل الكامل للعمل عبر Git و GitHub وتوثيق طلب الدمج PR #16</h1>
<p>
يمثل Git نظام التحكم بالإصدارات المحلي، بينما يمثل GitHub المنصة السحابية لإدارة المشاريع والعمل الجماعي:
</p>

<h2>استراتيجية إدارة الفروع (Branching Strategy):</h2>
<p>
كل عضو في الفريق يمتلك فرعاً مستقلاً يبدأ بـ <code class="inline">feature/</code>، ويمنع الرفع المباشر إلى الفرع الرئيسي <code class="inline">main</code> إلا من خلال طلب دمج (Pull Request) يوافق عليه المشرف:
</p>
<ul>
    <li>فرع الواجهات المخصص لك: <code class="inline">feature/frontend-studio</code></li>
    <li>الفرع الرئيسي للمشروع: <code class="inline">main</code></li>
</ul>

<h2>أهم أوامر Git العملية خطوة بخطوة:</h2>
<pre># 1. فحص حالة الملفات والتأكد من نظافة مساحة العمل
git status

# 2. إضافة الملفات المعدلة
git add resources/ public/ python_engine/ start_studio.bat

# 3. توثيق التعديلات برسالة واضحة
git commit -m "fix(frontend): route API via Laravel gateway, fix DOM references, add error handling and AR accessories studio"

# 4. رفع التعديلات لفرعك على المستودع السحابي
git push -u origin feature/frontend-studio

# 5. سحب آخر تحديثات المشرف وتفادي التعارضات
git fetch origin
git merge origin/main</pre>

<h2>توثيق طلب الدمج الحالي المفتوح: Pull Request #16</h2>
<div class="callout callout-success no-break">
    <strong>تفاصيل طلب الدمج المسجل رسمياً باسم أحمد القاضي:</strong><br>
    - <strong>رقم الطلب:</strong> Pull Request #16<br>
    - <strong>العنوان:</strong> تطوير وإصلاح الواجهة الأمامية: ربط الـ API ببوابة لارافل، تصحيح أخطاء الـ DOM، وبناء استوديو الواقع المعزز<br>
    - <strong>الفرع المصدري:</strong> <code class="inline">feature/frontend-studio</code> ➔ <strong>الفرع المستهدف:</strong> <code class="inline">main</code><br>
    - <strong>حالة الدمج:</strong> <span class="badge badge-success">Able to merge</span> (متوافق بنسبة 100% وبدون أي تعارضات - 0 Conflicts)<br>
    - <strong>الكوميتات الثلاثة المضمنة في الطلب:</strong>
    <ol style="margin:5px 0 0 0; padding-right:20px;">
        <li><code class="inline">a579cae</code>: إصلاحات الفرونت إند وتوجيه الـ API وتصحيح مراجع الـ DOM ومودال الواقع المعزز.</li>
        <li><code class="inline">5729f3b</code>: تطوير التشغيل التلقائي عبر <code class="inline">run.py</code> ونقل المستخدم فوراً لصفحة التصميم.</li>
        <li><code class="inline">69d3ab1</code>: مزامنة الفرع مع آخر تحديثات المستودع وحل كافة التعارضات.</li>
    </ol>
</div>

<div class="page-break"></div>

<!-- SECTION 8: FULL ARCHITECTURE -->
<h1>8. الشرح المعماري لبقية ملفات المشروع (لارافل، بايثون، وقاعدة البيانات)</h1>
<p>
لتكون على دراية كاملة بالمعمارية المتكاملة للنظام والرد على أي سؤال يخص تدفق البيانات:
</p>

<table>
    <thead>
        <tr>
            <th>المكون / المسار</th>
            <th>التقنية</th>
            <th>الوظيفة في معمارية النظام</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code class="inline">routes/web.php</code></td>
            <td>Laravel Routing</td>
            <td>يستقبل طلبات المتصفح على <code class="inline">/</code> ويعرض قالب <code class="inline">welcome.blade.php</code>.</td>
        </tr>
        <tr>
            <td><code class="inline">routes/api.php</code></td>
            <td>Laravel API Routing</td>
            <td>يعرّف مسار <code class="inline">POST /api/process</code> ومسار فحص الصحة <code class="inline">GET /api/health</code>.</td>
        </tr>
        <tr>
            <td><code class="inline">ImageProcessingController.php</code></td>
            <td>Laravel Controller</td>
            <td>يعمل كوسيط عكسي (Reverse Proxy) بنقل الطلبات داخلياً إلى بايثون مع مهلة 60 ثانية للعمليات الكبيرة.</td>
        </tr>
        <tr>
            <td><code class="inline">database/database.sqlite</code></td>
            <td>SQLite Engine</td>
            <td>قاعدة البيانات المحلية لتخزين جلسات العمل (Sessions) وسجلات المستخدمين وتوكنات الحماية.</td>
        </tr>
        <tr>
            <td><code class="inline">python_engine/core/</code></td>
            <td>NumPy / OpenCV</td>
            <td>حزمة الخوارزميات الرياضية العلمية: العمليات النقطية، الفلاتر المكانية، تحويل فوريه 2D-FFT، والمورفولوجيا.</td>
        </tr>
        <tr>
            <td><code class="inline">composer.json</code></td>
            <td>PHP Package Manager</td>
            <td>ملف إدارة مكتبات بيئة لارافل وحزم الـ HTTP Client والـ Framework.</td>
        </tr>
        <tr>
            <td><code class="inline">package.json</code></td>
            <td>Node / Vite</td>
            <td>ملف إدارة حزم الواجهة الأمامية وإعدادات تجميع الأصول (Assets Bundler).</td>
        </tr>
        <tr>
            <td><code class="inline">.env</code></td>
            <td>Environment Config</td>
            <td>ملف متغيرات البيئة المحلية (منافذ الخوادم، مفتاح تشفير التطبيق APP_KEY، واتصال قاعدة البيانات).</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 9: INTERVIEW Q&A -->
<h1>9. بنك الأسئلة المتوقعة في مناقشة المشروع وإجاباتها النموذجية</h1>

<div class="feature-card no-break">
    <h3>س 1: ما هو دورك المحدد في هذا المشروع البرمجي المشترك؟</h3>
    <p><strong>الإجابة النموذجية:</strong> "دوري هو مهندس الواجهات وتجربة المستخدم (Frontend Developer). قمت ببناء استوديو المعالجة الرقمية بمحاكاة فوتوشوب، وتطوير محرك الـ Canvas والمقارنة الحية، واستوديو الواقع المعزز (AR Try-On)، وتأسيس مسارات الـ API في خادم بايثون، وربط الواجهة عبر طلبات AJAX آمنة مع نظام إشعارات حي، وإدارة فرع الواجهة في Git."</p>
</div>

<div class="feature-card no-break">
    <h3>س 2: لماذا اخترتم خادم Flask في بايثون بدلاً من دمج الكود داخل PHP أو استخدام Django؟</h3>
    <p><strong>الإجابة النموذجية:</strong> "وفقاً للتحليل الموثق في الـ AI Log، تم رفض دمج بايثون داخل PHP لأن حزمة php-python غير مستقرة وبطيئة في تمرير المصفوفات لـ OpenCV. وتم رفض Django لأنه إطار ضخم يفرض ميزات إضافية ثقيلة (ORM و Admin) لا نحتاجها، بينما Flask خفيف جداً وأسرع لمعالجة مصفوفات البكسلات الرقمية كخدمة مصغرة (Microservice)."</p>
</div>

<div class="feature-card no-break">
    <h3>س 3: كيف تعمل ميزة مقارنة الصور (Split Canvas Slider) برمجياً؟</h3>
    <p><strong>الإجابة النموذجية:</strong> "نستخدم عنصري Canvas متطابقين تماماً في الأبعاد، ونقوم بالتحكم في شريحة العرض عبر تعديل عرض الحاوية العلوية أو الـ Clip-Path بناءً على نسبة موضع الفأرة من 0% إلى 100% لحظياً دون أي إعادة تحميل للصفحة."</p>
</div>

<div class="feature-card no-break">
    <h3>س 4: ما هي الآلية المتبعة لدمج التعديلات بين أعضاء الفريق في Git؟</h3>
    <p><strong>الإجابة النموذجية:</strong> "اعتمدنا نموذج الفروع الوظيفية (Feature Branch Workflow). كل طالب يعمل على فرعه الخاص (<code class="inline">feature/frontend-studio</code>)، وعند اكتمال الميزة يتم فتح طلب دمج (Pull Request) ومراجعته من المشرف ودمجه في فرع <code class="inline">main</code> بدون أي تعارضات (0 Conflicts) كما هو موثق في طلب الدمج رقم #16."</p>
</div>

<div class="feature-card no-break">
    <h3>س 5: كيف قمت بحل مشكلة الـ CORS وحماية الطلبات؟</h3>
    <p><strong>الإجابة النموذجية:</strong> "قمنا بتوحيد كافة الطلبات عبر بوابة لارافل الداخلية <code class="inline">/api/process</code> التي تعمل كوسيط عكسي (Reverse Proxy)، وقمنا بتمرير رمز الأمان <code class="inline">X-CSRF-TOKEN</code> في رأس الطلب لمنع هجمات التزوير وحل قيود الـ CORS نهائياً."</p>
</div>

<div class="callout callout-success no-break" style="text-align:center; font-weight:bold; margin-top:20px;">
    تم بحمد الله وتوفيقه إعداد هذا المرجع الأكاديمي الشامل ليكون عوناً وسنداً للطالب في مسيرته الأكاديمية والمهنية.
</div>

</body>
</html>
"""

def generate_pdf():
    desktop_dir = r"C:\Users\ucer\Desktop"
    project_docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs"))
    
    desktop_pdf_path = os.path.join(desktop_dir, "دليل_مهندس_الواجهة_الأمامية_VisionCraft.pdf")
    docs_pdf_path = os.path.join(project_docs_dir, "VisionCraft_Frontend_Engineering_Manual.pdf")
    temp_html_path = os.path.join(project_docs_dir, "temp_frontend_manual.html")

    os.makedirs(project_docs_dir, exist_ok=True)

    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print(f"[PDF Generator] Rendering updated comprehensive PDF via Playwright Chromium...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(f"file:///{temp_html_path.replace(os.sep, '/')}", wait_until="networkidle")
        
        # Print to Desktop PDF
        page.pdf(
            path=desktop_pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "0mm",
                "bottom": "0mm",
                "left": "0mm",
                "right": "0mm"
            }
        )
        print(f"[PDF Generator] Successfully generated Desktop PDF: {desktop_pdf_path}")

        # Also print to Docs PDF in project
        page.pdf(
            path=docs_pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "0mm",
                "bottom": "0mm",
                "left": "0mm",
                "right": "0mm"
            }
        )
        print(f"[PDF Generator] Successfully saved in Project Docs: {docs_pdf_path}")

        browser.close()

    # Also make English named copy on Desktop
    english_desktop_pdf = os.path.join(desktop_dir, "VisionCraft_Frontend_Engineering_Manual.pdf")
    try:
        import shutil
        shutil.copyfile(desktop_pdf_path, english_desktop_pdf)
        print(f"[PDF Generator] Copied to English desktop path: {english_desktop_pdf}")
    except Exception as e:
        print(f"Warning copying to English desktop path: {e}")

    # Cleanup temp html
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

if __name__ == "__main__":
    generate_pdf()
