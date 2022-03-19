import numpy as np
import cv2


def get_text_size(text, font_size):
    font = cv2.FONT_HERSHEY_TRIPLEX
    text_size = cv2.getTextSize(text, font, font_size, 1)[0]
    return text_size


# Get position of text on image
def get_text_position(text, font_size, image_size):
    text_size = get_text_size(text, font_size)
    text_position = (image_size[1] // 2 - text_size[0] // 2,
                     image_size[0] // 2 + text_size[1] // 2)
    return text_position


def watermark(
    image,
    text,
    font_size,
    color=(255, 255, 255),
    thickness=1
):
    font_size = int(font_size)
    thickness = int(thickness)

    # Make watermark
    watermark = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)

    # Get text position
    position = get_text_position(text, font_size, image.shape)

    # Draw text
    cv2.putText(watermark, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                font_size, color, thickness)

    # Merge watermark
    merge_img = cv2.addWeighted(watermark, 0.5, image, 1.0, 0)

    return merge_img


if __name__ == "__main__":
    test_image = cv2.imread('assets/book.jpg')
    test_image_arr = np.asarray(test_image, np.uint8)
    watermark_image = watermark(
        test_image_arr, 'Watermarked', 1, (255, 255, 255), 3)

    cv2.imwrite('assets/book_watermark.jpg', watermark_image)
