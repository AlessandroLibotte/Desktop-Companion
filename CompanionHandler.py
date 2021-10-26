from dataclasses import dataclass, field
from pynput import mouse, keyboard
from random import randint, seed
from time import time
import CompanionGraphics


class CompanionHandler:

    @dataclass
    class Companion:

        @dataclass
        class PlayerParams:
            attack: bool = False
            hit: bool = False
            hit_t: float = 0.0
            player: bool = False
            player_going_r: bool = False
            player_going_l: bool = False
            jumping: bool = False
            falling: bool = False
            sprint: bool = False
            jump_t: int = 0

        @dataclass
        class AnimParams:
            lb_t: float = 1
            t: int = 0
            sprite: str = 'Girl'
            state: int = 4
            spr_index: int = 0
            state_3_anim: bool = 0

        @dataclass
        class InteractionParams:
            grabbed: bool = False
            grab_rel_x: int = 0
            grab_rel_y: int = 0

        id: int
        x: int = 0
        y: int = CompanionGraphics.SCREEN_HEIGHT / 2
        life: int = 11
        target_x: int = None
        player_params: PlayerParams = None
        anim_params: AnimParams = None
        interaction_params: InteractionParams = None

        def __post_init__(self):

            if self.player_params is None:
                self.player_params = self.PlayerParams()
            if self.anim_params is None:
                self.anim_params = self.AnimParams()
            if self.interaction_params is None:
                self.interaction_params = self.InteractionParams()

            return

    def __init__(self):

        seed(time())

        self.companion_number = 0
        self.companions = list()
        self.playing_companion = None

        self._load_companions()

        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()

        self.mouse_listener = mouse.Listener(on_click=self._grabbed)
        self.mouse_listener.start()
        self.keyboard_listener = keyboard.Listener(
                                    on_press=lambda key: self._companion_controller(
                                                            key, 
                                                            self.companions[self.playing_companion]
                                                                if self.playing_companion is not None else None,
                                                            pressed=True,
                                                            released=False),
                                    on_release=lambda key: self._companion_controller(
                                                            key,
                                                            self.companions[self.playing_companion]
                                                                if self.playing_companion is not None else None,
                                                            pressed=False, 
                                                            released=True))
        self.keyboard_listener.start()
        return

    def _load_companions(self):

        try:
            f = open("DC-persistence.txt", "r")
        except FileNotFoundError:
            return

        for line in f:
            line = line[27:-2]
            line = line.replace(",", '')
            line = line.replace('(', ' ')
            line = line.replace(')', ' ')
            params = line.split()
            companion_params = [CompanionGraphics.SCREEN_HEIGHT if param.split("=")[0] == "y"
                                else int(param.split("=")[1]) if param.split("=")[1].isdecimal()
                                else [False for player_param in params[6:13]] if param.split("=")[0] == "player_params"
                                else [float(anim_param.split("=")[1]) if anim_param.split("=")[0] == "t"
                                      else anim_param.split("=")[1][1:-1] if not anim_param.split("=")[1].isdigit()
                                      else int(anim_param.split("=")[1]) if anim_param.split("=")[1].isdecimal() else None
                                      for anim_param in params[17:22]] if param.split("=")[0] == "anim_params"
                                else [False if interaction_param.split("=")[0] == "grabbed"
                                      else 0 if interaction_param.split("=")[0] == "grab_rel_x"
                                      else 0 if interaction_param.split("=")[0] == "grab_rel_y" else None
                                      for interaction_param in params[23:26]] if param.split("=")[0] == "interaction_params"
                                else None
                                for param in params]
            companion_params = list(filter((None).__ne__, companion_params))
            c_params = companion_params[:6]
            for param in companion_params[6:]:
                if type(param) is list:
                    c_params.append(param)
            companion_params = c_params

            print(companion_params)

            self.companion_number += 1
            self.companions.append(self.Companion(
                id=companion_params[0],
                x=companion_params[1],
                y=companion_params[2],
                life=companion_params[3],
                target_x=companion_params[4],
                player_params=self.Companion.PlayerParams(
                    player=companion_params[5][0],
                    player_going_r=companion_params[5][1],
                    player_going_l=companion_params[5][2],
                    jumping=companion_params[5][3],
                    falling=companion_params[5][4],
                    sprint=companion_params[5][5],
                    jump_t=companion_params[5][6],
                ),
                anim_params=self.Companion.AnimParams(
                    t=companion_params[6][0],
                    sprite=companion_params[6][1],
                    state=companion_params[6][2],
                    spr_index=companion_params[6][3],
                    state_3_anim=companion_params[6][4],
                ),
                interaction_params=self.Companion.InteractionParams(
                    grabbed=companion_params[7][0],
                    grab_rel_x=companion_params[7][1],
                    grab_rel_y=companion_params[7][2],
                )
            ))

        return

    def _companion_controller(self, key, playing_companion, pressed: bool, released: bool):

        if self.playing_companion is not None:
            try:
                if key == keyboard.Key.space:
                    if pressed:
                        if not playing_companion.player_params.jumping and not playing_companion.player_params.falling:
                            playing_companion.player_params.jump_t = 0.01
                            playing_companion.player_params.jumping = True
                    if released:
                        if playing_companion.player_params.jumping and not playing_companion.player_params.falling:
                            playing_companion.player_params.falling = True
                if key == keyboard.Key.shift:
                    if pressed:
                        playing_companion.player_params.sprint = True
                    else:
                        playing_companion.player_params.sprint = False
                else:

                    if key.char == 'a':
                        if pressed:
                            if not playing_companion.player_params.player_going_l:
                                playing_companion.player_params.player_going_l = True
                        if released:
                            if playing_companion.player_params.sprint:
                                playing_companion.player_params.sprint = False
                            playing_companion.player_params.player_going_l = False
                            playing_companion.anim_params.spr_index = 4

                    if key.char == 'd':
                        if pressed:
                            if not playing_companion.player_params.player_going_r:
                                playing_companion.player_params.player_going_r = True
                        if released:
                            if playing_companion.player_params.sprint:
                                playing_companion.player_params.sprint = False
                            playing_companion.player_params.player_going_r = False
                            playing_companion.anim_params.spr_index = 7

                    if key.char == 'D':
                        if pressed:
                            playing_companion.player_params.player_going_r = True
                            playing_companion.player_params.sprint = True
                        if released:
                            playing_companion.player_params.player_going_r = False
                            playing_companion.player_params.sprint = False
                            playing_companion.anim_params.spr_index = 7

                    if key.char == 'A':
                        if pressed:
                            playing_companion.player_params.player_going_l = True
                            playing_companion.player_params.sprint = True
                        if released:
                            playing_companion.player_params.player_going_l = False
                            playing_companion.player_params.sprint = False
                            playing_companion.anim_params.spr_index = 4

                    if key.char == 'e':
                        if pressed:
                            if playing_companion.player_params.attack is False:
                                playing_companion.player_params.attack = True

            except AttributeError:
                return

        return

    def _grabbed(self, mouse_x, mouse_y, button, pressed):

        if button == button.left:
            for companion in self.companions:
                if companion.x < mouse_x < companion.x + (CompanionGraphics.SPRITE_WIDTH * CompanionGraphics.SPRITE_SCALE) \
                        and companion.y - (CompanionGraphics.SPRITE_HEIGHT * CompanionGraphics.SPRITE_SCALE) < mouse_y < companion.y:
                    if pressed:
                        companion.interaction_params.grab_rel_x = companion.x - mouse_x
                        companion.interaction_params.grab_rel_y = companion.y - mouse_y
                        companion.interaction_params.grabbed = True
                    else:
                        companion.interaction_params.grab_rel_x = 0
                        companion.interaction_params.grab_rel_y = 0
                        companion.anim_params.state = 4
                        companion.interaction_params.grabbed = False
                        companion.anim_params.t = 0

        return

    def create_companion(self, sprite: str = None):

        self.companion_number += 1
        self.companions.append(self.Companion(self.companion_number))

        if sprite is not None:
            self.companions[-1].sprite = sprite
        return self.companions[-1]

    def update_position(self, companion: Companion):

        if not companion.player_params.player:
            if not companion.interaction_params.grabbed:

                if companion.anim_params.state == 0:  # Deciding where to go
                    r = randint(0, 2)
                    if r == 1:
                        companion.anim_params.state = 1
                        companion.target_x = randint(companion.x, CompanionGraphics.SCREEN_WIDTH - (CompanionGraphics.SPRITE_WIDTH * CompanionGraphics.SPRITE_SCALE))
                    elif r == 0:
                        companion.anim_params.state = 2
                        companion.target_x = randint(0, companion.x)
                    elif r == 2:
                        companion.anim_params.state = 3  # Looking around

                else:

                    if companion.anim_params.state == 1:  # Going right
                        if companion.x < companion.target_x:
                            companion.x += 1
                        else:
                            companion.anim_params.state = 0

                    if companion.anim_params.state == 2:  # Going left
                        if companion.x > companion.target_x:
                            companion.x -= 1
                        else:
                            companion.anim_params.state = 0

                    if companion.anim_params.state == 4:  # Falling
                        if companion.y < CompanionGraphics.SCREEN_HEIGHT:
                            companion.y += 1 * (companion.anim_params.t * 10)
                        elif companion.y >= CompanionGraphics.SCREEN_HEIGHT:
                            companion.y = CompanionGraphics.SCREEN_HEIGHT
                            companion.anim_params.t = 0
                            companion.anim_params.state = 0

                if companion.player_params.hit is True:
                    if companion.player_params.hit_t <= 1:
                        companion.player_params.hit_t += 0.01
                    else:
                        companion.player_params.hit_t = 0
                        companion.player_params.hit = False

            else:
                companion.x = companion.interaction_params.grab_rel_x + self.mouse_controller.position[0]
                companion.y = companion.interaction_params.grab_rel_y + self.mouse_controller.position[1]
        else:

            if companion.player_params.jumping:
                if companion.player_params.jump_t > 10 and companion.player_params.falling is False:
                    companion.player_params.falling = True
                elif companion.player_params.falling:
                    if companion.y < CompanionGraphics.SCREEN_HEIGHT:
                        companion.y += companion.player_params.jump_t
                    elif companion.y > CompanionGraphics.SCREEN_HEIGHT:
                        companion.y = CompanionGraphics.SCREEN_HEIGHT
                        companion.player_params.jump_t = 0
                        companion.player_params.falling = False
                        companion.player_params.jumping = False
                        companion.anim_params.state = 0
                else:
                    companion.y -= 1 / companion.player_params.jump_t
                companion.player_params.jump_t += 0.1

            if companion.player_params.player_going_r:
                if companion.player_params.sprint:
                    companion.x += 5
                else:
                    companion.x += 1
            elif companion.player_params.player_going_l:
                if companion.player_params.sprint:
                    companion.x -= 5
                else:
                    companion.x -= 1
            else:
                if companion.player_params.attack is True:

                    if companion.anim_params.t <= 0.2:
                        if companion.anim_params.spr_index == 4:
                            companion.x -= 5
                        if companion.anim_params.spr_index == 7:
                            companion.x += 5
                    elif companion.anim_params.t <= 0.4:
                        if companion.anim_params.spr_index == 4:
                            companion.x += 3
                        if companion.anim_params.spr_index == 7:
                            companion.x -= 3
                    else:
                        companion.anim_params.t = 0
                        companion.player_params.attack = False

                    for other_companion in self.companions:
                        if other_companion is not companion:
                            if other_companion.x < companion.x < other_companion.x + (CompanionGraphics.SPRITE_WIDTH * CompanionGraphics.SPRITE_SCALE) \
                                    or other_companion.x < companion.x + (CompanionGraphics.SPRITE_WIDTH * CompanionGraphics.SPRITE_SCALE) < companion.x + (CompanionGraphics.SPRITE_WIDTH * CompanionGraphics.SPRITE_SCALE):
                                if other_companion.life > 0 and other_companion.player_params.hit is not True:
                                    other_companion.life -= 1
                                    other_companion.anim_params.lb_t = 1
                                    other_companion.player_params.hit = True
                else:
                    companion.anim_params.t = 0

        return

    def quit(self):

        f = open("DC-persistence.txt", "w")

        for companion in self.companions:
            f.write(str(companion))
            f.write('\n')

        self.mouse_listener.stop()
        self.keyboard_listener.stop()

        return
