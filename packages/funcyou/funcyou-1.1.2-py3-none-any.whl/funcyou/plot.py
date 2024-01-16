import os, random
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import os
import random
import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import plotly.express as px

from sklearn.metrics import silhouette_samples, silhouette_score, confusion_matrix
from sklearn.preprocessing import PolynomialFeatures
from sklearn.manifold import TSNE
import itertools

def plot_random_dataset(
    main_path, row: int = 2, col: int = 5, figsize: tuple = (15, 6), recursive=True
):
    """
    Plots random images from the Path provided

    Args:
      main_path:str = path to the directory
      row:int       = number of rows needed
      col:int		  = number of columns needed
      figsize		 = size of the figure

      Returns:
          A figure of row*cols of random images from dataset

    """
    main_path = Path(main_path)
    all_images = []
    image_extension = ["jpg", "jpeg", "png", "tiff", "webp", "svg", "pjpeg"]

    if recursive:  # walk through all dir and get images
        for dir, folders, files in os.walk(main_path):
            filles = [
                f"{dir}/{i}" for i in files if i.split(".")[-1] in image_extension
            ]
            all_images += filles
    else:
        for i in main_path.iterdir():
            if i.suffix in image_extension:
                all_images.append(i)
    # sampling random images
    sample_images = random.sample(all_images, row * col)

    # plotting figure
    fig = plt.figure(figsize=figsize)

    if len(all_images) <= 0:
        print("No Image Found", len(all_images))

    for i, image in enumerate(sample_images):
        title = str(image).split("/")[-2]
        img = mpimg.imread(image)
        plt.subplot(row, col, i + 1)
        plt.title(title)
        plt.imshow(img)

    plt.show()



def make_confusion_matrix(
    y_true,
    y_pred,
    classes=None,
    figsize=(10, 10),
    text_size=15,
    norm=False,
    savefig=False,
):
    """
    Makes a labelled confusion matrix comparing predictions and ground truth labels.
    If classes is passed, confusion matrix will be labelled, if not, integer class values
    will be used.
    Args:
      y_true: Array of truth labels (must be same shape as y_pred).
      y_pred: Array of predicted labels (must be same shape as y_true).
      classes: Array of class labels (e.g. string form). If `None`, integer labels are used.
      figsize: Size of output figure (default=(10, 10)).
      text_size: Size of output figure text (default=15).
      norm: normalize values or not (default=False).
      savefig: save confusion matrix to file (default=False).

    Returns:
      A labelled confusion matrix plot comparing y_true and y_pred.
    Example usage:
      make_confusion_matrix(y_true=test_labels, # ground truth test labels
                            y_pred=y_preds, # predicted labels
                            classes=class_names, # array of class label names
                            figsize=(15, 15),
                            text_size=10)
    """
    # Create the confustion matrix
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]  # normalize it
    n_classes = cm.shape[0]  # find the number of classes we're dealing with

    # Plot the figure and make it pretty
    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.matshow(
        cm, cmap=plt.cm.Blues
    )  # colors will represent how 'correct' a class is, darker == better
    fig.colorbar(cax)

    # Are there a list of classes?
    labels = classes or np.arange(cm.shape[0])
    # Label the axes
    ax.set(
        title="Confusion Matrix",
        xlabel="Predicted label",
        ylabel="True label",
        xticks=np.arange(n_classes),  # create enough axis slots for each class
        yticks=np.arange(n_classes),
        xticklabels=labels,  # axes will labeled with class names (if they exist) or ints
        yticklabels=labels,
    )

    # Make x-axis labels appear on bottom
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()

    # Set the threshold for different colors
    threshold = (cm.max() + cm.min()) / 2.0

    # Plot the text on each cell
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if norm:
            plt.text(
                j,
                i,
                f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
                horizontalalignment="center",
                color="white" if cm[i, j] > threshold else "black",
                size=text_size,
            )
        else:
            plt.text(
                j,
                i,
                f"{cm[i, j]}",
                horizontalalignment="center",
                color="white" if cm[i, j] > threshold else "black",
                size=text_size,
            )

    # Save the figure to the current working directory
    if savefig:
        fig.savefig("confusion_matrix.png")
