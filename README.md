# BI-VWM-LSI vector model

LSI vector model


## Binaries:  
### Instalation:  
Download from: www.uschovna.cz/zasilka/YA9JALG5L3ASZM8P-K2A  
  *  (for linux: dist_linux.zip)  
  *  (for windows 10: dist_win10.zip)  

Extract downloaded zip file  
### Executing:  
Run mainGuiApp (mainGiuApp.exe for windows)    
 - Wait until apllication loads (for first time it can take up to 10 minutes)  

## Python packages:  
### Instalation:  
pip install -r requirements.txt    

#### + for debian-derived distributions:  
apt-get install python3-tk  
#### + for arch-derived distributions:  
pacman -S tk  

### Executing:   
python mainGuiApp.py  


## Runtime notes:  
For LSI model recalculation program needs a lot of RAM (Approximately 16+ GB) and quite a lot of time (approximately 15 minutes).
If program doesnt have sufficient amount of RAM it can crash whem recalculating LSI model. If
this happens you need to replace data folder with original data folder or else the program will try to recalculate
whole model each time when you run it, which will never be completed because of insufficient amount of RAM.  

## References:  

Test data are from package  "Reuters-21578, Distribution 1.0"  

The Reuters-21578, Distribution 1.0 test collection is available
from David D. Lewis' professional home page, currently:
             http://www.research.att.com/~lewis  

Sparse matrix manipulations:
https://datascience.blog.wzb.eu/2016/06/17/creating-a-sparse-document-term-matrix-for-topic-modeling-via-lda/

Data preprocessing:
https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python