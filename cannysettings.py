class CannySettings:
    def __init__(self, blur_kernel_size=None, gaussian_sigma=None, low_threshold=None, high_threshhold=None):
        self.blur_kernel_size = blur_kernel_size
        self.gaussian_sigma = gaussian_sigma
        self.low_threshold = low_threshold
        self.high_threshold = high_threshhold