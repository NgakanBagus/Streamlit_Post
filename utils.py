import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def visualize_type(df: pd.DataFrame) -> plt.Figure:
    x: pd.DataFrame = df.groupby('Title')['Title']
    return x