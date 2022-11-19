# CompressedCrack

Compressed Crack is a simple tool to help you crack password zip and rar files.

Clone from [this project](https://github.com/mnismt/CompressedCrack), and make functional enhancements on the basis of the original 

## Features:
* Muti-Processe to brute compress file.
* Completely open source
* Code according to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)



## Requirements:

[Python 3.x](https://www.python.org/downloads/)

[Unrar](https://www.rarlab.com/rar_add.htm): This is a RAR decompression program written in C++. If your operating system is Windows, no action is required. If you are using a Linux operating system, you need to install Unrar manually. For the installation method, refer to the official RARLIB documentation

## Install

```
apt-get -y install git
git clone https://github.com/Rhythm-2019/CompressedCrack
cd ./CompressedCrack
```
## Use
```
python crack.py -i INPUT [rules [rules ...]]

positional arguments:
  rules                 <min> <max> <character>

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Insert the file path of compressed file
                        
```                       

## Ref
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [Python Multiprocessing: The Complete Guide](]https://superfastpython.com/multiprocessing-in-python/)