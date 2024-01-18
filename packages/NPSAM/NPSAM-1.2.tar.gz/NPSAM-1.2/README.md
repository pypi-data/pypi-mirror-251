# NP-SAM

## Introduction

In this project we propose an easily implementable workflow for a fast, accurate and seamless experience of segmentation of nanoparticles.

The project's experience could be significantly enhanced with the presence of a CUDA-compatible device; alternatively, Google Colab can be utilized if such a device is not accessible. For a quick access to the program and a CUDA-GPU try our Google Colab notebook. <br>
[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TorbenVilladsen/np-sam/blob/main/NPSAM_GoogleColab.ipynb)

## installation

Clone the repo with git and enter the newly created np-sam directory. Just copy the code and paste in the terminal for macOS or in Anaconda Prompt for Windows:
```
git clone https://oauth2:glpat-sqaQGhx_qFWdG3nB7Tx9@gitlab.au.dk/disorder/np-sam.git
cd np-sam
```
Alternativly, to circumvent Git, download the files manually from the repo and place in a directory called `np-sam` and enter the directory with `cd np-sam`.


Create a new conda environment called `NPSAM` and activate it.
```
conda create -n NPSAM python=3.10
conda activate NPSAM
```
**Install [PyTorch](https://pytorch.org/get-started/locally/)**.

Now install the remaining required packages, and make a static link to the ipykernel
```
pip install -r requirements.txt
python -m ipykernel install --user --name NPSAM --display-name NPSAM
```
Finally, download the weights for SAM from their [GitHub page](https://github.com/facebookresearch/segment-anything#model-checkpoints) or with the following command:
```
curl -O https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
```

### Get started
In the working directory and NPSAM environment execute `jupyter lab` in the terminal. This will launch jupyterlab. 

## Citation
```
@article{NPSAM,
   author = {Larsen, Rasmus and Villadsen, Torben L. and Mathiesen, Jette K. and Jensen, Kirsten M. Ø and Bøjesen, Espen D.},
   title = {NP-SAM: Implementing the Segment Anything Model for Easy Nanoparticle Segmentation in Electron Microscopy Images},
   journal = {ChemRxiv},
   DOI = {10.26434/chemrxiv-2023-k73qz-v2},
   year = {2023},
   type = {Journal Article}
}
```

## Acknowledgment
This repo benefits from Meta's [Segment Anything](https://github.com/facebookresearch/segment-anything) and [FastSAM](https://github.com/CASIA-IVA-Lab/FastSAM). Thanks for their great work.


