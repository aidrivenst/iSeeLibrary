import os
import cv2
from robot.api import logger
from .keywordgroup import KeywordGroup

class ImageScaler(KeywordGroup):

    @staticmethod
    def scale_image_two_factors(self, path, scale_x: float, scale_y: float):
        """
        Scale the image using two factors (scale_x and scale_y).
        
        Args:
        path (str): The path to the image file.
        scale_x (float): The scaling factor for the x-axis.
        scale_y (float): The scaling factor for the y-axis.
        
        Returns:
        scaled_image (numpy.ndarray): The scaled image.
        """
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError(f"The image at path {path} could not be found.")
        
        scaled_image = cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
        
        base_name = os.path.basename(path)
        name, ext = os.path.splitext(base_name)
        output_path = f"scaled_{scale_x:.2f}_{scale_y:.2f}_{name}{ext}"
        cv2.imwrite(output_path, scaled_image)
        logger.info(f"Image saved at {output_path}")
        self._embed_image_to_log()

    @staticmethod
    def scale_image_single_factor(path, scale: float):
        """
        Scale the image using a single factor.
        
        Args:
        path (str): The path to the image file.
        scale (float): The scaling factor for both axes.
        
        Returns:
        output_path (str): The path to the scaled image file.
        """
        image = cv2.imread(path)
        if image is None:
            raise FileNotFoundError(f"The image at path {path} could not be found.")

        scaled_image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        
        base_name = os.path.basename(path)
        name, ext = os.path.splitext(base_name)
        output_path = f"scaled_{scale:.2f}_{name}{ext}"
        cv2.imwrite(output_path, scaled_image)
        logger.info(f"Image saved at {output_path}")
        