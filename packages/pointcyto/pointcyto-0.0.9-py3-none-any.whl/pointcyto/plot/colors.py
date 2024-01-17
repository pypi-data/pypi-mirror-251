import numpy as np
from matplotlib import colormaps


# from https://gist.github.com/jakevdp/91077b0cae40f8f8244a
def discrete_cmap(n, base_cmap=None, alpha: float = 0.2, return_color_list=False):
    """
    Create an N-bin discrete colormap from the specified input map

    Args:
        n:
            How many colors do you want
        base_cmap:
            The base color map
        alpha:
            alpha from RGBA model https://en.wikipedia.org/wiki/RGBA_color_model
        return_color_list:
            Should a color list or a colormap be returned? Default: colormap

    Returns:
        Depending on return_color_list:
            - A list of colors
            - A colormap
    """

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = colormaps[base_cmap]
    color_list = base(np.linspace(0, 1, n))
    color_list[:, 3] = alpha
    if return_color_list:
        retval = color_list
    else:
        cmap_name = base.name + str(n)
        retval = base.from_list(cmap_name, color_list, n, gamma=0.3)
    return retval
