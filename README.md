## On-demand training of a CNTK model on Azure N-Series using VSTS

This example shows how training a CNTK (or many other frameworks) model can be automated through azure and VSTS.

### Scenarios:
* You want to train different models and compare how they perform (or just change some hyperparameter and check the impact).
* You want your team to have a way to easily train a model without having to setup everything on their workstation (or you don't want their GPU to be busy for a long time :) )

### Overview & Assumptions:
* We are going to use Azure N-Series VM to profit from CNTK's GPU integration (on Linux).
* Docker will be used as the unit of deployment to make CNTK's installation and dependency management easier, and to accelerate deployment (more specifically, `nvidia-docker` to access GPU)
* Your CNTK's model code should be hosted on Github (or another Git repository). Branches will be used to host different versions of the model. The `master` branches correspond to the model currently in production (or planned to be). Other branches corresponds to experiments.

### Getting Started

1. [Creating a custom VM image](/doc/custom-image.md).


