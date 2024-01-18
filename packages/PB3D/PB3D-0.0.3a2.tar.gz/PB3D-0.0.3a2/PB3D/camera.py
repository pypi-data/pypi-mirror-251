import numpy as np
from math import sin, cos, radians

import pygame
from pygame import *
from OpenGL.GLU import *


def normalize(vector):
    length = np.linalg.norm(vector)
    if length != 0:
        return vector / length
    else:
        return vector


def cross(vec1, vec2):
    return np.cross(vec1, vec2)

class Camera:
    def __init__(self):
        self.position = [0.0, 0.0, 5.0]
        self.front = [0.0, 0.0, -1.0]
        self.up = [0.0, 1.0, 0.0]
        self.right = [1.0, 0.0, 0.0]
        self.world_up = [0.0, 1.0, 0.0]
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 0.1
        self.sensitivity = 0.1
        self.zoom = 45.0

    def update_camera_vectors(self):
        front = [
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        ]
        self.front = normalize(front)
        self.right = normalize(cross(self.front, self.world_up))
        self.up = normalize(cross(self.right, self.front))

    def update_view_matrix(self):
        gluLookAt(*self.position, *self.front, *self.up)

    def process_keyboard(self):
        keys = pygame.key.get_pressed()
        velocity = self.speed

        if keys[K_w]:
            self.position += np.array(self.front) * velocity
        elif keys[K_s]:
            self.position -= np.array(self.front) * velocity
        elif keys[K_a]:
            self.position -= np.array(self.right) * velocity
        elif keys[K_d]:
            self.position += np.array(self.right) * velocity

        self.update_view_matrix()

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            elif self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def look_at(self, target):
        self.front = normalize(target - self.position)
        self.yaw = np.degrees(np.arctan2(self.front[2], self.front[0]))
        self.pitch = np.degrees(np.arcsin(self.front[1]))
        self.right = normalize(np.cross(self.front, self.world_up))
        self.up = normalize(np.cross(self.right, self.front))
