# FusionX - A deep learning pipeline for cell-cell fusion analysis
Leveraging the capabilities of deep learning, we employ advanced techniques to generate a csv file with the number of nuclei per cell as well as masked images.
FusionX is the solution giving statistics to the Fusion community.
By uploading membrane and nuclei channel, you can get both the masks as well as the CSV file.

![Picture1](https://github.com/fusionxpipeline/FusionX/assets/153498022/7300832e-27e0-4f03-82da-045aeae2c997)

---------
## Installation
```bash
conda create --name fusionx python==3.8
```
```bash
conda activate fusionx
```
```bash
pip install fusionx
```
---------
### Requirements
* CUDA 11.1 (to check CUDA nvcc --version)

  ### All libraries will be automatically downloaded with the installation of fusionx
* Torch 1.10.1
* Torchaudio 0.10.1
* Torchvision 0.11.2
* Numpy 1.23.1
* Setuptools 59.5.0
* Pandas
* Cv2
* Matplotlib
* Random
*  Os
*  PIL
*  Detectron2
*  cellpose
*  Pickle5
*  Cloudpickle
---------

## Contact Information

FusionX was written by Bar Ben David and Suman Khan.

FusionX_pipeline@hotmail.com
