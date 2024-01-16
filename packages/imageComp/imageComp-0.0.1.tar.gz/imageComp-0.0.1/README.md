# image_compression

## What is this

Compresses images.</br>
Instead of losing color, the image size is reduced.</br>
It also makes features more pronounced, making it ideal for AI training.

## How to install

`$ pip install imageComp`

## Packages required to run this

`$ from PIL import Image`</br>
`$ import numpy as np`</br>
`$ from sklearn.decomposition import PCA`

## How to use

`$ imageComp`</br>
Enter any image including the extension</br>
`$ Enter the path to the image: filepath`</br>
then you can see "compressed_image.jpg" file

## Before:input image

![](landscape.jpg)

## After: output image

![](src/compressed_image.jpg)
