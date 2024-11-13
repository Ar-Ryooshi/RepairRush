import vlc
import threading
import os
import errno

class SoundManager:
    def __init__(self):
        # Deux lecteurs distincts : un pour la musique de fond, l'autre pour les effets sonores
        self.music_player = None
        self.effect_player = None
        self.music_volume = 100
        self.effect_volume = 100
        self.music_path = ""
        self.loop_music = False

    def __create_vlc_player(self, sound_path):
        if not os.path.isfile(sound_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sound_path)
        player = vlc.MediaPlayer()
        media = vlc.Media(sound_path)
        player.set_media(media)
        return player

    def __thread_play_music(self, sound_path):
        self.music_player = self.__create_vlc_player(sound_path)
        self.music_player.audio_set_volume(self.music_volume)
        self.music_player.play()

        # Boucle la musique si besoin
        if self.loop_music:
            event_manager = self.music_player.event_manager()
            event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.__loop_music)

    def __loop_music(self, event):
        self.play_music(self.music_path, loop=True)

    def __thread_play_effect(self, sound_path):
        self.effect_player = self.__create_vlc_player(sound_path)
        self.effect_player.audio_set_volume(self.effect_volume)
        self.effect_player.play()

    def play_music(self, sound_path, loop=False):
        """
        Joue une musique, en boucle si demandé.
        :param sound_path: Chemin du fichier audio à jouer.
        :param loop: Si True, la musique est jouée en boucle.
        """
        self.music_path = sound_path
        self.loop_music = loop
        threading.Thread(target=self.__thread_play_music, args=(sound_path,), daemon=True).start()

    def play_effect(self, sound_path):
        """
        Joue un effet sonore.
        :param sound_path: Chemin du fichier audio de l'effet.
        """
        threading.Thread(target=self.__thread_play_effect, args=(sound_path,), daemon=True).start()

    def set_music_volume(self, volume):
        """
        Définit le volume de la musique de fond.
        :param volume: Niveau du volume (0-100).
        """
        self.music_volume = volume
        if self.music_player:
            self.music_player.audio_set_volume(volume)

    def set_effect_volume(self, volume):
        """
        Définit le volume des effets sonores.
        :param volume: Niveau du volume (0-100).
        """
        self.effect_volume = volume
        if self.effect_player:
            self.effect_player.audio_set_volume(volume)

    def stop_music(self):
        """
        Arrête la musique de fond.
        """
        if self.music_player:
            self.music_player.stop()

    def stop_all_effects(self):
        """
        Arrête tous les effets sonores en cours.
        """
        if self.effect_player:
            self.effect_player.stop()

# Exemple d'utilisation
if __name__ == "__main__":
    sound_manager = SoundManager()
    sound_manager.play_music("sounds/mainost.mp3", loop=True)
    sound_manager.play_effect("sounds/ca-ching.mp3")
    
    # Ajuster le volume
    sound_manager.set_music_volume(80)
    sound_manager.set_effect_volume(50)
