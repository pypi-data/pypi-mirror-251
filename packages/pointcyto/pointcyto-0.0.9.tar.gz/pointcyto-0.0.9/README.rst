.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/pointcyto.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/pointcyto
    .. image:: https://readthedocs.org/projects/pointcyto/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://pointcyto.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/pointcyto/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/pointcyto
    .. image:: https://img.shields.io/pypi/v/pointcyto.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/pointcyto/
    .. image:: https://img.shields.io/conda/vn/conda-forge/pointcyto.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/pointcyto
    .. image:: https://pepy.tech/badge/pointcyto/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/pointcyto
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/pointcyto

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=========
pointcyto
=========


    Cytometry data as point cloud representation for use with `pytorch <https://github.com/pytorch/pytorch>`_ and `pytorch_geometric <https://github.com/pyg-team/pytorch_geometric>`_.


A longer description of your project goes here...



Package setup
=============

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.

.. code-block:: bash

    pip install pyscaffold
    putup pointcyto
    cd pointcyto
    # Create pointcyto within gitlab, without README
    git branch -m master main
    git remote add origin git@git.uni-regensburg.de:ggrlab/pointcyto.git
    git push --set-upstream origin --all
    git push --set-upstream origin --tags
    conda create -y -n conda_pointcyto python=3.10
    conda activate conda_pointcyto
    # Select conda_nbnode as default python interpreter in VsCode
    #   select a single python file, then on the bottom right, the current python interpreter name
    #   pops up. Click on it and select the "conda_nbnode" interpreter.
    # Make sure that the correct pip is used:
    #   Something like: /home/gugl/.conda_envs/conda_pointcyto/bin/pip
    which pip
    pip install tox
    tox --help

    # Have a clean git, then add "gitlab-CI" with pyscaffold
    putup --update . --gitlab
    putup --update . --github

    # Add pre-commit hooks
    pip install pre-commit
    pre-commit autoupdate

    # Documentation
    # To use gitlab-pages, you need to place the created htmls in the "public/" directory
    # as artifact within the gitlab-ci.yml file.
    # Right now, it is created within: .gitlab-ci.yml//docs
