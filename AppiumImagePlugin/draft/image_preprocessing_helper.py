
import base64
import os
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import uuid
import cv2
import numpy as np
from PIL import Image 


"""
Refactor + use decorators + OOP
"""

def crop_image(image_path, left, top, right, bottom, output_dir):
    # Convert the coordinates to integers --> refactor = pass types to argument + use @keyword decorator accordingly to robot api doc
    left = int(left)
    top = int(top)
    right = int(right)
    bottom = int(bottom)
    output_dir = str(output_dir)

    # to be done :  add context manger ++ refactor
    image = Image.open(image_path)

    # region to crop
    image_width, image_height = image.size
    if left < 0 or top < 0 or right > image_width or bottom > image_height:
        print("Invalid cropping region. Please ensure the coordinates are within the image bounds.")
        return

    #cropper l'image et convertir 
    cropped_image = image.crop((left, top, right, bottom))
    if cropped_image.mode == 'RGBA':
        cropped_image = cropped_image.convert('RGB')

    # save file cropped --> WIP : refactor 
    output_file_name = os.path.splitext(os.path.basename(image_path))[0] + "_cropped.png"
    output_path = os.path.join(output_dir, output_file_name)
    cropped_image.save(output_path, 'PNG')




def image_contained_grey(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray2, gray1, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8

    if cv2.minMaxLoc(result)[1] >= threshold:
        return True
    else:
        return False


def Is_Image_Contained(element_path, screenshot_path):

    # Debugging
    print("Image 1 path:", element_path)
    print("Image 2 path:", screenshot_path)

    # Charger les images
    image1 = cv2.imread(element_path)
    image2 = cv2.imread(screenshot_path)
    if image1 is None or image2 is None:
        raise ValueError("Impossible de charger les images.")
###
    result = cv2.matchTemplate(image2, image1, cv2.TM_CCOEFF_NORMED)
    threshold = .85
    locations = np.where(result >= threshold)
    logger.info(locations)
####
    with open(element_path, 'rb') as img_file:
        image_data = img_file.read()
        encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
    
    with open(screenshot_path, 'rb') as img_file:
        image_data = img_file.read()
        encoded_image2_data = base64.b64encode(image_data).decode('utf-8')

    image1_tag = f'<img text="Element cherché: " src="data:image/png;base64,{encoded_image1_data}" width="10%">'
    image2_tag = f'<img src="data:image/png;base64,{encoded_image2_data}" width="10%">'
        # Vérifier s'il y a des correspondances
    if locations[0].size > 0:
        y, x = locations[::-1]
        x, y = x[0], y[0]
        cv2.rectangle(image2, (x, y), (x + image1.shape[1], y + image1.shape[0]), (0, 0, 255), 2)
        
        cv2.imwrite('image2.png', image2)
        
        with open('image2.png', 'rb') as img_file:
            image_data = img_file.read()
            encoded_image_res_data = base64.b64encode(image_data).decode('utf-8')

        with open(element_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image1_data = base64.b64encode(image_data).decode('utf-8')
        
        with open(screenshot_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image2_data = base64.b64encode(image_data).decode('utf-8')
        image_res_tag = f'<img src="data:image/png;base64,{encoded_image_res_data}" width="10%">'
        logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
        logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
        logger.info(" <br> Resultat du vérification à l'aide de comparison des images <br> " + image_res_tag, html=True)
    else:
        logger.info('Element not found in devices screen')
        logger.info(" <br> Element cible cherché sur la screenshot <br> " + image1_tag, html=True)
        logger.info(" <br> Screenshot pris en cours du test <br> "  + image2_tag, html=True)
        raise AssertionError ("Element not found in devices screen")



def embed_screenshot_to_log(rel_screenshot_path, title=''):
    screenshot_format = 'jpg'  # (e.g., jpg, png)
    screenshot_name = str(uuid.uuid1()) + title + '.{}'.format(screenshot_format)
    PABOTQUEUEINDEX = BuiltIn().get_variable_value('${PABOTQUEUEINDEX}', None)

    if PABOTQUEUEINDEX is not None:
        rel_screenshot_path = '{}-{}'.format(PABOTQUEUEINDEX, screenshot_name)
    else:
        rel_screenshot_path = screenshot_name

    image_html = "<a href='{}' target='_blank'><img src='{}' alt='{}' style='width:50%; height: auto;'/></a>".format(
        rel_screenshot_path, rel_screenshot_path, title)

    # Log the HTML to the report
    BuiltIn().log("*HTML* " + image_html, html=True)



def find_element_in_image(image2_path, image1_path):

    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise ValueError("Could not read one or both of the images")

    # matching templates
    result = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF)
    _, _, _, max_loc = cv2.minMaxLoc(result)

    #  top-left coordinates
    x, y = max_loc

     # coordinates
    h, w = img1.shape
    center_x = x + w // 2
    center_y = y + h // 2
    #logger.info("result ", result)

    logger.info(x)
    logger.info(y)

    logger.info(center_x)
    logger.info(center_y)
    return center_x, center_y

def start_findNeedle( needleImagePath, sourceImagePath):
    image = cv2.imread(sourceImagePath)
    # cv2.imshow('Rainforest', image)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(needleImagePath, 0)

    result = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("min_val: ", min_val)
    print("min_loc: ", min_loc)

    height, width = template.shape[:2]

    top_left = max_loc
    bottom_right = (top_left[0] + width, top_left[1] + height)
    cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 5)
    cv2.imwrite('poc.png', image)

    # Calculer le center coordinates of the found element
    center_x = min_loc[0] + width // 2
    center_y = min_loc[1] + height // 2

    logger.info(center_x)
    logger.info(center_y)
    # cv2.imshow('Rainforest', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return center_x, center_y


def find_matches( needle, haystack):
    arr_h = np.asarray(haystack)
    arr_n = np.asarray(needle)

    y_h, x_h = arr_h.shape[:2]
    y_n, x_n = arr_n.shape[:2]

    xstop = x_h - x_n + 1
    ystop = y_h - y_n + 1

    matches = []
    for xmin in range(0, xstop):
        for ymin in range(0, ystop):
            xmax = xmin + x_n
            ymax = ymin + y_n

            arr_s = arr_h[ymin:ymax, xmin:xmax]     # Extract subimage
            arr_t = (arr_s == arr_n)                # Create test matrix
            if arr_t.all():                         # Only consider exact matches
                matches.append((xmin,ymin))

    return matches


def find_left_boundary(image):
    # Find the leftmost non-white pixel in each row
    width, height = image.size
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel != (255, 255, 255, 255):  # Check if the pixel is not white
                return x

def find_right_boundary(image):
    # Find the rightmost non-white pixel in each row
    width, height = image.size
    for x in range(width - 1, -1, -1):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel != (255, 255, 255, 255):  # Check if the pixel is not white
                return x

def crop_image_boundries(image_path, top, bottom, output_dir):
    # to be done : open with context manager -- (to handle crash in Azure : happened 2 times )
    image = Image.open(image_path)

    width, height = image.size

    # Find the left and right boundarie
    left_boundary = find_left_boundary(image)
    right_boundary = find_right_boundary(image)

    # Set the crop box coordinates
    left = left_boundary
    right = right_boundary
    top = int(top)
    bottom = int(bottom)

    if left < 0 or top < 0 or right > width or bottom > height:
        raise ValueError("Invalid cropping region. Please ensure the coordinates are within the image bounds.")
        
    cropped_image = image.crop((left, top, right, bottom))

    if cropped_image.mode == 'RGBA':
        cropped_image = cropped_image.convert('RGB')

    # Nom du fichier
    output_file_name = os.path.splitext(os.path.basename(image_path))[0] + "_cropped.png"

    output_path = os.path.join(output_dir, output_file_name)

    cropped_image.save(output_path, 'PNG')

    logger.info(f"Image cropped successfully and saved as '{output_file_name}' in '{output_dir}'.")
