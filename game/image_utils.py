import pygame


def get_bottom_padding(image):
    """
    Returns how many fully-transparent pixel rows
    exist at the very bottom of an image.

    Many sprite/scene PNGs leave empty transparent
    space below the actual artwork (uneven export,
    shadow space, extra canvas, etc). If we align
    the image's raw bottom edge with the ground,
    the visible character/building will appear to
    float above the ground by that many pixels.

    This scans the alpha channel from the bottom
    row upward and returns the offset of the first
    row that contains any non-transparent pixel.
    """

    width, height = image.get_size()

    for y in range(height - 1, -1, -1):

        row_has_pixel = False

        for x in range(0, width, 2):
            # Step by 2 pixels for speed. Good
            # enough to detect a mostly-empty row.

            if image.get_at((x, y))[3] != 0:

                row_has_pixel = True
                break

        if row_has_pixel:

            return height - 1 - y

    # Fully transparent image
    return 0