def plot_history(history, metrics=None, colors=None, markers=None, linestyles=None, figsize=(15, 4)):
    """
    Plot training history metrics using Matplotlib.

    Args:
        history (History): History object returned by model.fit.
        metrics (list): List of metrics to plot (e.g., ['loss', 'accuracy']).
        colors (list): List of colors for corresponding metrics.
        markers (list): List of markers for corresponding metrics.
        linestyles (list): List of line styles for corresponding metrics.
        figsize (tuple): Figure size (width, height).
    """
    if metrics is None:
        metrics = ["loss", "accuracy"]
    if colors is None:
        colors = ["blue", "red", "orange", "green", "purple", "brown", "pink", "gray"]
    if markers is None:
        markers = ["o", "s", "D", "^", "v", "<", ">", "p"]
    if linestyles is None:
        linestyles = ["-", "--", "-.", ":"]

    for metric_idx, metric in enumerate(metrics):
        plt.figure(figsize=figsize)
        plt.title(f"{metric.capitalize()}")
        plt.grid(True)

        for i, metric_type in enumerate(["train", "val"]):
            metric_name = metric if metric_type == "train" else f"val_{metric}"

            data = history.history.get(metric_name, None)
            if data is not None:
                plt.plot(
                    range(1, len(data) + 1),
                    data,
                    label=f"{metric_type.capitalize()} {metric}",
                    color=colors[i % len(colors)],
                    marker=markers[i % len(markers)],
                    linestyle=linestyles[i % len(linestyles)],
                )

        plt.xlabel("Epoch")
        plt.ylabel(metric.capitalize())
        plt.legend()

    plt.show()


def compare_histories(
    histories: list,
    plot=["loss", "accuracy"],
    split=["train", "val"],
    epoch: int = None,
    figsize=(20, 10),
    colors=None,
    **plot_kwargs,
):
    """Compares Histories

    Arguments:
    ###############
    histroies	:	list of Histories to compare
    plot:list	:   what to plot (what metrics you want to compare)  -> ['loss', 'accuracy']
    split:list  :   what split to compare -> ['train', 'val']
    epoch:int   :   for how many epochs to comapre (cannot be greater than highest epoch of histories)
    colors		: 	list of colors for each histories to represent
    figsize:tuple:  tuple of size
    plot_kwargs :   kwargs to plt.plot to customize plot

    Returns:
    ##############
    Plots plot of len(plot) * len(split) of comparing histories

    """
    if colors is not None and len(colors) != len(histories):
        print("Number of Histories and number of Colors are not equal")
        colors = None

    try:
        cols = []
        for i in plot:
            for j in split:
                if j == "val":
                    cols.append(f"{j}_{i}")
                else:
                    cols.append(i)

        # compare to epoch
        if epoch is None:
            max_epoch = sorted(histories, key=(lambda x: max(x.epoch)), reverse=True)[0]
            epoch = max(max_epoch.epoch) + 1

        def display(col, plot_num, history, epoch: int = None, **plot_kwargs):
            plt.subplot(len(plot), len(split), plot_num)
            plt.grid(True)

            if epoch is None:
                epoch = history.epoch

            plt.plot(
                np.arange(epoch),
                pd.DataFrame(history.history)[col],
                label=history.model.name,
                **plot_kwargs,
            )
            plt.title((" ".join(col.split("_"))).upper())
            plt.xlabel("epochs")
            plt.ylabel(col.split("_")[-1])
            plt.legend()

        plt.figure(figsize=figsize)
        plot_title = " ".join(plot).upper() + " PLOT"
        plt.suptitle(plot_title)

        for plot_num, col in enumerate(cols, 1):
            if colors is None:
                for hist in histories:
                    display(col, plot_num, hist, epoch)

            else:
                for hist, color in zip(histories, colors):
                    display(col, plot_num, hist, epoch, color=color)

    except Exception as e:
        print("Error Occured: ", e)



