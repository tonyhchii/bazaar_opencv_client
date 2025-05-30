class CannySettings:
    def __init__(self,bilateral_filter_diameter=None, bilateral_sigma_color=None, bilateral_sigma_space=None,  blur_kernel_size=None, gaussian_sigma=None, low_threshold=None, high_threshhold=None):
        self.bilateral_filter_diameter = bilateral_filter_diameter
        self.bilateral_sigma_color = bilateral_sigma_color
        self.bilateral_sigma_space = bilateral_sigma_space
        self.blur_kernel_size = blur_kernel_size
        self.gaussian_sigma = gaussian_sigma
        self.low_threshold = low_threshold
        self.high_threshold = high_threshhold