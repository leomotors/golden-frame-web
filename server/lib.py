import os

import cv2
import numpy as np

from golden_frame.lib import ASSET_PATH, build_frame, get_target_resolution, list_frames,  load_config


def build_golden_frame(frame_name: str, input_image: np.ndarray, res: int, crop: bool):
    frame_path = os.path.join(ASSET_PATH, frame_name)
    frame_image = cv2.imread(frame_path)
    cfg = load_config(frame_path)

    target_resolution = get_target_resolution(res, cfg, frame_image)

    out_image = build_frame(
        source_image=input_image,
        frame_image=frame_image,
        frame_marks=load_config(frame_path)["pos"],
        target_resolution=target_resolution,
        crop=crop,
    )

    return out_image


def line_to_json(line: str):
    tokens = line.split(":")
    name = ":".join(tokens[:2]).strip()
    name_tokens = name.split(" ")
    description = tokens[2].strip()

    return {
        "name": name_tokens[0].strip(),
        "description": description,
        "ratio": float(name_tokens[1].strip()[1:].split(":")[0])
    }


def list_frame_json():
    frames = list_frames()
    items = list(map(line_to_json, filter(
        lambda x: len(x), frames.split("\n")[1:])))

    return items
