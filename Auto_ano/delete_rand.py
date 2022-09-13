import os

os.chdir(r'C:\Users\PyPit\OneDrive\Documents\CODE\Valorant_Auto_anotate\dataset copy\images\train')

for i,f in enumerate(os.listdir()):
    
    print(f)

    if i%3 == 0:
      os.remove(f);