
from utils.utils import read_blast_output
from scipy.stats import gaussian_kde
import polars as pl
import utils.constants as constants
import matplotlib.pyplot as plt
import numpy as np


df = read_blast_output(constants.BLAST_OUT_PATH)



mlendf = (df
          .group_by('query')
          .agg([pl.col('al_len')
                .max()])
                .rename({"al_len":"max_len"}))

df = df.join(mlendf,on="query")

df = df.with_columns(
    qcovhsp = pl.col("al_len")/pl.col("max_len")
)

df = df.filter(pl.col("qcovhsp")>0.25)

grouped = df.group_by(['query'])

for group_key, group_df in grouped:
    nbins=constants.NKERNEL_BINS
    x,y = group_df["qcovhsp"]*100,group_df["perc_id"]
    k = gaussian_kde([x,y])

    xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))
 
   #Plot the 2D density plot using Matplotlib
    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='auto',snap=True,rasterized=True)
    plt.title(group_key[0])
    plt.xlabel('Query coverage')
    plt.ylabel('Percentage identity')
    plt.savefig(constants.PIC_SAVE_ROOT + str(group_key[0]) + "_density.png")
    plt.clf()