def plot_silhouette(x, cluster_labels, name=' ', ax=None, **kwargs):
    """
    Plots the silhouette scores for each cluster in a clustering result. The function visualizes the silhouette coefficients and cluster labels.

    Args:
        x (array-like): The data points.
        cluster_labels (array-like): The cluster labels for each data point.
        name (str): The name of the clustering result.

        ax (matplotlib Axes, optional): The axes to plot the silhouette. If not provided, a new figure and axes will be created.
        **kwargs: Additional keyword arguments to be passed to the `fill_betweenx` function.

    Returns:
        ax (matplotlib Axes): The axes containing the silhouette plot.

    Raises:
        None

    Example:
        ```
        import matplotlib.pyplot as plt
        import numpy as np

        cluster_labels = np.array([0, 1, 0, 1, 2])
        x = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])

        fig, ax = plt.subplots()
        plot_silhouette("Clustering Result", cluster_labels, x, ax=ax)

        plt.show()
        ```
    """


    if ax is None:
        fig, ax = plt.subplots()

    n_clusters = np.unique(cluster_labels).size
    
    silhouette_avg = silhouette_score(x, cluster_labels)    
    ax.set_title(f"{name} - Silhouette Score: {silhouette_avg:.2f}")

    sample_silhouette_values = silhouette_samples(x, cluster_labels)

    y_lower = 10
    for i in range(cluster_labels.max() + 1):
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = plt.cm.Spectral(float(i) / cluster_labels.max())
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_values, facecolor=color, edgecolor=color, alpha=0.7, **kwargs)
        ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10

    ax.set_xlabel("Silhouette Coefficient Values")
    ax.set_ylabel("Cluster label")
    ax.set_title(f"{name}: Clusters({n_clusters}) Silhouette Score({silhouette_avg:.2f})")
    # The vertical line for the average silhouette score of all the values
    ax.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax.set_xlim(-0.2, 1)

    return ax

def get_cluster_centers(X, cluster_labels, n_clusters):
    centers = np.zeros((n_clusters, X.shape[1]))
    for i in range(n_clusters):
        centers[i] = np.mean(X[cluster_labels == i], axis=0)
    return centers


def plot_scatter_2d(x, cluster_labels, ax=None, random_state=42, **kwargs):
    """
    Plots a 2D scatter plot of data points with cluster labels. The function visualizes the data points and highlights the cluster centers.

    Args:
        x (array-like): The data points.
        cluster_labels (array-like): The cluster labels for each data point.
        ax (matplotlib Axes, optional): The axes to plot the scatter plot. If not provided, a new figure and axes will be created.
        random_state (int, optional): The random seed for reproducibility. Defaults to 42.
        **kwargs: Additional keyword arguments to be passed to the `scatter` function.

    Returns:
        ax (matplotlib Axes): The axes containing the scatter plot.

    Raises:
        None

    Example:
        ```
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
        cluster_labels = np.array([0, 1, 0, 1, 2])

        fig, ax = plt.subplots()
        plot_scatter_2d(x, cluster_labels, ax=ax, c='red', marker='o')

        plt.show()
        ```
    """
    n_clusters = len(np.unique(cluster_labels))
        
    if x.shape[-1] < 2:
        x = PolynomialFeatures(3).fit_transform(x)

    if x.shape[-1] != 2:
        x = TSNE(n_components=2, random_state=random_state).fit_transform(x)
        
    if ax is None:
        fig, ax = plt.subplots()
        
    if 'c' not in kwargs:
        kwargs['c'] = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)

    ax.scatter(x[:, 0], x[:, 1], **kwargs)
    
    centers = get_cluster_centers(x, cluster_labels, n_clusters)
    ax.scatter(
        centers[:, 0],
        centers[:, 1],
        marker="o",
        c="white",
        alpha=1,
        s=200,
        edgecolor="k",
    )

    for i, c in enumerate(centers,1):
        ax.scatter(c[0], c[1], marker="$%d$" % i)

    return ax


