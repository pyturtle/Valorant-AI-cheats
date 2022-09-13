import os
import shutil


os.chdir(r'train folder path here')



# the code will loop over all the files in your train folder and will move 1/5 of them to your val folder, you can change this number moved by changing the number by the mod operator.
for i,f in enumerate(os.listdir()):
    
    print(f)

    if i%5 == 0:
        shutil.move(f, r"put val folder path here"+"\\"+f)