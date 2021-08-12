import json
import math
import os
import time

import cv2
import numpy as np

from common.utils import get_distance


class PathController:
	"Responsible to controle the drone based on loaded path plan"

	wp = []
	current_point = -1
	way_points = []
	x = 0
	y = 0
	accumulated_angle = 0
	angle = 0
	rotating = False
	done = False
	contain_path_plan = False
	loaded_plan = {}

	def __init__(self):
		self.delete_path_plan_file()
		pass

	def read_path_plan(self):
		if not os.path.exists("waypoint.json"):
			return
		f = open("waypoint.json")
		self.loaded_plan = json.load(f)
		self.wp = self.loaded_plan["wp"]
		if len(self.loaded_plan["pos"]) > 0:
			self.x, self.y = self.loaded_plan["pos"][0]
			self.contain_path_plan = True

	def move(self):
		self.current_point = self.current_point + 1
		if self.current_point >= len(self.wp):
			self.done = True
			return
		self.angle = self.get_angle()
		self.accumulated_angle += self.angle
		self.calculate_point()
		self.way_points.append((self.x, self.y))

	def get_command(self):
		if self.done:
			return {"rotation": 0, "right-left": 0, "forward-back": 0, "up-down": 0}

		if not self.rotating:
			return {"rotation": 0, "right-left": 0, "forward-back": 35, "up-down": 0}

		rotation_speed = 80
		if self.angle < 0:
			rotation_speed = -80

		return {"rotation": rotation_speed, "right-left": 0, "forward-back": 0, "up-down": 0}

	def calculate_point(self):
		distance_px = self.wp[self.current_point]["dist_px"]
		self.x += int(distance_px * math.cos(math.radians(self.accumulated_angle)))
		self.y += int(distance_px * math.sin(math.radians(self.accumulated_angle)))

	def get_angle(self):
		angle = int(self.wp[self.current_point]["angle_deg"])
		distance_px = self.wp[self.current_point]["dist_px"]
		guess_x = self.x + int(distance_px * math.cos(math.radians(self.accumulated_angle + angle)))
		guess_y = self.y + int(distance_px * math.sin(math.radians(self.accumulated_angle + angle)))

		x, y = self.loaded_plan['pos'][self.current_point + 1]
		# checking which direction is the angle
		distance_guess = get_distance((x, y), (guess_x, guess_y))
		if distance_guess < distance_px:
			return angle

		return -angle

	def draw_way_points(self, img=None):
		if img is None:
			img = np.zeros((1000, 800, 3), np.uint8)

		for point in self.way_points:
			cv2.circle(img, point, 8, (0, 255, 0), cv2.FILLED)
		return img

	def has_reached_point(self, x, y):
		if self.current_point < 0:
			return True

		dist = get_distance((x, y), (self.x, self.y))

		if dist < 10:
			self.rotating = True
			return True

		return False

	@staticmethod
	def delete_path_plan_file():
		if os.path.exists("waypoint.json"):
			os.remove("waypoint.json")
