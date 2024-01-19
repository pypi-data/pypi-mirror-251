import pygame


class Channel:
    def __init__(self, path: str):

        self.path : str = path


    def pause(self):
        self.pygame_channel.pause()
        self._is_playing = False

    def is_playing(self) -> bool:
        return self._is_playing

    def unpause(self):
        self.pygame_channel.unpause()
        self._is_playing = True

    def stop(self):
        self.pygame_channel.stop()
        self._is_playing = False
        self.stopped = True

    def set_volume(self, volume):
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
        self.volume = volume
        if self.pygame_channel:
            self.pygame_channel.set_volume(volume / 100)

    def get_volume(self):
        return self.volume

    def play(self, loop = -1):
        sound = pygame.mixer.Sound(self.path)
        self.pygame_channel.play(sound, -1)