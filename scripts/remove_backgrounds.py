from rembg import remove
import os

input_folder = "assets/images"
output_folder = "assets/images/clean"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        with open(os.path.join(input_folder, filename), "rb") as inp_file:
            input_data = inp_file.read()
        output_data = remove(input_data)
        with open(os.path.join(output_folder, filename), "wb") as out_file:
            out_file.write(output_data)