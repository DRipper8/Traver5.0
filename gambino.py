import pygame
import os

pygame.init()
pygame.mixer.init()

def Gambinopl():
    lists_of_gabino = os.listdir("C:/Users/Dominik Vogel/PycharmProjects/Traver 4.0/Music/")

    for song in lists_of_gabino:
        if song.endswith(".mp3"):
            file_path = "C:/Users/Dominik Vogel/PycharmProjects/Traver 4.0/Music/" + song
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play()
            print("playing")
            while pygame.mixer.music.get_busy() == True:
                continue



print(f"playing childish gambino, {Gambinopl()}")