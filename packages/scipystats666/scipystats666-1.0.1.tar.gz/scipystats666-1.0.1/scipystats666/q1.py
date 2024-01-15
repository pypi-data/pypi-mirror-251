from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

link_sample = f"https://crewstore.ru/wp-content/uploads/2024/01/"

# ax, fig = plt.axes(), plt.figure(figsize=(1,1))

def n1(num: int):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.set_axis_off()
    if num in np.arange(1, 35, 1):
        if num not in (15, 20):
            resp = requests.get(link_sample + f"{num}.png")
        else:
            resp = requests.get(link_sample + "15plus20.png")
        img = Image.open(BytesIO(resp.content))
        ax.imshow(np.asarray(img), cmap = 'YlGn', interpolation = 'sinc', vmin = 0, vmax = 0.9);
