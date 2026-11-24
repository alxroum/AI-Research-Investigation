from pathlib import Path
from urllib.request import urlretrieve
from datasets import load_dataset
from PIL import Image
import vizualizer as vs

# This program is responsible for setting up the project. This includes setting up the data and model.

# Load the Flickr8k dataset
ds = load_dataset("jxie/flickr8k", split="train")

visualizer = vs.Visualizer(ds, 4, 4)

visualizer.display()