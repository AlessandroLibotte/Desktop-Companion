import cv2
import numpy
import os


class ExtractSprites:

    def __init__(self, path: str, spr_h: int, spr_w: int, offset_x: int = 1, offset_y: int = 1, ):

        self.spr_height = spr_h
        self.spr_width = spr_w

        self.sprite_sheet = cv2.imread(path, cv2.IMREAD_UNCHANGED)

        self.extract(offset_x, offset_y)

        return

    def extract(self, offset_x: int, offset_y: int):

        i = 1
        offset = (offset_x, offset_y)
        for y in range(4 * (offset[0]-1), 4 * offset[0]):
            for x in range(3 * (offset[1]-1), 3 * offset[1]):

                spr = self.sprite_sheet[self.spr_height * y:self.spr_height * (y + 1), self.spr_width * x:self.spr_width * (x + 1)]

                bgr = spr[:, :, :3]
                alpha = spr[:, :, 3]
                result = numpy.dstack([bgr, alpha])

                filename = "Sprites/Spr" + str(i) + ".png"

                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass

                cv2.imwrite(filename, result)

                i += 1
        return
