import pygame.mixer
import time

pygame.mixer.init()
pygame.mixer.music.load("correct1.mp3")

pygame.mixer.music.play(-1)

time.sleep(10)

pygame.mixer.music.stop()
