from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
# import seaborn as sns

import streamlit as st
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def draw_pca(df,features):
    # if st.button("Draw PCA"):

        features=features.tolist()
        pca(df,features)



def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    ## Using a special case to obtain the eigenvalues of this
    ## two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    ## Calculating the standard deviation of x from
    ## the squareroot of the variance and multiplying
    ## with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    ## calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def pca(df, features):

    # Separating out the features
    x = df.loc[:, features].values

    # Separating out the target
    y = df.loc[:,['Group']].values

    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=2)

    principalComponents = pca.fit_transform(x)

    principalDf = pd.DataFrame(data=principalComponents
                               , columns=['principal component 1', 'principal component 2'])

    finalDf = pd.concat([principalDf, df[['Group']]], axis=1)
    explained_variance_per_component = pca.explained_variance_ratio_
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    pc1_var = explained_variance_per_component[0] * 100
    pc1_var = f"{pc1_var:.1f}"
    pc2_var = explained_variance_per_component[1] * 100
    pc2_var = f"{pc2_var:.1f}"
    ax.set_xlabel('Principal Component 1 (' + str(pc1_var) + "%)", fontsize=15)
    ax.set_ylabel('Principal Component 2 (' + str(pc2_var) + "%)", fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)

    targets  = st.multiselect(
            "Select groups for PCA",
            np.unique(y).tolist(),
            max_selections=len(np.unique(y).tolist()),
            accept_new_options=False,
        )
    if len(targets)>1 and st.button("Draw PCA"):
        num_lines = len(targets)
        # ax.set_prop_cycle(sns.color_palette("coolwarm_r", num_lines))
        colors = ['salmon', 'lawngreen', 'dodgerblue','c','m','y','aquamarine', 'mediumseagreen',
                  'xkcd:sky blue', 'orange', "red", "darkslategray", "teal", "indigo", "purple",
                  "darkgreen", "mediumvioletred","crimson", "slategray", "royalblue"]*(len(targets)//3+1)
        markers = (['.']*8+ [11]*8+ ["P"]*8+ ["*"]*8 +["+"]*8)*(len(targets)//3+1)
        for target, m, color in zip(targets,markers, colors):
            indicesToKeep = finalDf['Group'] == target
            ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                       , finalDf.loc[indicesToKeep, 'principal component 2']
                       , c=color
                       , s=50
                       , marker=m)


        for target, color in zip(targets,colors):
            pc_scores = finalDf.loc[finalDf["Group"] == target]

            x = pc_scores.iloc[:, 0]
            y = pc_scores.iloc[:, 1]

            # Plot a 95% confidence ellipse (approx 2 std deviations for a general sense)
            confidence_ellipse(x, y, ax, n_std=2.0, edgecolor=color, label='~95% Confidence')

            # You can also use the built-in function directly if your Matplotlib is up to date:
            # ax.confidence_ellipse(x, y, edgecolor='blue', label='Built-in 95%', n_std=2.0)

        # ax.legend(targets)
        ax.legend(targets,loc='center left', bbox_to_anchor=(1, 0.5))
        ax.grid()
        st.pyplot(fig)
        # if st.button("Save figure"):
        path = str("pca") + "_" + str(targets) + ".svg"
        out_fig = fig.savefig(path, bbox_inches="tight")
        # st.download_button('Download SVG', out_fig, file_name=path, mime='image/svg+xml')