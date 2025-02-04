from pathlib import *
import encode, sys


input_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\orgin\\a_op_h")
output_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\\a_op_h")
json_file = Path("d:\game\ヤっても出られない部屋に閉じ込められたので引き続きもっとヤる話\out\\t\\a_op_h.json")


encode.encode(input_file, json_file, output_file)