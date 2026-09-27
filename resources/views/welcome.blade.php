<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>🐝 VisionCraft Studio - Digital Image Processing & AR Mirror</title>
    <link rel="icon" type="image/x-icon" href="{{ asset('favicon.ico') }}">
    <link rel="icon" type="image/png" sizes="64x64" href="{{ asset('bee_logo.png') }}">
    <link rel="apple-touch-icon" href="{{ asset('bee_logo.png') }}">
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('css/photoshop.css') }}">
    <link rel="stylesheet" href="{{ asset('css/gestures.css') }}">
</head>
<body>

    <!-- Hidden file inputs for uploading custom images, overlay, and background -->
    <input type="file" id="fileInput" accept="image/*" style="display: none;">
    <input type="file" id="overlayFileInput" accept="image/*" style="display: none;">
    <input type="file" id="bgFileInput" accept="image/*" style="display: none;">

    <!-- 1. TOP MENU BAR WITH FUNCTIONAL DROPDOWNS -->
    <div class="ps-menubar">
        <div class="ps-menu-left">
            <div class="ps-icon-badge" title="VisionCraft Bee Studio 🐝" onclick="alert('VisionCraft Bee Studio 🐝\nGraduation Project Level Four - Digital Image Processing\nPowered by Pure Python, OpenCV, NumPy & HTML5 Canvas')">
                <img src="{{ asset('bee_logo.png') }}" alt="VisionCraft Bee Logo">
            </div>
            
            <!-- File Menu -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item">File</span>
                <div class="ps-dropdown-content">
                    <div class="ps-dropdown-item" onclick="document.getElementById('fileInput').click()"><span>Open Image...</span><span style="color:#888;">Ctrl+O</span></div>
                    <div class="ps-dropdown-item" onclick="app.openCollageModal()"><span>📐 قوالب الكولاج وشبكات دمج الصور (Collage Grid)...</span><span style="color:#f59e0b;">Ctrl+Shift+G</span></div>
                    <div class="ps-dropdown-item" onclick="app.openBlendModal()"><span>🖼️ دمج صورتين (Blend Two Images)...</span><span style="color:#10b981;">Ctrl+Shift+M</span></div>
                    <div class="ps-dropdown-item" onclick="document.getElementById('overlayFileInput').click()"><span>Place Image (Overlay / Watermark)...</span><span style="color:#00e5ff;">Ctrl+Shift+P</span></div>
                    <div class="ps-dropdown-item" onclick="app.openAccessoriesModal()"><span style="color:#c084fc;">👓 استوديو الملحقات والواقع المعزز (AR Try-On)...</span><span style="color:#a855f7;">Ctrl+Shift+A</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.loadSampleImage('portrait_model.png')"><span style="color:#00e5ff;">👤 Load Portrait Face Model (AR Try-On)</span></div>
                    <div class="ps-dropdown-item" onclick="app.loadSampleImage('benchmark.png')"><span>Load Benchmark Test Pattern</span></div>
                    <div class="ps-dropdown-item" onclick="app.loadSampleImage('noisy.png')"><span>Load Noisy Image (Salt & Pepper)</span></div>
                    <div class="ps-dropdown-item" onclick="app.loadSampleImage('low_contrast.png')"><span>Load Low-Contrast Image</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.downloadResult()"><span>Quick Export as PNG</span><span style="color:#888;">Ctrl+S</span></div>
                </div>
            </div>

            <!-- Edit Menu -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item">Edit</span>
                <div class="ps-dropdown-content">
                    <div class="ps-dropdown-item" onclick="app.undo()"><span style="color:#00e5ff;">↩️ Undo (تراجع)</span><span style="color:#00e5ff;">Ctrl+Z</span></div>
                    <div class="ps-dropdown-item" onclick="app.redo()"><span style="color:#00e5ff;">↪️ Redo (إعادة)</span><span style="color:#00e5ff;">Ctrl+Y / Ctrl+Shift+Z</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.copyPythonCode()"><span>Copy Generated Python Code</span><span style="color:#888;">Ctrl+C</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('none', {}, 'Original Image', '')"><span>Revert to Original Image</span><span style="color:#888;">F12</span></div>
                </div>
            </div>

            <!-- Image Menu (Point Operations & Adjustments) -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item">Image</span>
                <div class="ps-dropdown-content">
                    <div class="ps-dropdown-item" onclick="app.openCollageModal()"><span>📐 قوالب الكولاج وشبكات دمج الصور (Collage Grid)...</span><span style="color:#f59e0b;">Ctrl+Shift+G</span></div>
                    <div class="ps-dropdown-item" onclick="app.openBlendModal()"><span>🖼️ دمج ومزج صورتين (DIP Blend)...</span><span style="color:#10b981;">Ctrl+Shift+M</span></div>
                    <div class="ps-dropdown-item" onclick="app.activateBackgroundRemovalTool()"><span style="color:#00e5ff;">✂️ موازنة وتفريغ عزل الخلفية (Background Removal)...</span><span style="color:#00e5ff;">Ctrl+Shift+B</span></div>
                    <div class="ps-dropdown-item" onclick="app.openBgReplaceModal()"><span>🌅 استبدال الخلفية بصورة أخرى أو استوديو...</span></div>
                    <div class="ps-dropdown-item" onclick="app.openAccessoriesModal()"><span style="color:#c084fc;">👓 تجربة الملحقات الافتراضية (AR Virtual Try-On)...</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('negative', {}, 'Negative Invert', '')"><span>Invert Negative</span><span style="color:#888;">Ctrl+I</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('color_space', {target: 'gray'}, 'Convert to Grayscale', '')"><span>Grayscale Mode</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('histogram_equalization', {method: 'global'}, 'Histogram Equalization', '')"><span>Histogram Equalization (Global)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('histogram_equalization', {method: 'clahe', clip_limit: 2.0}, 'Adaptive Equalization (CLAHE)', '<div class=\'ps-prop-row\'><span>Clip Limit:</span><span id=\'val_clip_limit\' style=\'color:#fff;\'>2.0</span></div><input type=\'range\' class=\'ps-range\' min=\'1\' max=\'10\' step=\'0.5\' value=\'2.0\' data-param=\'clip_limit\'>')"><span>Adaptive CLAHE Equalization</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('gamma', {gamma: 0.6}, 'Gamma Correction', '<div class=\'ps-prop-row\'><span>Gamma (γ):</span><span id=\'val_gamma\' style=\'color:#fff;\'>0.6</span></div><input type=\'range\' class=\'ps-range\' min=\'0.1\' max=\'3.0\' step=\'0.05\' value=\'0.6\' data-param=\'gamma\'>')"><span>Gamma / Power-Law Correction</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('log', {c: 1.0}, 'Logarithmic Transform', '<div class=\'ps-prop-row\'><span>Scaling (c):</span><span id=\'val_c\' style=\'color:#fff;\'>1.0</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'2.5\' step=\'0.1\' value=\'1.0\' data-param=\'c\'>')"><span>Logarithmic Transform</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('threshold', {threshold: 128, method: 'binary'}, 'Binary Thresholding', '<div class=\'ps-prop-row\'><span>Threshold (T):</span><span id=\'val_threshold\' style=\'color:#fff;\'>128</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'128\' data-param=\'threshold\'>')"><span>Binary Thresholding</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('threshold', {method: 'otsu'}, 'Otsu Thresholding (Optimal)', '')"><span>Otsu Global Auto-Threshold</span></div>
                </div>
            </div>

            <!-- Filters Menu (Core Image Processing Algorithms) -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item" style="color:#ffffff; font-weight:700;">Filter (معالجة الصور)</span>
                <div class="ps-dropdown-content" style="min-width: 260px;">
                    <!-- Edge Detectors -->
                    <div class="ps-dropdown-item" onclick="app.setFilter('canny', {t1: 50, t2: 150, sigma: 1.4}, 'Canny Edge Detector', '<div class=\'ps-prop-row\'><span>High Threshold (T2):</span><span id=\'val_t2\' style=\'color:#fff;\'>150</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'150\' data-param=\'t2\'><div class=\'ps-prop-row\'><span>Low Threshold (T1):</span><span id=\'val_t1\' style=\'color:#fff;\'>50</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'50\' data-param=\'t1\'><div class=\'ps-prop-row\'><span>Gaussian Sigma:</span><span id=\'val_sigma\' style=\'color:#fff;\'>1.4</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'4.0\' step=\'0.1\' value=\'1.4\' data-param=\'sigma\'>')"><span><b>🔍 Canny Multi-stage Edge Detector</b></span><span style="color:#00e5ff;">Optimal</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('sobel', {ksize: 3}, 'Sobel Gradient Filter', '<div class=\'ps-prop-row\'><span>Kernel Size:</span><span id=\'val_ksize\' style=\'color:#fff;\'>3</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'7\' step=\'2\' value=\'3\' data-param=\'ksize\'>')"><span>Sobel Gradient (Gx + Gy)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('prewitt', {}, 'Prewitt Edge Filter', '')"><span>Prewitt Gradient</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('laplacian', {ksize: 3}, 'Laplacian 2nd Derivative', '')"><span>Laplacian (∇²f)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('unsharp_mask', {sigma: 1.5, strength: 1.5}, 'Unsharp Masking (High-Boost)', '')"><span>Unsharp Mask / High-Boost</span></div>
                    <div class="ps-dropdown-separator"></div>

                    <!-- Smoothing & Denoise & Restoration -->
                    <div class="ps-dropdown-item" onclick="app.setFilter('gaussian', {ksize: 5, sigma: 1.4}, 'Separable Gaussian Blur', '<div class=\'ps-prop-row\'><span>Sigma (σ):</span><span id=\'val_sigma\' style=\'color:#fff;\'>1.4</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'5.0\' step=\'0.2\' value=\'1.4\' data-param=\'sigma\'>')"><span><b>🌊 Gaussian Blur (Separable O(2K))</b></span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('median', {ksize: 5}, 'Median Filter (Salt & Pepper)', '<div class=\'ps-prop-row\'><span>Kernel Window:</span><span id=\'val_ksize\' style=\'color:#fff;\'>5</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'15\' step=\'2\' value=\'5\' data-param=\'ksize\'>')"><span>Median Filter (Noise Removal)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('wiener', {ksize: 5}, 'Wiener Filter (MMSE)', '<div class=\'ps-prop-row\'><span>Window Size:</span><span id=\'val_ksize\' style=\'color:#fff;\'>5</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'11\' step=\'2\' value=\'5\' data-param=\'ksize\'>')"><span>Wiener Filter (Optimal Denoise)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('motion_deblur', {length: 15, angle: 45, snr: 0.01}, 'Motion Deblur (Wiener PSF Restoration)', '<div class=\'ps-prop-row\'><span>Motion Length:</span><span id=\'val_length\' style=\'color:#fff;\'>15px</span></div><input type=\'range\' class=\'ps-range\' min=\'2\' max=\'60\' value=\'15\' data-param=\'length\'><div class=\'ps-prop-row\'><span>Motion Angle (θ):</span><span id=\'val_angle\' style=\'color:#fff;\'>45°</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'180\' value=\'45\' data-param=\'angle\'><div class=\'ps-prop-row\'><span>Regularization (K):</span><span id=\'val_snr\' style=\'color:#fff;\'>0.01</span></div><input type=\'range\' class=\'ps-range\' min=\'0.001\' max=\'0.08\' step=\'0.002\' value=\'0.01\' data-param=\'snr\'>')"><span><b>✨ Motion Deblur (Wiener Deconvolution)</b></span><span style="color:#00e5ff;">Restoration</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('bilateral', {d: 9, sigma_color: 75, sigma_space: 75}, 'Bilateral Filter', '')"><span>Bilateral Edge-Preserving Blur</span></div>
                    <div class="ps-dropdown-separator"></div>

                    <!-- Morphology -->
                    <div class="ps-dropdown-item" onclick="app.setFilter('erosion', {ksize: 5, shape: 'rect', iterations: 1}, 'Morphological Erosion', '')"><span><b>📐 Erosion (A ⊖ B)</b></span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('dilation', {ksize: 5, shape: 'rect', iterations: 1}, 'Morphological Dilation', '')"><span>Dilation (A ⊕ B)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('opening', {ksize: 5, shape: 'rect'}, 'Morphological Opening', '')"><span>Opening (Erode then Dilate)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('closing', {ksize: 5, shape: 'rect'}, 'Morphological Closing', '')"><span>Closing (Dilate then Erode)</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('skeleton', {}, 'Skeletonization (Thinning)', '')"><span>Morphological Skeleton</span></div>
                    <div class="ps-dropdown-separator"></div>

                    <!-- Frequency FFT -->
                    <div class="ps-dropdown-item" onclick="app.setFilter('fft_spectrum', {}, '2D-FFT Magnitude Spectrum', '')"><span><b>📡 2D-FFT Magnitude Spectrum</b></span></div>
                    <div class="ps-dropdown-item" onclick="app.openNotchModal()"><span><b>🎯 Interactive Notch Reject Filter</b></span><span style="color:#00e5ff;">Moiré Clean</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('frequency_filter', {filter_type: 'lowpass', cutoff: 40.0, filter_model: 'gaussian'}, 'Gaussian Low-Pass Frequency Filter', '')"><span>Frequency Low-Pass Filter</span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('frequency_filter', {filter_type: 'highpass', cutoff: 40.0, filter_model: 'gaussian'}, 'Gaussian High-Pass Frequency Filter', '')"><span>Frequency High-Pass Filter</span></div>
                    <div class="ps-dropdown-separator"></div>

                    <!-- Color & K-Means -->
                    <div class="ps-dropdown-item" onclick="app.setFilter('color_splash', {target_bgr: [0, 0, 220], tolerance: 24}, 'Color Splash (Selective Hue Slicing)', '<div class=\'ps-prop-row\'><span>Hue Tolerance (ΔH):</span><span id=\'val_tolerance\' style=\'color:#fff;\'>24°</span></div><input type=\'range\' class=\'ps-range\' min=\'8\' max=\'60\' value=\'24\' data-param=\'tolerance\'>')"><span><b>🎨 Color Splash (Selective Color Slicing)</b></span></div>
                    <div class="ps-dropdown-item" onclick="app.setFilter('kmeans', {k: 4}, 'K-Means Color Quantization', '<div class=\'ps-prop-row\'><span>Clusters (K):</span><span id=\'val_k\' style=\'color:#fff;\'>4</span></div><input type=\'range\' class=\'ps-range\' min=\'2\' max=\'10\' value=\'4\' data-param=\'k\'>')"><span>K-Means Color Segmentation</span></div>
                </div>
            </div>

            <!-- View Menu -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item">View</span>
                <div class="ps-dropdown-content">
                    <div class="ps-dropdown-item" onclick="app.zoomStep(1.25)"><span>Zoom In</span><span style="color:#888;">Ctrl++</span></div>
                    <div class="ps-dropdown-item" onclick="app.zoomStep(0.8)"><span>Zoom Out</span><span style="color:#888;">Ctrl+-</span></div>
                    <div class="ps-dropdown-item" onclick="app.resetZoom()"><span>Actual Pixels (100%)</span><span style="color:#888;">Ctrl+0</span></div>
                    <div class="ps-dropdown-item" onclick="app.fitToScreen()"><span>Fit on Screen</span><span style="color:#888;">Ctrl+1</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="app.setSplitPercent(50)"><span>Reset Compare Split to 50%</span></div>
                    <div class="ps-dropdown-item" onclick="app.setSplitPercent(0)"><span>Show 100% Processed</span></div>
                    <div class="ps-dropdown-item" onclick="app.setSplitPercent(100)"><span>Show 100% Original</span></div>
                </div>
            </div>

            <!-- Help Menu -->
            <div class="ps-menu-dropdown">
                <span class="ps-menu-item">Help</span>
                <div class="ps-dropdown-content">
                    <div class="ps-dropdown-item" onclick="app.openShortcutsModal()"><span>⌨️ Keyboard Shortcuts...</span><span style="color:#00e5ff;">F1 / ?</span></div>
                    <div class="ps-dropdown-separator"></div>
                    <div class="ps-dropdown-item" onclick="alert('🐝 VisionCraft Studio (Bee Edition)\nGraduation Project Level Four - Digital Image Processing\nPowered by Pure Python, OpenCV, NumPy & HTML5 Canvas')"><span>🐝 About VisionCraft Bee Studio</span></div>
                </div>
            </div>
        </div>

        <div class="ps-menu-right">
            <span id="perfBadge" style="background:#003426; border:1px solid #00875a; color:#36b37e; font-size:10px; padding:2px 8px; border-radius:3px; font-family:'Fira Code'; font-weight:600;">⚡ Ready</span>
        </div>
    </div>

    <!-- 2. TOOL OPTIONS BAR -->
    <div class="ps-optionsbar">
        <div class="ps-tool-active-icon">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="#00e5ff"><path d="M10 9h4V6h3l-5-5-5 5h3v3zm-1 1H6V7l-5 5 5 5v-3h3v-4zm11 2l-5-5v3h-3v4h3v3l5-5zm-9 3h-4v3H3l5 5 5-5h-3v-3z"/></svg>
            <span id="filterTitle" style="color:#ffffff;">Original Image</span>
        </div>
        <div style="width:1px; height:18px; background:var(--ps-border);"></div>
        
        <div class="ps-opt-item">
            <span>Blend Mode:</span>
            <select class="ps-select" id="blendModeSelect" onchange="app.setBlendMode(this.value)">
                <option value="normal">Normal</option>
                <option value="screen">Screen (Neon Glow FX)</option>
                <option value="color-dodge">Color Dodge</option>
                <option value="multiply">Multiply</option>
                <option value="overlay">Overlay</option>
                <option value="difference">Difference</option>
            </select>
        </div>
        <div class="ps-opt-item">
            <span>Opacity:</span>
            <input type="text" class="ps-input ps-input-num" id="layerOpacityInput" value="100%" oninput="app.setLayerOpacity(this.value)">
        </div>

        <!-- Crop Controls (Visible when Crop tool is active) -->
        <div id="cropOptionsBar" style="display:none; align-items:center; gap:8px; background:rgba(245,158,11,0.12); padding:2px 10px; border-radius:3px; border:1px solid rgba(245,158,11,0.4);">
            <span style="color:#f59e0b; font-weight:bold;">✂️ Crop:</span>
            <span>Ratio:</span>
            <select id="cropRatioSelect" class="ps-select" style="width:75px; font-size:11px;" onchange="app.setCropRatio(this.value)">
                <option value="free">Free</option>
                <option value="1:1">1:1</option>
                <option value="4:3">4:3</option>
                <option value="16:9">16:9</option>
            </select>
            <span id="cropDimensionsLabel" style="color:#fff; font-family:'Fira Code'; font-size:11px;">0 × 0 px</span>
            <button class="ps-btn ps-btn-accent" style="background:#d97706; border-color:#f59e0b; padding:1px 8px; font-size:11px;" onclick="app.applyCrop()">Apply Crop</button>
            <button class="ps-btn" style="padding:1px 6px; font-size:11px;" onclick="app.cancelCrop()">Cancel</button>
        </div>

        <!-- Drawing Suite Controls (Visible when Draw/Paint tool is active) -->
        <div id="drawOptionsBar" style="display:none; align-items:center; gap:8px; background:rgba(168,85,247,0.12); padding:2px 10px; border-radius:3px; border:1px solid rgba(168,85,247,0.4);">
            <span style="color:#c084fc; font-weight:bold;">🎨 Draw:</span>
            <select id="drawShapeSelect" class="ps-select" style="width:95px; font-size:11px;" onchange="app.setDrawShape(this.value)">
                <option value="pen">🖌 Pen / Brush</option>
                <option value="rect">⬛ Rectangle</option>
                <option value="circle">⭕ Circle</option>
                <option value="line">📏 Line</option>
                <option value="arrow">➔ Arrow</option>
                <option value="eraser">🧹 Eraser</option>
            </select>
            <span>Size:</span>
            <input type="range" class="ps-range" style="width:65px;" min="1" max="60" value="4" id="drawStrokeSizeSlider" oninput="app.setDrawStrokeSize(this.value)">
            <span id="drawStrokeSizeLabel" style="color:#fff; min-width:26px; font-size:11px;">4px</span>
            <span>Color:</span>
            <input type="color" id="drawColorPicker" value="#00e5ff" style="width:24px; height:20px; border:none; padding:0; background:transparent; cursor:pointer;" onchange="app.setDrawColor(this.value)">
            <span>Fill:</span>
            <input type="checkbox" id="drawFillCheckbox" onchange="app.setDrawFill(this.checked)" title="Fill shape with color">
            <button class="ps-btn" style="padding:1px 6px; font-size:11px;" onclick="app.clearDrawingLayer()">Clear</button>
            <button class="ps-btn ps-btn-accent" style="background:#7c3aed; border-color:#a855f7; padding:1px 8px; font-size:11px;" onclick="app.mergeDrawingToImage()">Merge Down</button>
        </div>

        <!-- Brush Controls (Visible when Selective Brush tool is active) -->
        <div id="brushOptionsBar" style="display:none; align-items:center; gap:8px; background:rgba(0,229,255,0.08); padding:2px 8px; border-radius:3px; border:1px solid rgba(0,229,255,0.3);">
            <span style="color:#00e5ff; font-weight:bold;">🖌 Brush:</span>
            <span>Size:</span>
            <input type="range" class="ps-range" style="width:70px;" min="5" max="150" value="35" id="brushSizeSlider" oninput="app.setBrushSize(this.value)">
            <span id="brushSizeLabel" style="color:#fff; min-width:32px;">35px</span>
            <span>Feather:</span>
            <input type="range" class="ps-range" style="width:60px;" min="0" max="100" value="50" id="brushFeatherSlider" oninput="app.setBrushFeather(this.value)">
            <button class="ps-btn" style="padding:1px 6px; font-size:10px;" onclick="app.clearBrushMask()">Clear Mask</button>
        </div>

        <!-- Text Tool Controls (Visible when Text tool is active) -->
        <div id="textOptionsBar" style="display:none; align-items:center; gap:8px; background:rgba(20,115,230,0.12); padding:2px 10px; border-radius:3px; border:1px solid rgba(20,115,230,0.4);">
            <span style="color:#4597f7; font-weight:bold;">🔤 Typography:</span>
            <input type="text" id="textOverlayInput" class="ps-input" placeholder="اكتب النص هنا..." value="VisionCraft Studio" style="width:150px; font-size:11px;" onkeydown="if(event.key==='Enter')app.applyTextToImage()">
            <select id="textFontFamily" class="ps-select" style="width:85px; font-size:11px;">
                <option value="tahoma">Tahoma</option>
                <option value="segoe">Segoe UI</option>
                <option value="arial">Arial</option>
                <option value="impact">Impact</option>
            </select>
            <span>Size:</span>
            <input type="number" id="textFontSize" class="ps-input ps-input-num" min="12" max="180" value="42" style="width:45px; font-size:11px;">
            <span>Color:</span>
            <input type="color" id="textOverlayColor" value="#ffffff" style="width:24px; height:20px; border:none; padding:0; background:transparent; cursor:pointer;">
            <button class="ps-btn ps-btn-accent" style="padding:1px 8px; font-size:11px;" onclick="app.applyTextToImage()">Render Text</button>
            <button class="ps-btn" style="padding:1px 6px; font-size:11px;" onclick="app.cancelTextTool()">Cancel</button>
        </div>

        <!-- Overlay Image Controls (Visible when an overlay image is placed) -->
        <div id="overlayOptionsBar" style="display:none; align-items:center; gap:8px; background:rgba(16,185,129,0.12); padding:2px 10px; border-radius:3px; border:1px solid rgba(16,185,129,0.4);">
            <span style="color:#10b981; font-weight:bold;">🖼 Overlay:</span>
            <span>Scale:</span>
            <input type="range" class="ps-range" style="width:70px;" min="0.1" max="2.5" step="0.05" value="1.0" id="overlayScaleSlider" oninput="app.setOverlayScale(this.value)">
            <span id="overlayScaleLabel" style="color:#fff; min-width:32px;">1.0x</span>
            <span>Opacity:</span>
            <input type="range" class="ps-range" style="width:60px;" min="0.05" max="1.0" step="0.05" value="1.0" id="overlayOpacitySlider" oninput="app.setOverlayOpacity(this.value)">
            <span id="overlayOpacityLabel" style="color:#fff; min-width:32px;">100%</span>
            <button class="ps-btn ps-btn-accent" style="background:#059669; border-color:#10b981; padding:1px 8px; font-size:11px;" onclick="app.applyOverlayToImage()">Merge Down</button>
        </div>

        <div style="margin-left:auto; display:flex; gap:8px; align-items:center;">
            <button class="ps-btn" id="btnToggleAccessories" style="border-color:#a855f7; color:#c084fc; background:rgba(168,85,247,0.12);" onclick="app.openAccessoriesModal()" title="Virtual Try-On / Accessories Studio (👓)">👓 AR Try-On</button>
            <button class="ps-btn" id="btnToggleLoupe" style="border-color:#00e5ff; color:#00e5ff;" onclick="app.togglePixelLoupe()" title="Toggle 7x7 Numeric Pixel Matrix Loupe">🔬 7×7 Matrix HUD</button>
            <button class="ps-btn" onclick="app.setSplitPercent(50)" title="مقارنة الصورة الأصلية والمعالجة بنسبة 50%">Split 50%</button>
            <button class="ps-btn ps-btn-accent" onclick="app.copyPythonCode()" title="نسخ كود بايثون العلمي المقابل للفلتر">📋 Copy Python Code</button>
            <button class="ps-btn" style="background:#1b4d3e; border-color:#2a7e66;" onclick="app.openExportModal()" title="حفظ وتصدير الصورة وتحويل الصيغ (PNG, JPG, WEBP, BMP)">💾 Export & Convert</button>
        </div>
    </div>

    <!-- 3. MAIN WORKSPACE -->
    <div class="ps-workspace">

        <!-- PHOTOSHOP DYNAMIC TOOLBAR WITH TABBED FLYOUT GROUPS -->
        <div class="ps-toolbar" id="psToolbar">
            
            <!-- 1. Move Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn active" title="Move Tool (V)" onclick="app.activateToolGroup(this, 'move')">
                    <svg viewBox="0 0 24 24"><path d="M10 9h4V6h3l-5-5-5 5h3v3zm-1 1H6V7l-5 5 5 5v-3h3v-4zm11 2l-5-5v3h-3v4h3v3l5-5zm-9 3h-4v3H3l5 5 5-5h-3v-3z"/></svg>
                </div>
            </div>

            <!-- 1.2 Cutout & Background Removal Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" id="btnCutoutTool" title="أداة موازنة وتفريغ عزل الخلفية (Background Removal Tool) - Ctrl+Shift+B" onclick="app.activateBackgroundRemovalTool(this)">
                    <svg viewBox="0 0 24 24"><path d="M9.64 7.64c.23-.5.36-1.05.36-1.64 0-2.21-1.79-4-4-4S2 3.79 2 6s1.79 4 4 4c.59 0 1.14-.13 1.64-.36L10 12l-2.36 2.36C7.14 14.13 6.59 14 6 14c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4c0-.59-.13-1.14-.36-1.64L12 14l7 7h3v-1L9.64 7.64zM6 8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm0 12c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm6-7.5c-.28 0-.5-.22-.5-.5s.22-.5.5-.5.5.22.5.5-.22.5-.5.5zM19 3l-6 6 2 2 7-7V3h-3z"/></svg>
                </div>
            </div>

            <!-- 1.5 Crop Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" id="btnCropTool" title="Crop Tool - أداة القص وتأطير الصورة (C)" onclick="app.activateToolGroup(this, 'crop')">
                    <svg viewBox="0 0 24 24"><path d="M17 15h2V7c0-1.1-.9-2-2-2H9v2h8v8zM7 17V1H5v4H1v2h4v10c0 1.1.9 2 2 2h10v4h2v-4h4v-2H7z"/></svg>
                </div>
            </div>

            <!-- 2. Geometry & Transform Group -->
            <div class="ps-tool-group" id="groupTransform">
                <div class="ps-tbtn has-flyout" id="btnGroupTransform" title="Geometry & Transform Tools (C)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M17 15h2V7c0-1.1-.9-2-2-2H9v2h8v8zM7 17V1H5v4H1v2h4v10c0 1.1.9 2 2 2h10v4h2v-4h4v-2H7z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">التحويلات الهندسية والقص (Transform)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('rotate', {angle: 45, scale: 1.0}, 'Rotate 45° (Affine)', '<div class=\'ps-prop-row\'><span>Angle (θ):</span><span id=\'val_angle\' style=\'color:#fff;\'>45°</span></div><input type=\'range\' class=\'ps-range\' min=\'-180\' max=\'180\' value=\'45\' data-param=\'angle\'><div class=\'ps-prop-row\'><span>Scale:</span><span id=\'val_scale\' style=\'color:#fff;\'>1.0x</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'2.0\' step=\'0.1\' value=\'1.0\' data-param=\'scale\'>', 'groupTransform')">
                        <span class="ps-flyout-item-name">🔄 تدوير حر (Arbitrary Rotation)</span><span class="ps-flyout-item-badge">R</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('resize', {scale: 0.6, interpolation: 'bicubic'}, 'Resize (Bicubic Interpolation)', '<div class=\'ps-prop-row\'><span>Scale Factor:</span><span id=\'val_scale\' style=\'color:#fff;\'>0.6x</span></div><input type=\'range\' class=\'ps-range\' min=\'0.1\' max=\'2.0\' step=\'0.05\' value=\'0.6\' data-param=\'scale\'>', 'groupTransform')">
                        <span class="ps-flyout-item-name">📐 تغيير الحجم بالاستيفاء (Resize Bicubic)</span><span class="ps-flyout-item-badge">S</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('flip', {mode: 'horizontal'}, 'Flip Horizontal', '', 'groupTransform')">
                        <span class="ps-flyout-item-name">⇄ انعكاس أفقي (Flip Horizontal)</span><span class="ps-flyout-item-badge">H</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('flip', {mode: 'vertical'}, 'Flip Vertical', '', 'groupTransform')">
                        <span class="ps-flyout-item-name">⇅ انعكاس رأسي (Flip Vertical)</span><span class="ps-flyout-item-badge">V</span>
                    </div>
                </div>
            </div>

            <!-- 3. Point Operations & Adjustments Group -->
            <div class="ps-tool-group" id="groupPoint">
                <div class="ps-tbtn has-flyout" id="btnGroupPoint" title="Point Operations & Adjustments (Ctrl+L)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18V4c4.41 0 8 3.59 8 8s-3.59 8-8 8z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">العمليات النقطية والهستوغرام (Point Operations)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('histogram_equalization', {method: 'global'}, 'Global Histogram Equalization', '', 'groupPoint')">
                        <span class="ps-flyout-item-name">📊 تسوية الهستوغرام (Global Equalize)</span><span class="ps-flyout-item-badge">LUT</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('histogram_equalization', {method: 'clahe', clip_limit: 2.0}, 'Adaptive CLAHE Equalization', '<div class=\'ps-prop-row\'><span>Clip Limit:</span><span id=\'val_clip_limit\' style=\'color:#fff;\'>2.0</span></div><input type=\'range\' class=\'ps-range\' min=\'1\' max=\'10\' step=\'0.5\' value=\'2.0\' data-param=\'clip_limit\'>', 'groupPoint')">
                        <span class="ps-flyout-item-name">📈 تسوية تكيفية CLAHE</span><span class="ps-flyout-item-badge">Local</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('gamma', {gamma: 0.6}, 'Gamma Power-Law Correction', '<div class=\'ps-prop-row\'><span>Gamma (γ):</span><span id=\'val_gamma\' style=\'color:#fff;\'>0.6</span></div><input type=\'range\' class=\'ps-range\' min=\'0.1\' max=\'3.0\' step=\'0.05\' value=\'0.6\' data-param=\'gamma\'>', 'groupPoint')">
                        <span class="ps-flyout-item-name">⚡ تصحيح جاما (Gamma Power-Law)</span><span class="ps-flyout-item-badge">s=cr^γ</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('log', {c: 1.0}, 'Logarithmic Transform', '<div class=\'ps-prop-row\'><span>Scaling (c):</span><span id=\'val_c\' style=\'color:#fff;\'>1.0</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'2.5\' step=\'0.1\' value=\'1.0\' data-param=\'c\'>', 'groupPoint')">
                        <span class="ps-flyout-item-name">🪵 التحويل اللوغاريتمي (Log Transform)</span><span class="ps-flyout-item-badge">s=log(1+r)</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.activateThresholdCutout()">
                        <span class="ps-flyout-item-name">✂️ عزل وقص الخلفية بالعتبة (Threshold Cutout)</span><span class="ps-flyout-item-badge">T1/T2</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('threshold', {threshold: 128, method: 'binary'}, 'Binary Thresholding', '<div class=\'ps-prop-row\'><span>Threshold (T):</span><span id=\'val_threshold\' style=\'color:#fff;\'>128</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'128\' data-param=\'threshold\'>', 'groupPoint')">
                        <span class="ps-flyout-item-name">🔲 العتبة الثنائية (Binary Threshold)</span><span class="ps-flyout-item-badge">T</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('threshold', {method: 'otsu'}, 'Otsu Global Auto-Threshold', '', 'groupPoint')">
                        <span class="ps-flyout-item-name">🎯 عتبة أوتسو الذاتية (Otsu Optimal)</span><span class="ps-flyout-item-badge">Auto</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('negative', {}, 'Invert Negative', '', 'groupPoint')">
                        <span class="ps-flyout-item-name">🎞 العكس السالب (Invert Negative)</span><span class="ps-flyout-item-badge">255-r</span>
                    </div>
                </div>
            </div>

            <!-- 4. Edge Detection Group -->
            <div class="ps-tool-group" id="groupEdges">
                <div class="ps-tbtn has-flyout" id="btnGroupEdges" title="Edge Detection Tools (E)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">كشف الحواف والمشتقات (Edge Detection)</div>
                    <div class="ps-flyout-item selected" onclick="app.selectSubTool('canny', {t1: 50, t2: 150, sigma: 1.4}, 'Canny Multi-stage Edge Detector', '<div class=\'ps-prop-row\'><span>High Threshold (T2):</span><span id=\'val_t2\' style=\'color:#fff;\'>150</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'150\' data-param=\'t2\'><div class=\'ps-prop-row\'><span>Low Threshold (T1):</span><span id=\'val_t1\' style=\'color:#fff;\'>50</span></div><input type=\'range\' class=\'ps-range\' min=\'0\' max=\'255\' value=\'50\' data-param=\'t1\'><div class=\'ps-prop-row\'><span>Gaussian Sigma:</span><span id=\'val_sigma\' style=\'color:#fff;\'>1.4</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'4.0\' step=\'0.1\' value=\'1.4\' data-param=\'sigma\'>', 'groupEdges')">
                        <span class="ps-flyout-item-name">🔍 كاشف كاني متعدد المراحل (Canny)</span><span class="ps-flyout-item-badge">Optimal</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('sobel', {ksize: 3}, 'Sobel Gradient Filter (Gx + Gy)', '<div class=\'ps-prop-row\'><span>Kernel Size:</span><span id=\'val_ksize\' style=\'color:#fff;\'>3</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'7\' step=\'2\' value=\'3\' data-param=\'ksize\'>', 'groupEdges')">
                        <span class="ps-flyout-item-name">📐 مشتقات سوبل (Sobel Gradient)</span><span class="ps-flyout-item-badge">∇f</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('prewitt', {}, 'Prewitt Edge Filter', '', 'groupEdges')">
                        <span class="ps-flyout-item-name">📏 مرشح بريويت (Prewitt Edge)</span><span class="ps-flyout-item-badge">[-1 0 1]</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('laplacian', {ksize: 3}, 'Laplacian 2nd Derivative', '', 'groupEdges')">
                        <span class="ps-flyout-item-name">⚡ لابلاسيان المشتقة الثانية (Laplacian)</span><span class="ps-flyout-item-badge">∇²f</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('unsharp_mask', {sigma: 1.5, strength: 1.5}, 'Unsharp Masking (High-Boost)', '', 'groupEdges')">
                        <span class="ps-flyout-item-name">✨ قناع تعزيز الوضوح (Unsharp Mask)</span><span class="ps-flyout-item-badge">HighBoost</span>
                    </div>
                </div>
            </div>

            <!-- 5. Smoothing & Denoise Group -->
            <div class="ps-tool-group" id="groupBlur">
                <div class="ps-tbtn has-flyout" id="btnGroupBlur" title="Smoothing & Denoise Tools (R)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M12 2c-5.33 4-8 8-8 12a8 8 0 0 0 16 0c0-4-2.67-8-8-12zm0 18a6 6 0 0 1-6-6c0-3.1 1.9-6.3 6-9.7 4.1 3.4 6 6.6 6 9.7a6 6 0 0 1-6 6z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">التنعيم وتصفية الضوضاء (Blur & Denoise)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('gaussian', {ksize: 5, sigma: 1.4}, 'Separable Gaussian Blur O(2K)', '<div class=\'ps-prop-row\'><span>Sigma (σ):</span><span id=\'val_sigma\' style=\'color:#fff;\'>1.4</span></div><input type=\'range\' class=\'ps-range\' min=\'0.2\' max=\'5.0\' step=\'0.2\' value=\'1.4\' data-param=\'sigma\'>', 'groupBlur')">
                        <span class="ps-flyout-item-name">🌊 تنعيم جاوس القابل للفصل (Gaussian)</span><span class="ps-flyout-item-badge">O(2K)</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('median', {ksize: 5}, 'Median Noise Filter', '<div class=\'ps-prop-row\'><span>Kernel Window:</span><span id=\'val_ksize\' style=\'color:#fff;\'>5</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'15\' step=\'2\' value=\'5\' data-param=\'ksize\'>', 'groupBlur')">
                        <span class="ps-flyout-item-name">🧂 مرشح الوسيط لضوضاء الملح والفلفل (Median)</span><span class="ps-flyout-item-badge">Salt&Pepper</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('wiener', {ksize: 5}, 'Adaptive Wiener Filter (MMSE)', '<div class=\'ps-prop-row\'><span>Window Size:</span><span id=\'val_ksize\' style=\'color:#fff;\'>5</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'11\' step=\'2\' value=\'5\' data-param=\'ksize\'>', 'groupBlur')">
                        <span class="ps-flyout-item-name">🛡 مرشح وينر التكيفي (Wiener MMSE)</span><span class="ps-flyout-item-badge">Optimal</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('box_blur', {ksize: 5}, 'Box / Mean Blur Filter', '<div class=\'ps-prop-row\'><span>Kernel Window:</span><span id=\'val_ksize\' style=\'color:#fff;\'>5</span></div><input type=\'range\' class=\'ps-range\' min=\'3\' max=\'15\' step=\'2\' value=\'5\' data-param=\'ksize\'>', 'groupBlur')">
                        <span class="ps-flyout-item-name">📦 مرشح الصندوق والمتوسط (Box Blur)</span><span class="ps-flyout-item-badge">Mean</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('bilateral', {d: 9, sigma_color: 75, sigma_space: 75}, 'Bilateral Filter', '', 'groupBlur')">
                        <span class="ps-flyout-item-name">💎 المرشح الثنائي لحفظ الحواف (Bilateral)</span><span class="ps-flyout-item-badge">Preserve</span>
                    </div>
                </div>
            </div>

            <!-- 6. Morphology Group -->
            <div class="ps-tool-group" id="groupMorph">
                <div class="ps-tbtn has-flyout" id="btnGroupMorph" title="Mathematical Morphology (M)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M12 2l-5.5 9h11z M3 15h8v7H3z M18 13a4.5 4.5 0 1 0 0 9 4.5 4.5 0 0 0 0-9z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">المورفولوجيا ونظرية المجموعات (Morphology)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('erosion', {ksize: 5, shape: 'rect', iterations: 1}, 'Morphological Erosion', '<div class=\'ps-prop-row\'><span>Iterations:</span><span id=\'val_iterations\' style=\'color:#fff;\'>1</span></div><input type=\'range\' class=\'ps-range\' min=\'1\' max=\'6\' value=\'1\' data-param=\'iterations\'>', 'groupMorph')">
                        <span class="ps-flyout-item-name">🔻 التآكل المورفولوجي (Erosion)</span><span class="ps-flyout-item-badge">A ⊖ B</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('dilation', {ksize: 5, shape: 'rect', iterations: 1}, 'Morphological Dilation', '<div class=\'ps-prop-row\'><span>Iterations:</span><span id=\'val_iterations\' style=\'color:#fff;\'>1</span></div><input type=\'range\' class=\'ps-range\' min=\'1\' max=\'6\' value=\'1\' data-param=\'iterations\'>', 'groupMorph')">
                        <span class="ps-flyout-item-name">🔺 التمدد المورفولوجي (Dilation)</span><span class="ps-flyout-item-badge">A ⊕ B</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('opening', {ksize: 5, shape: 'rect'}, 'Morphological Opening', '', 'groupMorph')">
                        <span class="ps-flyout-item-name">⭕ الفتح (Opening - تنعيم الحدود)</span><span class="ps-flyout-item-badge">A ∘ B</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('closing', {ksize: 5, shape: 'rect'}, 'Morphological Closing', '', 'groupMorph')">
                        <span class="ps-flyout-item-name">⚫ الإغلاق (Closing - سد الثغرات)</span><span class="ps-flyout-item-badge">A • B</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('skeleton', {}, 'Skeletonization (Thinning)', '', 'groupMorph')">
                        <span class="ps-flyout-item-name">🦴 استخراج الهيكل العظمي (Skeleton)</span><span class="ps-flyout-item-badge">Thinning</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('morph_gradient', {ksize: 3}, 'Morphological Gradient', '', 'groupMorph')">
                        <span class="ps-flyout-item-name">📶 التدرج المورفولوجي (Gradient)</span><span class="ps-flyout-item-badge">D - E</span>
                    </div>
                </div>
            </div>

            <!-- 7. Frequency Domain FFT Group -->
            <div class="ps-tool-group" id="groupFreq">
                <div class="ps-tbtn has-flyout" id="btnGroupFreq" title="Fourier FFT Frequency Domain (F)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M2 12c2-6 4-6 6 0s4 6 6 0 4-6 6 0"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">مجال الترددات وتحويل فورييه (Fourier 2D-FFT)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('fft_spectrum', {}, '2D-FFT Magnitude Spectrum', '', 'groupFreq')">
                        <span class="ps-flyout-item-name">📡 طيف قدرة فورييه (FFT Spectrum)</span><span class="ps-flyout-item-badge">2D-DFT</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('frequency_filter', {filter_type: 'lowpass', cutoff: 40.0, filter_model: 'gaussian'}, 'Gaussian Low-Pass Frequency Filter', '<div class=\'ps-prop-row\'><span>Cutoff (D0):</span><span id=\'val_cutoff\' style=\'color:#fff;\'>40</span></div><input type=\'range\' class=\'ps-range\' min=\'5\' max=\'100\' value=\'40\' data-param=\'cutoff\'>', 'groupFreq')">
                        <span class="ps-flyout-item-name">📉 مرشح التردد المنخفض (Low-Pass)</span><span class="ps-flyout-item-badge">LPF</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('frequency_filter', {filter_type: 'highpass', cutoff: 40.0, filter_model: 'gaussian'}, 'Gaussian High-Pass Frequency Filter', '<div class=\'ps-prop-row\'><span>Cutoff (D0):</span><span id=\'val_cutoff\' style=\'color:#fff;\'>40</span></div><input type=\'range\' class=\'ps-range\' min=\'5\' max=\'100\' value=\'40\' data-param=\'cutoff\'>', 'groupFreq')">
                        <span class="ps-flyout-item-name">📈 مرشح التردد العالي (High-Pass)</span><span class="ps-flyout-item-badge">HPF</span>
                    </div>
                </div>
            </div>

            <!-- 8. Color & Segmentation Group -->
            <div class="ps-tool-group" id="groupColor">
                <div class="ps-tbtn has-flyout" id="btnGroupColor" title="Color Spaces & Segmentation (W)" onclick="app.toggleFlyout(this)">
                    <svg viewBox="0 0 24 24"><path d="M12 3a9 9 0 0 0 0 18c.83 0 1.5-.67 1.5-1.5 0-.39-.15-.74-.39-1.01-.23-.26-.38-.61-.38-.99 0-.83.67-1.5 1.5-1.5H16c2.76 0 5-2.24 5-5 0-4.42-4.03-8-9-8zm-5.5 9c-.83 0-1.5-.67-1.5-1.5S5.67 9 6.5 9 8 9.67 8 10.5 7.33 12 6.5 12zm3-4C8.67 8 8 7.33 8 6.5S8.67 5 9.5 5s1.5.67 1.5 1.5S10.33 8 9.5 8zm5 0c-.83 0-1.5-.67-1.5-1.5S13.67 5 14.5 5s1.5.67 1.5 1.5S15.33 8 14.5 8zm3 4c-.83 0-1.5-.67-1.5-1.5S16.67 9 17.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
                </div>
                <div class="ps-tool-flyout">
                    <div class="ps-flyout-header">مساحات الألوان والتقطيع (Color & Segmentation)</div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('kmeans', {k: 4}, 'K-Means Color Segmentation', '<div class=\'ps-prop-row\'><span>Clusters (K):</span><span id=\'val_k\' style=\'color:#fff;\'>4</span></div><input type=\'range\' class=\'ps-range\' min=\'2\' max=\'10\' value=\'4\' data-param=\'k\'>', 'groupColor')">
                        <span class="ps-flyout-item-name">🎨 تقطيع وعزل الألوان (K-Means)</span><span class="ps-flyout-item-badge">Clusters</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('color_space', {target: 'gray'}, 'Convert to Grayscale', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🌑 تحويل للأبيض والأسود (Grayscale)</span><span class="ps-flyout-item-badge">Y=0.299R+</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('color_space', {target: 'hsv'}, 'HSV Color Space', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🌈 فضاء HSV (Hue, Saturation, Value)</span><span class="ps-flyout-item-badge">HSV</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('color_space', {target: 'lab'}, 'CIE L*a*b* Color Space', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🧪 فضاء الألوان المعياري CIE LAB</span><span class="ps-flyout-item-badge">L*a*b*</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('isolate_channel', {channel: 'r'}, 'Isolate Red Channel', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🔴 عزل القناة الحمراء (Red Channel)</span><span class="ps-flyout-item-badge">[0,0,R]</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('isolate_channel', {channel: 'g'}, 'Isolate Green Channel', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🟢 عزل القناة الخضراء (Green Channel)</span><span class="ps-flyout-item-badge">[0,G,0]</span>
                    </div>
                    <div class="ps-flyout-item" onclick="app.selectSubTool('isolate_channel', {channel: 'b'}, 'Isolate Blue Channel', '', 'groupColor')">
                        <span class="ps-flyout-item-name">🔵 عزل القناة الزرقاء (Blue Channel)</span><span class="ps-flyout-item-badge">[B,0,0]</span>
                    </div>
                </div>
            </div>

            <!-- Divider -->
            <div class="ps-tsep"></div>

            <!-- 7. Drawing & Shapes Suite Tool -->
            <div class="ps-tool-group" id="groupDraw">
                <div class="ps-tbtn" id="btnGroupDraw" title="Drawing Suite - أدوات الرسم والأشكال الهندسية (P)" onclick="app.activateToolGroup(this, 'draw')">
                    <svg viewBox="0 0 24 24"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>
                </div>
            </div>

            <!-- 7.2. Dual Image Blending Tool -->
            <div class="ps-tool-group" id="groupBlend">
                <div class="ps-tbtn" id="btnGroupBlend" title="دمج صورتين معاً (Blend Two Images) - Ctrl+Shift+M" onclick="app.openBlendModal()">
                    <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-5.04-6.71l-2.75 3.54-1.96-2.36L6.5 17h11l-3.54-4.71z"/></svg>
                </div>
            </div>

            <!-- 7.3. Photo Collage Tool -->
            <div class="ps-tool-group" id="groupCollage">
                <div class="ps-tbtn" id="btnGroupCollage" title="قوالب الكولاج وشبكات دمج الصور (Collage Grid) - Ctrl+Shift+G" onclick="app.openCollageModal()">
                    <svg viewBox="0 0 24 24"><path d="M3 3v8h8V3H3zm6 6H5V5h4v4zm-6 4v8h8v-8H3zm6 6H5v-4h4v4zm4-16v8h8V3h-8zm6 6h-4V5h4v4zm-6 4v8h8v-8h-8zm6 6h-4v-4h4v4z"/></svg>
                </div>
            </div>

            <!-- 7.5. Selective Processing Brush Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" id="btnBrushTool" title="Selective Processing Brush (B)" onclick="app.activateToolGroup(this, 'brush')">
                    <svg viewBox="0 0 24 24"><path d="M7 14c-1.66 0-3 1.34-3 3 0 1.31-1.16 2-2 2 .92 1.22 2.49 2 4 2 2.21 0 4-1.79 4-4 0-1.66-1.34-3-3-3zm13.71-9.37l-1.34-1.34a.996.996 0 0 0-1.41 0L9 12.25 11.75 15l8.96-8.96c.39-.39.39-1.02 0-1.41z"/></svg>
                </div>
            </div>

            <!-- 8. Smart Color Splash Pipette Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" id="btnSplashTool" title="Color Splash Pipette (S)" onclick="app.activateToolGroup(this, 'splash')">
                    <svg viewBox="0 0 24 24"><path d="M12 2c-5.33 4-8 8-8 12a8 8 0 0 0 16 0c0-4-2.67-8-8-12zm0 18a6 6 0 0 1-6-6c0-3.1 1.9-6.3 6-9.7 4.1 3.4 6 6.6 6 9.7a6 6 0 0 1-6 6zm-1-10v5l4 2.5.75-1.23-3.25-2V10h-1.5z"/></svg>
                </div>
            </div>

            <!-- 9. Horizontal Type / Text Tool (T) -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" id="btnTextTool" title="Horizontal Type Tool (T)" onclick="app.activateToolGroup(this, 'text')">
                    <svg viewBox="0 0 24 24"><path d="M5 4v3h5.5v12h3V7H19V4z"/></svg>
                </div>
            </div>

            <!-- 10. Eyedropper Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" title="Eyedropper / Pixel Inspector (I)" onclick="app.activateToolGroup(this, 'eyedropper')">
                    <svg viewBox="0 0 24 24"><path d="M20.71 5.63l-2.34-2.34a1 1 0 0 0-1.41 0l-3.12 3.12-1.23-1.21-1.41 1.41 1.23 1.22L3 17.25V21h3.75l9.44-9.44 1.22 1.23 1.41-1.41-1.21-1.23 3.1-3.12a1 1 0 0 0 0-1.4z"/></svg>
                </div>
            </div>

            <!-- 10. Zoom Tool -->
            <div class="ps-tool-group">
                <div class="ps-tbtn" title="Zoom View (Z)" onclick="app.activateToolGroup(this, 'zoom')">
                    <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14zm-1-5h2v2h-2v-2zm0-4h2v2h-2V5z"/></svg>
                </div>
            </div>

            <!-- Color Swatches -->
            <div class="ps-colors">
                <div class="ps-fg-color" title="Foreground Color: Cyan"></div>
                <div class="ps-bg-color" title="Background Color: Black"></div>
            </div>
        </div>

        <!-- CANVAS & DOCUMENT STAGE -->
        <div class="ps-canvas-container">
            <!-- Document Tab -->
            <div class="ps-doc-tabs">
                <div class="ps-tab">
                    <span id="docTabTitle">benchmark.png @ 100% (RGB/8#)*</span>
                </div>
            </div>

            <!-- Stage & Photoshop Rulers -->
            <div class="ps-stage-wrapper">
                <div class="ps-ruler-corner"></div>
                <div class="ps-ruler-h">
                    <div class="ps-ruler-ticks-h">
                        <span>0</span><span>100</span><span>200</span><span>300</span><span>400</span><span>500</span><span>600</span><span>700</span><span>800</span><span>900</span><span>1000</span>
                    </div>
                </div>
                <div class="ps-ruler-v">
                    <span>0</span><span>100</span><span>200</span><span>300</span><span>400</span><span>500</span><span>600</span><span>700</span><span>800</span>
                </div>

                <div class="ps-viewport" id="viewport">
                    <!-- The Floating Document Canvas -->
                    <div class="ps-document-frame" id="docFrame">
                        <!-- Bottom layer: Raw Image -->
                        <img id="mainCanvasRaw" alt="Raw Image">

                        <!-- Top layer: Processed Image with interactive clip-path -->
                        <img id="mainCanvasProcessed" alt="Processed Image">

                        <!-- Selective Processing Brush Mask Canvas -->
                        <canvas id="brushMaskCanvas"></canvas>

                        <!-- Interactive Drawing Layer Canvas -->
                        <canvas id="drawingCanvas" style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:12;"></canvas>

                        <!-- Interactive Crop Overlay -->
                        <div id="cropOverlay" class="ps-crop-overlay" style="display:none;">
                            <div class="ps-crop-box" id="cropBox">
                                <div class="ps-crop-grid">
                                    <div class="ps-crop-line-h h1"></div>
                                    <div class="ps-crop-line-h h2"></div>
                                    <div class="ps-crop-line-v v1"></div>
                                    <div class="ps-crop-line-v v2"></div>
                                </div>
                                <div class="ps-crop-handle nw" data-handle="nw"></div>
                                <div class="ps-crop-handle ne" data-handle="ne"></div>
                                <div class="ps-crop-handle sw" data-handle="sw"></div>
                                <div class="ps-crop-handle se" data-handle="se"></div>
                                <div class="ps-crop-dim" id="cropBoxDim">0 × 0</div>
                            </div>
                        </div>

                        <!-- Interactive On-Canvas Text Box Overlay -->
                        <div id="canvasTextBox" class="ps-canvas-text-box" style="display:none;">
                            <div class="ps-text-box-header" id="canvasTextBoxHeader">
                                <span class="ps-text-box-title">🔤 منطقة كتابة النص (Text Box)</span>
                                <div class="ps-text-box-actions">
                                    <button type="button" class="ps-tbtn-action confirm" onclick="app.applyTextToImage()" title="تطبيق النص على الصورة (Enter)">✓</button>
                                    <button type="button" class="ps-tbtn-action cancel" onclick="app.cancelTextTool()" title="إلغاء (Esc)">✕</button>
                                </div>
                            </div>
                            <div class="ps-text-box-body">
                                <textarea id="canvasTextInput" class="ps-text-area" placeholder="اكتب النص هنا (يمكنك سحب هذا المربع لأي مكان على الصورة)...">VisionCraft Studio</textarea>
                            </div>
                            <div class="ps-text-box-footer">
                                <div class="ps-text-prop">
                                    <span>الحجم:</span>
                                    <input type="number" id="canvasTextSize" class="ps-input ps-input-num" min="10" max="180" value="42" style="width:48px; font-size:11px;">
                                </div>
                                <div class="ps-text-prop">
                                    <span>اللون:</span>
                                    <input type="color" id="canvasTextColor" value="#ffffff" style="width:24px; height:20px; border:none; padding:0; background:transparent; cursor:pointer;">
                                </div>
                                <div class="ps-text-prop">
                                    <span>الخط:</span>
                                    <select id="canvasTextFont" class="ps-select" style="width:80px; font-size:11px;">
                                        <option value="tahoma">Tahoma</option>
                                        <option value="segoe">Segoe UI</option>
                                        <option value="arial">Arial</option>
                                        <option value="impact">Impact</option>
                                    </select>
                                </div>
                                <button type="button" class="ps-btn ps-btn-accent" style="padding:2px 10px; font-size:11px; margin-left:auto;" onclick="app.applyTextToImage()">تطبيق (Apply)</button>
                            </div>
                        </div>

                        <!-- Split compare bar & knob -->
                        <div class="ps-split-bar" id="splitBar"></div>
                        <div class="ps-split-knob" id="splitKnob">⮂ ⮃</div>
                    </div>

                    <!-- Circular Brush Cursor -->
                    <div id="brushCursor"></div>

                    <!-- 7x7 Pixel Matrix Loupe Inspector HUD -->
                    <div class="ps-matrix-loupe" id="pixelMatrixLoupe" style="display:none;">
                        <div class="ps-matrix-header">
                            <span>🔬 7×7 Pixel Matrix</span>
                            <span id="loupeCenterCoord" style="color:#ffffff;">(0, 0)</span>
                        </div>
                        <div class="ps-matrix-grid" id="loupeGrid">
                            <!-- Populated with 49 live cells by JS -->
                        </div>
                        <div class="ps-matrix-stats">
                            <div>Center: <b id="loupeCenterVal" style="color:#00e5ff;">RGB(---)</b></div>
                            <div>Δ Edge: <b id="loupeDeltaVal" style="color:#10b981;">0</b></div>
                        </div>
                    </div>

                    <!-- Pixel Loupe HUD (Cursor Coordinates Inspector) -->
                    <div class="ps-hud-loupe">
                        <div id="hudCoords" style="color:#00e5ff;">X: 420px  Y: 280px</div>
                        <div id="hudRGB" style="color:#ffffff;">RGB Inspector Active</div>
                        <div id="hudStat" style="color:#10b981;">Dual Split Mode</div>
                    </div>
                </div>
            </div>

            <!-- Bottom Status Bar -->
            <div class="ps-doc-status">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span id="statusZoom" style="cursor:pointer; font-weight:700; color:#31a8ff; background:#1b2838; padding:1px 6px; border-radius:3px; border:1px solid #1473e6;" title="Click to reset zoom to 100%" onclick="app.resetZoom()">100%</span>
                    <button class="ps-btn" style="padding:0 5px; height:18px; font-size:11px; line-height:16px;" title="Zoom Out (Ctrl -)" onclick="app.zoomStep(0.8)">−</button>
                    <button class="ps-btn" style="padding:0 5px; height:18px; font-size:11px; line-height:16px;" title="Zoom In (Ctrl +)" onclick="app.zoomStep(1.25)">+</button>
                    <button class="ps-btn" style="padding:0 5px; height:18px; font-size:10px; line-height:16px;" title="Fit on Screen" onclick="app.fitToScreen()">Fit</button>
                    <span style="color:#555; margin:0 2px;">|</span>
                    <span id="statusDimensions">800 × 600 px</span>
                    <span style="color:#555; margin:0 2px;">|</span>
                    <span>RGB / 8-bit</span>
                </div>
                <div>
                    <span style="color:#10b981;">● Image Pan & Zoom Ready (Mouse Wheel / Space+Drag)</span>
                </div>
            </div>
        </div>

        <!-- RIGHT DOCKABLE PANELS -->
        <div class="ps-dock">
            
            <!-- GROUP 1: HISTOGRAM & PALETTE -->
            <div class="ps-panel-group">
                <div class="ps-panel-tabs">
                    <div class="ps-ptab active">📊 Histogram & Dominant Palette</div>
                </div>
                <div class="ps-panel-body">
                    <div style="display:flex; justify-content:space-between; font-size:10px; color:#aaa;">
                        <span>Channel: <b>RGB Luminance</b></span>
                        <span style="color:#1473e6;">Real-time</span>
                    </div>
                    <!-- Histogram Bars Container -->
                    <div class="ps-hist-graph" id="histGraph">
                        <!-- Populated by JS -->
                    </div>
                    <div class="ps-hist-stats">
                        <div>Mean: <span class="ps-hstat-val" id="statMean">--</span></div>
                        <div>Std Dev: <span class="ps-hstat-val" id="statStd">--</span></div>
                        <div>Median: <span class="ps-hstat-val" id="statMedian">--</span></div>
                        <div>Entropy: <span class="ps-hstat-val" id="statEntropy">--</span></div>
                    </div>

                    <!-- K-Means Dominant Color Palette -->
                    <div class="ps-palette-dock" id="paletteDock">
                        <div style="display:flex; justify-content:space-between; align-items:center; font-size:9.5px; color:#aaa; margin-bottom:4px;">
                            <span>🎨 Dominant Palette (K-Means):</span>
                            <button class="ps-btn" style="padding:1px 5px; font-size:9px;" onclick="app.refreshPalette()">Extract</button>
                        </div>
                        <div class="ps-palette-list" id="paletteList">
                            <!-- Populated with color chips -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- GROUP 2: PROPERTIES (FILTER PARAMETERS) -->
            <div class="ps-panel-group" style="max-height: 250px; overflow-y: auto;">
                <div class="ps-panel-tabs">
                    <div class="ps-ptab active">⚙️ Properties & Formula</div>
                </div>
                <div class="ps-panel-body">
                    <div id="dynamicControls">
                        <div style="color:#888; font-size:11px; padding:10px 0; text-align:center;">
                            🖼️ الصورة الأصلية (بدون فلاتر).<br>اختر أي فلتر أو أداة من شريط الأدوات أو القوائم لتطبيقه.
                        </div>
                    </div>

                    <!-- LaTeX Formula Box -->
                    <div style="background:#181818; border:1px solid #333; padding:6px; border-radius:3px; margin-top:4px;">
                        <div style="font-size:9px; color:#888; margin-bottom:2px;">Mathematical Model:</div>
                        <div id="formulaBox" style="font-family:'Fira Code'; font-size:10px; color:#00e5ff; text-align:center;">|∇f| = √(Gx² + Gy²)</div>
                    </div>
                </div>
            </div>

            <!-- GROUP 3: LAYERS PANEL -->
            <div class="ps-layers-panel">
                <div class="ps-panel-tabs">
                    <div class="ps-ptab active">📑 Layers & Python Code</div>
                </div>

                <!-- Layers Stack -->
                <div class="ps-layers-stack" id="layersStack">
                    <!-- Layer 1: Filter FX Layer -->
                    <div class="ps-layer-row selected">
                        <span class="ps-layer-eye active" id="layerEye_1" onclick="app.toggleLayerVisibility(1)">👁</span>
                        <div class="ps-layer-thumb" style="border-color:#1473e6;">
                            <span style="color:#00e5ff; font-weight:bold; font-size:9px;">FX</span>
                        </div>
                        <div class="ps-layer-title">Active Filter Layer</div>
                        <span class="ps-layer-badge">Filter FX</span>
                    </div>

                    <!-- Layer 0: Background -->
                    <div class="ps-layer-row">
                        <span class="ps-layer-eye active">👁</span>
                        <div class="ps-layer-thumb">
                            <span style="color:#666; font-size:9px;">RAW</span>
                        </div>
                        <div class="ps-layer-title">Background (Original Image)</div>
                        <span style="color:#888; font-size:10px;">🔒</span>
                    </div>
                </div>

                <!-- Python Code Preview Drawer -->
                <div style="background:#141414; border-top:1px solid #222; padding:8px 10px; max-height:120px; overflow-y:auto;">
                    <div style="display:flex; justify-content:space-between; font-size:9.5px; color:#888; margin-bottom:4px;">
                        <span>🐍 Generated Python Code:</span>
                        <span style="color:#00e5ff; cursor:pointer; font-weight:600;" onclick="app.copyPythonCode()">📋 Copy Code</span>
                    </div>
                    <pre id="codeSnippet" style="font-family:'Fira Code'; font-size:9.5px; color:#a7f3d0; margin:0; line-height:1.35;"></pre>
                </div>
            </div>

        </div>

    </div>

    <!-- 2D-FFT Interactive Notch Reject Modal -->
    <div class="ps-notch-modal" id="notchModal">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#00e5ff; font-weight:bold; font-size:12px;">📡 2D-FFT Interactive Notch Reject Filter (Moiré Eradicator)</span>
            <span style="cursor:pointer; color:#888; font-size:14px;" onclick="app.closeNotchModal()">✕</span>
        </div>
        <div style="font-size:10px; color:#bbb;">Click on periodic frequency spikes in the spectrum below to set notch reject coordinates:</div>
        <div class="ps-notch-canvas-wrap" style="text-align:center;">
            <canvas id="notchSpectrumCanvas" width="256" height="256" style="display:inline-block; background:#000; border:1px solid #555;"></canvas>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:10px;">
            <span id="notchCountDisplay" style="color:#10b981; font-family:'Fira Code';">0 notches set</span>
            <div style="display:flex; gap:6px;">
                <button class="ps-btn" onclick="app.clearNotches()">Clear Notches</button>
                <button class="ps-btn ps-btn-accent" onclick="app.applyNotchToImage()">Apply Notch Filter</button>
            </div>
        </div>
    </div>

    <!-- Background Replacement & Product Studio Modal -->
    <div class="ps-modal-backdrop" id="bgReplaceModal" style="display:none;" onclick="if(event.target===this)app.closeBgReplaceModal()">
        <div class="ps-shortcuts-modal" style="width:530px; max-width:94%;">
            <div class="ps-shortcuts-header">
                <span>🌅 Change Background & Product Studio (استبدال وعزل الخلفية)</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeBgReplaceModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body" style="padding:16px; display:flex; flex-direction:column; gap:14px;">
                <!-- Mode Cards -->
                <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px;">
                    <button class="ps-btn" id="tabBtnProductStudio" style="height:54px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; border-color:#00e5ff; background:rgba(0,229,255,0.08);" onclick="app.showBgTab('presets')">
                        <span style="font-size:18px;">🏆</span>
                        <span style="font-size:10px; font-weight:700; color:#00e5ff;">Product Studio</span>
                    </button>
                    <button class="ps-btn" id="tabBtnColor" style="height:54px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; border-color:#555;" onclick="app.showBgTab('color')">
                        <span style="font-size:18px;">🎨</span>
                        <span style="font-size:10px; font-weight:600;">Solid Color</span>
                    </button>
                    <button class="ps-btn" style="height:54px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; border-color:#555;" onclick="app.applyBackgroundReplace('gradient')">
                        <span style="font-size:18px;">🌌</span>
                        <span style="font-size:10px; font-weight:600;">Studio Gradient</span>
                    </button>
                    <button class="ps-btn" style="height:54px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:3px; border-color:#10b981; background:rgba(16,185,129,0.08);" onclick="document.getElementById('bgFileInput').click()" title="اختر صورة من جهازك لوضعها كخلفية جديدة مكان الخلفية القديمة">
                        <span style="font-size:18px;">📁</span>
                        <span style="font-size:10px; font-weight:700; color:#10b981;">رفع صورة مخصصة</span>
                    </button>
                </div>

                <!-- Product Studio Presets View -->
                <div id="productPresetsSection">
                    <div style="font-size:11px; color:#aaa; margin-bottom:8px;">
                        اختر منصة استوديو جاهزة لعرض وتصوير المنتجات بدقة تجارية عالية (GrabCut Auto-Compose):
                    </div>
                    <div class="ps-product-grid">
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('minimal_white.jpg')">
                            <img src="backgrounds/minimal_white.jpg" class="ps-product-thumb" alt="Minimal Studio">
                            <div class="ps-product-title">Minimalist White Studio</div>
                        </div>
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('wooden_podium.jpg')">
                            <img src="backgrounds/wooden_podium.jpg" class="ps-product-thumb" alt="Wooden Podium">
                            <div class="ps-product-title">Warm Wooden Podium</div>
                        </div>
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('marble_luxury.jpg')">
                            <img src="backgrounds/marble_luxury.jpg" class="ps-product-thumb" alt="Luxury Marble">
                            <div class="ps-product-title">Luxury White Marble</div>
                        </div>
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('neon_cyberpunk.jpg')">
                            <img src="backgrounds/neon_cyberpunk.jpg" class="ps-product-thumb" alt="Neon Cyberpunk">
                            <div class="ps-product-title">Neon Cyberpunk Display</div>
                        </div>
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('botanical_nature.jpg')">
                            <img src="backgrounds/botanical_nature.jpg" class="ps-product-thumb" alt="Botanical Nature">
                            <div class="ps-product-title">Botanical Stone Podium</div>
                        </div>
                        <div class="ps-product-card" onclick="app.applyProductStudioBg('gold_luxury.jpg')">
                            <img src="backgrounds/gold_luxury.jpg" class="ps-product-thumb" alt="Gold Luxury">
                            <div class="ps-product-title">Gold Luxury Pedestal</div>
                        </div>
                    </div>
                </div>

                <!-- Solid Color Picker Row -->
                <div id="solidColorPickerRow" style="display:none; align-items:center; justify-content:space-between; background:#1b1b1b; padding:10px 14px; border-radius:4px; border:1px solid #333;">
                    <span style="font-size:11px; color:#ccc;">Select Solid Background Color:</span>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <input type="color" id="bgColorPicker" value="#ffffff" style="width:38px; height:26px; border:none; cursor:pointer; background:transparent;">
                        <button class="ps-btn ps-btn-accent" style="padding:2px 10px; font-size:11px;" onclick="app.applyBackgroundReplace('color')">Apply Color</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Export & Format Conversion Modal -->
    <div class="ps-modal-backdrop" id="exportModal" style="display:none;" onclick="if(event.target===this)app.closeExportModal()">
        <div class="ps-shortcuts-modal" style="width:480px; max-width:92%;">
            <div class="ps-shortcuts-header">
                <span>💾 Export & Format Conversion (تصدير وتحويل الصيغ)</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeExportModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body" style="padding:18px; display:flex; flex-direction:column; gap:16px;">
                <!-- Format Selector Cards -->
                <div style="font-size:11px; color:#aaa;">اختر صيغة الملف المراد التحويل إليها:</div>
                <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px;">
                    <div class="ps-format-card active" id="cardFmtPng" onclick="app.selectExportFormat('png', this)">
                        <span style="font-size:16px; font-weight:bold; color:#00e5ff;">PNG</span>
                        <span style="font-size:9px; color:#888;">Lossless / Alpha</span>
                    </div>
                    <div class="ps-format-card" id="cardFmtJpg" onclick="app.selectExportFormat('jpeg', this)">
                        <span style="font-size:16px; font-weight:bold; color:#f59e0b;">JPG</span>
                        <span style="font-size:9px; color:#888;">Compact Photo</span>
                    </div>
                    <div class="ps-format-card" id="cardFmtWebp" onclick="app.selectExportFormat('webp', this)">
                        <span style="font-size:16px; font-weight:bold; color:#10b981;">WEBP</span>
                        <span style="font-size:9px; color:#888;">Modern Web</span>
                    </div>
                    <div class="ps-format-card" id="cardFmtBmp" onclick="app.selectExportFormat('bmp', this)">
                        <span style="font-size:16px; font-weight:bold; color:#a78bfa;">BMP</span>
                        <span style="font-size:9px; color:#888;">Windows Bitmap</span>
                    </div>
                </div>

                <!-- Quality Slider (Visible for JPG / WEBP) -->
                <div id="exportQualityRow" style="display:none; flex-direction:column; gap:6px; background:#1b1b1b; padding:10px 14px; border-radius:4px; border:1px solid #333;">
                    <div style="display:flex; justify-content:space-between; font-size:11px;">
                        <span>Image Quality (نسبة جودة الضغط):</span>
                        <span id="exportQualityLabel" style="color:#00e5ff; font-weight:bold; font-family:'Fira Code';">92%</span>
                    </div>
                    <input type="range" class="ps-range" id="exportQualitySlider" min="10" max="100" value="92" oninput="app.updateExportQuality(this.value)">
                </div>

                <!-- File Name & Extension -->
                <div style="display:flex; flex-direction:column; gap:6px;">
                    <span style="font-size:11px; color:#aaa;">File Name:</span>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <input type="text" class="ps-input" id="exportFileNameInput" value="visioncraft_export" style="flex:1; font-size:12px; font-family:'Fira Code';">
                        <span id="exportExtLabel" style="color:#00e5ff; font-weight:bold; font-family:'Fira Code'; font-size:12px;">.png</span>
                    </div>
                </div>

                <!-- Live Estimates -->
                <div style="display:flex; justify-content:space-between; align-items:center; background:#111; padding:8px 12px; border-radius:4px; font-size:11px; color:#aaa;">
                    <span>Estimated Size: <b id="exportSizeEstimate" style="color:#10b981; font-family:'Fira Code';">~350 KB</b></span>
                    <span>Resolution: <b id="exportResEstimate" style="color:#fff; font-family:'Fira Code';">1024 × 768 px</b></span>
                </div>

                <!-- Action Buttons -->
                <div style="display:flex; justify-content:flex-end; gap:8px;">
                    <button class="ps-btn" onclick="app.closeExportModal()">Cancel</button>
                    <button class="ps-btn ps-btn-accent" style="padding:6px 18px; font-size:12px;" onclick="app.performExport()">💾 Download Image</button>
                </div>
            </div>
        </div>
    </div>

    <!-- DIP Dual Image Blending Modal -->
    <div class="ps-modal-backdrop" id="blendModal" style="display:none;" onclick="if(event.target===this)app.closeBlendModal()">
        <div class="ps-shortcuts-modal" style="width:520px; max-width:92%;">
            <div class="ps-shortcuts-header">
                <span>🖼️ دمج صورتين معاً (DIP Image Blending)</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeBlendModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body" style="padding:18px; display:flex; flex-direction:column; gap:16px;">
                <div style="font-size:11px; color:#aaa; line-height:1.5;">
                    دمج صورتين معاً رياضياً عبر معادلة الاستيفاء الخطي مع موازنة الشفافية: <code style="color:#00e5ff; font-family:'Fira Code';">g = (1 - α)·f₁ + α·f₂</code>
                </div>
                
                <!-- Dual Image Preview Grid -->
                <div style="display:grid; grid-template-columns: 1fr auto 1fr; gap:12px; align-items:center;">
                    <!-- Image 1 -->
                    <div style="background:#1b1b1b; border:1px solid #333; border-radius:6px; padding:10px; text-align:center;">
                        <div style="font-size:11px; color:#888; margin-bottom:6px;">الصورة 1 (الأساسية f₁)</div>
                        <img id="blendThumb1" style="max-width:100%; height:90px; object-fit:contain; border-radius:4px; background:#111;">
                    </div>
                    
                    <div style="font-size:24px; color:#00e5ff; font-weight:bold;">+</div>
                    
                    <!-- Image 2 -->
                    <div style="background:#1b1b1b; border:1px dashed #555; border-radius:6px; padding:10px; text-align:center; position:relative;">
                        <div style="font-size:11px; color:#888; margin-bottom:6px;">الصورة 2 (الثانوية f₂)</div>
                        <img id="blendThumb2" style="max-width:100%; height:90px; object-fit:contain; border-radius:4px; background:#111; display:none;">
                        <div id="blendThumb2Placeholder" style="height:90px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px;">
                            <span style="font-size:22px;">📁</span>
                            <button class="ps-btn ps-btn-accent" style="font-size:11px; padding:3px 10px;" onclick="document.getElementById('blendSecondFileInput').click()">اختر صورة 2...</button>
                        </div>
                        <input type="file" id="blendSecondFileInput" accept="image/*" style="display:none;" onchange="app.handleBlendSecondImage(event)">
                    </div>
                </div>

                <!-- Blending Ratio Slider (Alpha) -->
                <div style="background:#1b1b1b; padding:12px; border-radius:6px; border:1px solid #333;">
                    <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:8px;">
                        <span style="color:#00e5ff;">نسبة الصورة 1: <strong id="blendRatio1Label">50%</strong></span>
                        <span style="color:#aaa;">معامل الدمج (α): <strong id="blendAlphaLabel" style="color:#fff;">0.50</strong></span>
                        <span style="color:#10b981;">نسبة الصورة 2: <strong id="blendRatio2Label">50%</strong></span>
                    </div>
                    <input type="range" class="ps-range" min="0" max="1" step="0.02" value="0.5" id="blendAlphaSlider" oninput="app.updateBlendSlider(this.value)">
                </div>

                <!-- Blending Mode Selector -->
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px;">
                    <span style="color:#ccc;">خوارزمية ونمط الدمج (Algorithm):</span>
                    <select class="ps-select" id="blendAlgorithmSelect" style="width:230px;">
                        <option value="linear">دمج خطي نسبي (cv2.addWeighted)</option>
                        <option value="multiply">ضرب البكسلات (Multiply Blend)</option>
                        <option value="screen">الشاشة والإنارة (Screen Blend)</option>
                        <option value="addition">جمع البكسلات المباشر (Addition)</option>
                        <option value="subtraction">طرح الفروقات (Subtraction/Diff)</option>
                    </select>
                </div>

                <!-- Action Buttons -->
                <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:8px;">
                    <button class="ps-btn" onclick="app.closeBlendModal()">إلغاء</button>
                    <button class="ps-btn ps-btn-accent" style="background:#059669; border-color:#10b981; padding:6px 16px;" onclick="app.executeBlendImages()">✨ دمج وتطبيق على الصورة</button>
                </div>
            </div>
        </div>
    </div>

    <!-- DIP Multi-Image Collage & Grid Layout Modal -->
    <div class="ps-modal-backdrop" id="collageModal" style="display:none;" onclick="if(event.target===this)app.closeCollageModal()">
        <div class="ps-shortcuts-modal" style="width:620px; max-width:95%;">
            <div class="ps-shortcuts-header">
                <span>📐 قوالب الكولاج وشبكات دمج الصور (DIP Photo Collage)</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeCollageModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body" style="padding:16px; display:flex; flex-direction:column; gap:14px;">
                <div style="font-size:11px; color:#aaa; line-height:1.5;">
                    اختر قالباً هندسياً لدمج عدة صور جنباً إلى جنب أو في شبكة مصفوفية متناسقة مع اقتصاص ملء ذكي (Aspect-Fill):
                </div>

                <!-- Template Selector Cards -->
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                    <!-- Template 1: 2 Images Side-by-Side -->
                    <div class="ps-collage-card active" id="tplSideBySide" onclick="app.selectCollageTemplate('side_by_side', 2, this)">
                        <div class="ps-collage-preview">
                            <div style="width:50%; height:100%; border-right:2px solid #222; background:#3b82f6;"></div>
                            <div style="width:50%; height:100%; background:#10b981;"></div>
                        </div>
                        <div class="ps-collage-label">جنباً إلى جنب (1:1)</div>
                        <div class="ps-collage-sub">صورتين أفقياً</div>
                    </div>

                    <!-- Template 2: 2 Images Top & Bottom -->
                    <div class="ps-collage-card" id="tplTopBottom" onclick="app.selectCollageTemplate('top_bottom', 2, this)">
                        <div class="ps-collage-preview" style="flex-direction:column;">
                            <div style="width:100%; height:50%; border-bottom:2px solid #222; background:#3b82f6;"></div>
                            <div style="width:100%; height:50%; background:#10b981;"></div>
                        </div>
                        <div class="ps-collage-label">أعلى وأسفل</div>
                        <div class="ps-collage-sub">صورتين رأسياً</div>
                    </div>

                    <!-- Template 3: 3 Images (1 Big + 2 Stacked) -->
                    <div class="ps-collage-card" id="tplThreeOneLeft" onclick="app.selectCollageTemplate('three_one_left', 3, this)">
                        <div class="ps-collage-preview">
                            <div style="width:60%; height:100%; border-right:2px solid #222; background:#3b82f6;"></div>
                            <div style="width:40%; height:100%; display:flex; flex-direction:column;">
                                <div style="height:50%; border-bottom:2px solid #222; background:#10b981;"></div>
                                <div style="height:50%; background:#f59e0b;"></div>
                            </div>
                        </div>
                        <div class="ps-collage-label">1 رئيسية + 2 فرعية</div>
                        <div class="ps-collage-sub">3 صور لمنتج أو قصة</div>
                    </div>

                    <!-- Template 4: 3 Columns -->
                    <div class="ps-collage-card" id="tplThreeCols" onclick="app.selectCollageTemplate('three_columns', 3, this)">
                        <div class="ps-collage-preview">
                            <div style="width:33.3%; height:100%; border-right:2px solid #222; background:#3b82f6;"></div>
                            <div style="width:33.3%; height:100%; border-right:2px solid #222; background:#10b981;"></div>
                            <div style="width:33.4%; height:100%; background:#f59e0b;"></div>
                        </div>
                        <div class="ps-collage-label">شريط ثلاثي</div>
                        <div class="ps-collage-sub">3 أعمدة متساوية</div>
                    </div>

                    <!-- Template 5: 4 Images 2x2 Grid -->
                    <div class="ps-collage-card" id="tplGrid2x2" onclick="app.selectCollageTemplate('grid_2x2', 4, this)">
                        <div class="ps-collage-preview" style="display:grid; grid-template-columns:1fr 1fr; grid-template-rows:1fr 1fr; gap:2px; background:#222;">
                            <div style="background:#3b82f6;"></div>
                            <div style="background:#10b981;"></div>
                            <div style="background:#f59e0b;"></div>
                            <div style="background:#ec4899;"></div>
                        </div>
                        <div class="ps-collage-label">شبكة 2×2 كلاسيكية</div>
                        <div class="ps-collage-sub">4 صور متساوية</div>
                    </div>

                    <!-- Template 6: Panorama Header + 3 Columns -->
                    <div class="ps-collage-card" id="tplFourHeader" onclick="app.selectCollageTemplate('four_header', 4, this)">
                        <div class="ps-collage-preview" style="flex-direction:column;">
                            <div style="width:100%; height:55%; border-bottom:2px solid #222; background:#3b82f6;"></div>
                            <div style="width:100%; height:45%; display:flex;">
                                <div style="width:33.3%; border-right:2px solid #222; background:#10b981;"></div>
                                <div style="width:33.3%; border-right:2px solid #222; background:#f59e0b;"></div>
                                <div style="width:33.4%; background:#ec4899;"></div>
                            </div>
                        </div>
                        <div class="ps-collage-label">بانوراما + 3 صور</div>
                        <div class="ps-collage-sub">4 صور سينمائية</div>
                    </div>
                </div>

                <!-- Slots Manager Container -->
                <div style="background:#181818; padding:12px; border-radius:6px; border:1px solid #333;">
                    <div style="font-size:11px; color:#ccc; margin-bottom:8px; display:flex; justify-content:space-between;">
                        <span>خانات الصور في القالب (<span id="collageSlotsCountLabel">2 صور</span>):</span>
                        <span style="color:#00e5ff; font-size:10px;">انقر على أي خانة لرفع صورتها</span>
                    </div>
                    <div id="collageSlotsContainer" style="display:grid; grid-template-columns:repeat(4, 1fr); gap:10px;">
                        <!-- Slots injected dynamically -->
                    </div>
                    <input type="file" id="collageSlotFileInput" accept="image/*" style="display:none;" onchange="app.handleCollageSlotFile(event)">
                </div>

                <!-- Spacing and Border Color Controls -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; background:#181818; padding:12px; border-radius:6px; border:1px solid #333;">
                    <!-- Border Gap Slider -->
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:6px;">
                            <span style="color:#aaa;">سماكة الفاصل (Gap):</span>
                            <span id="collageGapLabel" style="color:#00e5ff; font-weight:bold;">10 px</span>
                        </div>
                        <input type="range" class="ps-range" min="0" max="40" value="10" id="collageGapSlider" oninput="app.setCollageGap(this.value)">
                    </div>

                    <!-- Border Color Picker -->
                    <div>
                        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:6px;">
                            <span style="color:#aaa;">لون الفواصل (Border Color):</span>
                            <span id="collageColorLabel" style="color:#fff;">#ffffff</span>
                        </div>
                        <div style="display:flex; gap:8px; align-items:center;">
                            <input type="color" id="collageColorPicker" value="#ffffff" style="width:34px; height:24px; border:none; cursor:pointer; background:transparent;" onchange="app.setCollageColor(this.value)">
                            <button class="ps-btn" style="padding:1px 8px; font-size:10px;" onclick="app.setCollageColor('#ffffff')">أبيض</button>
                            <button class="ps-btn" style="padding:1px 8px; font-size:10px;" onclick="app.setCollageColor('#000000')">أسود</button>
                            <button class="ps-btn" style="padding:1px 8px; font-size:10px;" onclick="app.setCollageColor('#262626')">رمادي</button>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div style="display:flex; justify-content:flex-end; gap:8px;">
                    <button class="ps-btn" onclick="app.closeCollageModal()">إلغاء</button>
                    <button class="ps-btn ps-btn-accent" style="background:#2563eb; border-color:#3b82f6; padding:6px 18px;" onclick="app.executeCollage()">✨ توليد وتطبيق الكولاج على اللوحة</button>
                </div>
            </div>
        </div>
    </div>

    <!-- AR Virtual Try-On & Accessories Studio Modal -->
    <div class="ps-modal-backdrop" id="accessoriesModal" style="display:none;" onclick="if(event.target===this)app.closeAccessoriesModal()">
        <div class="ps-shortcuts-modal" style="width:580px; max-width:94%;">
            <div class="ps-shortcuts-header">
                <span style="color:#c084fc;">👓 استوديو الملحقات والواقع المعزز (AR Virtual Try-On Studio)</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeAccessoriesModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body" style="padding:16px; display:flex; flex-direction:column; gap:14px;">
                <div style="font-size:11px; color:#aaa; line-height:1.5;">
                    اختر أي ملحق لتجربته وتطبيقه كطبقة تراكب ذكية (Overlay) على صورتك أو نموذج الوجه، مع إمكانية التحريك وتغيير الحجم والشفافية:
                </div>
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                    <div class="ps-product-card" onclick="app.applyAccessoryOverlay('glasses_black.png', 'نظارة شمسية كلاسيكية')">
                        <img src="{{ asset('accessories/glasses_black.png') }}" class="ps-product-thumb" style="object-fit:contain; background:#1e293b; padding:8px; height:85px;" alt="نظارة سوداء">
                        <div class="ps-product-title">نظارة شمسية سوداء</div>
                    </div>
                    <div class="ps-product-card" onclick="app.applyAccessoryOverlay('glasses_optical.png', 'نظارة طبية ذكية')">
                        <img src="{{ asset('accessories/glasses_optical.png') }}" class="ps-product-thumb" style="object-fit:contain; background:#1e293b; padding:8px; height:85px;" alt="نظارة طبية">
                        <div class="ps-product-title">نظارة طبية شفافة</div>
                    </div>
                    <div class="ps-product-card" onclick="app.applyAccessoryOverlay('hat_fedora.png', 'قبعة فيدورا كلاسيكية')">
                        <img src="{{ asset('accessories/hat_fedora.png') }}" class="ps-product-thumb" style="object-fit:contain; background:#1e293b; padding:8px; height:85px;" alt="قبعة فيدورا">
                        <div class="ps-product-title">قبعة فيدورا أنيقة</div>
                    </div>
                    <div class="ps-product-card" onclick="app.applyAccessoryOverlay('scarf_winter.png', 'وشاح شتوي دافئ')">
                        <img src="{{ asset('accessories/scarf_winter.png') }}" class="ps-product-thumb" style="object-fit:contain; background:#1e293b; padding:8px; height:85px;" alt="وشاح شتوي">
                        <div class="ps-product-title">وشاح شتوي دافئ</div>
                    </div>
                    <div class="ps-product-card" onclick="app.applyAccessoryOverlay('suit_formal.png', 'بدلة رسمية فاخرة')">
                        <img src="{{ asset('accessories/suit_formal.png') }}" class="ps-product-thumb" style="object-fit:contain; background:#1e293b; padding:8px; height:85px;" alt="بدلة رسمية">
                        <div class="ps-product-title">طقم بدلة رسمية</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; background:#181818; padding:8px 12px; border-radius:4px; border:1px solid #333; font-size:11px;">
                    <span style="color:#888;">💡 نصيحة: يمكنك أيضاً تحميل نموذج الوجه القياسي للاختبار:</span>
                    <button class="ps-btn ps-btn-accent" style="font-size:10px; padding:2px 8px;" onclick="app.loadSampleImage('portrait_model.png'); app.closeAccessoriesModal();">👤 تحميل الموديل</button>
                </div>
            </div>
        </div>
    </div>



    <!-- On-Screen HUD Toast Notification for Shortcut Feedback -->
    <div class="ps-hud-toast" id="hudToast">
        <span id="hudToastIcon">⚡</span>
        <span id="hudToastText">Shortcut Activated</span>
    </div>

    <!-- Keyboard Shortcuts Cheatsheet Modal -->
    <div class="ps-modal-backdrop" id="shortcutsModalBackdrop" onclick="if(event.target===this)app.closeShortcutsModal()">
        <div class="ps-shortcuts-modal">
            <div class="ps-shortcuts-header">
                <span>⌨️ VisionCraft Keyboard Shortcuts Cheatsheet</span>
                <span style="cursor:pointer; color:#888; font-size:16px;" onclick="app.closeShortcutsModal()">✕</span>
            </div>
            <div class="ps-shortcuts-body">
                <!-- Section: Tools -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">Toolbar & Creation Tools</div>
                    <div class="ps-shortcut-row"><span>Move Tool / Pan Canvas</span><span class="ps-kbd">V</span></div>
                    <div class="ps-shortcut-row"><span>Horizontal Type / Text Tool</span><span class="ps-kbd">T</span></div>
                    <div class="ps-shortcut-row"><span>Selective Processing Brush</span><span class="ps-kbd">B</span></div>
                    <div class="ps-shortcut-row"><span>Eraser / Clear Brush Mask</span><span class="ps-kbd">E</span></div>
                    <div class="ps-shortcut-row"><span>Color Splash Pipette</span><span class="ps-kbd">S</span></div>
                    <div class="ps-shortcut-row"><span>Eyedropper / Pixel Sampler</span><span class="ps-kbd">I</span></div>
                    <div class="ps-shortcut-row"><span>Zoom Tool</span><span class="ps-kbd">Z</span></div>
                    <div class="ps-shortcut-row"><span>Hand Tool (Hold & Drag)</span><span class="ps-kbd">Space</span></div>
                </div>

                <!-- Section: Studio Composition -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">Studio Composition Superpowers</div>
                    <div class="ps-shortcut-row"><span>Remove Background (GrabCut)</span><span class="ps-kbd">Ctrl + Shift + B</span></div>
                    <div class="ps-shortcut-row"><span>Place Image Overlay</span><span class="ps-kbd">Ctrl + Shift + P</span></div>
                    <div class="ps-shortcut-row"><span>Apply Text / Overlay</span><span class="ps-kbd">Enter</span></div>
                    <div class="ps-shortcut-row"><span>Cancel Text / Overlay</span><span class="ps-kbd">Esc</span></div>
                </div>

                <!-- Section: Brush Controls -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">Brush Dynamic Adjustments</div>
                    <div class="ps-shortcut-row"><span>Decrease Brush Size (-5px)</span><span class="ps-kbd">[</span></div>
                    <div class="ps-shortcut-row"><span>Increase Brush Size (+5px)</span><span class="ps-kbd">]</span></div>
                    <div class="ps-shortcut-row"><span>Softer Brush Feather (-10%)</span><span class="ps-kbd">Shift + [</span></div>
                    <div class="ps-shortcut-row"><span>Harder Brush Feather (+10%)</span><span class="ps-kbd">Shift + ]</span></div>
                </div>

                <!-- Section: View & Canvas Navigation -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">View & Canvas Navigation</div>
                    <div class="ps-shortcut-row"><span>Zoom In</span><span class="ps-kbd">Ctrl + +</span></div>
                    <div class="ps-shortcut-row"><span>Zoom Out</span><span class="ps-kbd">Ctrl + -</span></div>
                    <div class="ps-shortcut-row"><span>Actual Pixels (100%)</span><span class="ps-kbd">Ctrl + 0</span></div>
                    <div class="ps-shortcut-row"><span>Fit to Screen</span><span class="ps-kbd">Ctrl + 1</span></div>
                    <div class="ps-shortcut-row"><span>Toggle Split View Modes</span><span class="ps-kbd">\</span></div>
                    <div class="ps-shortcut-row"><span>Zen Fullscreen Canvas Mode</span><span class="ps-kbd">Tab</span></div>
                </div>

                <!-- Section: File & History -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">File & History Operations</div>
                    <div class="ps-shortcut-row"><span>Open Local Image</span><span class="ps-kbd">Ctrl + O</span></div>
                    <div class="ps-shortcut-row"><span>Export Image (PNG)</span><span class="ps-kbd">Ctrl + S</span></div>
                    <div class="ps-shortcut-row"><span>Undo (تراجع عن العملية)</span><span class="ps-kbd">Ctrl + Z</span></div>
                    <div class="ps-shortcut-row"><span>Redo (إعادة العملية)</span><span class="ps-kbd">Ctrl + Y</span> / <span class="ps-kbd">Ctrl + Shift + Z</span></div>
                    <div class="ps-shortcut-row"><span>Copy Python Code</span><span class="ps-kbd">Ctrl + C</span></div>
                    <div class="ps-shortcut-row"><span>Revert to Original</span><span class="ps-kbd">F12</span></div>
                </div>

                <!-- Section: Digital Image Processing Superpowers -->
                <div class="ps-shortcut-section">
                    <div class="ps-shortcut-title">DIP Superpowers & Adjustments</div>
                    <div class="ps-shortcut-row"><span>Air Gestures (Hand Tracking)</span><span class="ps-kbd">G</span></div>
                    <div class="ps-shortcut-row"><span>7×7 Pixel Matrix HUD Loupe</span><span class="ps-kbd">M</span></div>
                    <div class="ps-shortcut-row"><span>2D-FFT Notch Reject Filter Modal</span><span class="ps-kbd">N</span></div>
                    <div class="ps-shortcut-row"><span>Invert Negative</span><span class="ps-kbd">Ctrl + I</span></div>
                    <div class="ps-shortcut-row"><span>Histogram Equalization (Levels)</span><span class="ps-kbd">Ctrl + L</span></div>
                    <div class="ps-shortcut-row"><span>Grayscale Desaturation</span><span class="ps-kbd">Ctrl + Shift + U</span></div>
                    <div class="ps-shortcut-row"><span>Shortcuts Help Modal</span><span class="ps-kbd">F1</span> / <span class="ps-kbd">?</span></div>
                </div>
            </div>
        </div>
    </div>


    <!-- Realtime WebSocket & Photoshop Core Engine -->
    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
    <script src="{{ asset('js/app.js') }}?v={{ time() }}"></script>
</body>
</html>
