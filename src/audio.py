import pygame


class Audio:

    def __init__(self, sound_name, sound_type, volume):
        super().__init__()
        # Starting the mixer
        pygame.mixer.init()

        # Loading the song
        pygame.mixer.music.load(f"../audios/{sound_type}/{sound_name}.mp3")

        # Setting the volume
        pygame.mixer.music.set_volume(volume)

        # Start playing the song
        pygame.mixer.music.play()

    # # infinite loop
    # while True:
    #
    #     print("Press 'p' to pause, 'r' to resume")
    #     print("Press 'e' to exit the program")
    #     query = input("  ")
    #
    #     if query == 'p':
    #
    #         # Pausing the music
    #         mixer.music.pause()
    #     elif query == 'r':
    #
    #         # Resuming the music
    #         mixer.music.unpause()
    #     elif query == 'e':
    #
    #         # Stop the mixer
    #         mixer.music.stop()
    #         break
