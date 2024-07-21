import cv2
import numpy as np
from typing import Tuple, List, Dict, Union

DEFAULT_MATCH_THRESHOLD = 0.5
MATCH_NEIGHBOUR_THRESHOLD = 10
DEFAULT_MATCHING_METHOD = cv2.TM_CCOEFF_NORMED

def highlight_region(image: np.ndarray, region: Dict[str, int], color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    Draws a rectangle on the given image matrix.

    :param image: The source image.
    :param region: The region to highlight.
    :param color: The color of the rectangle (default is green).
    :return: The same image with the rectangle on it.
    """
    if region['width'] <= 0 or region['height'] <= 0:
        return image
    top_left = (region['x'], region['y'])
    bottom_right = (region['x'] + region['width'], region['y'] + region['height'])
    cv2.rectangle(image, top_left, bottom_right, color, 2)
    return image

def filter_near_matches(matches: List[Dict[str, Union[int, float]]], threshold: int) -> List[Dict[str, Union[int, float]]]:
    """
    Filter out match results which have a matched neighbor.

    :param matches: List of match results.
    :param threshold: The pixel distance within which we consider an element being a neighbor of an existing match.
    :return: The filtered array of matched points.
    """
    def distance(point1, point2):
        return np.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)

    filtered_matches = []
    for match in matches:
        if not any(distance(match, existing) <= threshold for existing in filtered_matches):
            filtered_matches.append(match)
    return filtered_matches

def get_image_occurrence(full_img_path: str, partial_img_path: str, threshold: float = DEFAULT_MATCH_THRESHOLD, multiple: bool = False, visualize: bool = False, method: int = DEFAULT_MATCHING_METHOD) -> Dict:
    """
    Calculates the occurrence position of a partial image in the full image.

    :param full_img_path: Path to the full image.
    :param partial_img_path: Path to the partial image.
    :param threshold: Match threshold (default is 0.5).
    :param multiple: Find multiple matches in the image (default is False).
    :param visualize: Whether to return the resulting visualization as an image (default is False).
    :param method: The template matching method (default is cv2.TM_CCOEFF_NORMED).
    :return: Dictionary containing the occurrence results.
    """
    full_img = cv2.imread(full_img_path, cv2.IMREAD_COLOR)
    partial_img = cv2.imread(partial_img_path, cv2.IMREAD_COLOR)

    if full_img is None or partial_img is None:
        raise ValueError("Could not open or find the images.")

    matched = cv2.matchTemplate(full_img, partial_img, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)

    results = []

    if multiple:
        matches = [{'score': matched[y, x], 'x': x, 'y': y} for y in range(matched.shape[0]) for x in range(matched.shape[1]) if matched[y, x] >= threshold]
        matches = filter_near_matches(matches, MATCH_NEIGHBOUR_THRESHOLD)

        for match in matches:
            results.append({
                'score': match['score'],
                'rect': {'x': match['x'], 'y': match['y'], 'width': partial_img.shape[1], 'height': partial_img.shape[0]}
            })
    else:
        if (method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]):
            top_left = min_loc
            match_score = min_val
        else:
            top_left = max_loc
            match_score = max_val
        
        if match_score >= threshold:
            results.append({
                'score': match_score,
                'rect': {'x': top_left[0], 'y': top_left[1], 'width': partial_img.shape[1], 'height': partial_img.shape[0]}
            })
    
    if not results:
        raise ValueError("Cannot find any occurrences of the partial image in the full image.")
    
    if visualize:
        full_img_highlighted = full_img.copy()
        for result in results:
            full_img_highlighted = highlight_region(full_img_highlighted, result['rect'])
        cv2.imshow('Matched Image', full_img_highlighted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return {
        'rect': results[0]['rect'],
        'score': results[0]['score'],
        'visualization': full_img_highlighted if visualize else None,
        'multiple': results if multiple else None
    }

# Example usage
result = get_image_occurrence('full_image.png', 'partial_image.png', multiple=True, visualize=True)
print(result)
