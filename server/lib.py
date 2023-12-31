import os
import time

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


frames_info = list_frames()
