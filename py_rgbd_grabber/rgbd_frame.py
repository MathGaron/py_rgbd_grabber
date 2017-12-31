
class RgbdFrame:
    """
    Contains:
    rgb : numpy [H, W, C]
    depth : numpy [H, W] where unavailable pixels equal 0
    timestamp : second
    """
    def __init__(self, rgb, depth, timestamp=0):
        self.rgb = rgb
        self.depth = depth
        self.timestamp = timestamp