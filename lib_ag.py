import imp
from ruamel.yaml import YAML
import os
import sys
yaml_reader = YAML()
os.chdir(r'C:\Users\ekim\Desktop\autogenerator\autogenerator\examples')
print(os.listdir())
with open('h2_z_main_docum_2zi23261.yaml','r') as f:
    template = yaml_reader.load(f.read())
    yaml_reader.dump(template,sys.stdout)
    print (template)