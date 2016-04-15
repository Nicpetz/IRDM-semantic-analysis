import pandas as pd
from Util.Import import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sklearn import linear_model


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
    density = (desired - (1.04854984e-01 * numTweets) - 21.96103482) / 1.78221924e+02
    return density



if __name__ ==  "__main__":
    df = pd.read_csv("../gridResults2.csv", index_col = 0)
    df = df[0:29]

    #plot3d(df)

    X = df[[0,1]]
    y = df[[2]]
    print(X)
    print(y)

    model = linear_model.LinearRegression()
    model = model.fit(X, y)

    #print(model.coef_)
    #print(model.intercept_)


    #print(getConstant(1000))
