#!/usr/bin/python3
"""
main file of the ascii art generator.
"""
import os
import time
import sys
import cv2

# grayscale_characters = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]


class Frame:
    """
    Frame class for actions on frames
    """

    def __init__(self, ascii_char=False, colored=True):
        self.__ascii_char = ascii_char
        self.__colored = colored

    def resize_image(self, image):
        """Resize image to fit rows and columns on screen"""
        cols, rows = os.get_terminal_size()
        resized_image = cv2.resize(image, (cols, rows))
        return resized_image

    def color_frame(self, image):
        """
        Convert image into a colored ascii image
        """
        color_image = []
        for row in image:
            new_row = []
            for char in row:
                new_row.append(self.__add_color_to_pixel(char))
            color_image.append(new_row)
        return color_image

    def __add_color_to_pixel(self, rgb_value):
        """Add color to the individual characters(pixels)"""
        if self.__ascii_char:
            return f"\033[38;2;{rgb_value[2]};{rgb_value[1]};{rgb_value[0]}m{'@'}\033[0m"  # For foreground with character to represent color
        return f"\033[48;2;{rgb_value[2]};{rgb_value[1]};{rgb_value[0]}m{' '}\033[0m"  # Background itself representing color every characters background representing one pixel

    def paint_on_screen(self, image):
        """Paint Frame on Screen"""
        frame = ""
        for row in image:
            frame += f'{"".join(row)}\n'
        sys.stdout.write(frame)
        sys.stdout.flush()

    def clear_screen(self):
        """Clear Screen"""
        sys.stdout.write("\033[H")
        sys.stdout.flush()


class TerminalVideoPlayer(Frame):
    """Terminal Video Player"""

    def __init__(self, video_url, ascii_char=False, colored=True):
        super().__init__(ascii_char, colored)
        self.__video_url = video_url

    def play(self):
        """Play Video"""
        video_obj = self.__get_video()
        success = 1
        while success:
            self.clear_screen()
            success, image = video_obj.read()
            if image is None:
                continue
            video_fps = video_obj.get(cv2.CAP_PROP_FPS)
            resized_image = self.resize_image(image)
            colored_image = self.color_frame(resized_image)
            start_time = time.perf_counter()
            timereq = 1 / video_fps
            if time.perf_counter() - start_time < timereq:
                time.sleep(timereq - (time.perf_counter() - start_time))
            self.paint_on_screen(colored_image)

    def __get_video(self):
        """Get video from the source"""
        # "https://videocdn.cdnpk.net/videos/dfedd6d9-20e8-40b5-8e93-9303f9f31930/horizontal/previews/videvo_watermarked/large.mp4"
        return cv2.VideoCapture(self.__video_url)


class TerminalImageViewer(Frame):

    def __init__(self, image_url, ascii_char=False, colored=True):
        super().__init__(ascii_char, colored)
        self.__image_url = image_url

    def view(self):
        """View method for Terminal Image Viewer"""
        image = self.__get_image()
        resized_image = self.resize_image(image)
        colored_image = self.color_frame(resized_image)
        self.paint_on_screen(colored_image)

    def __get_image(self):
        return cv2.imread(self.__image_url)


#
# def clear_screen():
#     """
#     Clear Screen between frames
#     """
#     sys.stdout.write("\033[H")  # ANSI escape code to move cursor to top-left
#     sys.stdout.flush()
#
#
# def print_in_ascii(image):
#     """
#     Print the final image
#     """
#     pic = ""
#     for row in image:
#         pic += f'{"".join(row)}\n'
#     sys.stdout.write(pic)
#     sys.stdout.flush()
#
#
# def add_color_to_character(rgb_value):
#     """
#     add RGB color to the character
#     """
#     # return f"\033[38;2;{RGB_value[2]};{RGB_value[1]};{RGB_value[0]}m{'@'}\033[0m"    # For foreground with character to represent color
#     return f"\033[48;2;{rgb_value[2]};{rgb_value[1]};{rgb_value[0]}m{' '}\033[0m"  # Background itself representing color every characters background representing one pixel
#
#
# def ascii_colored_image(image):
#     """
#     Convert image into a colored ascii image
#     """
#     color_image = []
#     for row in image:
#         new_row = []
#         for char in row:
#             new_row.append(add_color_to_character(char))
#         color_image.append(new_row)
#     return color_image
#
#
# def resize_image(image):
#     """
#     Resize image to terminal window size
#     """
#     cols, rows = os.get_terminal_size()
#     resized_image = cv2.resize(image, (cols, rows))
#     return resized_image
#
# # ----------------------------------------------------------------------------
# # def convert_to_grascale(image):
# #     """
# #     Convert to only gray scale values
# #     """
# #     return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #
# #
# # def covert_into_charaters(image):
# #     """
# #     Convert grayscale image into characters
# #     """
# #     ascii_image = []
# #     for row in image:
# #         new_row = []
# #         for char in row:
# #             percentage = int((char / 255) * 9)
# #             new_row.append(grayscale_characters[percentage])
# #         ascii_image.append(new_row)
# #     return ascii_image
# # ----------------------------------------------------------------------------------
#
# def get_youtube_stream_url(url):
#     """
#     Get Youtube stream url
#     """
#     ydl_opts = {
#         "quiet": True,
#         "format": "bestaudio/best",  # Adjust format preference
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info_dict = ydl.extract_info(url, download=False)
#         stream_url = info_dict["formats"][0][
#             "url"
#         ]  # Get the first available stream URL
#         return stream_url
#
#
# def get_video():
#     """
#     Get the video
#     """
#     # stream_url = get_youtube_stream_url("https://www.youtube.com/watch?v=u-O59jWbKZE")
#     # print(stream_url)
#     stream_url = "https://videocdn.cdnpk.net/videos/dfedd6d9-20e8-40b5-8e93-9303f9f31930/horizontal/previews/videvo_watermarked/large.mp4"
#     video_obj = cv2.VideoCapture(stream_url)
#     success = 1
#     while success:
#         clear_screen()
#         success, image = video_obj.read()
#         if image is None:
#             continue
#         video_fps = video_obj.get(cv2.CAP_PROP_FPS)
#         resized_image = resize_image(image)
#         color_image = ascii_colored_image(resized_image)
#         # grayscaled_image = convert_to_grascale(resized_image)
#         # ascii_image = covert_into_charaters(grayscaled_image)
#         start_time = time.perf_counter()
#         timereq = 1 / video_fps
#         if time.perf_counter() - start_time < timereq:
#             time.sleep(timereq - (time.perf_counter() - start_time))
#         print_in_ascii(color_image)
#
#


def main():
    """
    main function the entry point for ascii art generator
    """
    # new_video = TerminalVideoPlayer(
    #     "https://videocdn.cdnpk.net/videos/dfedd6d9-20e8-40b5-8e93-9303f9f31930/horizontal/previews/videvo_watermarked/large.mp4",
    #     True,
    # )
    # new_video.play()
    new_image = TerminalImageViewer("./Images/Image-10.jpg")
    new_image.view()
    # image = cv2.imread(f"./Images/Image-{image_number}.jpg")


if __name__ == "__main__":
    main()
