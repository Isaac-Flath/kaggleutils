import os
from pathlib import Path

import os
from pathlib import Path
import subprocess
        
def run_bash(bashCommand,return=True):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return process, output, error

def update_datset(dataset_path,update_message):
    if os.path.exists(dataset_path/'.ipynb_checkpoints'): shutil.rmtree(dataset_path/'.ipynb_checkpoints')
    os.system(f'''kaggle datasets version -p {dataset_path} -m "{update_message}" --dir-mode zip''')
    
    
def create_dataset(dataset_path,dataset_name):
    if not os.path.exists(dataset_path): os.makedirs(dataset_path)
    os.system(f"kaggle datasets init -p {dataset_path}")
    with open(dataset_path/'dataset-metadata.json','r') as f: txt = f.readlines()
    txt = '\n'.join(txt)
    txt = txt.replace("INSERT_TITLE_HERE",dataset_name)
    txt = txt.replace("INSERT_SLUG_HERE",dataset_name)
    with open(dataset_path/'dataset-metadata.json','w') as f: f.write(txt)  
    os.system(f"touch {dataset_path/'test.txt'}")
    os.system(f"kaggle datasets create -p {dataset_path}")

def download_dataset_metadata(dataset_path,dataset_id):
    '''example: kaggle datasets metadata -p /path/to/download zillow/zecon'''
    bashCommand = f"kaggle datasets metadata -p {dataset_path} {dataset_id}"
    process, output, error = run_bash(bashCommand)
    if str(output).find('404') != -1: print('404: Dataset not found')              
    return process, output, error

def download_dataset_content(dataset_id):
    '''example: kaggle datasets download -d /path/to/download zillow/zecon'''
    bashCommand = f"kaggle datasets download -d {dataset_id}"
    process, output, error = run_bash(bashCommand)
    if str(output).find('404') != -1: print('404: Dataset not found')
    return process, output, error

def download_dataset(dataset_path,dataset_id,dataset_name,unzip=True):
    dataset_name = dataset_id.split('/')[-1]
    process, output, error = download_dataset_metadata(dataset_path,dataset_id)
    if str(output).find('404') == -1: 
        download_dataset_content(dataset_id)
        os.system(f"mv {dataset_name}.zip {dataset_path}")
        if unzip: os.system(f"unzip {dataset_path/(dataset_name+'.zip')} -d {dataset_path}")
    else: create_dataset(dataset_path,dataset_name)
    
def add_library_to_dataset(library,dataset_path,pip_cmd="pip3",):
    if not os.path.exists(dataset_path/library): os.makedirs(dataset_path/library)
    print(f"{pip_cmd} download {library} -d {dataset_path/library}")
    os.system(f"{pip_cmd} download {library} -d {dataset_path/library}")
    print(f"In kaggle kernal you will need to run special command to install from this")
    print(f"!pip install -Uqq {library} --no-index --find-links=file:///kaggle/input/your_dataset/")

    
if __name__ == "__main__":
    libraries = ['fastai','timm','torch','torchvision','huggingface']
    for library in libraries:
        download_dataset(Path(library),f'isaacflath/{library}',library,unzip=True)
        add_library_to_dataset(library,Path(library),'pip')
        
        
    
    