def plot_scatter_3d(x, cluster_labels, n_clusters=None, ax=None, random_state=42,**kwargs):
    """
    Plots a 3D scatter plot.

    This function takes in data points `x` and their corresponding `cluster_labels` and plots them in a 3D scatter plot. It also plots the cluster centers as white markers.

    Args:
        x (array-like): The data points to be plotted.
        cluster_labels (array-like): The labels corresponding to each data point.
        n_clusters (int, optional): The number of clusters. If not provided, it will be inferred from the unique values in `cluster_labels`.
        ax (Axes3D, optional): The 3D axes to plot on. If not provided, a new figure and axes will be created.
        random_state (int, optional): The random seed for the t-SNE algorithm.

    Returns:
        Axes3D: The 3D axes object containing the scatter plot.

    Raises:
        None

    Examples:
        ```
        x = np.random.rand(100, 2)
        cluster_labels = np.random.randint(0, 3, 100)
        plot_scatter_3d(x, cluster_labels)
        ```
    """

    

    n_clusters = np.unique(cluster_labels).size

    if x.shape[-1] < 3:
        x = PolynomialFeatures(3).fit_transform(x)
        
    if x.shape[-1] != 3:
        x = TSNE(n_components=3, random_state=random_state).fit_transform(x)
        
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
    if 'c' not in kwargs:
        kwargs['c'] = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)

    ax.scatter(x[:, 0], x[:, 1], x[:, 2], **kwargs)

    centers = get_cluster_centers(x, cluster_labels, n_clusters)
    ax.scatter(
        centers[:, 0],
        centers[:, 1],
        centers[:, 2],
        marker="o",
        c="white",
        alpha=1,
        s=200,
        edgecolor="k",
    )

    for i, c in enumerate(centers, 1):
        ax.scatter(c[0], c[1], c[2], marker="$%d$" % i)

    return ax


def plot_scatter(x, y, n_components=2, **kwargs):
    """
    Plots a scatter plot of data points.

    This function takes in data points `x` and their corresponding labels `y` and plots them as a scatter plot. The number of dimensions of the plot can be specified using the `n_components` parameter.

    Args:
        x (array-like): The data points to be plotted.
        y (array-like): The labels corresponding to each data point.
        n_components (int, optional): The number of dimensions for the scatter plot. Must be either 2 or 3. Defaults to 2.
        **kwargs: Additional keyword arguments to customize the scatter plot.

    Returns:
        None

    Raises:
        ValueError: Raised when `n_components` is not 2 or 3.

    Examples:
        ```
        x = np.random.rand(100, 2)
        y = np.random.randint(0, 3, 100)
        plot_scatter(x, y, n_components=2, color='red', marker='o')
        ```
    """
    
    if n_components not in [2, 3]:
        raise ValueError("n_components must be in [2, 3]")
        
    if x.shape[-1] != n_components:
        x = TSNE(n_components=n_components, random_state=42).fit_transform(x)
    
    x = pd.DataFrame(x, columns=["x", "y", "z"] if n_components == 3 else ["x", "y"])
    x['cluster']=y
    x['cluster'] = x['cluster'].astype('category')
    if n_components == 2:
        fig=px.scatter(data_frame=x, x='x', y='y', color='cluster', symbol='cluster', **kwargs)
    elif n_components == 3:
        fig=px.scatter_3d(data_frame=x, x='x', y='y', z='z', color='cluster', symbol='cluster', **kwargs)
    
    fig.show()


def main():
    pass


if __name__ == "__main__":
    main()
