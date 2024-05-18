from io import BytesIO
from typing import Callable, List

import datashader as ds
import numpy as np
import pandas as pd
from colorcet import palette
from datashader import transfer_functions as tf
from datashader.colors import inferno, viridis

from app.services.helper.traj_cordinates import trajectory_coords
from app.utils.logger import logger_system as logger
from pandas import DataFrame
from PIL import Image
from app.schemas.request.attractor import BackgroundColor

palette["viridis"] = viridis
palette["inferno"] = inferno

class AttractorService:
    def __init__(self, n: int = 10000000, background_color: BackgroundColor = BackgroundColor.BLACK):
        self.n = n
        self.background_color = background_color

    def trajectory(self, fn, x0, y0, a, b=0, c=0, d=0, e=0, f=0, n=10000000):
        x, y = trajectory_coords(fn, x0, y0, a, b, c, d, e, f, n)
        return pd.DataFrame(dict(x=x, y=y))

    def gen_random(self, func, desired_empty=10000):
        non_empty = 0
        tries = 0
        while non_empty < desired_empty or tries <= 10:
            initial_conditions = np.c_[np.zeros((1, 2)), np.random.random((1, 6)) * 4 - 2][0]
            df = self.trajectory(func, *initial_conditions, n=20000)
            cvs = ds.Canvas(plot_width=500, plot_height=500)
            agg = cvs.points(df, "x", "y")
            non_empty = np.count_nonzero(np.array(agg))
            tries += 1
        return initial_conditions

    def make_dataframe(self, initial_conditions: List[float], function: Callable, label=True):
        lab = (
            ("{}, " * (len(initial_conditions) - 1) + " {}").format(*initial_conditions)
            if label
            else None
        )
        logger.info(f"label: {lab}")
        df = self.trajectory(function, *initial_conditions, n=self.n)  # type: ignore
        return df

    def df_to_imgs(self, df: DataFrame, cmap: str):
        imgs = []
        cvs = ds.Canvas(plot_width=500, plot_height=500)
        frames = np.geomspace(200, self.n, 45).astype(int)
        color_map = palette[cmap]
        bg_color_value = (0 , 0 , 0) if self.background_color == BackgroundColor.BLACK else (255 , 255 , 255)
        for i in frames:
            agg = cvs.points(df[:i] , "x" , "y")
            img = tf.shade(agg , cmap = color_map , how = 'log').to_pil()
            bg_img = Image.new("RGB" , img.size , bg_color_value)
            bg_img.paste(img , mask = img.split()[3])  # use alpha channel as mask
            imgs.append(bg_img)

        for _ in range(5):
            imgs.append(imgs[-1])
        return imgs

    def make_gif_from_df(self, df: DataFrame, cmap: str, bg_color: BackgroundColor) -> (BytesIO, str):
        self.background_color = bg_color
        imgs = self.df_to_imgs(df, cmap=cmap)
        fp_out = BytesIO()
        imgs[0].save(
            fp=fp_out,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=100,  # 100ms per frame
            loop=0,
        )
        file_size_mb = len(fp_out.getvalue()) / (1024 * 1024)  # Calculate file size in MB
        #! utils/looger logger_system Should be through this !!!!!!!!!!
        logger.info(f"GIF created successfully, Size: {file_size_mb:.2f} MB")
        fp_out.seek(0)
        filename = "attractor.gif"
        return fp_out, filename, file_size_mb