# -*- coding: utf-8 -*-
"""
VisionCraft DIP Studio - API Documentation PDF Generator
Generates a comprehensive, publication-quality technical report in PDF format.
"""

import os
from playwright.sync_api import sync_playwright

HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<title>تقرير توثيق وهندسة واجهة برمجة التطبيقات (API) - VisionCraft DIP Studio</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Fira+Code:wght@400;600&display=swap');

    @page {
        size: A4;
        margin: 20mm 15mm 20mm 15mm;
        @bottom-left {
            content: "VisionCraft DIP Studio - تقرير هندسة وتوثيق الـ API";
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
        font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 10.5pt;
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
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 25mm 15mm 15mm 15mm;
        text-align: center;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #311042 100%);
        color: #ffffff;
        border-radius: 8px;
    }

    .cover-header {
        border-bottom: 2px solid rgba(255, 215, 0, 0.4);
        padding-bottom: 20px;
    }

    .univ-title {
        font-size: 13pt;
        font-weight: 600;
        color: #94a3b8;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .faculty-title {
        font-size: 11pt;
        color: #cbd5e1;
        margin-bottom: 4px;
    }

    .cover-body {
        margin: auto 0;
    }

    .project-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.5);
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 10.5pt;
        font-weight: 700;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    .cover-main-title {
        font-size: 26pt;
        font-weight: 900;
        line-height: 1.3;
        margin-bottom: 12px;
        background: linear-gradient(90deg, #ffffff, #fef08a, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .cover-sub-title {
        font-size: 14pt;
        font-weight: 600;
        color: #93c5fd;
        margin-bottom: 25px;
    }

    .cover-description {
        font-size: 11pt;
        color: #cbd5e1;
        max-width: 85%;
        margin: 0 auto;
        line-height: 1.8;
    }

    .cover-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 10pt;
        color: #94a3b8;
    }

    /* Standard Content Styling */
    h1 {
        font-size: 18pt;
        font-weight: 800;
        color: #0f172a;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    h1 .badge-num {
        background: #3b82f6;
        color: #fff;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 11pt;
        margin-left: 8px;
    }

    h2 {
        font-size: 14pt;
        font-weight: 700;
        color: #1e3a8a;
        margin-top: 20px;
        margin-bottom: 10px;
        border-right: 4px solid #f59e0b;
        padding-right: 10px;
    }

    h3 {
        font-size: 12pt;
        font-weight: 700;
        color: #334155;
        margin-top: 14px;
        margin-bottom: 8px;
    }

    p {
        margin: 0 0 10px 0;
        text-align: justify;
    }

    ul, ol {
        margin: 0 0 12px 0;
        padding-right: 22px;
    }

    li {
        margin-bottom: 5px;
    }

    /* Callout Boxes */
    .callout {
        border-radius: 8px;
        padding: 12px 16px;
        margin: 14px 0;
        font-size: 10pt;
        page-break-inside: avoid;
    }

    .callout-info {
        background: #eff6ff;
        border-right: 4px solid #3b82f6;
        color: #1e40af;
    }

    .callout-tip {
        background: #f0fdf4;
        border-right: 4px solid #22c55e;
        color: #15803d;
    }

    .callout-warning {
        background: #fffbeb;
        border-right: 4px solid #f59e0b;
        color: #b45309;
    }

    .callout-title {
        font-weight: 700;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 9.5pt;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 8px 10px;
        text-align: right;
    }

    th {
        background-color: #0f172a;
        color: #ffffff;
        font-weight: 700;
    }

    tr:nth-child(even) {
        background-color: #f8fafc;
    }

    /* Badges */
    .tag {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 8.5pt;
        font-weight: 700;
        font-family: 'Fira Code', monospace;
    }

    .tag-post { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .tag-get { background: #dbeafe; color: #1d4ed8; border: 1px solid #93c5fd; }
    .tag-ws { background: #fae8ff; color: #86198f; border: 1px solid #f0abfc; }

    /* Code blocks */
    pre, code {
        font-family: 'Fira Code', Consolas, monospace;
        direction: ltr;
        text-align: left;
    }

    pre {
        background: #0f172a;
        color: #e2e8f0;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 8.5pt;
        overflow-x: auto;
        line-height: 1.5;
        border: 1px solid #334155;
        page-break-inside: avoid;
        margin: 10px 0;
    }

    code:not(pre code) {
        background: #f1f5f9;
        color: #0f172a;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 9pt;
        border: 1px solid #e2e8f0;
    }

    /* Architecture Visual Diagram Box */
    .arch-diagram {
        background: #f8fafc;
        border: 2px dashed #94a3b8;
        border-radius: 10px;
        padding: 18px;
        margin: 18px 0;
        text-align: center;
        page-break-inside: avoid;
    }

    .arch-grid {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        direction: rtl;
    }

    .arch-box {
        flex: 1;
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 12px 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }

    .arch-box.highlight-laravel {
        border-top: 4px solid #ef4444;
    }
    .arch-box.highlight-python {
        border-top: 4px solid #3b82f6;
    }
    .arch-box.highlight-frontend {
        border-top: 4px solid #10b981;
    }

    .arch-title {
        font-weight: 700;
        font-size: 10.5pt;
        margin-bottom: 4px;
        color: #0f172a;
    }

    .arch-desc {
        font-size: 8.5pt;
        color: #64748b;
        line-height: 1.4;
    }

    .arch-arrow {
        font-size: 16pt;
        color: #94a3b8;
        font-weight: bold;
    }

    .meta-box {
        display: flex;
        gap: 20px;
        margin-bottom: 15px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 10px 15px;
        border-radius: 6px;
        font-size: 9pt;
    }

    .meta-item {
        display: flex;
        gap: 6px;
    }
    .meta-label { font-weight: 700; color: #475569; }
    .meta-value { color: #0f172a; }
</style>
</head>
<body>

<!-- صفحة الغلاف -->
<div class="cover-page">
    <div class="cover-header">
        <div class="univ-title">جامعة ذمار - كلية الحاسبات والمعلوماتية</div>
        <div class="faculty-title">قسم هندسة البرمجيات (Software Engineering) - المستوى الرابع</div>
        <div class="faculty-title">مشروع تخرج: استوديو معالجة الصور الرقمية وتطبيق الواقع المعزز (VisionCraft)</div>
    </div>

    <div class="cover-body">
        <div class="project-badge">وثيقة هندسية رسمية • Technical Specification Report</div>
        <div class="cover-main-title">دليل وهندسة واجهة برمجة التطبيقات<br>(API Architecture & Specifications)</div>
        <div class="cover-sub-title">تحليل معماري شامل لآلية عمل الـ API، مسارات الربط، البروتوكولات الحسابية، ونواة المعالجة الثنائية (Laravel & Python)</div>
        
        <div class="cover-description">
            يقدم هذا التقرير تحليلاً هندسياً دقيقاً ومفصلاً لجميع نقاط النهاية (Endpoints)، هيكلية تدفق البيانات (Data Flow Pipeline)، نسق الرسائل (JSON Schema & Protocols)، والوظائف الرياضية لمكتبات OpenCV و NumPy المدعومة داخل المنظومة.
        </div>
    </div>

    <div class="cover-footer">
        <div><strong>إعداد وتطوير:</strong> فريق مشروع VisionCraft Studio</div>
        <div><strong>النسخة:</strong> Release v1.0 • 2026</div>
    </div>
</div>

<div class="page-break"></div>

<!-- فهرس المحتويات -->
<h1><span class="badge-num">1</span> الملخص التنفيذي وهيكلية النظام (System Architecture)</h1>

<p>
يعتمد استوديو <strong>VisionCraft DIP Studio</strong> على نمط معماري متقدم يُعرف بـ <strong>المعمارية الخدمية المصغرة الثنائية (Dual-Core Microservices Architecture)</strong> التي تفصل بذكاء بين بيئة إدارة المستخدمين وتوجيه الطلبات من جهة، وبيئة الحسابات العلمية المكثفة ومعالجة المصفوفات الرياضية من جهة أخرى.
</p>

<div class="arch-diagram">
    <div style="font-weight:700; font-size:11pt; margin-bottom:12px; color:#1e293b;">مخطط تدفق البيانات ومعمارية المنظومة (Architecture Data Flow)</div>
    <div class="arch-grid">
        <div class="arch-box highlight-frontend">
            <div class="arch-title">🌐 واجهة الويب (Client)</div>
            <div class="arch-desc">Photoshop Canvas UI<br>JavaScript / WebSockets<br>أخذ لقطة Base64</div>
        </div>
        <div class="arch-arrow">⮂</div>
        <div class="arch-box highlight-laravel">
            <div class="arch-title">🛡️ بوابة لارافيل (API Gateway)</div>
            <div class="arch-desc">Laravel 11 / PHP 8.2+<br>مسارات <code>routes/api.php</code><br>Reverse Proxy & Validation</div>
        </div>
        <div class="arch-arrow">⮂</div>
        <div class="arch-box highlight-python">
            <div class="arch-title">⚡ محرك بايثون العلمي (Engine)</div>
            <div class="arch-desc">Flask Microservice (Port 5001)<br>OpenCV + NumPy + SciPy<br>تنفيذ خوارزميات الـ DIP</div>
        </div>
    </div>
</div>

<h2>1.1 لماذا تم استخدام هذا النمط المعماري؟</h2>
<ul>
    <li><strong>أقصى كفاءة حسابية (High Computational Throughput):</strong> لغة بايثون بمكتباتها المكتوبة بلغة C/C++ (مثل OpenCV و NumPy و SciPy) توفر أداءً فائقاً في ضرب المصفوفات، التحويل الترددي السريع (2D Fast Fourier Transform)، والتعامل مع بكسلات الصورة مقارنةً بـ PHP.</li>
    <li><strong>فصل الاهتمامات (Separation of Concerns):</strong> يتفرغ خادم Laravel لإدارة الجلسات، التخزين المؤقت، المسارات، وأمان التطبيق، بينما يتفرغ خادم بايثون حصرياً للحسابات الجبرية للصور.</li>
    <li><strong>قابلية التوسع المستقل (Independent Scalability):</strong> يمكن مستقبلاً نقل خادم بايثون ليعمل على خوادم مجهزة بمعالجات رسومية (GPU Servers) دون أي تعديل على كود الواجهة أو خادم Laravel.</li>
</ul>

<div class="callout callout-info">
    <div class="callout-title">ℹ️ معلومة هندسية حول مسار الاتصال</div>
    يقوم التطبيق بالربط بطريقتين: إما بشكل مباشر وفائق السرعة من واجهة الويب إلى محرك بايثون <code>http://127.0.0.1:5001/api/process</code> لتجنب تأخير النقل (Lowest Latency)، أو عبر وسيط لارافيل <code>/api/process</code> كبوابة خلفية معتمدة.
</div>

<div class="page-break"></div>

<!-- قسم نقاط النهاية والبروتوكول -->
<h1><span class="badge-num">2</span> نقاط النهاية وبروتوكول الاتصال (API Endpoints & Protocol)</h1>

<p>
تعتمد واجهة برمجة التطبيقات على بروتوكول <strong>RESTful JSON HTTP</strong> لجميع الطلبات الفردية والتفاعلية، بالإضافة إلى بروتوكول <strong>WebSocket (Flask-SocketIO)</strong> للمهام الفورية وبث الإطارات المباشرة.
</p>

<h2>2.1 جدول نقاط النهاية المعتمدة (Endpoints Summary)</h2>

<table>
    <thead>
        <tr>
            <th style="width: 14%;">البروتوكول</th>
            <th style="width: 26%;">المسار (URI)</th>
            <th style="width: 25%;">الطبقة المستضيفة</th>
            <th style="width: 35%;">الوظيفة التقنية</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="tag tag-post">POST</span></td>
            <td><code>/api/process</code></td>
            <td>Laravel Gateway & Python Engine</td>
            <td>نقطة المعالجة المركزية، تستقبل الصورة والمعاملات وتعيد الصورة الناتجة والمقاييس.</td>
        </tr>
        <tr>
            <td><span class="tag tag-get">GET</span></td>
            <td><code>/api/health</code></td>
            <td>Laravel Gateway & Python Engine</td>
            <td>فحص نبض وجاهزية محرك المعالجة وتوافر مكتبات OpenCV.</td>
        </tr>
        <tr>
            <td><span class="tag tag-ws">WebSocket</span></td>
            <td><code>socket.io / process_frame</code></td>
            <td>Python Microservice Engine</td>
            <td>قناة ثنائية الاتجاه لمعالجة الإطارات اللحظية من الكاميرا بمعدل يصل لـ 60 FPS.</td>
        </tr>
    </tbody>
</table>

<h2>2.2 نقطة النهاية المركزية: <code>POST /api/process</code></h2>
<p>
تمثل هذه النقطة الشريان الأساسي لعمل الاستوديو، حيث تستقبل طلباً بهيئة <strong>JSON</strong> مشفراً بـ <code>application/json</code>، وتقوم بفك تشفير الصورة، معالجة اتجاه الدوران الذكي، تطبيق الخوارزمية المطلوبة، ثم تشفير النتيجة وإرجاعها في غضون أجزاء من الثانية.
</p>

<h3>أ. بنية الطلب (Request Payload Schema)</h3>
<pre><code>{
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "operation": "canny",
  "params": {
    "t1": 50,
    "t2": 150,
    "sigma": 1.4,
    "extract_palette": false
  }
}</code></pre>

<table>
    <thead>
        <tr>
            <th>الحقل (Field)</th>
            <th>النوع (Type)</th>
            <th>إلزامي؟</th>
            <th>الوصف التقني</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>image</code></td>
            <td>String (Base64)</td>
            <td>نعم</td>
            <td>بيانات الصورة الأصلية إما بصيغة Data-URL أو سلسلة Base64 نقية بصيغ (PNG, JPEG, WEBP).</td>
        </tr>
        <tr>
            <td><code>operation</code></td>
            <td>String</td>
            <td>نعم</td>
            <td>معرّف العملية الرياضية المطلوب تنفيذها (مثل: <code>gaussian</code>, <code>sobel</code>, <code>remove_background</code>).</td>
        </tr>
        <tr>
            <td><code>params</code></td>
            <td>Object (Dict)</td>
            <td>اختياري</td>
            <td>قاموس يحتوي على المعاملات العددية والخيارات الخاصة بالخوارزمية المحددة.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h3>ب. بنية الاستجابة القياسية (Response Payload Schema)</h3>
<p>
تستخدم المنظومة كائناً معيارياً يُدعى <code>ProcessingResult</code>، حيث يقوم بتجميع مخرجات الحسابات الرياضية في نسق موحد وغني بالبيانات:
</p>

<pre><code>{
  "status": "success",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...",
  "execution_time_ms": 14.85,
  "formula": "g(x,y) = |G_x| + |G_y| \\quad \\text{(Canny Magnitude & NMS)}",
  "code": "edges = cv2.Canny(gray, threshold1=50, threshold2=150)",
  "histogram": {
    "gray": [120, 450, 890, ...],   /* 64 حزمة إحصائية Bins */
    "r": [...], "g": [...], "b": [...]
  },
  "stats": {
    "width": 800,
    "height": 600,
    "channels": 3,
    "mean": 128.45,
    "std_dev": 42.10,
    "median": 125.0,
    "entropy": 7.42                 /* الإنتروبيا: مقياس كثافة وعشوائية المعلومات */
  },
  "palette": ["#1a2b3c", "#f4a261", "#e76f51"]  /* اختياري في عمليات الألوان */
}</code></pre>

<table>
    <thead>
        <tr>
            <th>عنصر الاستجابة</th>
            <th>النوع</th>
            <th>الأهمية والفائدة في واجهة المستخدم</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>image</code></td>
            <td>Base64 URI</td>
            <td>يتم عرضه فوراً داخل لوحة العرض (HTML5 Canvas) ودمجه مع طبقات الفوتوشوب.</td>
        </tr>
        <tr>
            <td><code>execution_time_ms</code></td>
            <td>Float</td>
            <td>يغذي شارة الأداء الحي (Performance Badge) لتبيان سرعة المعالجة اللحظية للمستخدم.</td>
        </tr>
        <tr>
            <td><code>histogram</code></td>
            <td>Object (Arrays)</td>
            <td>يُرسم مباشرة في نافذة المدرج التكراري الحي (Live Histogram Visualizer) للقنوات RGB والرمادي.</td>
        </tr>
        <tr>
            <td><code>stats</code></td>
            <td>Object</td>
            <td>يحدد المتوسط الحسابي، الانحراف المعياري، والإنتروبيا (Shannon Entropy) لتقييم تباين وجودة الصورة.</td>
        </tr>
        <tr>
            <td><code>formula</code> & <code>code</code></td>
            <td>String</td>
            <td>يُعرض في لوحة الشرح الأكاديمي لإظهار المعادلة الرياضية وكود بايثون المقابل لها للمستخدم.</td>
        </tr>
    </tbody>
</table>

<div class="callout callout-tip">
    <div class="callout-title">💡 ميزة فريدة: القيمة التعليمية والهندسية</div>
    لا يكتفي الـ API بإرجاع الصورة المعالجة فحسب، بل يرفق مع كل استجابة المعادلة الفيزيائية والرياضية المطبقة بالإضافة إلى كود بايثون البرمجي المقابل لها، مما يحول الاستوديو إلى أداة تعليمية وأكاديمية متكاملة لمساق معالجة الصور الرقمية.
</div>

<div class="page-break"></div>

<!-- قسم كتالوج العمليات -->
<h1><span class="badge-num">3</span> كتالوج العمليات والخوارزميات المدعومة (Operations Catalog)</h1>

<p>
يدعم محرك المعالجة أكثر من 30 خوارزمية موزعة على 8 مجالات هندسية متخصصة. يوضح الجدول التالي تفاصيل كل عملية ومعاملاتها:
</p>

<h2>3.1 عمليات النقاط والمستوى الرمادي (Point Operations)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>القيمة الافتراضية</th>
            <th>الوصف الرياضي والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>negative</code></td>
            <td>لا يوجد</td>
            <td>-</td>
            <td>عكس قيم البكسلات: <code>s = 255 - r</code> لإنتاج الصورة السالبة.</td>
        </tr>
        <tr>
            <td><code>log</code></td>
            <td><code>c</code> (مقياس التوسيع)</td>
            <td><code>1.0</code></td>
            <td>التحويل اللوغاريتمي: <code>s = c * log(1 + r)</code> لإبراز التفاصيل المعتمة.</td>
        </tr>
        <tr>
            <td><code>gamma</code></td>
            <td><code>gamma</code> (قيمة غاما)</td>
            <td><code>1.0</code></td>
            <td>قانون القوى (Power-law): <code>s = c * r^gamma</code> لتصحيح شدة الإضاءة.</td>
        </tr>
        <tr>
            <td><code>brightness_contrast</code></td>
            <td><code>brightness</code>, <code>contrast</code></td>
            <td><code>0, 1.0</code></td>
            <td>تعديل خطي للسطوع والتباين: <code>g(x,y) = contrast * f(x,y) + brightness</code>.</td>
        </tr>
        <tr>
            <td><code>threshold</code></td>
            <td><code>threshold</code>, <code>method</code></td>
            <td><code>128, "binary"</code></td>
            <td>التقطيع الثنائي للصور وتحويلها إلى أبيض وأسود بناءً على حد عتبة.</td>
        </tr>
        <tr>
            <td><code>histogram_equalization</code></td>
            <td><code>method</code>, <code>clip_limit</code></td>
            <td><code>"global", 2.0</code></td>
            <td>مساواة الهستوغرام (عالمي أو محلي ذكي متكيف CLAHE) لتحسين التباين.</td>
        </tr>
    </tbody>
</table>

<h2>3.2 المرشحات المكانية وتنعيم الصور (Spatial Filtering)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>القيمة الافتراضية</th>
            <th>الوصف الرياضي والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>gaussian</code></td>
            <td><code>ksize</code>, <code>sigma</code></td>
            <td><code>5, 1.4</code></td>
            <td>تنعيم غاوسي عبر مصفوفة التفافية بحجم فردي لتقليل الضوضاء.</td>
        </tr>
        <tr>
            <td><code>box_blur</code></td>
            <td><code>ksize</code></td>
            <td><code>5</code></td>
            <td>مرشح المتوسط الحسابي (Mean Box Filter) للتنعيم المتماثل.</td>
        </tr>
        <tr>
            <td><code>median</code></td>
            <td><code>ksize</code></td>
            <td><code>5</code></td>
            <td>مرشح الوسيط الإحصائي غير الخطي، مثالي لإزالة ضوضاء الملح والفلفل.</td>
        </tr>
        <tr>
            <td><code>wiener</code></td>
            <td><code>ksize</code></td>
            <td><code>5</code></td>
            <td>مرشح التقدير التكيفي للتنعيم مع الحفاظ على التباين الموضعي.</td>
        </tr>
        <tr>
            <td><code>bilateral</code></td>
            <td><code>d</code>, <code>sigma_color</code>, <code>sigma_space</code></td>
            <td><code>9, 75, 75</code></td>
            <td>تنعيم فائق مع الحفاظ الدقيق على الحواف وحماية ملامح الوجوه.</td>
        </tr>
        <tr>
            <td><code>custom_kernel</code></td>
            <td><code>kernel</code> (مصفوفة 3x3)</td>
            <td>مصفوفة شارب</td>
            <td>تطبيق مصفوفة التفاف مخصصة يُدخلها المستخدم يدوياً عبر الـ API.</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>3.3 كشف الحواف والاشتقاق المكاني (Edge Detection)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>القيمة الافتراضية</th>
            <th>الوصف الرياضي والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>sobel</code></td>
            <td><code>ksize</code></td>
            <td><code>3</code></td>
            <td>حساب مشتقات الصورة عبر نوى سوبل الأفقية والعمودية لاستخراج الحواف.</td>
        </tr>
        <tr>
            <td><code>prewitt</code></td>
            <td>لا يوجد</td>
            <td>-</td>
            <td>كشف الحواف عبر أقنعة بريويت التفاضلية الخطية.</td>
        </tr>
        <tr>
            <td><code>laplacian</code></td>
            <td><code>ksize</code></td>
            <td><code>3</code></td>
            <td>المشتقة المكانية من الدرجة الثانية لكشف الحواف السريعة ومناطق التغير الفجائي.</td>
        </tr>
        <tr>
            <td><code>canny</code></td>
            <td><code>t1</code>, <code>t2</code>, <code>sigma</code></td>
            <td><code>50, 150, 1.4</code></td>
            <td>الخوارزمية المثالية لكشف الحواف مع قمع غير العظمى (Non-Max Suppression).</td>
        </tr>
        <tr>
            <td><code>unsharp_mask</code></td>
            <td><code>sigma</code>, <code>strength</code></td>
            <td><code>1.5, 1.5</code></td>
            <td>تقنية تعزيز الحدة بطرح الصورة المنعمة من الأصلية ثم إعادة دمجها بمقياس قوة.</td>
        </tr>
    </tbody>
</table>

<h2>3.4 العمليات المورفولوجية على الأشكال (Morphology)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>الوصف الرياضي والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>erosion</code> / <code>dilation</code></td>
            <td><code>ksize</code>, <code>shape</code>, <code>iterations</code></td>
            <td>التآكل (تقليص المساحات البيضاء) والاتساع (توسيع وتعبئة الفجوات).</td>
        </tr>
        <tr>
            <td><code>opening</code> / <code>closing</code></td>
            <td><code>ksize</code>, <code>shape</code></td>
            <td>الفتح (تآكل ثم اتساع لإزالة النتوءات) والإغلاق (اتساع ثم تآكل لغلق الثغرات).</td>
        </tr>
        <tr>
            <td><code>morph_gradient</code></td>
            <td><code>ksize</code></td>
            <td>التدرج المورفولوجي: الفارق بين الاتساع والتآكل لاستخلاص محيط الأجسام.</td>
        </tr>
        <tr>
            <td><code>skeleton</code></td>
            <td>لا يوجد</td>
            <td>استخراج الهيكل النحيف الداخلي للأجسام الثنائية (Skeletonization).</td>
        </tr>
    </tbody>
</table>

<h2>3.5 النطاق الترددي والترميم (Frequency Domain & FFT)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>الوصف الرياضي والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>fft_spectrum</code></td>
            <td>لا يوجد</td>
            <td>حساب طيف الطور والشدة للتحويل الترددي ثنائي الأبعاد 2D-FFT وعرضه بصرياً.</td>
        </tr>
        <tr>
            <td><code>frequency_filter</code></td>
            <td><code>filter_type</code>, <code>cutoff</code>, <code>filter_model</code></td>
            <td>مرشحات التردد المنخفض والعالي (Low/High Pass) بنماذج Ideal و Butterworth و Gaussian.</td>
        </tr>
        <tr>
            <td><code>notch_filter</code></td>
            <td><code>notches</code> (مصفوفة إحداثيات), <code>d0</code></td>
            <td>مرشح حجب الترددات الدورية (Notch Reject Filter) للقضاء على أنماط تموجات المواريه (Moiré).</td>
        </tr>
        <tr>
            <td><code>motion_deblur</code></td>
            <td><code>length</code>, <code>angle</code>, <code>snr</code></td>
            <td>عكس تشوه الحركة وإزالة التغبيش الحركي عبر التفكيك الترددي العكسي (Wiener Deconvolution).</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h2>3.6 تركيب وتكوين الاستوديو (Studio Composition & Superpowers)</h2>
<table>
    <thead>
        <tr>
            <th>العملية (Operation)</th>
            <th>المعاملات (Parameters)</th>
            <th>الوصف الفني والتطبيقي</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>remove_background</code></td>
            <td><code>margin</code>, <code>iterations</code>, <code>sigma</code></td>
            <td>عزل ذكي للخلفية عبر خوارزمية GrabCut الرياضية التكرارية وتحويل الصورة إلى BGRA شفافة.</td>
        </tr>
        <tr>
            <td><code>replace_background</code></td>
            <td><code>bg_type</code>, <code>bg_color</code>, <code>bg_image</code></td>
            <td>استبدال خلفية الصورة المفروغة إما بلون نقي أو بصورة مخصصة ثانية.</td>
        </tr>
        <tr>
            <td><code>blend_images</code></td>
            <td><code>second_image</code>, <code>alpha</code>, <code>mode</code></td>
            <td>دمج صورتين بأنماط متعددة (خطي، شاشة، ضرب، أو تراكب رياضي).</td>
        </tr>
        <tr>
            <td><code>add_text</code></td>
            <td><code>text</code>, <code>x</code>, <code>y</code>, <code>font_size</code>, <code>color</code></td>
            <td>رسم نصوص عربية وإنجليزية عالية الدقة باستخدام مكتبة Pillow مع دعم الخطوط الحرة.</td>
        </tr>
        <tr>
            <td><code>photo_collage</code></td>
            <td><code>images</code>, <code>template</code>, <code>border_size</code></td>
            <td>توليد شبكات كولاج وتجميع للصور بقوالب شبكية (Grid 2x2, Vertical 1+2, etc.).</td>
        </tr>
    </tbody>
</table>

<hr style="border:0; border-top:1px solid #cbd5e1; margin:25px 0;">

<h1><span class="badge-num">4</span> متانة النظام والأمان وإدارة الأداء (Performance & Reliability)</h1>

<p>
تم تدعيم بنية الـ API بمجموعة من التدابير الهندسية الصارمة لضمان استقرار النظام تحت الحمولات الحسابية العالية:
</p>

<ol>
    <li>
        <strong>التصحيح التلقائي لتدوير الهواتف (Auto EXIF Transposition):</strong>
        تتضمن بعض الصور الملتقطة بكاميرات الهواتف الذكية وسوماً تدويرية (EXIF Tags). يقوم المحرك بقراءة هذه الوسوم وتصحيح زاوية الصورة فورياً عبر <code>ImageOps.exif_transpose</code> قبل بدء المعالجة حتى لا تظهر مقلوبة للمستخدم.
    </li>
    <li>
        <strong>آلية النقل الاحتياطي وفك التشفير (Robust Decoding Pipeline):</strong>
        يستخدم النظام خطة معالجة ذات مرحلتين لفك تشفير مصفوفة الصورة: تبدأ بمحرك Pillow المتقدم، وفي حال وجود بيانات غير متوافقة يتم الانتقال تلقائياً إلى <code>cv2.imdecode</code> الاحتياطي لضمان عدم انهيار الـ API.
    </li>
    <li>
        <strong>إدارة المهل الزمنية وحماية الذاكرة (Timeout & Payload Management):</strong>
        نظراً لأن بعض العمليات مثل GrabCut و 2D-FFT تتطلب قدرات حسابية، تم ضبط مهلة وسيط لارافيل <code>Http::timeout(60)</code> بحد أقصى 60 ثانية، مع ضغط البيانات عبر صيغة JPEG/PNG لمنع تجاوز حد حمولة الذاكرة المسموح بها في خادم الويب (POST Max Size).
    </li>
    <li>
        <strong>تواصل الكاميرا اللحظي عبر WebSocket:</strong>
        لتشغيل ميزات الواقع المعزز (AR Mirror) وكشف الحواف اللحظي، يوفر المحرك اتصال WebSocket دائم عبر <code>socketio</code> يتيح معالجة الإطارات اللحظية دون إنشاء أو إغلاق اتصالات HTTP متكررة، مما يوفر سرعة استجابة فائقة (Sub-30ms Latency).
    </li>
</ol>

<div class="callout callout-info" style="margin-top:20px;">
    <div class="callout-title">📋 خاتمة التقرير الهندسي</div>
    تثبت هندسة الـ API في مشروع <strong>VisionCraft DIP Studio</strong> قدرة استثنائية على الجمع بين مرونة وأناقة إطار العمل <strong>Laravel</strong> والسرعة والقدرة الرياضية الخارقة لمكتبات <strong>Python & OpenCV</strong>، مما يوفر بيئة استوديو فوتوشوب متكاملة تلبي أعلى المتطلبات الأكاديمية والمهنية.
</div>

</body>
</html>
"""

def generate_pdf():
    output_pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "VisionCraft_API_Architecture_Report.pdf"))
    temp_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_report.html"))

    print(f"Writing temporary HTML to {temp_html_path}...")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    print("Launching Playwright Chromium...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the local file
        file_url = f"file:///{temp_html_path.replace(os.sep, '/')}"
        page.goto(file_url, wait_until="networkidle")
        
        # Print to PDF with full colors and exact margins
        page.pdf(
            path=output_pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "0mm",
                "bottom": "0mm",
                "left": "0mm",
                "right": "0mm"
            }
        )
        browser.close()

    print(f"PDF generated successfully at: {output_pdf_path}")
    
    # Clean up temporary HTML
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

if __name__ == "__main__":
    generate_pdf()
