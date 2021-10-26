from bin.lib.psgtrayunderAlexEdit import SystemTray
from CompanionGraphics import CompanionGraphics
from CompanionHandler import CompanionHandler
from sys import exit
from time import sleep


class CompanionMain:

    COMPANION_SUBMENU = ['Control',
                         'Change Sprite', [
                             'Characters', ['Boy', 'Girl', 'Sorceress', 'Warrior'],
                             'Fox', ['OrangeFox', 'BrownFox', 'WhiteFox', 'GrayFox']],
                         'Remove Companion']

    MENU = ['', ['Add Companion', [
        'Characters', ['Boy', 'Girl', 'Sorceress', 'Warrior'],
        'Fox', ['OrangeFox', 'BrownFox', 'WhiteFox', 'GrayFox']],
                      '---',
                      '---',
                      'Quit'
                      ]]

    def __init__(self):

        self._create_tray_icon()

        self.companion_graphics = CompanionGraphics()

        self.companion_handler = CompanionHandler()

        for companion in self.companion_handler.companions:
            self.companion_graphics.create_sprites(companion.id, False, companion.anim_params.sprite)
            self.add_companion_tray_field(companion)

        self.event = None

        self._mainloop()

        return

    def _mainloop(self):

        while True:

            self.loop()

            sleep(0.01)

    def _create_tray_icon(self):

        self.tray_icon = SystemTray(self.MENU, single_click_events=False, window=self, tooltip="Desktop Companion",
                                    icon="Desktop-Companion.ico")

        return

    def add_companion_tray_field(self, companion):

        self.tray_icon.close()
        self.MENU[1].insert(3, 'Companion' + str(companion.id))
        self.MENU[1].insert(4, self.COMPANION_SUBMENU)
        self._create_tray_icon()

        return

    def remove_companion_tray_field(self, tray_field):

        self.tray_icon.close()
        for element in self.MENU[1]:
            if element == tray_field:
                index = self.MENU[1].index(element)
                self.MENU[1].pop(index)
                self.MENU[1].pop(index)
        self._create_tray_icon()

        return

    def write_event_value(self, key, event):

        self.event = key if key is not None else event

        return

    def event_handler(self):

        if self.event is not None:
            print(f"Occurred event: {self.event}.")  # Print for debug purposes.

            if self.event == 'Quit':
                self.quit()
            else:

                _event_keys = self.event.split('-')

                if 'Companion' in _event_keys[0] and 'Add' not in _event_keys[0]:
                    _companion_index = 0
                    for companion in self.companion_handler.companions:
                        if companion.id == int(_event_keys[0][-1]):
                            _companion_index = self.companion_handler.companions.index(companion)
                    print(f"index: {_companion_index}, id: {int(_event_keys[0][-1])}")
                    if _event_keys[1] == 'Change Sprite':
                        self.companion_handler.companions[_companion_index].anim_params.sprite = _event_keys[3]
                        self.companion_graphics.create_sprites(int(_event_keys[0][-1]), True, _event_keys[3])
                    if _event_keys[1] == 'Control':
                        if self.companion_handler.playing_companion is None:
                            self.companion_handler.companions[_companion_index].anim_params.spr_index = 1
                            self.companion_handler.playing_companion = _companion_index
                            self.companion_handler.companions[_companion_index].player_params.player = True
                        else:
                            if self.companion_handler.companions[_companion_index].player_params.player:
                                self.companion_handler.playing_companion = None
                                self.companion_handler.companions[_companion_index].player_params.player = False
                            else:
                                self.companion_handler.companions[self.companion_handler.playing_companion].player_params.player = False
                                self.companion_handler.companions[_companion_index].anim_params.spr_index = 1
                                self.companion_handler.playing_companion = _companion_index
                                self.companion_handler.companions[_companion_index].player_params.player = True
                    if _event_keys[1] == 'Remove Companion':
                        self.companion_handler.companions.pop(_companion_index)
                        self.companion_graphics.spr_objs.pop(_companion_index)
                        self.remove_companion_tray_field(_event_keys[0])

                if _event_keys[0] == 'Add Companion':
                    _new_companion = self.companion_handler.create_companion(_event_keys[2])
                    self.companion_graphics.create_sprites(self.companion_handler.companions[-1].id, False, _event_keys[2])
                    self.add_companion_tray_field(_new_companion)

            self.event = None

        return

    def loop(self):

        self.event_handler()

        self.companion_graphics.clear_screen()

        for companion in self.companion_handler.companions:
            self.companion_handler.update_position(companion)
            self.companion_graphics.animate(companion)
            self.companion_graphics.draw(companion, companion.id)
            companion.anim_params.t += 0.01

        self.companion_graphics.update_window()

        return

    def quit(self):

        self.tray_icon.close()
        self.companion_handler.quit()
        self.companion_graphics.quit()

        exit()


def __main():
    CompanionMain()


if __name__ == "__main__":
    __main()
