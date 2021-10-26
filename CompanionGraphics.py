import tkinter as tk
from bin.lib.SpriteExtractor import ExtractSprites
from os import remove
from random import randint, seed
from time import time
from win32api import GetMonitorInfo, MonitorFromPoint
from PIL import Image, ImageTk

SPRITE_WIDTH = 48
SPRITE_HEIGHT = 48
SPRITE_SCALE = 3

SCREEN_WIDTH = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")[2]
SCREEN_HEIGHT = GetMonitorInfo(MonitorFromPoint((0, 0))).get("Work")[3]


class CompanionGraphics:

    def __init__(self):

        seed(time())

        self.master = tk.Tk()

        self.master.title("Desktop Companion")
        self.master.resizable(False, False)
        self.master.geometry(str(SCREEN_WIDTH) + "x" + str(SCREEN_HEIGHT))
        self.master.lift()
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-transparentcolor", "blue")

        self.transparent_canvas = tk.Canvas(self.master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='blue', highlightthickness='0')
        self.transparent_canvas.pack(fill=tk.BOTH)

        self.spr_objs = list()
        self.lb = list()
        self.lifebar_spr = list()

        self.create_sprites(lb=True)

        return

    def create_sprites(self, c_id: int = None, change: bool = False, sprite: str = "Boy", lb: bool = False):

        def _load_sprites(_id: int = None, _change: bool = False, _lb: bool = False):

            _spr_file_names = [
                "Sprites/Spr1.png",
                "Sprites/Spr2.png",
                "Sprites/Spr3.png",
                "Sprites/Spr4.png",
                "Sprites/Spr5.png",
                "Sprites/Spr6.png",
                "Sprites/Spr7.png",
                "Sprites/Spr8.png",
                "Sprites/Spr9.png",
                "Sprites/Spr10.png",
                "Sprites/Spr11.png",
                "Sprites/Spr12.png"
            ]

            if _lb:
                self.lifebar_spr = [tk.PhotoImage(file=spr).zoom(SPRITE_SCALE, SPRITE_SCALE) for spr in _spr_file_names][::-1]
                self.lb
            else:
                if _change:
                    index = 0
                    for obj in self.spr_objs:
                        if obj[0] == _id:
                            index = self.spr_objs.index(obj)
                            self.spr_objs.remove(obj)
                            break

                    self.spr_objs.insert(index, [_id, [tk.PhotoImage(file=spr).zoom(SPRITE_SCALE, SPRITE_SCALE) for spr in _spr_file_names]])
                else:
                    self.spr_objs.append([_id, [tk.PhotoImage(file=spr).zoom(SPRITE_SCALE, SPRITE_SCALE) for spr in _spr_file_names]])

            return

        _sort_sprite = {
            'Boy': ("Sprites/Sprite Sheets/characters.png", 48, 48, 1, 1),
            'Girl': ("Sprites/Sprite Sheets/characters.png", 48, 48, 1, 2),
            'Sorceress': ("Sprites/Sprite Sheets/characters.png", 48, 48, 1, 3),
            'Warrior': ("Sprites/Sprite Sheets/characters.png", 48, 48, 1, 4),
            'OrangeFox': ("Sprites/Sprite Sheets/Fox.png", 48, 48, 1, 1),
            'BrownFox': ("Sprites/Sprite Sheets/Fox.png", 48, 48, 2, 1),
            'WhiteFox': ("Sprites/Sprite Sheets/Fox.png", 48, 48, 1, 2),
            'GrayFox': ("Sprites/Sprite Sheets/Fox.png", 48, 48, 2, 2),
            'LifeBar': ("Sprites/Sprite Sheets/LifeBar.png", 12, 48, 1, 1)
        }

        if lb:
            spr_params = _sort_sprite['LifeBar']
        else:
            spr_params = _sort_sprite[sprite]

        ExtractSprites(spr_params[0], spr_params[1], spr_params[2], spr_params[3], spr_params[4])

        _load_sprites(c_id, change, lb)

        for i in range(1, 13):
            remove("Sprites/Spr" + str(i) + ".png")

        return

    def draw(self, companion, c_id, hitbox: bool = False):

        index = 0
        for obj in self.spr_objs:
            if obj[0] == c_id:
                index = self.spr_objs.index(obj)
                break

        if companion.anim_params.lb_t > 0:
            self.transparent_canvas.create_image(companion.x, companion.y - (48 * SPRITE_SCALE), anchor=tk.SW, image=self.lifebar_spr[companion.life])
            companion.anim_params.lb_t -= 0.01
        self.transparent_canvas.create_image(companion.x, companion.y, anchor=tk.SW, image=self.spr_objs[index][1][companion.anim_params.spr_index])

        if hitbox:
            self.transparent_canvas.create_rectangle(companion.x, companion.y, companion.x + (SPRITE_WIDTH * SPRITE_SCALE), companion.y - (SPRITE_HEIGHT * SPRITE_SCALE), outline='red')

        return

    def lifebar_appear(self, companion):

        lb = self.lb[companion.life]

        lb = lb.putalpha(255 / companion.anim_params.lb_t)
        lb = ImageTk.PhotoImage(lb)
        self.transparent_canvas.create_image(companion.x, companion.y - (48 * SPRITE_SCALE), anchor=tk.SW, image=lb)

        return

    @staticmethod
    def animate(companion):

        def idle(_companion):
            _companion.spr_index = 1

        def _state1(_companion):  # Going left
            if _companion.t <= 0.25:
                _companion.spr_index = 6
            elif _companion.t <= 0.5:
                _companion.spr_index = 8
            else:
                _companion.t = 0
            return

        def _state2(_companion):  # Going right
            if _companion.t <= 0.25:
                _companion.spr_index = 3
            elif _companion.t <= 0.5:
                _companion.spr_index = 5
            else:
                _companion.t = 0
            return

        def _state11(_companion):  # Sprint left
            if _companion.t <= 0.05:
                _companion.spr_index = 6
            elif _companion.t <= 0.1:
                _companion.spr_index = 8

            else:
                _companion.t = 0
            return

        def _state12(_companion):  # Sprint right
            if _companion.t <= 0.05:
                _companion.spr_index = 3
            elif _companion.t <= 0.1:
                _companion.spr_index = 5
            else:
                _companion.t = 0
            return

        def _state3(_companion):  # Looking around.
            if _companion.t <= 1:
                _companion.spr_index = 1
                _companion.state_3_anim = randint(0, 1)
            elif _companion.t >= 1 and _companion.state_3_anim:
                if _companion.t <= 1.5:
                    _companion.spr_index = 4
                elif _companion.t <= 2.3:
                    _companion.spr_index = 7
                else:
                    _companion.t = 0
                    _companion.spr_index = 1
                    _companion.state = 0
            else:
                if _companion.t <= 1.7:
                    _companion.spr_index = 7
                elif _companion.t <= 2.2:
                    _companion.spr_index = 4
                else:
                    _companion.t = 0
                    _companion.spr_index = 1
                    _companion.state = 0
            return

        def _attack(_companion):


            return

        _sort_state = {
            0: idle,
            1: _state1,
            2: _state2,
            3: _state3,
            4: idle,
            5: _attack,
            11: _state11,
            12: _state12,
        }

        if not companion.player_params.player:
            _sort_state[companion.anim_params.state](companion.anim_params)
        else:
            if companion.player_params.player_going_r:
                if companion.player_params.sprint:
                    _sort_state[11](companion.anim_params)
                else:
                    _sort_state[1](companion.anim_params)
            elif companion.player_params.player_going_l:
                if companion.player_params.sprint:
                    _sort_state[12](companion.anim_params)
                else:
                    _sort_state[2](companion.anim_params)


        return

    def clear_screen(self):

        self.transparent_canvas.delete(tk.ALL)

        return

    def update_window(self):

        self.master.overrideredirect(True)
        self.master.update_idletasks()
        self.master.update()

        return

    def quit(self):

        self.master.destroy()

        return
