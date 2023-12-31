import os
import shutil

from dataclasses import asdict
import json

from golden_frame.lib import ASSET_PATH, list_frames

frames = list_frames()

os.system("rm -rf public/frames && mkdir -p public/frames")

for frame in frames:
    shutil.copyfile(ASSET_PATH + "/" + frame.name,
                    "public/frames/" + frame.name)


# Open the file in write mode
with open("src/data.g.json", "w") as file:
    # Write the text to the file
    file.write(json.dumps(list(map(asdict, frames))))
