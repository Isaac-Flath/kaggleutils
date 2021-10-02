import os
from pathlib import Path
import subprocess
import shutil
        
def run_bash(bashCommand):
    print('+'*30)
    print(f'Running command {bashCommand}')
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    print(error)
    print('+'*30)
    return process, output, error

def update_datset(dataset_path,update_message):
    if os.path.exists(dataset_path/'.ipynb_checkpoints'): shutil.rmtree(dataset_path/'.ipynb_checkpoints')
    if os.path.exists(dataset_path/'tmp.txt'): os.remove(dataset_path/'tmp.txt')
    bashCommand = f'''kaggle datasets version -p {dataset_path} -m "{update_message}" --dir-mode zip'''
    process, output, error = run_bash(bashCommand)
    return process, output, error
    
    
def create_dataset(dataset_path,dataset_name):
    if not os.path.exists(dataset_path): os.makedirs(dataset_path)
    
    bashCommand = f"kaggle datasets init -p {dataset_path}"
    process, output, error = run_bash(bashCommand)
        
    with open(dataset_path/'dataset-metadata.json','r') as f: txt = f.readlines()
    txt = '\n'.join(txt)
    txt = txt.replace("INSERT_TITLE_HERE",dataset_name)
    txt = txt.replace("INSERT_SLUG_HERE",dataset_name)
    with open(dataset_path/'dataset-metadata.json','w') as f: f.write(txt)  
    os.system(f"touch {dataset_path/'tmp.txt'}")
    bashCommand = f"kaggle datasets create -p {dataset_path} -u"
    process, output, error = run_bash(bashCommand)
    return process, output, error             

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

def download_dataset(dataset_path,dataset_id,dataset_name,content=True, unzip=True):
    dataset_name = dataset_id.split('/')[-1]
    process, output, error = download_dataset_metadata(dataset_path,dataset_id)
    if (str(output).find('404') == -1 )and content: 
        download_dataset_content(dataset_id)
        os.system(f"mv {dataset_name}.zip {dataset_path}")
        if unzip: 
                bashCommand = f"unzip {dataset_path/(dataset_name+'.zip')} -d {dataset_path}"
                process, output, error = run_bash(bashCommand)
    else: process, output, error = create_dataset(dataset_path,dataset_name)
    return output, error
    
def add_library_to_dataset(library,dataset_path,pip_cmd="pip3",):        
    bashCommand = f"{pip_cmd} download {library} -d {dataset_path}"
    process, output, error = run_bash(bashCommand)
    return process, output, error

if __name__ == '__main__':
    libraries = ['huggingface','timm','torch','torchvision','fastai']

    for library in libraries: 
        dataset_path = Path(library)

        print("downloading dataset...")
        download_dataset(dataset_path,f'isaacflath/library{library}',f'library{library}',content=False,unzip=True)


        print("adding library...")
        add_library_to_dataset(library,dataset_path)

        print("updating dataset...")
        update_datset(dataset_path,"UpdateLibrary")

        print('+'*30)
        
        
    
    
