import os
import io
import time
import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import core
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# Disable caching for rapid development
from PIL import Image, ImageOps
import io

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def decode_image_from_base64(base64_str: str) -> np.ndarray:
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]
    img_bytes = base64.b64decode(base64_str)
    
    # 1. تصحيح تدوير الهواتف الذكية تلقائياً عبر EXIF Orientation
    try:
        pil_img = Image.open(io.BytesIO(img_bytes))
        pil_img = ImageOps.exif_transpose(pil_img)
        if pil_img.mode == 'RGBA':
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGRA)
        elif pil_img.mode == 'RGB':
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        elif pil_img.mode == 'L':
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_GRAY2BGR)
        else:
            img = cv2.cvtColor(np.array(pil_img.convert('RGB')), cv2.COLOR_RGB2BGR)
        return img
    except Exception:
        # 2. خط رجوع احتياطي عبر OpenCV
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Could not decode image from payload.")
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

# No frontend routes served from Python anymore

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "engine": "VisionCraft Photoshop Studio Engine v1.0"})

@app.route("/api/process", methods=["POST"])

def process():
    try:
        data = request.get_json(force=True)
        img_b64 = data.get("image")
        if not img_b64:
            return jsonify({"status": "error", "message": "No image data provided"}), 400

        img = decode_image_from_base64(img_b64)
        op = data.get("operation", "none").lower()
        p = data.get("params", {})

        # Dispatching algorithms
        # 1. Point Operations
        if op == "negative":
            res = core.apply_negative(img)
        elif op == "log":
            res = core.apply_log(img, c=float(p.get("c", 1.0)))
        elif op == "gamma":
            res = core.apply_gamma(img, gamma=float(p.get("gamma", 1.0)))
        elif op == "brightness_contrast":
            res = core.apply_brightness_contrast(img, brightness=int(p.get("brightness", 0)), contrast=float(p.get("contrast", 1.0)))
        elif op == "threshold":
            res = core.apply_threshold(img, threshold=int(p.get("threshold", 128)), method=p.get("method", "binary"))
        elif op == "histogram_equalization":
            res = core.apply_histogram_equalization(img, method=p.get("method", "global"), clip_limit=float(p.get("clip_limit", 2.0)))

        # 2. Spatial Filtering
        elif op == "gaussian":
            res = core.apply_gaussian_blur(img, ksize=int(p.get("ksize", 5)), sigma=float(p.get("sigma", 1.4)))
        elif op == "box_blur":
            res = core.apply_box_blur(img, ksize=int(p.get("ksize", 5)))
        elif op == "median":
            res = core.apply_median_filter(img, ksize=int(p.get("ksize", 5)))
        elif op == "wiener":
            res = core.apply_wiener_filter(img, ksize=int(p.get("ksize", 5)))
        elif op == "bilateral":
            res = core.apply_bilateral_filter(img, d=int(p.get("d", 9)), sigma_color=float(p.get("sigma_color", 75.0)), sigma_space=float(p.get("sigma_space", 75.0)))
        elif op == "custom_kernel":
            k_matrix = p.get("kernel", [[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            res = core.apply_custom_kernel(img, k_matrix)

        # 3. Edge Detection
        elif op == "sobel":
            res = core.apply_sobel(img, ksize=int(p.get("ksize", 3)))
        elif op == "prewitt":
            res = core.apply_prewitt(img)
        elif op == "laplacian":
            res = core.apply_laplacian(img, ksize=int(p.get("ksize", 3)))
        elif op == "canny":
            res = core.apply_canny(img, t1=int(p.get("t1", 50)), t2=int(p.get("t2", 150)), sigma=float(p.get("sigma", 1.4)))
        elif op == "unsharp_mask":
            res = core.apply_unsharp_mask(img, sigma=float(p.get("sigma", 1.5)), strength=float(p.get("strength", 1.5)))

        # 4. Morphology
        elif op == "erosion":
            res = core.apply_erosion(img, ksize=int(p.get("ksize", 5)), shape=p.get("shape", "rect"), iterations=int(p.get("iterations", 1)))
        elif op == "dilation":
            res = core.apply_dilation(img, ksize=int(p.get("ksize", 5)), shape=p.get("shape", "rect"), iterations=int(p.get("iterations", 1)))
        elif op == "opening":
            res = core.apply_opening(img, ksize=int(p.get("ksize", 5)), shape=p.get("shape", "rect"))
        elif op == "closing":
            res = core.apply_closing(img, ksize=int(p.get("ksize", 5)), shape=p.get("shape", "rect"))
        elif op == "morph_gradient":
            res = core.apply_morphological_gradient(img, ksize=int(p.get("ksize", 3)))
        elif op == "tophat_blackhat":
            res = core.apply_tophat_blackhat(img, ksize=int(p.get("ksize", 9)), mode=p.get("mode", "tophat"))
        elif op == "skeleton":
            res = core.apply_skeleton(img)

        # 5. Color Spaces & Palette
        elif op == "color_space":
            res = core.convert_color_space(img, target=p.get("target", "gray"))
        elif op == "isolate_channel":
            res = core.isolate_channel(img, channel=p.get("channel", "r"))
        elif op == "kmeans":
            res = core.apply_kmeans_segmentation(img, k=int(p.get("k", 4)))
        elif op == "color_splash":
            res = core.apply_color_splash(img, target_bgr=p.get("target_bgr", [0, 0, 220]), tolerance=float(p.get("tolerance", 24.0)))

        # 6. Frequency Domain & Restoration
        elif op == "fft_spectrum":
            res = core.get_fft_spectrum(img)
        elif op == "frequency_filter":
            res = core.apply_frequency_filter(img, filter_type=p.get("filter_type", "lowpass"), cutoff=float(p.get("cutoff", 30.0)), filter_model=p.get("filter_model", "gaussian"))
        elif op == "notch_filter":
            res = core.apply_notch_filter(img, notches=p.get("notches", []), d0=float(p.get("d0", 18.0)))
        elif op == "motion_deblur":
            res = core.apply_motion_deblur(img, length=int(p.get("length", 15)), angle=float(p.get("angle", 45.0)), snr=float(p.get("snr", 0.01)))

        # 7. Geometric
        elif op == "rotate":
            res = core.apply_rotation(img, angle=float(p.get("angle", 45.0)), scale=float(p.get("scale", 1.0)))
        elif op == "resize":
            res = core.apply_resize(img, scale_factor=float(p.get("scale", 0.5)), interpolation=p.get("interpolation", "bicubic"))
        elif op == "flip":
            res = core.apply_flip(img, mode=p.get("mode", "horizontal"))
        elif op == "crop":
            res = core.apply_crop(img, x=int(p.get("x", 0)), y=int(p.get("y", 0)), width=int(p.get("width", 100)), height=int(p.get("height", 100)))

        # 8. Studio Composition & Superpowers
        elif op == "threshold_cut":
            t1 = int(p.get("t1", 50))
            t2 = int(p.get("t2", 150))
            sigma = float(p.get("sigma", 1.4))
            mode = p.get("mode", "band")
            invert = bool(p.get("invert", False))
            res = core.cut_background_by_threshold(img, t1=t1, t2=t2, sigma=sigma, mode=mode, invert=invert)
        elif op == "remove_background":
            margin = int(p.get("margin", 15))
            iterations = int(p.get("iterations", 5))
            sigma = float(p.get("sigma", 1.2))
            res = core.remove_background(img, margin=margin, iterations=iterations, sigma=sigma)
        elif op == "replace_background":
            bg_type = p.get("bg_type", "color")
            bg_color = p.get("bg_color", [255, 255, 255])
            bg_img = None
            if p.get("bg_image"):
                try:
                    bg_img = decode_image_from_base64(p.get("bg_image"))
                except Exception:
                    pass
            res = core.replace_background(img, bg_type=bg_type, bg_color=bg_color, bg_image=bg_img)
        elif op == "add_text":
            text = p.get("text", "")
            x = int(p.get("x", 50))
            y = int(p.get("y", 50))
            font_size = int(p.get("font_size", 36))
            color_bgr = p.get("color", [255, 255, 255])
            font_family = p.get("font_family", "tahoma")
            res = core.render_text_overlay(img, text=text, x=x, y=y, font_size=font_size, color_bgr=color_bgr, font_family=font_family)
        elif op == "image_overlay":
            overlay_b64 = p.get("overlay_image")
            if not overlay_b64:
                return jsonify({"status": "error", "message": "No overlay image provided"}), 400
            overlay_img = decode_image_from_base64(overlay_b64)
            x = int(p.get("x", 50))
            y = int(p.get("y", 50))
            scale = float(p.get("scale", 1.0))
            opacity = float(p.get("opacity", 1.0))
            res = core.composite_overlay_image(img, overlay_img, x=x, y=y, scale=scale, opacity=opacity)
        elif op == "blend_images":
            second_b64 = p.get("second_image")
            if not second_b64:
                return jsonify({"status": "error", "message": "No second image provided for blending"}), 400
            second_img = decode_image_from_base64(second_b64)
            alpha = float(p.get("alpha", 0.5))
            mode = p.get("mode", "linear")
            res = core.blend_two_images(img, second_img, alpha=alpha, mode=mode)
        elif op == "photo_collage":
            raw_b64_list = p.get("images", [])
            collage_imgs = []
            for b64 in raw_b64_list:
                try:
                    if b64:
                        collage_imgs.append(decode_image_from_base64(b64))
                except Exception:
                    pass
            if not collage_imgs and img is not None:
                collage_imgs = [img]
            template = p.get("template", "grid_2x2")
            border_size = int(p.get("border_size", 10))
            border_color = p.get("border_color", [255, 255, 255])
            res = core.generate_photo_collage(collage_imgs, template=template, border_size=border_size, border_color=border_color)

        else: # No-op or return raw stats
            res = core.ProcessingResult(img, "Raw Input Matrix", "# Original Image", 0.0)

        response_payload = res.to_dict()
        response_payload["status"] = "success"
        
        # Attach dominant color palette if requested or on color operations
        if p.get("extract_palette", False) or op in ["color_splash", "kmeans", "color_space"]:
            try:
                response_payload["palette"] = core.extract_color_palette(img, k=6)
            except Exception:
                response_payload["palette"] = []
                
        return jsonify(response_payload)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

# ==============================================================================
# WEBSOCKET REAL-TIME DISPATCH ENGINE (Flask-SocketIO 60 FPS Stream)
# ==============================================================================
@socketio.on("connect")
def handle_ws_connect():
    """اتصال العميل بنجاح عبر قناة الـ WebSocket الفورية"""
    print("[VisionCraft WebSocket] Client connected successfully.")
    emit("server_status", {
        "status": "connected",
        "engine": "VisionCraft Realtime WebSocket Core",
        "timestamp": time.time()
    })

@socketio.on("disconnect")
def handle_ws_disconnect():
    """قطع اتصال العميل"""
    print("[VisionCraft WebSocket] Client disconnected.")

@socketio.on("process_frame")
def handle_ws_process_frame(data):
    """
    معالجة الإطارات والصور في الوقت الفعلي عبر WebSocket
    بنية البيانات المتبادلة (JSON Protocol):
    {
        "image": "<base64_string>",
        "operation": "ar_tryon | canny | gaussian | ...",
        "params": { ... }
    }
    """
    try:
        img_b64 = data.get("image")
        if not img_b64:
            emit("error", {"message": "No image data received in WebSocket frame"})
            return

        img = decode_image_from_base64(img_b64)
        op = data.get("operation", "none").lower()
        p = data.get("params", {})

        if op == "canny":
            res = core.apply_canny(img, t1=int(p.get("t1", 50)), t2=int(p.get("t2", 150)), sigma=float(p.get("sigma", 1.4)))
        elif op == "gaussian":
            res = core.apply_gaussian_blur(img, ksize=int(p.get("ksize", 5)), sigma=float(p.get("sigma", 1.4)))
        elif op == "histogram_equalization":
            res = core.apply_histogram_equalization(img, method=p.get("method", "global"))
        elif op == "negative":
            res = core.apply_negative(img)
        elif op == "sobel":
            res = core.apply_sobel(img, ksize=int(p.get("ksize", 3)))
        elif op == "dilation":
            res = core.apply_dilation(img, ksize=int(p.get("ksize", 5)))
        else:
            res = core.ProcessingResult(img, "Raw Realtime Matrix", "", 0.0)

        response_payload = res.to_dict()
        response_payload["status"] = "success"
        response_payload["operation"] = op
        emit("frame_processed", response_payload)

    except Exception as e:
        emit("error", {"status": "error", "message": str(e)})

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5001, debug=True, allow_unsafe_werkzeug=True)

