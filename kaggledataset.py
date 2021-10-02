import os
from pathlib import Path

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
    os.system(f"kaggle datasets metadata -p {dataset_path} {dataset_id}")
              
def download_dataset_content(dataset_id):
    '''example: kaggle datasets download -d /path/to/download zillow/zecon'''
    os.system(f"kaggle datasets download -d {dataset_id}")

def download_dataset(dataset_path,dataset_id,unzip=True):
    dataset_name = dataset_id.split('/')[-1]
    download_dataset_metadata(dataset_path,dataset_id)
    download_dataset_content(dataset_id)
    os.system(f"mv {dataset_name}.zip {dataset_path}")
    if unzip: os.system(f"unzip {dataset_path/(dataset_name+'.zip')} -d {dataset_path}")
    


def add_library_to_dataset(library,dataset_path,pip_cmd="pip3",):
    if not os.path.exists(dataset_path/library): os.makedirs(dataset_path/library)
    print(f"{pip_cmd} download {library} -d {dataset_path/library}")
    os.system(f"{pip_cmd} download {library} -d {dataset_path/library}")
    print(f"In kaggle kernal you will need to run special command to install from this")
    print(f"!pip install -Uqq {library} --no-index --find-links=file:///kaggle/input/your_dataset/")
