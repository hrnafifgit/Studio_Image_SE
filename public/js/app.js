/**
 * VisionCraft Photoshop Pro - Web Engine
 * Digital Image Processing Studio (Photoshop Pro Edition)
 * Featuring 6 Unique DIP Superpowers:
 * 1. Selective Processing Brush (Interactive Masking)
 * 2. Motion Deblur (Wiener Deconvolution & PSF)
 * 3. 2D-FFT Interactive Notch Reject Filter (Moiré Eradicator)
 * 4. Smart Color Splash Pipette & K-Means Palette Extractor
 * 5. DIP Layer FX with Live Blending Modes (Neon Screen, etc.)
 * 6. 7x7 Numeric Pixel Matrix Loupe Inspector
 */

class PhotoshopApp {
    constructor() {
        this.rawImageBase64 = null;
        this.processedImageBase64 = null;
        this.currentFileName = "benchmark.png";
        this.activeOperation = "none";
        this.activeParams = {};
        this.isComparing = true;
        this.splitPercent = 50;

        // History State (Professional Undo / Redo Stack - Memento Pattern)
        this.undoStack = [];
        this.redoStack = [];
        this.maxHistory = 30;
        this.isRestoringHistory = false;
        this.currentHistogram = null;
        this.currentStats = null;

        // Viewport Zoom & Pan State
        this.zoomScale = 1.0;
        this.zoomLevel = 100;
        this.panX = 0;
        this.panY = 0;
        this.isSpacePressed = false;
        this.isPanning = false;

        // Active Tool
        this.activeTool = "move";

        // Superpower 1: Selective Processing Brush State
        this.brushSize = 35;
        this.brushFeather = 50;
        this.isPaintingBrush = false;
        this.hasBrushStrokes = false;

        // Superpower 3: 2D-FFT Notch Reject State
        this.notches = [];

        // Superpower 5: Blend Mode & Layer FX State
        this.blendMode = "normal";
        this.layerOpacity = 100;
        this.activeLayerIndex = 1;
        this.layers = [
            { id: "layer_0", name: "Background (Raw Image)", type: "raw", visible: true, opacity: 100 },
            { id: "layer_1", name: "Canny Edge Layer", type: "filter", op: "canny", visible: true, opacity: 100, badge: "Filter FX" }
        ];

        // Superpower 6: 7x7 Pixel Matrix Loupe State
        this.isLoupeActive = false;

        // Studio Composition State (Text, Background Cut & Replace, Image Overlay)
        this.textCoords = { x: 50, y: 80 };
        this.overlayCoords = { x: 50, y: 50 };
        this.overlayScale = 1.0;
        this.overlayOpacity = 1.0;
        this.overlayImageBase64 = null;

        // Interactive Crop Engine State
        this.isCropActive = false;
        this.cropBox = { x: 50, y: 50, w: 300, h: 220 };
        this.cropRatio = "free";
        this.isDraggingCrop = false;
        this.isResizingCrop = false;
        this.activeCropHandle = null;
        this.cropDragStart = { x: 0, y: 0, boxX: 0, boxY: 0, boxW: 0, boxH: 0 };

        // Drawing & Shapes Suite State
        this.drawShape = "pen";
        this.drawColor = "#00e5ff";
        this.drawStrokeSize = 4;
        this.drawFill = false;
        this.isDrawing = false;
        this.drawStart = { x: 0, y: 0 };

        // Export & Format Conversion State
        this.exportFormat = "png";
        this.exportQuality = 0.92;

        // Offscreen sampling caches
        this.rawOffscreenCanvas = document.createElement("canvas");
        this.rawOffscreenCtx = this.rawOffscreenCanvas.getContext("2d", { willReadFrequently: true });
        this.procOffscreenCanvas = document.createElement("canvas");
        this.procOffscreenCtx = this.procOffscreenCanvas.getContext("2d", { willReadFrequently: true });

        this.initDOM();
        this.initEvents();
        this.loadSampleImage("benchmark.png");
    }

    initDOM() {
        this.canvasRaw = document.getElementById("mainCanvasRaw");
        this.canvasProcessed = document.getElementById("mainCanvasProcessed");
        this.splitBar = document.getElementById("splitBar");
        this.splitKnob = document.getElementById("splitKnob");
        this.viewport = document.getElementById("viewport");
        this.docFrame = document.getElementById("docFrame");
        this.statusZoom = document.getElementById("statusZoom");
        this.histContainer = document.getElementById("histGraph");
        this.formulaBox = document.getElementById("formulaBox");
        this.codeSnippet = document.getElementById("codeSnippet");
        this.fileInput = document.getElementById("fileInput");
        this.perfBadge = document.getElementById("perfBadge");
        this.hudCoords = document.getElementById("hudCoords");
        this.hudRGB = document.getElementById("hudRGB");
        this.hudStat = document.getElementById("hudStat");
        this.docTabTitle = document.getElementById("docTabTitle");
        this.statusDimensions = document.getElementById("statusDimensions");
        this.layersList = document.getElementById("layersStack");
        this.filterTitle = document.getElementById("filterTitle");
        this.dynamicControls = document.getElementById("dynamicControls");

        // Superpower 1: Brush Elements
        this.brushCursor = document.getElementById("brushCursor");
        this.brushMaskCanvas = document.getElementById("brushMaskCanvas");
        this.brushMaskCtx = this.brushMaskCanvas ? this.brushMaskCanvas.getContext("2d") : null;
        this.brushOptionsBar = document.getElementById("brushOptionsBar");
        this.brushSizeSlider = document.getElementById("brushSizeSlider");
        this.brushSizeLabel = document.getElementById("brushSizeLabel");
        this.brushFeatherSlider = document.getElementById("brushFeatherSlider");

        // Superpower 3: Notch Filter Elements
        this.notchModal = document.getElementById("notchModal");
        this.notchSpectrumCanvas = document.getElementById("notchSpectrumCanvas");
        this.notchCountDisplay = document.getElementById("notchCountDisplay");

        // Superpower 4: Palette Elements
        this.paletteDock = document.getElementById("paletteDock");
        this.paletteList = document.getElementById("paletteList");

        // Superpower 5: Blend Mode & Opacity Elements
        this.blendModeSelect = document.getElementById("blendModeSelect");
        this.layerOpacityInput = document.getElementById("layerOpacityInput");

        // Superpower 6: 7x7 Pixel Matrix Elements
        this.pixelMatrixLoupe = document.getElementById("pixelMatrixLoupe");
        this.loupeGrid = document.getElementById("loupeGrid");
        this.loupeCenterCoord = document.getElementById("loupeCenterCoord");
        this.loupeCenterVal = document.getElementById("loupeCenterVal");
        this.loupeDeltaVal = document.getElementById("loupeDeltaVal");

        // Interactive Feedback & Shortcuts HUD
        this.hudToast = document.getElementById("hudToast");
        this.hudToastIcon = document.getElementById("hudToastIcon");
        this.hudToastText = document.getElementById("hudToastText");
        this.shortcutsModalBackdrop = document.getElementById("shortcutsModalBackdrop");
        this.splitCycle = 0;

        // Studio Composition Elements
        this.bgReplaceModal = document.getElementById("bgReplaceModal");
        this.bgColorPicker = document.getElementById("bgColorPicker");
        this.bgFileInput = document.getElementById("bgFileInput");
        this.overlayFileInput = document.getElementById("overlayFileInput");
        this.textOptionsBar = document.getElementById("textOptionsBar");
        this.textOverlayInput = document.getElementById("textOverlayInput");
        this.textFontFamily = document.getElementById("textFontFamily");
        this.textFontSize = document.getElementById("textFontSize");
        this.textOverlayColor = document.getElementById("textOverlayColor");

        // Interactive On-Canvas Text Box Elements
        this.canvasTextBox = document.getElementById("canvasTextBox");
        this.canvasTextBoxHeader = document.getElementById("canvasTextBoxHeader");
        this.canvasTextInput = document.getElementById("canvasTextInput");
        this.canvasTextSize = document.getElementById("canvasTextSize");
        this.canvasTextColor = document.getElementById("canvasTextColor");
        this.canvasTextFont = document.getElementById("canvasTextFont");
        this.overlayOptionsBar = document.getElementById("overlayOptionsBar");
        this.overlayScaleSlider = document.getElementById("overlayScaleSlider");
        this.overlayScaleLabel = document.getElementById("overlayScaleLabel");
        this.overlayOpacitySlider = document.getElementById("overlayOpacitySlider");
        this.overlayOpacityLabel = document.getElementById("overlayOpacityLabel");

        // Crop Tool Elements
        this.cropOptionsBar = document.getElementById("cropOptionsBar");
        this.cropRatioSelect = document.getElementById("cropRatioSelect");
        this.cropDimensionsLabel = document.getElementById("cropDimensionsLabel");
        this.cropOverlay = document.getElementById("cropOverlay");
        this.cropBoxEl = document.getElementById("cropBox");
        this.cropBoxDim = document.getElementById("cropBoxDim");

        // Drawing Suite Elements
        this.drawOptionsBar = document.getElementById("drawOptionsBar");
        this.drawShapeSelect = document.getElementById("drawShapeSelect");
        this.drawStrokeSizeSlider = document.getElementById("drawStrokeSizeSlider");
        this.drawStrokeSizeLabel = document.getElementById("drawStrokeSizeLabel");
        this.drawColorPicker = document.getElementById("drawColorPicker");
        this.drawFillCheckbox = document.getElementById("drawFillCheckbox");
        this.drawingCanvas = document.getElementById("drawingCanvas");
        this.drawingCtx = this.drawingCanvas ? this.drawingCanvas.getContext("2d") : null;

        // Export Modal Elements
        this.exportModal = document.getElementById("exportModal");
        this.exportQualityRow = document.getElementById("exportQualityRow");
        this.exportQualitySlider = document.getElementById("exportQualitySlider");
        this.exportQualityLabel = document.getElementById("exportQualityLabel");
        this.exportFileNameInput = document.getElementById("exportFileNameInput");
        this.exportExtLabel = document.getElementById("exportExtLabel");
        this.exportSizeEstimate = document.getElementById("exportSizeEstimate");
        this.exportResEstimate = document.getElementById("exportResEstimate");

        // Product Studio Presets Elements
        this.productPresetsSection = document.getElementById("productPresetsSection");
        this.solidColorPickerRow = document.getElementById("solidColorPickerRow");

        // DIP Dual Image Blending Modal Elements
        this.blendModal = document.getElementById("blendModal");
        this.blendThumb1 = document.getElementById("blendThumb1");
        this.blendThumb2 = document.getElementById("blendThumb2");
        this.blendThumb2Placeholder = document.getElementById("blendThumb2Placeholder");
        this.blendSecondFileInput = document.getElementById("blendSecondFileInput");
        this.blendAlphaSlider = document.getElementById("blendAlphaSlider");
        this.blendAlphaLabel = document.getElementById("blendAlphaLabel");
        this.blendRatio1Label = document.getElementById("blendRatio1Label");
        this.blendRatio2Label = document.getElementById("blendRatio2Label");
        this.blendAlgorithmSelect = document.getElementById("blendAlgorithmSelect");
        this.blendSecondImageBase64 = null;
        this.blendAlpha = 0.5;

        // DIP Collage & Layout State & Elements
        this.collageModal = document.getElementById("collageModal");
        this.collageSlotsContainer = document.getElementById("collageSlotsContainer");
        this.collageSlotsCountLabel = document.getElementById("collageSlotsCountLabel");
        this.collageSlotFileInput = document.getElementById("collageSlotFileInput");
        this.collageGapSlider = document.getElementById("collageGapSlider");
        this.collageGapLabel = document.getElementById("collageGapLabel");
        this.collageColorPicker = document.getElementById("collageColorPicker");
        this.collageColorLabel = document.getElementById("collageColorLabel");
        this.collageTemplate = "side_by_side";
        this.collageSlotCount = 2;
        this.collageSlotImages = [];
        this.collageActiveSlotIndex = 0;
        this.collageBorderGap = 10;
        this.collageBorderColor = [255, 255, 255];

        // AR Virtual Try-On & Accessories Modal
        this.accessoriesModal = document.getElementById("accessoriesModal");

        // Bind dynamic sliders on initial DOM ready
        this.bindDynamicSliders();
    }

    // =========================================================================
    // AR VIRTUAL TRY-ON & ACCESSORIES STUDIO
    // =========================================================================
    openAccessoriesModal() {
        if (this.accessoriesModal) this.accessoriesModal.style.display = "flex";
    }

    closeAccessoriesModal() {
        if (this.accessoriesModal) this.accessoriesModal.style.display = "none";
    }

