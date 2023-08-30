import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow import keras

caminho_pasta_pneumonia = "./chest_xray"
print(os.listdir(caminho_pasta_pneumonia))

#Verificar quantas imagens de pneumonia tem na pasta train
print(len(os.listdir("./chest_xray/train/PNEUMONIA")))

