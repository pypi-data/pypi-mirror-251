import os
import json
import moxing as mox
from ..utils import constants
from ..utils.util import unzip_data

def moxing_code_to_env(code_url, code_dir, unzip_required):    
    """
    copy code to training image
    """
    if unzip_required == constants.DATASET_NEED_UNZIP_TRUE:
        try:
            codefile_path = os.path.join(code_dir, os.path.basename(code_url))
            mox.file.copy(code_url, codefile_path) 
            moxing_success = True
            if not os.path.exists(code_dir):
                os.makedirs(code_dir)
            unzip_success = unzip_data(codefile_path, code_dir)
        except Exception as e:
            print(f'❌ moxing download {code_url} to {code_dir} failed: {str(e)}')
            moxing_success = False
    else:
        try:
            mox.file.copy_parallel(code_url, code_dir)
            unzip_success = True
        except Exception as e:
            print(f'❌ moxing download {code_url} to {code_dir} failed: {str(e)}')
    if moxing_success & unzip_success:
        print(f'✅ Successfully Prepare Code')
    return

def moxing_dataset_to_env(multi_data_url, data_dir, unzip_required):    
    """
    copy dataset to training image
    """
    multi_data_json = json.loads(multi_data_url)
    for i in range(len(multi_data_json)):
        datasetfile_path = os.path.join(data_dir, multi_data_json[i]["dataset_name"])
        if unzip_required == constants.DATASET_NEED_UNZIP_TRUE:
            try:
                mox.file.copy(multi_data_json[i]["dataset_url"], datasetfile_path) 
                moxing_success = True
                filename = os.path.splitext(multi_data_json[i]["dataset_name"])[0]
                unzipfile_path = data_dir + "/" + filename
                if not os.path.exists(unzipfile_path):
                    os.makedirs(unzipfile_path)
                unzip_success = unzip_data(datasetfile_path, unzipfile_path)
            except Exception as e:
                print(f'❌ moxing download {multi_data_json[i]["dataset_url"]} to {datasetfile_path} failed: {str(e)}')
                moxing_success = False
        else:
            try:
                mox.file.copy_parallel(multi_data_json[i]["dataset_url"], datasetfile_path)
            except Exception as e:
                print(f'❌ moxing download {multi_data_json[i]["dataset_url"]} to {datasetfile_path} failed: {str(e)}')
        if moxing_success & unzip_success:
            print(f'✅ Successfully Prepare Dataset {os.path.splitext(multi_data_json[i]["dataset_name"])[0]}')
    return

def moxing_pretrain_to_env(pretrain_url, pretrain_dir, unzip_required):
    """
    copy pretrain to training image
    """
    pretrain_url_json = json.loads(pretrain_url)  
    for i in range(len(pretrain_url_json)):
        modelfile_path = pretrain_dir + "/" + pretrain_url_json[i]["model_name"]
        if unzip_required == constants.DATASET_NEED_UNZIP_TRUE:
            try:
                mox.file.copy(pretrain_url_json[i]["model_url"], modelfile_path) 
                moxing_success = True
                filename = os.path.splitext(pretrain_url_json[i]["model_name"])[0]
                unzipfile_path = pretrain_dir + "/" + filename
                if not os.path.exists(unzipfile_path):
                    os.makedirs(unzipfile_path)
                unzip_success = unzip_data(modelfile_path, unzipfile_path)
            except Exception as e:
                print(f'❌ moxing download {pretrain_url_json[i]["model_url"]} to {modelfile_path} failed: {str(e)}')
                moxing_success = False
        else:
            try:
                mox.file.copy_parallel(pretrain_url_json[i]["model_url"], modelfile_path) 
                moxing_success = True
            except Exception as e:
                print(f'❌ moxing download {pretrain_url_json[i]["model_url"]} to {modelfile_path} failed: {str(e)}')
                moxing_success = True
        if moxing_success & unzip_success:
            print(f'✅ Successfully Prepare Pretrainmodel {os.path.splitext(pretrain_url_json[i]["model_name"])[0]}')
    return        

def obs_copy_file(obs_file_url, file_url):
    """
    cope file from obs to obs, or cope file from obs to env, or cope file from env to obs
    """
    try:
        mox.file.copy(obs_file_url, file_url)
        print(f'✅ Successfully Download {obs_file_url} to {file_url}')
    except Exception as e:
        print(f'❌ moxing download {obs_file_url} to {file_url} failed: {str(e)}')
    return    
    
def obs_copy_folder(folder_dir, obs_folder_url):
    """
    copy folder from obs to obs, or copy folder from obs to env, or copy folder from env to obs
    """
    try:
        mox.file.copy_parallel(folder_dir, obs_folder_url)
        print(f'✅ Successfully Download {folder_dir} to {obs_folder_url}')
    except Exception as e:
        print(f'❌ moxing download {folder_dir} to {obs_folder_url} failed: {str(e)}')
    return     

def upload_folder(folder_dir, obs_folder_url):
    """
    upload folder to obs
    """
    try:
        mox.file.copy_parallel(folder_dir, obs_folder_url)
        print(f'✅ Successfully Upload Output')
    except Exception as e:
        print(f'❌ moxing upload {folder_dir} to {obs_folder_url} failed: {str(e)}')
    return       