#!/usr/bin/python3
"""
main file of the ascii art generator.
"""
import time
import sys
import cv2
from os import system


# grayscale_characters = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


def clear_screen():
    """
    Clear Screen between frames
    """
    sys.stdout.write("\033[H")  # ANSI escape code to move cursor to top-left
    sys.stdout.flush()
    # system("clear")


def print_in_ascii(image):
    """
    Print the final image
    """
    pic = ""
    for row in image:
        pic += f'{"".join(row)}\n'
    print(pic)
    sys.stdout.flush()


def add_color_to_character(RGB_value):
    """
    add RGB color to the character
    """
    return f"\033[48;2;{RGB_value[2]};{RGB_value[1]};{RGB_value[0]}m{' '}\033[0m"


def ascii_colored_image(image):
    """
    Convert image into a colored ascii image
    """
    color_image = []
    for row in image:
        new_row = []
        for char in row:
            new_row.append(add_color_to_character(char))
        color_image.append(new_row)
    return color_image


def resize_image(image, new_width=750):
    """
    Resize image to new height and width
    """
    # (height, width) = image.shape[1], image.shape[0]
    # aspect_ratio = height / width
    # new_height = int(aspect_ratio * new_width)
    new_height = 130
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image


# def convert_to_grascale(image):
#     """
#     Convert to only gray scale values
#     """
#     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#
# def covert_into_charaters(image):
#     """
#     Convert grayscale image into characters
#     """
#     ascii_image = []
#     for row in image:
#         new_row = []
#         for char in row:
#             percentage = int((char / 255) * 9)
#             new_row.append(grayscale_characters[percentage])
#         ascii_image.append(new_row)
#     return ascii_image


def get_video():
    """
    Get the video
    """
    video_obj = cv2.VideoCapture("./Videos/Video-2.mp4")
    success = 1
    while success:
        clear_screen()
        success, image = video_obj.read()
        resized_image = resize_image(image)
        color_image = ascii_colored_image(resized_image)
        # grayscaled_image = convert_to_grascale(resized_image)
        # ascii_image = covert_into_charaters(grayscaled_image)
        print_in_ascii(color_image)


def main():
    """
    main function the entry point for ascii art generator
    """
    # image_number = input()
    # image = cv2.imread(f"./Images/Image-{image_number}.jpg")
    get_video()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Time : {(end - start)}")
