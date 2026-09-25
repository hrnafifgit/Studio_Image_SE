# VisionCraft Pure Mathematical Digital Image Processing Core
from core.base import ProcessingResult
from core.point_ops import (
    apply_negative, apply_log, apply_gamma,
    apply_brightness_contrast, apply_threshold, apply_histogram_equalization
)
from core.spatial_filters import (
    apply_gaussian_blur, apply_box_blur, apply_median_filter,
    apply_wiener_filter, apply_bilateral_filter, apply_custom_kernel
)
from core.edge_detectors import (
    apply_sobel, apply_prewitt, apply_laplacian,
    apply_canny, apply_unsharp_mask
)
from core.morphology import (
    apply_erosion, apply_dilation, apply_opening, apply_closing,
    apply_morphological_gradient, apply_tophat_blackhat, apply_skeleton
)
from core.color_spaces import (
    convert_color_space, isolate_channel, apply_kmeans_segmentation,
    apply_color_splash, extract_color_palette
)
from core.frequency_ops import (
    get_fft_spectrum, apply_frequency_filter, apply_notch_filter
)
from core.geometric_ops import (
    apply_rotation, apply_resize, apply_flip, apply_crop
)
from core.restoration import (
    apply_motion_deblur
)
from core.composition import (
    remove_background, replace_background,
    render_text_overlay, composite_overlay_image,
    blend_two_images, generate_photo_collage
)


