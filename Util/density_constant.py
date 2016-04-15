import pandas as pd
from Util.Import import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import statsmodels.api as sm

def plot3d(df):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = df[[0]]
    Y = df[[1]]
    X, Y = np.meshgrid(X, Y)
    Z = df[[2]]
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased = True)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def getConstant(numTweets, desired = 30):
    constant = (desired - (1.04854984e-01 * numTweets) - 21.96103482) / 1.78221924e+02
    density = (constant*1000) / numTweets
    if density > 1:
        density = 1
    return density



if __name__ ==  "__main__":
    df = pd.read_csv("../gridResults2.csv", index_col = 0)
    df["Intercept"] = 1
    df = df[0:48]

    #plot3d(df)

    X = df[[0,1,4]]
    y = df[[2]]


    model = sm.OLS(y, X)
    model = model.fit()

    print(model.params)



    #print(getConstant(1000))