    applyAccessoryOverlay(filename, label) {
        this.closeAccessoriesModal();
        this.showToast(`Loading ${label}...`, "👓");
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
            const c = document.createElement("canvas");
            c.width = img.width;
            c.height = img.height;
            const ctx = c.getContext("2d");
            ctx.drawImage(img, 0, 0);
            this.overlayImageBase64 = c.toDataURL("image/png");
            this.overlayScale = 0.85;
            this.overlayOpacity = 1.0;
            this.overlayCoords = { x: 50, y: 35 };
            if (this.overlayScaleSlider) this.overlayScaleSlider.value = 0.85;
            if (this.overlayScaleLabel) this.overlayScaleLabel.innerText = "0.85x";
            if (this.overlayOpacitySlider) this.overlayOpacitySlider.value = 1.0;
            if (this.overlayOpacityLabel) this.overlayOpacityLabel.innerText = "100%";
            if (this.overlayOptionsBar) this.overlayOptionsBar.style.display = "flex";
            this.showToast(`${label} placed. Drag or scale to fit!`, "✨");
        };
        img.onerror = () => {
            if (!img.src.startsWith("/")) {
                img.src = `/accessories/${filename}`;
            } else {
                this.showToast("Failed to load accessory image.", "❌");
            }
        };
        img.src = `/accessories/${filename}`;
    }

    initEvents() {
        // File Upload
        this.fileInput.addEventListener("change", (e) => this.handleFileUpload(e));

        // Overlay file upload & BG file upload
        if (this.overlayFileInput) {
            this.overlayFileInput.addEventListener("change", (e) => this.handleOverlayFileUpload(e));
        }
        if (this.bgFileInput) {
            this.bgFileInput.addEventListener("change", (e) => this.handleBgFileUpload(e));
        }

        // Initialize Crop, Drawing & Text Box event listeners
        this.initCropAndDrawingEvents();
        this.initTextBoxEvents();

        // Split slider mouse dragging
        let isDraggingSplit = false;
        const onMouseMove = (e) => {
            if (!isDraggingSplit) return;
            const rect = this.canvasRaw.getBoundingClientRect();
            if (rect.width === 0) return;
            let p = ((e.clientX - rect.left) / rect.width) * 100;
            p = Math.max(0, Math.min(100, p));
            this.setSplitPercent(p);
        };
        const onMouseUp = () => { isDraggingSplit = false; };

        this.splitBar.addEventListener("mousedown", (e) => {
            e.stopPropagation();
            isDraggingSplit = true;
        });
        this.splitKnob.addEventListener("mousedown", (e) => {
            e.stopPropagation();
            isDraggingSplit = true;
        });
        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);

        // Canvas-Only Zooming via Mouse Wheel (Keeps page stationary)
        this.viewport.addEventListener("wheel", (e) => {
            e.preventDefault();
            e.stopPropagation();
            const factor = e.deltaY < 0 ? 1.15 : (1 / 1.15);
            this.zoomAtPoint(factor, e.clientX, e.clientY);
        }, { passive: false });

        // Prevent accidental whole-page browser zoom with Ctrl+Wheel
        window.addEventListener("wheel", (e) => {
            if (e.ctrlKey) {
                e.preventDefault();
            }
        }, { passive: false });

        // Canvas Panning / Hand Tool (Spacebar + Drag, Middle-click, or Move Tool)
        let panStartX = 0;
        let panStartY = 0;
        let initialPanX = 0;
        let initialPanY = 0;

        this.viewport.addEventListener("mousedown", (e) => {
            if (e.target === this.splitBar || e.target === this.splitKnob) return;

            // 1. Selective Processing Brush Painting
            if (this.activeTool === "brush" && e.button === 0 && !this.isSpacePressed) {
                this.isPaintingBrush = true;
                this.hasBrushStrokes = true;
                this.paintBrushAt(e.clientX, e.clientY);
                e.preventDefault();
                return;
            }

            // 2. Color Splash Pipette Sample
            if (this.activeTool === "splash" && e.button === 0) {
                this.sampleColorSplashAt(e.clientX, e.clientY);
                e.preventDefault();
                return;
            }

            // 3. Type Tool: Click on canvas to set text coordinate & show on-canvas text box
            if (this.activeTool === "text" && e.button === 0) {
                if (e.target && e.target.closest && e.target.closest("#canvasTextBox")) {
                    return;
                }
                const rect = this.canvasRaw.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    const clickX = e.clientX - rect.left;
                    const clickY = e.clientY - rect.top;
                    const scaleX = this.canvasRaw.naturalWidth / rect.width;
                    const scaleY = this.canvasRaw.naturalHeight / rect.height;
                    this.textCoords.x = Math.max(0, Math.round(clickX * scaleX));
                    this.textCoords.y = Math.max(0, Math.round(clickY * scaleY));

                    if (this.canvasTextBox) {
                        const boxW = 320;
                        const boxH = 140;
                        const posX = Math.max(0, Math.min(rect.width - boxW, clickX));
                        const posY = Math.max(0, Math.min(rect.height - boxH, clickY));
                        this.canvasTextBox.style.left = `${posX}px`;
                        this.canvasTextBox.style.top = `${posY}px`;
                        this.canvasTextBox.style.display = "flex";
                        if (this.canvasTextInput) {
                            setTimeout(() => {
                                this.canvasTextInput.focus();
                                this.canvasTextInput.select();
                            }, 50);
                        }
                    }
                    this.showToast(`مربع النص نشط في الإحداثيات: (${this.textCoords.x}, ${this.textCoords.y})`, "🔤");
                }
                e.preventDefault();
                return;
            }

            // 3. Middle mouse (button 1) OR Spacebar held OR Move tool active
            if (e.button === 1 || this.isSpacePressed || this.activeTool === "move") {
                this.isPanning = true;
                panStartX = e.clientX;
                panStartY = e.clientY;
                initialPanX = this.panX;
                initialPanY = this.panY;
                this.viewport.classList.add("panning", "dragging");
                e.preventDefault();
            } else if (this.activeTool === "zoom") {
                const factor = e.altKey ? 0.75 : 1.35;
                this.zoomAtPoint(factor, e.clientX, e.clientY);
            }
        });

        window.addEventListener("mousemove", (e) => {
            // Pan logic
            if (this.isPanning) {
                const dx = e.clientX - panStartX;
                const dy = e.clientY - panStartY;
                this.panX = initialPanX + dx;
                this.panY = initialPanY + dy;
                this.applyTransform();
                return;
            }

            // Brush painting logic
            if (this.isPaintingBrush && this.activeTool === "brush") {
                this.paintBrushAt(e.clientX, e.clientY);
            }

            // Move custom circular brush cursor
            if (this.activeTool === "brush" && this.brushCursor) {
                const rect = this.viewport.getBoundingClientRect();
                if (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom) {
                    this.brushCursor.style.display = "block";
                    this.brushCursor.style.left = `${e.clientX - rect.left}px`;
                    this.brushCursor.style.top = `${e.clientY - rect.top}px`;
                    const renderDiameter = Math.max(8, this.brushSize * this.zoomScale);
                    this.brushCursor.style.width = `${renderDiameter}px`;
                    this.brushCursor.style.height = `${renderDiameter}px`;
                } else {
                    this.brushCursor.style.display = "none";
                }
            }
        });

        window.addEventListener("mouseup", () => {
            if (this.isPanning) {
                this.isPanning = false;
                this.viewport.classList.remove("dragging");
                if (!this.isSpacePressed && this.activeTool !== "move") {
                    this.viewport.classList.remove("panning");
                }
            }
            if (this.isPaintingBrush) {
                this.isPaintingBrush = false;
                this.compositeSelectiveBrush();
            }
        });

        // Double click inside viewport resets zoom to 100% and centers
        this.viewport.addEventListener("dblclick", (e) => {
            if (e.target === this.splitBar || e.target === this.splitKnob) return;
            this.resetZoom();
        });

        // Full Photoshop Professional Keyboard Shortcut Engine
        window.addEventListener("keydown", (e) => {
            // Allow Escape key even in inputs to blur or close
            if (e.key === "Escape") {
                this.closeShortcutsModal();
                this.closeNotchModal();
                this.closeBgReplaceModal();
                this.cancelTextTool();
                this.cancelOverlay();
                this.closeAllFlyouts();
                if (document.activeElement) document.activeElement.blur();
                return;
            }

            // Enter key to apply active Text or Overlay
            if (e.key === "Enter" && !(e.target.tagName === "INPUT" && e.target.id !== "textOverlayInput")) {
                if (this.textOptionsBar && this.textOptionsBar.style.display !== "none") {
                    this.applyTextToImage();
                    return;
                }
                if (this.overlayOptionsBar && this.overlayOptionsBar.style.display !== "none") {
                    this.applyOverlayToImage();
                    return;
                }
            }

            // Do not intercept standard typing in text inputs or textareas
            if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") {
                return;
            }

            const isCtrl = e.ctrlKey || e.metaKey;
            const isShift = e.shiftKey;

            // 1. Tab: Zen Fullscreen Canvas Mode
            if (e.key === "Tab") {
                e.preventDefault();
                document.body.classList.toggle("zen-mode");
                const isZen = document.body.classList.contains("zen-mode");
                this.showToast(isZen ? "Zen Fullscreen Mode (Press Tab to Exit)" : "Standard Interface Restored", "📐");
                return;
            }

            // 2. Spacebar: Hand Tool (Pan Mode)
            if (e.code === "Space" && !e.repeat) {
                this.isSpacePressed = true;
                this.viewport.classList.add("panning");
                e.preventDefault();
                return;
            }

            // 3. Single-Key Tool Switching
            if (!isCtrl && !isShift) {
                if (e.code === "KeyV") {
                    const btn = document.querySelector(".ps-tbtn[title*='Move']");
                    if (btn) this.activateToolGroup(btn, "move");
                    this.showToast("Move Tool (V)", "✋");
                    return;
                }
                if (e.code === "KeyT") {
                    const btn = document.getElementById("btnTextTool");
                    if (btn) this.activateToolGroup(btn, "text");
                    this.showToast("Horizontal Type Tool (T)", "🔤");
                    return;
                }
                if (e.code === "KeyB") {
                    const btn = document.getElementById("btnBrushTool");
                    if (btn) this.activateToolGroup(btn, "brush");
                    this.showToast("Selective Brush Tool (B)", "🖌");
                    return;
                }
                if (e.code === "KeyE") {
                    this.clearBrushMask();
                    this.showToast("Brush Mask Cleared (E)", "🧹");
                    return;
                }
                if (e.code === "KeyI") {
                    const btn = document.querySelector(".ps-tbtn[title*='Eyedropper']");
                    if (btn) this.activateToolGroup(btn, "eyedropper");
                    this.showToast("Eyedropper Tool (I)", "🧪");
                    return;
                }
                if (e.code === "KeyS") {
                    const btn = document.getElementById("btnSplashTool");
                    if (btn) this.activateToolGroup(btn, "splash");
                    this.showToast("Color Splash Pipette (S)", "🎨");
                    return;
                }
                if (e.code === "KeyZ") {
                    const btn = document.querySelector(".ps-tbtn[title*='Zoom']");
                    if (btn) this.activateToolGroup(btn, "zoom");
                    this.showToast("Zoom Tool (Z)", "🔍");
                    return;
                }
                if (e.code === "KeyM") {
                    this.togglePixelLoupe();
                    this.showToast(this.isLoupeActive ? "7×7 Matrix HUD Enabled (M)" : "7×7 Matrix HUD Hidden (M)", "🔬");
                    return;
                }
                if (e.code === "KeyG") {
                    if (typeof toggleAirGestures === "function") toggleAirGestures();
                    return;
                }
                if (e.code === "KeyN") {
                    this.openNotchModal();
                    this.showToast("2D-FFT Notch Reject Filter (N)", "📡");
                    return;
                }
                if (e.key === "\\" || e.code === "Backslash") {
                    this.splitCycle = ((this.splitCycle || 0) + 1) % 3;
                    if (this.splitCycle === 0) {
                        this.setSplitPercent(50);
                        this.showToast("Compare Split: 50%", "⚖️");
                    } else if (this.splitCycle === 1) {
                        this.setSplitPercent(0);
                        this.showToast("View: 100% Processed", "✨");
                    } else {
                        this.setSplitPercent(100);
                        this.showToast("View: 100% Original", "🖼");
                    }
                    return;
                }
                if (e.key === "[" || e.code === "BracketLeft") {
                    this.setBrushSize(this.brushSize - 5);
                    if (this.brushSizeSlider) this.brushSizeSlider.value = this.brushSize;
                    this.showToast(`Brush Size: ${this.brushSize}px`, "🖌");
                    return;
                }
                if (e.key === "]" || e.code === "BracketRight") {
                    this.setBrushSize(this.brushSize + 5);
                    if (this.brushSizeSlider) this.brushSizeSlider.value = this.brushSize;
                    this.showToast(`Brush Size: ${this.brushSize}px`, "🖌");
                    return;
                }
                if (e.key === "F1" || e.key === "?") {
                    this.openShortcutsModal();
                    return;
                }
                if (e.key === "F12") {
                    this.setFilter("none", {}, "Original Image", "");
                    this.showToast("Reverted to Original Image (F12)", "🔄");
                    return;
                }
            }

            // 4. Shift + Bracket: Brush Feather (Hardness / Softness)
            if (isShift && !isCtrl) {
                if (e.key === "{" || e.code === "BracketLeft") {
                    this.setBrushFeather(Math.max(0, this.brushFeather - 15));
                    if (this.brushFeatherSlider) this.brushFeatherSlider.value = this.brushFeather;
                    this.showToast(`Brush Feather: ${this.brushFeather}% (Softer)`, "🪶");
                    return;
                }
                if (e.key === "}" || e.code === "BracketRight") {
                    this.setBrushFeather(Math.min(100, this.brushFeather + 15));
                    if (this.brushFeatherSlider) this.brushFeatherSlider.value = this.brushFeather;
                    this.showToast(`Brush Feather: ${this.brushFeather}% (Harder)`, "🪶");
                    return;
                }
                if (e.key === "?") {
                    this.openShortcutsModal();
                    return;
                }
            }

            // 5. Ctrl Combinations
            if (isCtrl) {
                if (isShift && e.code === "KeyB") {
                    e.preventDefault();
                    this.removeBackground();
                    return;
                }
                if (isShift && e.code === "KeyP") {
                    e.preventDefault();
                    if (this.overlayFileInput) this.overlayFileInput.click();
                    return;
                }
                if (isShift && e.code === "KeyM") {
                    e.preventDefault();
                    this.openBlendModal();
                    return;
                }
                if (isShift && e.code === "KeyG") {
                    e.preventDefault();
                    this.openCollageModal();
                    return;
                }
                if (isShift && e.code === "KeyU") {
                    e.preventDefault();
                    this.setFilter("color_space", { target: "gray" }, "Convert to Grayscale (Desaturate)", "");
                    this.showToast("Desaturate Grayscale (Ctrl+Shift+U)", "⚪");
                    return;
                }
                if (e.code === "KeyO") {
                    e.preventDefault();
                    if (this.fileInput) this.fileInput.click();
                    return;
                }
                if (e.code === "KeyS") {
                    e.preventDefault();
                    this.downloadResult();
                    this.showToast("Exporting Image (Ctrl+S)", "💾");
                    return;
                }
                if (e.code === "KeyI") {
                    e.preventDefault();
                    this.setFilter("negative", {}, "Invert Negative", "");
                    this.showToast("Invert Negative (Ctrl+I)", "🎞");
                    return;
                }
                if (e.code === "KeyL") {
                    e.preventDefault();
                    this.setFilter("histogram_equalization", { method: "global" }, "Global Histogram Equalization", "");
                    this.showToast("Histogram Equalization (Ctrl+L)", "📊");
                    return;
                }
                if (e.code === "KeyM") {
                    e.preventDefault();
                    this.setFilter("gamma", { gamma: 0.6 }, "Gamma Correction", "");
                    this.showToast("Gamma Correction (Ctrl+M)", "⚡");
                    return;
                }
                if (!isShift && e.code === "KeyZ") {
                    e.preventDefault();
                    this.undo();
                    return;
                }
                if ((!isShift && e.code === "KeyY") || (isShift && e.code === "KeyZ")) {
                    e.preventDefault();
                    this.redo();
                    return;
                }
                if (e.key === "=" || e.key === "+") {
                    e.preventDefault();
                    this.zoomStep(1.25);
                    this.showToast(`Zoom: ${this.zoomLevel}%`, "🔍");
                    return;
                }
                if (e.key === "-" || e.key === "_") {
                    e.preventDefault();
                    this.zoomStep(0.8);
                    this.showToast(`Zoom: ${this.zoomLevel}%`, "🔍");
                    return;
                }
                if (e.key === "0") {
                    e.preventDefault();
                    this.resetZoom();
                    this.showToast("Actual Pixels: 100% (Ctrl+0)", "🎯");
                    return;
                }
                if (e.key === "1") {
                    e.preventDefault();
                    this.fitToScreen();
                    this.showToast(`Fit to Screen: ${this.zoomLevel}% (Ctrl+1)`, "🖥");
                    return;
                }
            }
        });

        window.addEventListener("keyup", (e) => {
            if (e.code === "Space") {
                this.isSpacePressed = false;
                if (!this.isPanning && this.activeTool !== "move") {
                    this.viewport.classList.remove("panning");
                }
            }
        });

        // Pixel inspector tracking
        this.canvasRaw.addEventListener("mousemove", (e) => this.handleCanvasHover(e));
        this.canvasProcessed.addEventListener("mousemove", (e) => this.handleCanvasHover(e));

        // Interactive 2D-FFT Notch Canvas Click
        if (this.notchSpectrumCanvas) {
            this.notchSpectrumCanvas.addEventListener("click", (e) => this.handleNotchCanvasClick(e));
        }

        // Close flyouts when clicking outside
        window.addEventListener("click", (e) => {
            if (!e.target.closest(".ps-tool-group")) {
                this.closeAllFlyouts();
            }
        });
    }

    toggleFlyout(btn) {
        const group = btn.closest(".ps-tool-group");
        const isOpen = group.classList.contains("open");
        this.closeAllFlyouts();
        if (!isOpen) {
            group.classList.add("open");
        }
    }

    closeAllFlyouts() {
        document.querySelectorAll(".ps-tool-group.open").forEach(g => g.classList.remove("open"));
    }

    selectSubTool(op, params, title, controlsHtml, groupId) {
        this.closeAllFlyouts();
        document.querySelectorAll(".ps-tbtn").forEach(b => b.classList.remove("active"));

        if (groupId) {
            const group = document.getElementById(groupId);
            if (group) {
                const btn = group.querySelector(".ps-tbtn");
                if (btn) btn.classList.add("active");
            }
        }

        document.querySelectorAll(".ps-flyout-item").forEach(item => item.classList.remove("selected"));
        if (event && event.currentTarget) {
            event.currentTarget.classList.add("selected");
        }

        this.setFilter(op, params, title, controlsHtml);
    }

    activateToolGroup(btn, toolType) {
        this.closeAllFlyouts();
        document.querySelectorAll(".ps-tbtn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.activeTool = toolType;

        // Hide tool options by default
        if (this.brushOptionsBar) this.brushOptionsBar.style.display = "none";
        if (this.brushCursor) this.brushCursor.style.display = "none";
        if (this.textOptionsBar && toolType !== "text") this.textOptionsBar.style.display = "none";
        if (this.canvasTextBox && toolType !== "text") this.canvasTextBox.style.display = "none";
        if (this.cropOptionsBar && toolType !== "crop") this.cropOptionsBar.style.display = "none";
        if (this.cropOverlay && toolType !== "crop") this.cropOverlay.style.display = "none";
        if (this.drawOptionsBar && toolType !== "draw") this.drawOptionsBar.style.display = "none";
        if (this.drawingCanvas) this.drawingCanvas.style.pointerEvents = toolType === "draw" ? "auto" : "none";
        this.viewport.style.cursor = "default";

        if (toolType === "crop") {
            this.filterTitle.innerText = "Crop Tool (اسحب الإطار لتحديد أبعاد القص ثم اضغط Apply Crop)";
            if (this.cropOptionsBar) this.cropOptionsBar.style.display = "flex";
            if (this.cropOverlay) this.cropOverlay.style.display = "block";
            this.initCropBox();
            this.viewport.style.cursor = "crosshair";
        } else if (toolType === "draw") {
            this.filterTitle.innerText = "Drawing & Shapes Suite (ارسم حراً أو اختر أشكال هندسية بألوان وأحجام مختلفة)";
            if (this.drawOptionsBar) this.drawOptionsBar.style.display = "flex";
            if (this.drawingCanvas) {
                this.drawingCanvas.style.pointerEvents = "auto";
                this.drawingCanvas.style.cursor = "crosshair";
            }
            this.viewport.style.cursor = "crosshair";
        } else if (toolType === "eyedropper") {
            this.filterTitle.innerText = "Eyedropper / Pixel Loupe Sampler";
            this.viewport.style.cursor = "crosshair";
        } else if (toolType === "move") {
            this.filterTitle.innerText = "Move Tool (Canvas Pan: Drag with Mouse / Space+Drag)";
            this.viewport.style.cursor = "grab";
        } else if (toolType === "zoom") {
            this.filterTitle.innerText = "Zoom View Tool (Mouse Wheel / Click / Alt+Click)";
            this.viewport.style.cursor = "zoom-in";
        } else if (toolType === "brush") {
            this.filterTitle.innerText = "Selective Processing Brush (Draw filter on selected areas)";
            if (this.brushOptionsBar) this.brushOptionsBar.style.display = "flex";
            this.viewport.style.cursor = "crosshair";
            if (this.brushMaskCanvas) this.brushMaskCanvas.style.display = "block";
        } else if (toolType === "splash") {
            this.filterTitle.innerText = "Color Splash Pipette (Click on any color to isolate it!)";
            this.viewport.style.cursor = "crosshair";
        } else if (toolType === "text") {
            this.filterTitle.innerText = "Horizontal Type Tool (T): انقر على الصورة لوضع مربع الكتابة، أو اكتب مباشرة واضغط تطبيق";
            if (this.textOptionsBar) this.textOptionsBar.style.display = "flex";
            if (this.canvasTextBox) {
                this.canvasTextBox.style.display = "flex";
                if (this.canvasTextInput) {
                    setTimeout(() => {
                        this.canvasTextInput.focus();
                        this.canvasTextInput.select();
                    }, 50);
                }
            }
            this.viewport.style.cursor = "text";
        } else if (toolType === "cutout") {
            this.filterTitle.innerText = "أداة موازنة وتفريغ عزل الخلفية (Background Removal & Cutout Suite)";
            this.viewport.style.cursor = "default";
            this.setCutoutMode(this.activeCutoutMode || "grabcut");
        }
    }

    setSplitPercent(p) {
        this.splitPercent = p;
        this.splitBar.style.left = `${p}%`;
        this.splitKnob.style.left = `${p}%`;
        if (!this.hasBrushStrokes) {
            this.canvasProcessed.style.clipPath = `polygon(${p}% 0, 100% 0, 100% 100%, ${p}% 100%)`;
        }
    }

    applyTransform() {
        if (!this.docFrame) return;
        this.docFrame.style.transform = `translate(${this.panX}px, ${this.panY}px) scale(${this.zoomScale})`;
        this.updateZoomDisplay();
    }

    updateZoomDisplay() {
        const percent = Math.round(this.zoomScale * 100);
        this.zoomLevel = percent;
        if (this.statusZoom) {
            this.statusZoom.innerText = `${percent}%`;
        }
        if (this.docTabTitle) {
            const name = this.currentFileName || "benchmark.png";
            this.docTabTitle.innerText = `${name} @ ${percent}% (RGB/8#)*`;
        }
    }

    zoomAtPoint(factor, clientX, clientY) {
        if (!this.viewport) return;
        const vRect = this.viewport.getBoundingClientRect();
        const cx = clientX - (vRect.left + vRect.width / 2);
        const cy = clientY - (vRect.top + vRect.height / 2);

        const dx = (cx - this.panX) / this.zoomScale;
        const dy = (cy - this.panY) / this.zoomScale;

        const newScale = Math.min(Math.max(this.zoomScale * factor, 0.15), 15.0);
        this.panX = cx - dx * newScale;
        this.panY = cy - dy * newScale;
        this.zoomScale = newScale;

        this.applyTransform();
    }

    zoomStep(factor) {
        if (!this.viewport) return;
        const vRect = this.viewport.getBoundingClientRect();
        const cx = vRect.left + vRect.width / 2;
        const cy = vRect.top + vRect.height / 2;
        this.zoomAtPoint(factor, cx, cy);
    }

    resetZoom() {
        this.zoomScale = 1.0;
        this.panX = 0;
        this.panY = 0;
        this.applyTransform();
    }

    fitToScreen() {
        if (!this.canvasRaw || !this.canvasRaw.naturalWidth || !this.viewport) {
            this.resetZoom();
            return;
        }
        const vRect = this.viewport.getBoundingClientRect();
        const pad = 40;
        const scaleW = (vRect.width - pad) / this.canvasRaw.naturalWidth;
        const scaleH = (vRect.height - pad) / this.canvasRaw.naturalHeight;
        this.zoomScale = Math.min(scaleW, scaleH, 1.0);
        this.panX = 0;
        this.panY = 0;
        this.applyTransform();
    }

    loadSampleImage(filename) {
        if (!this.isRestoringHistory && this.rawImageBase64) {
            this.pushUndoSnapshot(`Open Sample: ${filename}`);
        }
        this.currentFileName = filename;
        const img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => {
            const tempCanvas = document.createElement("canvas");
            tempCanvas.width = img.width;
            tempCanvas.height = img.height;
            const ctx = tempCanvas.getContext("2d");
            ctx.drawImage(img, 0, 0);
            this.rawImageBase64 = tempCanvas.toDataURL("image/png");
            this.canvasRaw.src = this.rawImageBase64;
            this.updateZoomDisplay();
            this.statusDimensions.innerText = `${img.width} × ${img.height} px`;

            // Resize Brush Mask Canvas to match image native resolution
            if (this.brushMaskCanvas) {
                this.brushMaskCanvas.width = img.width;
                this.brushMaskCanvas.height = img.height;
                this.clearBrushMask();
            }

            // Resize Drawing Canvas to match image native resolution
            if (this.drawingCanvas) {
                this.drawingCanvas.width = img.width;
                this.drawingCanvas.height = img.height;
                this.clearDrawingLayer();
            }

            this.cacheRawImageBitmap(img);
            this.applyCurrentFilter();
        };
        img.onerror = () => {
            if (!img.src.startsWith("/")) {
                img.src = `/samples/${filename}`;
            } else {
                this.showToast(`تعذر تحميل صورة العينة: ${filename}`, "❌");
            }
        };
        img.src = `/samples/${filename}`;
    }

    handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        if (!this.isRestoringHistory && this.rawImageBase64) {
            this.pushUndoSnapshot(`Open File: ${file.name}`);
        }
        this.currentFileName = file.name;
        this.activeOperation = "none";
        this.activeParams = {};
        if (this.filterTitle) this.filterTitle.innerText = "Original Image";
        if (this.dynamicControls) this.dynamicControls.innerHTML = "<div style='color:#888; font-size:11px; padding:8px 0;'>الصورة الأصلية (بدون فلاتر). اختر أي فلتر أو أداة لتطبيقه.</div>";
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                this.rawImageBase64 = event.target.result;
                this.canvasRaw.src = this.rawImageBase64;
                this.updateZoomDisplay();
                this.statusDimensions.innerText = `${img.width} × ${img.height} px`;

                if (this.brushMaskCanvas) {
                    this.brushMaskCanvas.width = img.width;
                    this.brushMaskCanvas.height = img.height;
                    this.clearBrushMask();
                }

                if (this.drawingCanvas) {
                    this.drawingCanvas.width = img.width;
                    this.drawingCanvas.height = img.height;
                    this.clearDrawingLayer();
                }

                this.cacheRawImageBitmap(img);
                this.applyCurrentFilter();
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }

    cacheRawImageBitmap(img) {
        this.rawOffscreenCanvas.width = img.width;
        this.rawOffscreenCanvas.height = img.height;
        this.rawOffscreenCtx.drawImage(img, 0, 0);
    }

    cacheProcessedImageBitmap() {
        const img = new Image();
        img.onload = () => {
            this.procOffscreenCanvas.width = img.width;
            this.procOffscreenCanvas.height = img.height;
            this.procOffscreenCtx.drawImage(img, 0, 0);
        };
        img.src = this.processedImageBase64;
    }

    // =========================================================================
    // SUPERPOWER 1: SELECTIVE PROCESSING BRUSH IMPLEMENTATION
    // =========================================================================
    setBrushSize(val) {
        this.brushSize = parseInt(val) || 35;
        if (this.brushSizeLabel) this.brushSizeLabel.innerText = `${this.brushSize}px`;
    }

    setBrushFeather(val) {
        this.brushFeather = parseInt(val) || 50;
    }

    clearBrushMask() {
        if (!this.brushMaskCanvas || !this.brushMaskCtx) return;
        this.brushMaskCtx.clearRect(0, 0, this.brushMaskCanvas.width, this.brushMaskCanvas.height);
        this.hasBrushStrokes = false;

        // Restore standard split slider view
        this.splitBar.style.display = "block";
        this.splitKnob.style.display = "block";
        if (this.processedImageBase64) {
            this.canvasProcessed.src = this.processedImageBase64;
        }
        this.setSplitPercent(this.splitPercent);
    }

    paintBrushAt(clientX, clientY) {
        if (!this.brushMaskCanvas || !this.brushMaskCtx || !this.canvasRaw) return;
        const rect = this.canvasRaw.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return;

        const scaleX = this.canvasRaw.naturalWidth / rect.width;
        const scaleY = this.canvasRaw.naturalHeight / rect.height;
        const imgX = (clientX - rect.left) * scaleX;
        const imgY = (clientY - rect.top) * scaleY;

        const radius = Math.max(3, this.brushSize / 2);
        const innerRadius = radius * (1.0 - (this.brushFeather / 100.0) * 0.85);

        const gradient = this.brushMaskCtx.createRadialGradient(imgX, imgY, innerRadius, imgX, imgY, radius);
        gradient.addColorStop(0, "rgba(255, 255, 255, 1.0)");
        gradient.addColorStop(1, "rgba(255, 255, 255, 0.0)");

        this.brushMaskCtx.fillStyle = gradient;
        this.brushMaskCtx.beginPath();
        this.brushMaskCtx.arc(imgX, imgY, radius, 0, Math.PI * 2);
        this.brushMaskCtx.fill();
    }

    compositeSelectiveBrush() {
        if (!this.hasBrushStrokes || !this.processedImageBase64 || !this.rawImageBase64) return;
        const width = this.canvasRaw.naturalWidth;
        const height = this.canvasRaw.naturalHeight;
        if (!width || !height) return;

        const compCanvas = document.createElement("canvas");
        compCanvas.width = width;
        compCanvas.height = height;
        const compCtx = compCanvas.getContext("2d");

        // 1. Draw raw background
        compCtx.drawImage(this.rawOffscreenCanvas, 0, 0);

        // 2. Prepare masked filter layer
        const tempCanvas = document.createElement("canvas");
        tempCanvas.width = width;
        tempCanvas.height = height;
        const tempCtx = tempCanvas.getContext("2d");

        const procImg = new Image();
        procImg.onload = () => {
            tempCtx.drawImage(procImg, 0, 0);
            tempCtx.globalCompositeOperation = "destination-in";
            tempCtx.drawImage(this.brushMaskCanvas, 0, 0);

            // 3. Composite over raw
            compCtx.drawImage(tempCanvas, 0, 0);

            // Update processed canvas and disable split clip-path
            this.canvasProcessed.src = compCanvas.toDataURL("image/png");
            this.canvasProcessed.style.clipPath = "none";
            this.splitBar.style.display = "none";
            this.splitKnob.style.display = "none";
        };
        procImg.src = this.processedImageBase64;
    }

    // =========================================================================
    // SUPERPOWER 4: SMART COLOR SPLASH PIPETTE & PALETTE EXTRACTOR
    // =========================================================================
    sampleColorSplashAt(clientX, clientY) {
        const rect = this.canvasRaw.getBoundingClientRect();
        if (rect.width === 0) return;
        const scaleX = this.canvasRaw.naturalWidth / rect.width;
        const scaleY = this.canvasRaw.naturalHeight / rect.height;
        const imgX = Math.floor((clientX - rect.left) * scaleX);
        const imgY = Math.floor((clientY - rect.top) * scaleY);

        if (imgX >= 0 && imgY >= 0 && imgX < this.rawOffscreenCanvas.width && imgY < this.rawOffscreenCanvas.height) {
            const pixel = this.rawOffscreenCtx.getImageData(imgX, imgY, 1, 1).data;
            const r = pixel[0], g = pixel[1], b = pixel[2];
            const target_bgr = [b, g, r];
            const hex = `#{:02X}{:02X}{:02X}`.replace(/:02X/g, (m, offset) => {
                const val = offset === 1 ? r : (offset === 5 ? g : b);
                return val.toString(16).padStart(2, '0').toUpperCase();
            });

            this.setFilter("color_splash", { target_bgr: target_bgr, tolerance: 26 }, `Color Splash (Target: RGB(${r}, ${g}, ${b}))`,
                `<div class='ps-prop-row'><span>Sampled Color:</span><span style='color:${hex}; font-weight:bold;'>${hex}</span></div>` +
                `<div class='ps-prop-row'><span>Hue Tolerance:</span><span id='val_tolerance' style='color:#fff;'>26°</span></div>` +
                `<input type='range' class='ps-range' min='8' max='60' value='26' data-param='tolerance'>`
            );
        }
    }

    renderPalette(palette) {
        if (!this.paletteList || !palette || !palette.length) return;
        this.paletteList.innerHTML = "";
        palette.forEach(p => {
            const chip = document.createElement("div");
            chip.className = "ps-palette-chip";
            chip.style.backgroundColor = p.hex;
            chip.setAttribute("data-hex", `${p.hex} (${p.percent}%)`);
            chip.title = `Click to copy ${p.hex} (${p.percent}%)`;
            chip.onclick = () => {
                navigator.clipboard.writeText(p.hex);
                alert(`تم نسخ كود اللون ${p.hex} إلى الحافظة بنجاح!`);
            };
            this.paletteList.appendChild(chip);
        });
    }

    refreshPalette() {
        if (!this.rawImageBase64) return;
        this.applyCurrentFilter();
    }

    // =========================================================================
    // SUPERPOWER 5: DIP LAYER FX & BLEND MODES
    // =========================================================================
    setBlendMode(mode) {
        this.blendMode = mode || "normal";
        if (this.canvasProcessed) {
            this.canvasProcessed.style.mixBlendMode = this.blendMode;
        }
        if (this.blendModeSelect) {
            this.blendModeSelect.value = this.blendMode;
        }
    }

    setLayerOpacity(val) {
        const num = Math.min(100, Math.max(0, parseInt(val) || 100));
        this.layerOpacity = num;
        if (this.canvasProcessed) {
            this.canvasProcessed.style.opacity = (num / 100).toString();
        }
        if (this.layerOpacityInput && !this.layerOpacityInput.matches(":focus")) {
            this.layerOpacityInput.value = `${num}%`;
        }
    }

    // =========================================================================
    // SUPERPOWER 6: 7x7 NUMERIC PIXEL MATRIX LOUPE INSPECTOR
    // =========================================================================
    togglePixelLoupe() {
        this.isLoupeActive = !this.isLoupeActive;
        if (this.pixelMatrixLoupe) {
            this.pixelMatrixLoupe.style.display = this.isLoupeActive ? "flex" : "none";
        }
        const btn = document.getElementById("btnToggleLoupe");
        if (btn) {
            btn.style.background = this.isLoupeActive ? "rgba(0,229,255,0.2)" : "";
        }
    }

    updatePixelMatrixLoupe(centerX, centerY) {
        if (!this.isLoupeActive || !this.loupeGrid || !this.rawOffscreenCanvas.width) return;

        const w = this.rawOffscreenCanvas.width;
        const h = this.rawOffscreenCanvas.height;
        if (centerX < 0 || centerY < 0 || centerX >= w || centerY >= h) return;

        const half = 3; // 7x7 grid (-3 to +3)
        const startX = Math.max(0, centerX - half);
        const startY = Math.max(0, centerY - half);
        const blockW = Math.min(7, w - startX);
        const blockH = Math.min(7, h - startY);

        try {
            const rawData = this.rawOffscreenCtx.getImageData(startX, startY, blockW, blockH).data;
            const procData = (this.procOffscreenCanvas.width === w) ?
                this.procOffscreenCtx.getImageData(startX, startY, blockW, blockH).data : null;

            this.loupeGrid.innerHTML = "";
            let centerRawLum = 0;
            let centerProcLum = 0;

            for (let r = 0; r < 7; r++) {
                for (let c = 0; c < 7; c++) {
                    const cell = document.createElement("div");
                    cell.className = "ps-matrix-cell";

                    const curX = centerX - half + c;
                    const curY = centerY - half + r;

                    if (curX >= 0 && curX < w && curY >= 0 && curY < h && (curX - startX) < blockW && (curY - startY) < blockH) {
                        const localIdx = ((curY - startY) * blockW + (curX - startX)) * 4;
                        const red = rawData[localIdx];
                        const green = rawData[localIdx + 1];
                        const blue = rawData[localIdx + 2];
                        const lum = Math.round(0.299 * red + 0.587 * green + 0.114 * blue);

                        cell.style.backgroundColor = `rgb(${red},${green},${blue})`;
                        cell.innerText = lum;

                        if (r === half && c === half) {
                            cell.classList.add("center");
                            centerRawLum = lum;
                            if (this.loupeCenterVal) this.loupeCenterVal.innerText = `RGB(${red},${green},${blue})`;
                            if (procData) {
                                const pr = procData[localIdx];
                                const pg = procData[localIdx + 1];
                                const pb = procData[localIdx + 2];
                                centerProcLum = Math.round(0.299 * pr + 0.587 * pg + 0.114 * pb);
                            }
                        }
                    } else {
                        cell.style.backgroundColor = "#080808";
                        cell.innerText = "-";
                    }
                    this.loupeGrid.appendChild(cell);
                }
            }

            if (this.loupeCenterCoord) this.loupeCenterCoord.innerText = `X:${centerX} Y:${centerY}`;
            if (this.loupeDeltaVal) {
                const diff = Math.abs(centerRawLum - centerProcLum);
                this.loupeDeltaVal.innerText = `Δ ${diff} (${centerRawLum} → ${centerProcLum})`;
            }
        } catch (e) {
            console.error("Matrix loupe sampling error:", e);
        }
    }

    // =========================================================================
    // SUPERPOWER 3: 2D-FFT NOTCH REJECT MODAL IMPLEMENTATION
    // =========================================================================
    async openNotchModal() {
        if (!this.notchModal || !this.notchSpectrumCanvas || !this.rawImageBase64) return;
        this.notchModal.style.display = "flex";

        try {
            const data = await this.sendApiProcess({ image: this.rawImageBase64, operation: "fft_spectrum" }, "FFT Spectrum");
            if (data && data.status === "success") {
                const img = new Image();
                img.onload = () => {
                    const ctx = this.notchSpectrumCanvas.getContext("2d");
                    ctx.drawImage(img, 0, 0, 256, 256);
                    this.renderNotchOverlay();
                };
                img.src = data.image;
            }
        } catch (e) {
            console.error("FFT spectrum error:", e);
        }
    }

    closeNotchModal() {
        if (this.notchModal) this.notchModal.style.display = "none";
    }

    handleNotchCanvasClick(e) {
        const rect = this.notchSpectrumCanvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const clickY = e.clientY - rect.top;

        const w = this.canvasRaw.naturalWidth || 512;
        const h = this.canvasRaw.naturalHeight || 512;

        // Map 256x256 click to image frequency matrix (u=rows, v=cols)
        const u = Math.round((clickY / 256) * h);
        const v = Math.round((clickX / 256) * w);

        this.notches.push({ u: u, v: v, clickX: clickX, clickY: clickY });
        this.renderNotchOverlay();
        if (this.notchCountDisplay) {
            this.notchCountDisplay.innerText = `${this.notches.length} notches set`;
        }
    }

    renderNotchOverlay() {
        const ctx = this.notchSpectrumCanvas.getContext("2d");
        this.notches.forEach(n => {
            // Draw primary notch point
            ctx.strokeStyle = "#00e5ff";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(n.clickX, n.clickY, 8, 0, Math.PI * 2);
            ctx.stroke();

            // Draw symmetric point
            const symX = 256 - n.clickX;
            const symY = 256 - n.clickY;
            ctx.strokeStyle = "#ff007f";
            ctx.beginPath();
            ctx.arc(symX, symY, 8, 0, Math.PI * 2);
            ctx.stroke();
        });
    }

    clearNotches() {
        this.notches = [];
        if (this.notchCountDisplay) this.notchCountDisplay.innerText = "0 notches set";
        this.openNotchModal();
    }

    applyNotchToImage() {
        this.closeNotchModal();
        if (!this.notches.length) return;
        this.setFilter("notch_filter", { notches: this.notches, d0: 18.0 }, `2D-FFT Notch Filter (${this.notches.length} Notches)`,
            `<div class='ps-prop-row'><span>Active Notches:</span><span style='color:#00e5ff;'>${this.notches.length} Pairs</span></div>` +
            `<div class='ps-prop-row'><span>Notch Radius (D₀):</span><span id='val_d0' style='color:#fff;'>18px</span></div>` +
            `<input type='range' class='ps-range' min='4' max='50' value='18' data-param='d0'>`
        );
    }

    // =========================================================================
    // GENERAL CANVAS INTERACTION & CORE DISPATCH
    // =========================================================================
    handleCanvasHover(e) {
        const rect = this.canvasRaw.getBoundingClientRect();
        const scaleX = this.canvasRaw.naturalWidth / rect.width;
        const scaleY = this.canvasRaw.naturalHeight / rect.height;
        const x = Math.floor((e.clientX - rect.left) * scaleX);
        const y = Math.floor((e.clientY - rect.top) * scaleY);

        if (x >= 0 && y >= 0 && x < this.canvasRaw.naturalWidth && y < this.canvasRaw.naturalHeight) {
            this.hudCoords.innerText = `X: ${x}px  Y: ${y}px`;
            if (this.isLoupeActive) {
                this.updatePixelMatrixLoupe(x, y);
            }
        }
    }

    setFilter(op, params, title, controlsHtml) {
        if (!this.isRestoringHistory && this.rawImageBase64) {
            this.pushUndoSnapshot(this.filterTitle ? this.filterTitle.innerText : "Change Filter");
        }
        this.activeOperation = op;
        this.activeParams = params || {};
        if (title) this.filterTitle.innerText = title;
        if (controlsHtml) {
            this.dynamicControls.innerHTML = controlsHtml;
            this.bindDynamicSliders();
        }
        this.applyCurrentFilter();
    }

    bindDynamicSliders() {
        const inputs = this.dynamicControls.querySelectorAll("input[data-param]");
        inputs.forEach(input => {
            input.addEventListener("pointerdown", () => {
                if (!this.isRestoringHistory && this.rawImageBase64) {
                    const paramName = input.getAttribute("data-param") || "param";
                    this.pushUndoSnapshot(`Adjust ${paramName}`);
                }
            }, { passive: true });

            input.addEventListener("input", (e) => {
                const paramName = e.target.getAttribute("data-param");
                const valDisplay = document.getElementById(`val_${paramName}`);
                if (valDisplay) valDisplay.innerText = e.target.value;
                this.activeParams[paramName] = parseFloat(e.target.value);
                this.debouncedApply();
            });
        });
    }

    debouncedApply() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.applyCurrentFilter();
        }, 60);
    }

    async sendApiProcess(payload, actionDescription = "") {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute("content");
        const headers = { "Content-Type": "application/json" };
        if (csrfToken) {
            headers["X-CSRF-TOKEN"] = csrfToken;
        }

        // Try Laravel Gateway (/api/process) first, then direct Python Server (http://127.0.0.1:5001/api/process)
        const endpoints = [
            "/api/process",
            "http://127.0.0.1:5001/api/process"
        ];

        let lastError = null;
        for (const endpoint of endpoints) {
            try {
                const resp = await fetch(endpoint, {
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify(payload)
                });
                if (!resp.ok) {
                    const errorJson = await resp.json().catch(() => ({}));
                    throw new Error(errorJson.message || `HTTP ${resp.status}`);
                }
                const data = await resp.json();
                return data;
            } catch (err) {
                lastError = err;
            }
        }
        console.error(`API process error for ${actionDescription}:`, lastError);
        this.showToast("تعذر الاتصال بمحرك المعالجة - تأكد من تشغيل الخادم", "⚠️");
        throw lastError;
    }

    async applyCurrentFilter() {
        if (!this.rawImageBase64) return;

        try {
            const payload = {
                image: this.rawImageBase64,
                operation: this.activeOperation,
                params: this.activeParams
            };

            const data = await this.sendApiProcess(payload, this.activeOperation);
            if (data && data.status === "success") {
                this.processedImageBase64 = data.image;
                this.currentHistogram = data.histogram;
                this.currentStats = data.stats;

                if (this.hasBrushStrokes && this.activeTool === "brush") {
                    this.compositeSelectiveBrush();
                } else {
                    this.canvasProcessed.src = data.image;
                }

                this.cacheProcessedImageBitmap();
                this.renderHistogram(data.histogram);
                this.updateStats(data.stats, data.execution_time_ms);
                this.formulaBox.innerText = data.formula || "";
                this.codeSnippet.innerText = data.code || "";
                this.perfBadge.innerText = `⚡ ${data.execution_time_ms}ms (Optimized Engine)`;

                if (data.palette) {
                    this.renderPalette(data.palette);
                }
            }
        } catch (err) {
            console.error("Filter application error:", err);
        }
    }

    renderHistogram(hist) {
        if (!hist) return;
        this.histContainer.innerHTML = "";
        const bars = hist.gray || hist.r || [];
        const maxVal = Math.max(...bars, 1);

        const step = Math.ceil(bars.length / 48);
        for (let i = 0; i < bars.length; i += step) {
            const h = (bars[i] / maxVal) * 100;
            const bar = document.createElement("div");
            bar.className = "ps-hist-bar";
            bar.style.height = `${Math.max(4, h)}%`;
            this.histContainer.appendChild(bar);
        }
    }

    updateStats(stats, ms) {
        if (!stats) return;
        document.getElementById("statMean").innerText = stats.mean ?? "--";
        document.getElementById("statStd").innerText = stats.std_dev ?? "--";
        document.getElementById("statMedian").innerText = stats.median ?? "--";
        document.getElementById("statEntropy").innerText = stats.entropy ?? "--";
    }

    toggleLayerVisibility(index) {
        if (index === 1) {
            const isVis = this.canvasProcessed.style.display !== "none";
            this.canvasProcessed.style.display = isVis ? "none" : "block";
            this.splitBar.style.display = isVis ? "none" : "block";
            this.splitKnob.style.display = isVis ? "none" : "block";
            const eye = document.getElementById("layerEye_1");
            if (eye) eye.style.opacity = isVis ? "0.3" : "1.0";
        }
    }

    downloadResult() {
        if (!this.processedImageBase64) return;
        const a = document.createElement("a");
        a.href = this.processedImageBase64;
        a.download = `visioncraft_${this.activeOperation}.png`;
        a.click();
    }

    copyPythonCode() {
        if (!this.codeSnippet) return;
        navigator.clipboard.writeText(this.codeSnippet.innerText);
        this.showToast("Python Code Copied to Clipboard (Ctrl+C)", "📋");
    }

    showToast(text, icon = "⚡") {
        if (!this.hudToast || !this.hudToastText) return;
        this.hudToastText.innerText = text;
        if (this.hudToastIcon) this.hudToastIcon.innerText = icon;
        this.hudToast.classList.add("show");
        clearTimeout(this.toastTimer);
        this.toastTimer = setTimeout(() => {
            this.hudToast.classList.remove("show");
        }, 1300);
    }

    openShortcutsModal() {
        if (this.shortcutsModalBackdrop) {
            this.shortcutsModalBackdrop.style.display = "flex";
        }
    }

    closeShortcutsModal() {
        if (this.shortcutsModalBackdrop) {
            this.shortcutsModalBackdrop.style.display = "none";
        }
    }

    // =========================================================================
    // PROFESSIONAL UNDO / REDO HISTORY ENGINE (CTRL+Z / CTRL+Y)
    // =========================================================================
    captureCurrentState(description = "") {
        return {
            description: description || (this.filterTitle ? this.filterTitle.innerText : "State"),
            rawImageBase64: this.rawImageBase64,
            processedImageBase64: this.processedImageBase64,
            currentFileName: this.currentFileName,
            activeOperation: this.activeOperation,
            activeParams: JSON.parse(JSON.stringify(this.activeParams || {})),
            filterTitle: this.filterTitle ? this.filterTitle.innerText : "",
            controlsHtml: this.dynamicControls ? this.dynamicControls.innerHTML : "",
            formula: this.formulaBox ? this.formulaBox.innerText : "",
            code: this.codeSnippet ? this.codeSnippet.innerText : "",
            perf: this.perfBadge ? this.perfBadge.innerText : "",
            dimensions: this.statusDimensions ? this.statusDimensions.innerText : "",
            histogram: this.currentHistogram || null,
            stats: this.currentStats || null
        };
    }

    pushUndoSnapshot(description = "") {
        if (this.isRestoringHistory || !this.rawImageBase64) return;
        const snapshot = this.captureCurrentState(description);
        this.undoStack.push(snapshot);
        if (this.undoStack.length > this.maxHistory) {
            this.undoStack.shift();
        }
        // New action clears forward redo history
        this.redoStack = [];
    }

    undo() {
        if (this.undoStack.length === 0) {
            this.showToast("لا توجد عمليات سابقة للتراجع عنها (No more undo)", "ℹ️");
            return;
        }

        // Capture current state and push into redoStack
        const currentState = this.captureCurrentState("Redo State");
        this.redoStack.push(currentState);
        if (this.redoStack.length > this.maxHistory) {
            this.redoStack.shift();
        }

        // Pop previous state and restore
        const previousState = this.undoStack.pop();
        this.restoreHistoryState(previousState, "Undo (تراجع)");
    }

    redo() {
        if (this.redoStack.length === 0) {
            this.showToast("لا توجد عمليات لاحقة لإعادتها (No more redo)", "ℹ️");
            return;
        }

        // Capture current state and push into undoStack
        const currentState = this.captureCurrentState("Undo State");
        this.undoStack.push(currentState);
        if (this.undoStack.length > this.maxHistory) {
            this.undoStack.shift();
        }

        // Pop next state and restore
        const nextState = this.redoStack.pop();
        this.restoreHistoryState(nextState, "Redo (إعادة)");
    }

    restoreHistoryState(state, actionName = "History") {
        if (!state) return;
        this.isRestoringHistory = true;

        try {
            this.currentFileName = state.currentFileName || this.currentFileName;
            this.activeOperation = state.activeOperation || "none";
            this.activeParams = state.activeParams ? JSON.parse(JSON.stringify(state.activeParams)) : {};

            // Restore base raw image if changed
            if (state.rawImageBase64 && state.rawImageBase64 !== this.rawImageBase64) {
                this.rawImageBase64 = state.rawImageBase64;
                this.canvasRaw.src = state.rawImageBase64;
                this.cacheRawImageBitmapFromSrc(state.rawImageBase64);
            }

            // Restore processed image
            if (state.processedImageBase64) {
                this.processedImageBase64 = state.processedImageBase64;
                this.canvasProcessed.src = state.processedImageBase64;
                this.cacheProcessedImageBitmap();
            } else if (state.rawImageBase64) {
                this.processedImageBase64 = state.rawImageBase64;
                this.canvasProcessed.src = state.rawImageBase64;
            }

            // Restore UI text / title / stats / code
            if (this.filterTitle && state.filterTitle) {
                this.filterTitle.innerText = state.filterTitle;
            }
            if (this.formulaBox) {
                this.formulaBox.innerText = state.formula || "";
            }
            if (this.codeSnippet) {
                this.codeSnippet.innerText = state.code || "";
            }
            if (this.perfBadge && state.perf) {
                this.perfBadge.innerText = state.perf;
            }
            if (this.statusDimensions && state.dimensions) {
                this.statusDimensions.innerText = state.dimensions;
            }

            // Restore controls HTML and rebind sliders
            if (this.dynamicControls && state.controlsHtml !== undefined) {
                this.dynamicControls.innerHTML = state.controlsHtml;
                this.bindDynamicSliders();
                this.syncSlidersToParams();
            }

            // Restore histogram if saved
            if (state.histogram) {
                this.renderHistogram(state.histogram);
                this.currentHistogram = state.histogram;
            }
            if (state.stats) {
                this.updateStats(state.stats);
                this.currentStats = state.stats;
            }

            this.updateZoomDisplay();
            this.showToast(`${actionName}: ${state.description || "State"}`, "↩️");
        } finally {
            setTimeout(() => {
                this.isRestoringHistory = false;
            }, 80);
        }
    }

    cacheRawImageBitmapFromSrc(src) {
        const img = new Image();
        img.onload = () => {
            this.cacheRawImageBitmap(img);
        };
        img.src = src;
    }

    syncSlidersToParams() {
        if (!this.dynamicControls || !this.activeParams) return;
        const inputs = this.dynamicControls.querySelectorAll("input[data-param]");
        inputs.forEach(input => {
            const paramName = input.getAttribute("data-param");
            if (this.activeParams[paramName] !== undefined) {
                input.value = this.activeParams[paramName];
                const valDisplay = document.getElementById(`val_${paramName}`);
                if (valDisplay) valDisplay.innerText = this.activeParams[paramName];
            }
        });
    }

    // =========================================================================
    // STUDIO COMPOSITION & SUPERPOWERS (TEXT, BG CUT, BG REPLACE, OVERLAY)
    // =========================================================================
    hexToBgr(hex) {
        hex = hex.replace("#", "");
        if (hex.length === 3) hex = hex.split("").map(c => c + c).join("");
        const num = parseInt(hex, 16);
        const r = (num >> 16) & 255;
        const g = (num >> 8) & 255;
        const b = num & 255;
        return [b, g, r];
    }

    // 1. Text Tool Typography
    cancelTextTool() {
        if (this.canvasTextBox) this.canvasTextBox.style.display = "none";
        if (this.textOptionsBar) this.textOptionsBar.style.display = "none";
        const moveBtn = document.querySelector(".ps-tbtn[title*='Move']");
        if (moveBtn) this.activateToolGroup(moveBtn, "move");
    }

    async applyTextToImage() {
        if (!this.rawImageBase64) return;
        const text = (this.canvasTextInput && this.canvasTextInput.value.trim())
            ? this.canvasTextInput.value.trim()
            : (this.textOverlayInput ? this.textOverlayInput.value.trim() : "VisionCraft Studio");
        if (!text) {
            this.showToast("يرجى كتابة النص أولاً", "⚠️");
            return;
        }
        const fontSize = this.canvasTextSize
            ? (parseInt(this.canvasTextSize.value) || 42)
            : (this.textFontSize ? parseInt(this.textFontSize.value) || 42 : 42);
        const fontFamily = this.canvasTextFont
            ? this.canvasTextFont.value
            : (this.textFontFamily ? this.textFontFamily.value : "tahoma");
        const colorHex = this.canvasTextColor ? this.canvasTextColor.value : (this.textOverlayColor ? this.textOverlayColor.value : "#ffffff");
        const colorBgr = this.hexToBgr(colorHex);
        const x = this.textCoords.x || 60;
        const y = this.textCoords.y || 80;

        this.showToast("جاري رسم وكتابة النص على الصورة...", "🔤");

        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "add_text",
                params: {
                    text: text,
                    x: x,
                    y: y,
                    font_size: fontSize,
                    font_family: fontFamily,
                    color: colorBgr
                }
            }, "Add Text");
            if (data && data.status === "success") {
                this.commitNewBaseImage(data.image);
                if (this.canvasTextBox) this.canvasTextBox.style.display = "none";
                if (this.textOptionsBar) this.textOptionsBar.style.display = "none";
                const moveBtn = document.querySelector(".ps-tbtn[title*='Move']");
                if (moveBtn) this.activateToolGroup(moveBtn, "move");
                this.showToast("تم تطبيق ودمج النص مع الصورة بنجاح", "🔤");
            } else {
                alert("Text rendering error: " + (data.message || "Failed"));
            }
        } catch (e) {
            console.error("Text render error:", e);
        }
    }

    // 2. Cutout & Background Removal Suite (GrabCut AI & Dual Threshold)
    removeBackground() {
        this.activateBackgroundRemovalTool();
    }

    activateBackgroundRemovalTool(btn = null) {
        if (!btn) btn = document.getElementById("btnCutoutTool");
        if (btn) {
            this.activateToolGroup(btn, "cutout");
        } else {
            this.setCutoutMode(this.activeCutoutMode || "grabcut");
        }
    }

    setCutoutMode(mode = "grabcut") {
        this.activeCutoutMode = mode;
        if (mode === "grabcut") {
            const margin = this.activeParams && this.activeParams.margin !== undefined ? this.activeParams.margin : 15;
            const iterations = this.activeParams && this.activeParams.iterations !== undefined ? this.activeParams.iterations : 5;
            const sigma = this.activeParams && this.activeParams.sigma !== undefined ? this.activeParams.sigma : 1.2;

            const controlsHtml = `
                <div style="background:#171717; border:1px solid #2a2a2a; border-radius:5px; padding:8px; margin-bottom:8px;">
                    <div style="font-size:11px; font-weight:700; color:#00e5ff; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;">
                        <span>✂️ موازنة وتحكم تفريغ الخلفية</span>
                        <span style="font-size:9px; background:#003344; color:#00e5ff; padding:1px 5px; border-radius:3px;">GrabCut AI</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; margin-bottom:10px;">
                        <button type="button" class="ps-btn ps-btn-accent" style="font-size:10px; padding:4px 3px; font-weight:bold;" onclick="app.setCutoutMode('grabcut')">🤖 عزل ذكي (GrabCut)</button>
                        <button type="button" class="ps-btn" style="font-size:10px; padding:4px 3px;" onclick="app.setCutoutMode('threshold')">🎚️ العتبة الثنائية T1/T2</button>
                    </div>

                    <div class="ps-prop-row">
                        <span>هامش الإطار المحيط (Margin):</span>
                        <span id="val_margin" style="color:#00e5ff; font-weight:700;">${margin}px</span>
                    </div>
                    <input type="range" class="ps-range" min="3" max="60" value="${margin}" data-param="margin">

                    <div class="ps-prop-row">
                        <span>دورات طاقة التجزئة (Iterations):</span>
                        <span id="val_iterations" style="color:#00e5ff; font-weight:700;">${iterations}</span>
                    </div>
                    <input type="range" class="ps-range" min="1" max="10" value="${iterations}" data-param="iterations">

                    <div class="ps-prop-row">
                        <span>تنعيم الحواف وصقل القناع (σ):</span>
                        <span id="val_sigma" style="color:#00e5ff; font-weight:700;">${sigma}</span>
                    </div>
                    <input type="range" class="ps-range" min="0.1" max="4.0" step="0.1" value="${sigma}" data-param="sigma">

                    <div style="margin-top:10px; display:flex; flex-direction:column; gap:5px;">
                        <button type="button" class="ps-btn ps-btn-accent" style="width:100%; padding:6px 6px; font-size:11px; font-weight:bold; background:#00b4d8; color:#000;" onclick="app.commitCurrentProcessedAsBase('تفريغ وعزل الخلفية الذكي (GrabCut)')">✓ قص واعتماد النتيجة (Commit Cutout)</button>
                        <div style="display:flex; gap:4px;">
                            <button type="button" class="ps-btn" style="flex:1; font-size:10px; padding:4px;" onclick="app.openBgReplaceModal()">🌅 استبدال الخلفية</button>
                            <button type="button" class="ps-btn" style="flex:1; font-size:10px; padding:4px;" onclick="app.resetCutout()">↩ إعادة ضبط</button>
                        </div>
                    </div>
                </div>
            `;
            this.setFilter("remove_background", { margin, iterations, sigma }, "✂️ تفريغ الخلفية الذكي (GrabCut AI)", controlsHtml);
        } else {
            const t1 = this.activeParams && this.activeParams.t1 !== undefined ? this.activeParams.t1 : 50;
            const t2 = this.activeParams && this.activeParams.t2 !== undefined ? this.activeParams.t2 : 150;
            const sigma = this.activeParams && this.activeParams.sigma !== undefined ? this.activeParams.sigma : 1.4;

            const controlsHtml = `
                <div style="background:#171717; border:1px solid #2a2a2a; border-radius:5px; padding:8px; margin-bottom:8px;">
                    <div style="font-size:11px; font-weight:700; color:#00e5ff; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;">
                        <span>✂️ موازنة وتحكم تفريغ الخلفية</span>
                        <span style="font-size:9px; background:#003344; color:#00e5ff; padding:1px 5px; border-radius:3px;">Dual Threshold</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; margin-bottom:10px;">
                        <button type="button" class="ps-btn" style="font-size:10px; padding:4px 3px;" onclick="app.setCutoutMode('grabcut')">🤖 عزل ذكي (GrabCut)</button>
                        <button type="button" class="ps-btn ps-btn-accent" style="font-size:10px; padding:4px 3px; font-weight:bold;" onclick="app.setCutoutMode('threshold')">🎚️ العتبة الثنائية T1/T2</button>
                    </div>

                    <div class="ps-prop-row">
                        <span>العتبة العليا (High T2):</span>
                        <span id="val_t2" style="color:#00e5ff; font-weight:700;">${t2}</span>
                    </div>
                    <input type="range" class="ps-range" min="0" max="255" value="${t2}" data-param="t2">

                    <div class="ps-prop-row">
                        <span>العتبة السفلى (Low T1):</span>
                        <span id="val_t1" style="color:#00e5ff; font-weight:700;">${t1}</span>
                    </div>
                    <input type="range" class="ps-range" min="0" max="255" value="${t1}" data-param="t1">

                    <div class="ps-prop-row">
                        <span>صقل وتنعيم القناع (σ):</span>
                        <span id="val_sigma" style="color:#00e5ff; font-weight:700;">${sigma}</span>
                    </div>
                    <input type="range" class="ps-range" min="0.1" max="4.0" step="0.1" value="${sigma}" data-param="sigma">

                    <div style="margin-top:10px; display:flex; flex-direction:column; gap:5px;">
                        <button type="button" class="ps-btn ps-btn-accent" style="width:100%; padding:6px 6px; font-size:11px; font-weight:bold; background:#00b4d8; color:#000;" onclick="app.commitCurrentProcessedAsBase('عزل وقص الخلفية بالعتبة')">✓ قص واعتماد النتيجة (Commit Cutout)</button>
                        <div style="display:flex; gap:4px;">
                            <button type="button" class="ps-btn" style="flex:1; font-size:10px; padding:4px;" onclick="app.openBgReplaceModal()">🌅 استبدال الخلفية</button>
                            <button type="button" class="ps-btn" style="flex:1; font-size:10px; padding:4px;" onclick="app.resetCutout()">↩ إعادة ضبط</button>
                        </div>
                    </div>
                </div>
            `;
            this.setFilter("threshold_cut", { t1, t2, sigma, mode: "band" }, "✂️ عزل الخلفية بالعتبة الثنائية", controlsHtml);
        }
    }

    resetCutout() {
        this.setFilter("none", {}, "Original Image", `<div style='color:#888; font-size:11px; padding:10px 0; text-align:center;'>🖼️ الصورة الأصلية (بدون فلاتر).<br>اختر أي فلتر أو أداة من شريط الأدوات لتطبيقه.</div>`);
        const moveBtn = document.querySelector(".ps-tbtn[title*='Move']");
        if (moveBtn) this.activateToolGroup(moveBtn, "move");
    }

    // 3. Background Replacement
    openBgReplaceModal() {
        if (this.bgReplaceModal) this.bgReplaceModal.style.display = "flex";
    }

    closeBgReplaceModal() {
        if (this.bgReplaceModal) this.bgReplaceModal.style.display = "none";
    }

    async applyBackgroundReplace(type, customImgBase64 = null) {
        this.closeBgReplaceModal();
        if (!this.rawImageBase64) return;

        let params = { bg_type: type };
        if (type === "color") {
            const hex = this.bgColorPicker ? this.bgColorPicker.value : "#ffffff";
            params.bg_color = this.hexToBgr(hex);
        } else if (type === "image" && customImgBase64) {
            params.bg_image = customImgBase64;
        }

        this.showToast(`Replacing Background (${type})...`, "🌅");

        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "replace_background",
                params: params
            }, "Replace Background");
            if (data && data.status === "success") {
                this.commitNewBaseImage(data.image);
                this.showToast(`Background Changed (${type})`, "🌅");
            } else {
                alert("Background replace error: " + (data.message || "Failed"));
            }
        } catch (e) {
            console.error("Replace background error:", e);
        }
    }

    handleBgFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            this.applyBackgroundReplace("image", event.target.result);
        };
        reader.readAsDataURL(file);
        e.target.value = "";
    }

    // 4. Picture-in-Picture / Image Overlay
    handleOverlayFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            this.overlayImageBase64 = event.target.result;
            this.overlayCoords = { x: 50, y: 50 };
            this.overlayScale = 1.0;
            this.overlayOpacity = 1.0;
            if (this.overlayScaleSlider) this.overlayScaleSlider.value = "1.0";
            if (this.overlayScaleLabel) this.overlayScaleLabel.innerText = "1.0x";
            if (this.overlayOpacitySlider) this.overlayOpacitySlider.value = "1.0";
            if (this.overlayOpacityLabel) this.overlayOpacityLabel.innerText = "100%";
            if (this.overlayOptionsBar) this.overlayOptionsBar.style.display = "flex";
            this.showToast("Overlay Image Loaded - Adjust Scale & Position", "🖼");
        };
        reader.readAsDataURL(file);
    }

    setOverlayScale(val) {
        this.overlayScale = parseFloat(val) || 1.0;
        if (this.overlayScaleLabel) this.overlayScaleLabel.innerText = `${this.overlayScale.toFixed(2)}x`;
    }

    setOverlayOpacity(val) {
        this.overlayOpacity = parseFloat(val) || 1.0;
        if (this.overlayOpacityLabel) this.overlayOpacityLabel.innerText = `${Math.round(this.overlayOpacity * 100)}%`;
    }

    cancelOverlay() {
        this.overlayImageBase64 = null;
        if (this.overlayOptionsBar) this.overlayOptionsBar.style.display = "none";
    }

    async applyOverlayToImage() {
        if (!this.rawImageBase64 || !this.overlayImageBase64) return;
        this.showToast("Merging Overlay Image...", "🖼");

        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "image_overlay",
                params: {
                    overlay_image: this.overlayImageBase64,
                    x: this.overlayCoords.x,
                    y: this.overlayCoords.y,
                    scale: this.overlayScale,
                    opacity: this.overlayOpacity
                }
            }, "Image Overlay");
            if (data && data.status === "success") {
                this.cancelOverlay();
                this.commitNewBaseImage(data.image);
                this.showToast("Overlay Merged Successfully", "🖼");
            } else {
                alert("Image overlay error: " + (data.message || "Failed"));
            }
        } catch (e) {
            console.error("Apply overlay error:", e);
        }
    }

    // 5. DIP Dual Image Blending (دمج صورتين معاً)
    openBlendModal() {
        if (!this.rawImageBase64) {
            this.showToast("Please load an image first", "⚠️");
            return;
        }
        if (this.blendThumb1) this.blendThumb1.src = this.rawImageBase64;
        if (this.blendModal) this.blendModal.style.display = "flex";
        this.updateBlendSlider(this.blendAlphaSlider ? this.blendAlphaSlider.value : 0.5);
    }

    closeBlendModal() {
        if (this.blendModal) this.blendModal.style.display = "none";
    }

    handleBlendSecondImage(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const maxDim = 1000;
                let w = img.width;
                let h = img.height;
                if (w > maxDim || h > maxDim) {
                    const ratio = Math.min(maxDim / w, maxDim / h);
                    w = Math.round(w * ratio);
                    h = Math.round(h * ratio);
                }
                const canvas = document.createElement('canvas');
                canvas.width = w;
                canvas.height = h;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, w, h);

                this.blendSecondImageBase64 = canvas.toDataURL('image/jpeg', 0.9);
                if (this.blendThumb2) {
                    this.blendThumb2.src = this.blendSecondImageBase64;
                    this.blendThumb2.style.display = "block";
                }
                if (this.blendThumb2Placeholder) {
                    this.blendThumb2Placeholder.style.display = "none";
                }
                this.showToast("Second image loaded for blending", "🖼️");
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }

    updateBlendSlider(val) {
        this.blendAlpha = parseFloat(val) || 0.5;
        const pct2 = Math.round(this.blendAlpha * 100);
        const pct1 = 100 - pct2;
        if (this.blendAlphaLabel) this.blendAlphaLabel.innerText = this.blendAlpha.toFixed(2);
        if (this.blendRatio1Label) this.blendRatio1Label.innerText = `${pct1}%`;
        if (this.blendRatio2Label) this.blendRatio2Label.innerText = `${pct2}%`;
    }

    async executeBlendImages() {
        if (!this.rawImageBase64) return;
        if (!this.blendSecondImageBase64) {
            alert("يرجى اختيار الصورة الثانية (f₂) أولاً لإتمام عملية الدمج");
            return;
        }
        this.closeBlendModal();
        this.showToast("DIP Blending in progress...", "✨");

        const mode = this.blendAlgorithmSelect ? this.blendAlgorithmSelect.value : "linear";
        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "blend_images",
                params: {
                    second_image: this.blendSecondImageBase64,
                    alpha: this.blendAlpha,
                    mode: mode
                }
            }, "Blend Images");
            if (data && data.status === "success") {
                this.commitNewBaseImage(data.image);
                if (data.formula && this.formulaBox) this.formulaBox.innerText = data.formula;
                if (data.code && this.codeSnippet) this.codeSnippet.innerText = data.code;
                this.showToast("Images Blended Successfully! 🎉", "✨");
            } else {
                alert("Blending error: " + (data.message || "Failed"));
            }
        } catch (e) {
            console.error("Execute blend error:", e);
            alert("Connection error during image blending");
        }
    }

    // 6. DIP PHOTO COLLAGE & MULTI-IMAGE TEMPLATES
    openCollageModal() {
        if (this.collageModal) {
            this.collageModal.style.display = "flex";
            if ((!this.collageSlotImages || this.collageSlotImages.length === 0) && this.rawImageBase64) {
                this.collageSlotImages = [this.rawImageBase64];
            }
            this.renderCollageSlots();
        }
    }

    closeCollageModal() {
        if (this.collageModal) this.collageModal.style.display = "none";
    }

    selectCollageTemplate(tpl, count, cardEl) {
        this.collageTemplate = tpl;
        this.collageSlotCount = count;
        document.querySelectorAll(".ps-collage-card").forEach(c => c.classList.remove("active"));
        if (cardEl) cardEl.classList.add("active");
        if (this.collageSlotsCountLabel) {
            this.collageSlotsCountLabel.innerText = `${count} صور`;
        }
        this.renderCollageSlots();
    }

    renderCollageSlots() {
        if (!this.collageSlotsContainer) return;
        this.collageSlotsContainer.innerHTML = "";

        while (this.collageSlotImages.length < this.collageSlotCount) {
            this.collageSlotImages.push(null);
        }

        for (let i = 0; i < this.collageSlotCount; i++) {
            const slotCard = document.createElement("div");
            slotCard.className = "ps-slot-card";

            const title = document.createElement("div");
            title.style.fontSize = "10px";
            title.style.color = "#aaa";
            title.innerText = `خانة ${i + 1}`;
            slotCard.appendChild(title);

            const imgEl = document.createElement("img");
            imgEl.className = "ps-slot-thumb";
            const imgData = this.collageSlotImages[i];
            if (imgData) {
                imgEl.src = imgData;
                imgEl.style.display = "block";
            } else {
                imgEl.style.display = "none";
            }
            slotCard.appendChild(imgEl);

            const btn = document.createElement("button");
            btn.className = "ps-btn ps-slot-btn" + (imgData ? "" : " ps-btn-accent");
            btn.innerText = imgData ? "تغيير الصورة" : "+ اختر صورة";
            btn.onclick = () => this.triggerSlotUpload(i);
            slotCard.appendChild(btn);

            this.collageSlotsContainer.appendChild(slotCard);
        }
    }

    triggerSlotUpload(index) {
        this.collageActiveSlotIndex = index;
        if (this.collageSlotFileInput) {
            this.collageSlotFileInput.click();
        }
    }

    handleCollageSlotFile(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const maxDim = 1000;
                let w = img.width;
                let h = img.height;
                if (w > maxDim || h > maxDim) {
                    const ratio = Math.min(maxDim / w, maxDim / h);
                    w = Math.round(w * ratio);
                    h = Math.round(h * ratio);
                }
                const canvas = document.createElement('canvas');
                canvas.width = w;
                canvas.height = h;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, w, h);

                // Use JPEG 0.9 to greatly reduce base64 size and prevent PHP POST max_size errors
                this.collageSlotImages[this.collageActiveSlotIndex] = canvas.toDataURL('image/jpeg', 0.9);
                this.renderCollageSlots();
                this.showToast(`Loaded image for Slot ${this.collageActiveSlotIndex + 1}`, "🖼️");
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
        e.target.value = "";
    }

    setCollageGap(val) {
        this.collageBorderGap = parseInt(val) || 0;
        if (this.collageGapLabel) this.collageGapLabel.innerText = `${this.collageBorderGap} px`;
    }

    setCollageColor(hex) {
        if (this.collageColorPicker) this.collageColorPicker.value = hex;
        if (this.collageColorLabel) this.collageColorLabel.innerText = hex;
        this.collageBorderColor = this.hexToBgr(hex);
    }

    async executeCollage() {
        const imgs = this.collageSlotImages.slice(0, this.collageSlotCount).filter(im => Boolean(im));
        if (imgs.length === 0) {
            if (this.rawImageBase64) {
                imgs.push(this.rawImageBase64);
            } else {
                alert("يرجى تحميل صورة واحدة على الأقل في خانات القالب");
                return;
            }
        }

        this.closeCollageModal();
        this.showToast("Generating Photo Collage...", "📐");

        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64 || imgs[0],
                operation: "photo_collage",
                params: {
                    images: imgs,
                    template: this.collageTemplate,
                    border_size: this.collageBorderGap,
                    border_color: this.collageBorderColor
                }
            }, "Photo Collage");
            if (data && data.status === "success") {
                this.commitNewBaseImage(data.image);
                if (data.formula && this.formulaBox) this.formulaBox.innerText = data.formula;
                if (data.code && this.codeSnippet) this.codeSnippet.innerText = data.code;
                this.showToast("Collage Assembled Successfully! 🎉", "📐");
            } else {
                alert("Collage error: " + (data.message || "Failed"));
            }
        } catch (e) {
            console.error("Execute collage error:", e);
            alert("Connection error during collage generation");
        }
    }

    commitCurrentProcessedAsBase(description = "اعتماد وقص الصورة") {
        if (!this.processedImageBase64) return;
        this.commitNewBaseImage(this.processedImageBase64, description);
        this.showToast("تم قص واعتماد الصورة كطبقة أساسية بنجاح", "✂️");
    }

    activateThresholdCutout() {
        this.activateBackgroundRemovalTool();
        this.setCutoutMode("threshold");
    }

    commitNewBaseImage(newBase64, description = "Base Image Modification") {
        if (!this.isRestoringHistory && this.rawImageBase64) {
            this.pushUndoSnapshot(description);
        }
        this.rawImageBase64 = newBase64;
        this.canvasRaw.src = newBase64;
        const img = new Image();
        img.onload = () => {
            this.statusDimensions.innerText = `${img.width} × ${img.height} px`;
            if (this.brushMaskCanvas) {
                this.brushMaskCanvas.width = img.width;
                this.brushMaskCanvas.height = img.height;
                this.clearBrushMask();
            }
            if (this.drawingCanvas) {
                this.drawingCanvas.width = img.width;
                this.drawingCanvas.height = img.height;
                this.clearDrawingLayer();
            }
            this.cacheRawImageBitmap(img);
            this.applyCurrentFilter();
        };
        img.src = newBase64;
    }

    // =========================================================================
    // SUPERPOWER 7: INTERACTIVE CROP ENGINE
    // =========================================================================
    initCropBox() {
        if (!this.canvasRaw || !this.canvasRaw.naturalWidth) return;
        const imgW = this.canvasRaw.naturalWidth;
        const imgH = this.canvasRaw.naturalHeight;

        const padX = imgW * 0.1;
        const padY = imgH * 0.1;
        this.cropBox = {
            x: padX,
            y: padY,
            w: imgW * 0.8,
            h: imgH * 0.8
        };
        this.updateCropOverlayUI();
    }

    updateCropOverlayUI() {
        if (!this.cropBoxEl || !this.canvasRaw || !this.canvasRaw.naturalWidth) return;
        const imgW = this.canvasRaw.naturalWidth;
        const imgH = this.canvasRaw.naturalHeight;

        const leftPct = (this.cropBox.x / imgW) * 100;
        const topPct = (this.cropBox.y / imgH) * 100;
        const widthPct = (this.cropBox.w / imgW) * 100;
        const heightPct = (this.cropBox.h / imgH) * 100;

        this.cropBoxEl.style.left = `${leftPct}%`;
        this.cropBoxEl.style.top = `${topPct}%`;
        this.cropBoxEl.style.width = `${widthPct}%`;
        this.cropBoxEl.style.height = `${heightPct}%`;

        const dimText = `${Math.round(this.cropBox.w)} × ${Math.round(this.cropBox.h)} px`;
        if (this.cropBoxDim) this.cropBoxDim.innerText = dimText;
        if (this.cropDimensionsLabel) this.cropDimensionsLabel.innerText = dimText;
    }

    setCropRatio(ratio) {
        this.cropRatio = ratio;
        if (!this.canvasRaw || !this.canvasRaw.naturalWidth) return;
        const imgW = this.canvasRaw.naturalWidth;
        const imgH = this.canvasRaw.naturalHeight;

        if (ratio === "1:1") {
            const side = Math.min(this.cropBox.w, this.cropBox.h);
            this.cropBox.w = side;
            this.cropBox.h = side;
        } else if (ratio === "4:3") {
            this.cropBox.h = (this.cropBox.w * 3) / 4;
            if (this.cropBox.y + this.cropBox.h > imgH) {
                this.cropBox.h = imgH - this.cropBox.y;
                this.cropBox.w = (this.cropBox.h * 4) / 3;
            }
        } else if (ratio === "16:9") {
            this.cropBox.h = (this.cropBox.w * 9) / 16;
            if (this.cropBox.y + this.cropBox.h > imgH) {
                this.cropBox.h = imgH - this.cropBox.y;
                this.cropBox.w = (this.cropBox.h * 16) / 9;
            }
        }
        this.updateCropOverlayUI();
    }

    async applyCrop() {
        if (!this.rawImageBase64) return;
        const { x, y, w, h } = this.cropBox;
        if (w < 10 || h < 10) {
            alert("Crop area too small.");
            return;
        }

        this.showToast("Applying Crop...", "✂️");

        try {
            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "crop",
                params: { x, y, width: w, height: h }
            }, "Crop");
            if (data && data.status === "success") {
                this.cancelCrop();
                this.commitNewBaseImage(data.image);
                this.fitToScreen();
                this.showToast(`Cropped to ${Math.round(w)} × ${Math.round(h)} px`, "✂️");
            } else {
                alert("Crop error: " + (data.message || "Failed"));
            }
        } catch (err) {
            console.error("Crop error:", err);
            const canvas = document.createElement("canvas");
            canvas.width = Math.round(w);
            canvas.height = Math.round(h);
            const ctx = canvas.getContext("2d");
            ctx.drawImage(this.canvasRaw, Math.round(x), Math.round(y), Math.round(w), Math.round(h), 0, 0, Math.round(w), Math.round(h));
            this.cancelCrop();
            this.commitNewBaseImage(canvas.toDataURL("image/png"));
            this.fitToScreen();
        }
    }

    cancelCrop() {
        if (this.cropOptionsBar) this.cropOptionsBar.style.display = "none";
        if (this.cropOverlay) this.cropOverlay.style.display = "none";
        const moveBtn = document.querySelector(".ps-tbtn[title*='Move']");
        if (moveBtn) this.activateToolGroup(moveBtn, "move");
    }

    // =========================================================================
    // SUPERPOWER 8: DRAWING & SHAPES SUITE
    // =========================================================================
    setDrawShape(shape) {
        this.drawShape = shape;
        this.showToast(`Draw Tool: ${shape.toUpperCase()}`, "🎨");
    }

    setDrawStrokeSize(size) {
        this.drawStrokeSize = parseInt(size, 10) || 4;
        if (this.drawStrokeSizeLabel) this.drawStrokeSizeLabel.innerText = `${this.drawStrokeSize}px`;
    }

    setDrawColor(color) {
        this.drawColor = color;
    }

    setDrawFill(checked) {
        this.drawFill = Boolean(checked);
    }

    clearDrawingLayer() {
        if (this.drawingCanvas && this.drawingCtx) {
            this.drawingCtx.clearRect(0, 0, this.drawingCanvas.width, this.drawingCanvas.height);
            this.showToast("Drawing Cleared", "🧹");
        }
    }

    applyDrawStrokeStyle() {
        if (!this.drawingCtx) return;
        if (this.drawShape === "eraser") {
            this.drawingCtx.globalCompositeOperation = "destination-out";
            this.drawingCtx.lineWidth = this.drawStrokeSize * 2.5;
        } else {
            this.drawingCtx.globalCompositeOperation = "source-over";
            this.drawingCtx.strokeStyle = this.drawColor;
            this.drawingCtx.lineWidth = this.drawStrokeSize;
        }
        this.drawingCtx.lineCap = "round";
        this.drawingCtx.lineJoin = "round";
    }

    renderShape(shape, start, end) {
        if (!this.drawingCtx) return;
        const ctx = this.drawingCtx;
        ctx.save();
        this.applyDrawStrokeStyle();

        if (shape === "rect") {
            const x = Math.min(start.x, end.x);
            const y = Math.min(start.y, end.y);
            const w = Math.abs(end.x - start.x);
            const h = Math.abs(end.y - start.y);
            if (this.drawFill) {
                ctx.fillStyle = this.drawColor;
                ctx.fillRect(x, y, w, h);
            }
            ctx.strokeRect(x, y, w, h);
        } else if (shape === "circle") {
            const rx = Math.abs(end.x - start.x) / 2;
            const ry = Math.abs(end.y - start.y) / 2;
            const cx = Math.min(start.x, end.x) + rx;
            const cy = Math.min(start.y, end.y) + ry;
            ctx.beginPath();
            ctx.ellipse(cx, cy, Math.max(1, rx), Math.max(1, ry), 0, 0, 2 * Math.PI);
            if (this.drawFill) {
                ctx.fillStyle = this.drawColor;
                ctx.fill();
            }
            ctx.stroke();
        } else if (shape === "line") {
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();
        } else if (shape === "arrow") {
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();

            const angle = Math.atan2(end.y - start.y, end.x - start.x);
            const headLen = Math.max(10, this.drawStrokeSize * 3);
            ctx.beginPath();
            ctx.moveTo(end.x, end.y);
            ctx.lineTo(end.x - headLen * Math.cos(angle - Math.PI / 6), end.y - headLen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(end.x - headLen * Math.cos(angle + Math.PI / 6), end.y - headLen * Math.sin(angle + Math.PI / 6));
            ctx.closePath();
            ctx.fillStyle = this.drawColor;
            ctx.fill();
        }
        ctx.restore();
    }

    mergeDrawingToImage() {
        if (!this.rawImageBase64 || !this.drawingCanvas) return;
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement("canvas");
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0);
            ctx.drawImage(this.drawingCanvas, 0, 0);
            const mergedBase64 = canvas.toDataURL("image/png");
            this.clearDrawingLayer();
            this.commitNewBaseImage(mergedBase64);
            this.showToast("Drawing Merged to Image Base", "✨");
        };
        img.src = this.rawImageBase64;
    }

    // =========================================================================
    // SUPERPOWER 9: EXPORT & FORMAT CONVERSION MODAL
    // =========================================================================
    openExportModal() {
        if (!this.exportModal) return;
        this.exportModal.style.display = "flex";

        const activeImg = (this.processedImageBase64 && this.canvasProcessed && this.canvasProcessed.src)
            ? this.canvasProcessed
            : this.canvasRaw;
        const w = activeImg ? activeImg.naturalWidth : 800;
        const h = activeImg ? activeImg.naturalHeight : 600;

        if (this.exportResEstimate) {
            this.exportResEstimate.innerText = `${w} × ${h} px`;
        }
        this.updateExportSizeEstimate();
    }

    closeExportModal() {
        if (this.exportModal) this.exportModal.style.display = "none";
    }

    selectExportFormat(fmt, cardEl) {
        this.exportFormat = fmt;
        document.querySelectorAll(".ps-format-card").forEach(c => c.classList.remove("active"));
        if (cardEl) cardEl.classList.add("active");

        if (this.exportExtLabel) {
            this.exportExtLabel.innerText = `.${fmt === 'jpeg' ? 'jpg' : fmt}`;
        }

        if (this.exportQualityRow) {
            this.exportQualityRow.style.display = (fmt === "jpeg" || fmt === "webp") ? "flex" : "none";
        }

        this.updateExportSizeEstimate();
    }

    updateExportQuality(val) {
        this.exportQuality = (parseInt(val, 10) || 90) / 100;
        if (this.exportQualityLabel) {
            this.exportQualityLabel.innerText = `${Math.round(this.exportQuality * 100)}%`;
        }
        this.updateExportSizeEstimate();
    }

    updateExportSizeEstimate() {
        if (!this.exportSizeEstimate) return;
        const activeImg = (this.processedImageBase64 && this.canvasProcessed && this.canvasProcessed.src)
            ? this.canvasProcessed
            : this.canvasRaw;
        const w = activeImg ? activeImg.naturalWidth : 800;
        const h = activeImg ? activeImg.naturalHeight : 600;
        const pixels = w * h;

        let bytes = 0;
        if (this.exportFormat === "bmp") {
            bytes = pixels * 3 + 54;
        } else if (this.exportFormat === "png") {
            bytes = pixels * 0.9;
        } else if (this.exportFormat === "jpeg") {
            bytes = pixels * 0.35 * (this.exportQuality || 0.9);
        } else if (this.exportFormat === "webp") {
            bytes = pixels * 0.22 * (this.exportQuality || 0.9);
        }

        const kb = Math.round(bytes / 1024);
        if (kb >= 1024) {
            this.exportSizeEstimate.innerText = `~${(kb / 1024).toFixed(1)} MB`;
        } else {
            this.exportSizeEstimate.innerText = `~${kb} KB`;
        }
    }

    generateBmpDataUrl(canvas) {
        const ctx = canvas.getContext("2d");
        const w = canvas.width;
        const h = canvas.height;
        const imgData = ctx.getImageData(0, 0, w, h);
        const data = imgData.data;

        const rowSize = Math.floor((24 * w + 31) / 32) * 4;
        const pixelArraySize = rowSize * h;
        const fileSize = 54 + pixelArraySize;

        const buffer = new ArrayBuffer(fileSize);
        const view = new DataView(buffer);

        view.setUint16(0, 0x4D42, false);
        view.setUint32(2, fileSize, true);
        view.setUint32(6, 0, true);
        view.setUint32(10, 54, true);

        view.setUint32(14, 40, true);
        view.setInt32(18, w, true);
        view.setInt32(22, h, true);
        view.setUint16(26, 1, true);
        view.setUint16(28, 24, true);
        view.setUint32(30, 0, true);
        view.setUint32(34, pixelArraySize, true);
        view.setInt32(38, 2835, true);
        view.setInt32(42, 2835, true);
        view.setUint32(46, 0, true);
        view.setUint32(50, 0, true);

        let pos = 54;
        for (let y = h - 1; y >= 0; y--) {
            for (let x = 0; x < w; x++) {
                const i = (y * w + x) * 4;
                view.setUint8(pos++, data[i + 2]);
                view.setUint8(pos++, data[i + 1]);
                view.setUint8(pos++, data[i]);
            }
            for (let p = 0; p < rowSize - w * 3; p++) {
                view.setUint8(pos++, 0);
            }
        }

        const blob = new Blob([buffer], { type: "image/bmp" });
        return URL.createObjectURL(blob);
    }

    performExport() {
        const fmt = this.exportFormat || "png";
        const name = (this.exportFileNameInput ? this.exportFileNameInput.value.trim() : "") || "visioncraft_export";
        const filename = `${name}.${fmt === 'jpeg' ? 'jpg' : fmt}`;

        const exportCanvas = document.createElement("canvas");
        const activeImg = (this.processedImageBase64 && this.canvasProcessed && this.canvasProcessed.src)
            ? this.canvasProcessed
            : this.canvasRaw;

        if (!activeImg || !activeImg.naturalWidth) {
            alert("No image available to export.");
            return;
        }

        exportCanvas.width = activeImg.naturalWidth;
        exportCanvas.height = activeImg.naturalHeight;
        const ctx = exportCanvas.getContext("2d");

        if (fmt === "jpeg" || fmt === "bmp") {
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, exportCanvas.width, exportCanvas.height);
        }

        ctx.drawImage(activeImg, 0, 0);

        if (this.drawingCanvas && this.drawingCanvas.width > 0) {
            ctx.drawImage(this.drawingCanvas, 0, 0);
        }

        let downloadUrl = null;
        let isBlobUrl = false;

        if (fmt === "bmp") {
            downloadUrl = this.generateBmpDataUrl(exportCanvas);
            isBlobUrl = true;
        } else if (fmt === "jpeg") {
            downloadUrl = exportCanvas.toDataURL("image/jpeg", this.exportQuality);
        } else if (fmt === "webp") {
            downloadUrl = exportCanvas.toDataURL("image/webp", this.exportQuality);
        } else {
            downloadUrl = exportCanvas.toDataURL("image/png");
        }

        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        if (isBlobUrl) {
            setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
        }

        this.closeExportModal();
        this.showToast(`Exported as ${filename}`, "💾");
    }

    // =========================================================================
    // SUPERPOWER 10: PRODUCT STUDIO BACKGROUNDS LIBRARY
    // =========================================================================
    showProductBgLibrary() {
        this.openBgReplaceModal();
        this.showBgTab("presets");
    }

    showBgTab(tab) {
        if (!this.productPresetsSection || !this.solidColorPickerRow) return;
        const tabPresets = document.getElementById("tabBtnProductStudio");
        const tabColor = document.getElementById("tabBtnColor");

        if (tab === "presets") {
            this.productPresetsSection.style.display = "block";
            this.solidColorPickerRow.style.display = "none";
            if (tabPresets) { tabPresets.style.borderColor = "#00e5ff"; tabPresets.style.background = "rgba(0,229,255,0.08)"; }
            if (tabColor) { tabColor.style.borderColor = "#555"; tabColor.style.background = ""; }
        } else {
            this.productPresetsSection.style.display = "none";
            this.solidColorPickerRow.style.display = "flex";
            if (tabColor) { tabColor.style.borderColor = "#00e5ff"; tabColor.style.background = "rgba(0,229,255,0.08)"; }
            if (tabPresets) { tabPresets.style.borderColor = "#555"; tabPresets.style.background = ""; }
        }
    }

    async applyProductStudioBg(bgFilename) {
        if (!this.rawImageBase64) return;
        this.closeBgReplaceModal();
        this.showToast(`Compositing Product Studio: ${bgFilename}...`, "🏆");

        try {
            const bgImg = new Image();
            bgImg.crossOrigin = "Anonymous";
            await new Promise((resolve, reject) => {
                bgImg.onload = resolve;
                bgImg.onerror = reject;
                bgImg.src = `backgrounds/${bgFilename}`;
            });

            const bgCanvas = document.createElement("canvas");
            bgCanvas.width = bgImg.width;
            bgCanvas.height = bgImg.height;
            const bgCtx = bgCanvas.getContext("2d");
            bgCtx.drawImage(bgImg, 0, 0);
            const bgBase64 = bgCanvas.toDataURL("image/jpeg", 0.95);

            const data = await this.sendApiProcess({
                image: this.rawImageBase64,
                operation: "replace_background",
                params: {
                    bg_type: "image",
                    bg_image: bgBase64,
                    margin: 15
                }
            }, "Product Studio");

            if (data && data.status === "success") {
                this.commitNewBaseImage(data.image);
                this.showToast("Product Studio Applied Successfully!", "✨");
            } else {
                alert("Product studio error: " + (data.message || "Failed"));
            }
        } catch (err) {
            console.error("Product studio error:", err);
            alert("Failed to apply product background: " + err.message);
        }
    }

    // =========================================================================
    // EVENT LISTENERS FOR CROP & DRAWING INTERACTION
    // =========================================================================
    initCropAndDrawingEvents() {
        const getCoords = (e) => {
            if (!this.canvasRaw) return { x: 0, y: 0 };
            const rect = this.canvasRaw.getBoundingClientRect();
            const imgW = this.canvasRaw.naturalWidth || 1;
            const imgH = this.canvasRaw.naturalHeight || 1;
            const x = Math.max(0, Math.min(imgW, Math.round((e.clientX - rect.left) * (imgW / rect.width))));
            const y = Math.max(0, Math.min(imgH, Math.round((e.clientY - rect.top) * (imgH / rect.height))));
            return { x, y };
        };

        // 1. Drawing Canvas Interaction
        if (this.drawingCanvas) {
            this.drawingCanvas.addEventListener("mousedown", (e) => {
                if (this.activeTool !== "draw" || e.button !== 0) return;
                this.isDrawing = true;
                const pt = getCoords(e);
                this.drawStart = pt;

                if (this.drawShape === "pen" || this.drawShape === "eraser") {
                    this.drawingCtx.beginPath();
                    this.drawingCtx.moveTo(pt.x, pt.y);
                    this.applyDrawStrokeStyle();
                } else {
                    this.drawSnapshot = this.drawingCtx.getImageData(0, 0, this.drawingCanvas.width, this.drawingCanvas.height);
                }
                e.preventDefault();
            });

            window.addEventListener("mousemove", (e) => {
                if (!this.isDrawing || this.activeTool !== "draw") return;
                const pt = getCoords(e);

                if (this.drawShape === "pen" || this.drawShape === "eraser") {
                    this.applyDrawStrokeStyle();
                    this.drawingCtx.lineTo(pt.x, pt.y);
                    this.drawingCtx.stroke();
                } else if (this.drawSnapshot) {
                    this.drawingCtx.putImageData(this.drawSnapshot, 0, 0);
                    this.renderShape(this.drawShape, this.drawStart, pt);
                }
            });

            window.addEventListener("mouseup", (e) => {
                if (this.isDrawing && this.activeTool === "draw") {
                    if (this.drawShape !== "pen" && this.drawShape !== "eraser" && this.drawSnapshot) {
                        const pt = getCoords(e);
                        this.drawingCtx.putImageData(this.drawSnapshot, 0, 0);
                        this.renderShape(this.drawShape, this.drawStart, pt);
                        this.drawSnapshot = null;
                    }
                    this.isDrawing = false;
                }
            });
        }

        // 2. Crop Overlay Dragging & Resizing
        if (this.cropOverlay) {
            this.cropOverlay.addEventListener("mousedown", (e) => {
                if (this.activeTool !== "crop") return;
                const imgW = this.canvasRaw.naturalWidth;
                const imgH = this.canvasRaw.naturalHeight;
                const pt = getCoords(e);

                if (e.target.classList.contains("ps-crop-handle")) {
                    this.isResizingCrop = true;
                    this.activeCropHandle = e.target.dataset.handle;
                    this.cropDragStart = { x: pt.x, y: pt.y, ...this.cropBox };
                    e.stopPropagation();
                    return;
                }

                if (e.target.closest("#cropBox")) {
                    this.isDraggingCrop = true;
                    this.cropDragStart = { x: pt.x, y: pt.y, ...this.cropBox };
                    e.stopPropagation();
                    return;
                }

                this.isResizingCrop = true;
                this.activeCropHandle = "se";
                this.cropBox.x = pt.x;
                this.cropBox.y = pt.y;
                this.cropBox.w = 10;
                this.cropBox.h = 10;
                this.cropDragStart = { x: pt.x, y: pt.y, ...this.cropBox };
                this.updateCropOverlayUI();
            });

            window.addEventListener("mousemove", (e) => {
                if (this.activeTool !== "crop") return;
                const imgW = this.canvasRaw.naturalWidth;
                const imgH = this.canvasRaw.naturalHeight;
                const pt = getCoords(e);

                if (this.isDraggingCrop) {
                    const dx = pt.x - this.cropDragStart.x;
                    const dy = pt.y - this.cropDragStart.y;
                    this.cropBox.x = Math.max(0, Math.min(imgW - this.cropBox.w, this.cropDragStart.x + dx));
                    this.cropBox.y = Math.max(0, Math.min(imgH - this.cropBox.h, this.cropDragStart.y + dy));
                    this.updateCropOverlayUI();
                } else if (this.isResizingCrop) {
                    const dx = pt.x - this.cropDragStart.x;
                    const dy = pt.y - this.cropDragStart.y;
                    const h = this.activeCropHandle;

                    if (h === "se") {
                        this.cropBox.w = Math.max(20, Math.min(imgW - this.cropBox.x, this.cropDragStart.w + dx));
                        this.cropBox.h = Math.max(20, Math.min(imgH - this.cropBox.y, this.cropDragStart.h + dy));
                    } else if (h === "nw") {
                        const newW = Math.max(20, this.cropDragStart.w - dx);
                        const newH = Math.max(20, this.cropDragStart.h - dy);
                        this.cropBox.x = Math.max(0, this.cropDragStart.x + dx);
                        this.cropBox.y = Math.max(0, this.cropDragStart.y + dy);
                        this.cropBox.w = newW;
                        this.cropBox.h = newH;
                    } else if (h === "ne") {
                        this.cropBox.w = Math.max(20, Math.min(imgW - this.cropBox.x, this.cropDragStart.w + dx));
                        const newH = Math.max(20, this.cropDragStart.h - dy);
                        this.cropBox.y = Math.max(0, this.cropDragStart.y + dy);
                        this.cropBox.h = newH;
                    } else if (h === "sw") {
                        const newW = Math.max(20, this.cropDragStart.w - dx);
                        this.cropBox.x = Math.max(0, this.cropDragStart.x + dx);
                        this.cropBox.w = newW;
                        this.cropBox.h = Math.max(20, Math.min(imgH - this.cropBox.y, this.cropDragStart.h + dy));
                    }

                    if (this.cropRatio === "1:1") {
                        const side = Math.min(this.cropBox.w, this.cropBox.h);
                        this.cropBox.w = side;
                        this.cropBox.h = side;
                    }
                    this.updateCropOverlayUI();
                }
            });

            window.addEventListener("mouseup", () => {
                this.isDraggingCrop = false;
                this.isResizingCrop = false;
                this.activeCropHandle = null;
            });
        }
    }

    initTextBoxEvents() {
        if (!this.canvasTextBox) return;

        // 1. Dragging the Text Box by its header
        let isDraggingBox = false;
        let dragStartX = 0;
        let dragStartY = 0;
        let initialLeft = 50;
        let initialTop = 50;

        if (this.canvasTextBoxHeader) {
            this.canvasTextBoxHeader.addEventListener("mousedown", (e) => {
                if (e.target.closest && e.target.closest(".ps-text-box-actions")) return;
                isDraggingBox = true;
                dragStartX = e.clientX;
                dragStartY = e.clientY;
                initialLeft = parseFloat(this.canvasTextBox.style.left) || 50;
                initialTop = parseFloat(this.canvasTextBox.style.top) || 50;
                e.stopPropagation();
                e.preventDefault();
            });

            window.addEventListener("mousemove", (e) => {
                if (!isDraggingBox || !this.canvasRaw) return;
                const rect = this.canvasRaw.getBoundingClientRect();
                const deltaX = (e.clientX - dragStartX) / (this.zoomScale || 1.0);
                const deltaY = (e.clientY - dragStartY) / (this.zoomScale || 1.0);
                const boxW = this.canvasTextBox.offsetWidth || 320;
                const boxH = this.canvasTextBox.offsetHeight || 140;

                let newLeft = Math.max(0, Math.min(rect.width - boxW, initialLeft + deltaX));
                let newTop = Math.max(0, Math.min(rect.height - boxH, initialTop + deltaY));

                this.canvasTextBox.style.left = `${newLeft}px`;
                this.canvasTextBox.style.top = `${newTop}px`;

                const scaleX = this.canvasRaw.naturalWidth / rect.width;
                const scaleY = this.canvasRaw.naturalHeight / rect.height;
                this.textCoords.x = Math.max(0, Math.round(newLeft * scaleX));
                this.textCoords.y = Math.max(0, Math.round((newTop + 25) * scaleY));
            });

            window.addEventListener("mouseup", () => {
                isDraggingBox = false;
            });
        }

        // 2. Synchronize inputs between Canvas Text Box and Top Options Bar
        if (this.canvasTextInput) {
            this.canvasTextInput.addEventListener("input", (e) => {
                if (this.textOverlayInput) this.textOverlayInput.value = e.target.value;
            });
            this.canvasTextInput.addEventListener("keydown", (e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    this.applyTextToImage();
                } else if (e.key === "Escape") {
                    this.cancelTextTool();
                }
            });
        }
        if (this.textOverlayInput) {
            this.textOverlayInput.addEventListener("input", (e) => {
                if (this.canvasTextInput) this.canvasTextInput.value = e.target.value;
            });
        }

        if (this.canvasTextSize) {
            this.canvasTextSize.addEventListener("input", (e) => {
                if (this.textFontSize) this.textFontSize.value = e.target.value;
            });
        }
        if (this.textFontSize) {
            this.textFontSize.addEventListener("input", (e) => {
                if (this.canvasTextSize) this.canvasTextSize.value = e.target.value;
            });
        }

        if (this.canvasTextColor) {
            this.canvasTextColor.addEventListener("input", (e) => {
                if (this.textOverlayColor) this.textOverlayColor.value = e.target.value;
                if (this.canvasTextInput) this.canvasTextInput.style.color = e.target.value;
            });
        }
        if (this.textOverlayColor) {
            this.textOverlayColor.addEventListener("input", (e) => {
                if (this.canvasTextColor) this.canvasTextColor.value = e.target.value;
                if (this.canvasTextInput) this.canvasTextInput.style.color = e.target.value;
            });
        }

        if (this.canvasTextFont) {
            this.canvasTextFont.addEventListener("change", (e) => {
                if (this.textFontFamily) this.textFontFamily.value = e.target.value;
                if (this.canvasTextInput) this.canvasTextInput.style.fontFamily = e.target.value;
            });
        }
        if (this.textFontFamily) {
            this.textFontFamily.addEventListener("change", (e) => {
                if (this.canvasTextFont) this.canvasTextFont.value = e.target.value;
                if (this.canvasTextInput) this.canvasTextInput.style.fontFamily = e.target.value;
            });
        }
    }
}

// Global instance
window.app = null;
window.addEventListener("DOMContentLoaded", () => {
    window.app = new PhotoshopApp();
});
