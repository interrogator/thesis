# Linguistic change in an online support group

This repository contains materials related to my PhD research, which involves identifying linguistic change over the course of membership in an online forum for bipolar disorder. These materials consist mostly of:

1. The thesis itself, in `.TeX` and `.pdf`
2. *Jupyter Notebooks* containing code used to generate findings
3. The dataset used for the thesis (inside `bipolar.tar.gz` and `bipolar-parsed.tar.gz`)
4. Slides from presentations

The thesis relies extensively on *corpkit*, a purpose-built Python module, which is available via [GitHub](https://www.github.com/interrogator/corpkit) and documented at [ReadtheDocs](http://corpkit.readthedocs.io).

## Cloning the repository

This repository uses [Git Large File Storage](https://git-lfs.github.com/) to host the thesis data. This means that `git-lfs` must be installed in order to automatically download the investigation data. If you get [an error when cloning](https://github.com/github/git-lfs/issues/1166), try removing the `www.` from the `git clone` command.

## Working with Jupyter Notebooks

The *Jupyter Notebooks* in the `notebooks` directory can be viewed online, or downloaded and run locally. If you clone the whole repository, it is possible to unzip the data and run interrogations yourself.

There are three notebooks, each of which corresponds to a chapter in the thesis:

1. [Shallow features](https://github.com/interrogator/thesis/blob/master/notebooks/shallow-findings.ipynb)
2. [Mood features](https://github.com/interrogator/thesis/blob/master/notebooks/mood-findings.ipynb)
3. [Transitivity features](https://github.com/interrogator/thesis/blob/master/notebooks/transitivity-findings.ipynb)

Tweet me if you need help with anything: [@interro_gator](https://twitter.com/interro_gator)
