from pathlib import *
import encode, sys


input_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\orgin\\b_door_c10")
output_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\\b_door_c10")
json_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\\json_t\\b_door_c10.json")


encode.encode(input_file, json_file, output_file)