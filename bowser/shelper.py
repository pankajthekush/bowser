import os
import json
from pathlib import Path
import sys

current_path =Path.home()
#sys_platform = sys.platform
sys_platform = 'linux'

#if running inside linux ,do not create config file in home create from whereit is being
#executed,this is for docker support

def create_db_file():
    d_list = ['dbname','user','host','password','ApplicationName']
    jobj = None

    if sys_platform == 'linux':
        config_file_path = 'dbdata.json'
    else:
        config_file_path = os.path.join(current_path,'dbdata.json')

    if os.path.exists(config_file_path):
        with open(config_file_path,'r',encoding='utf-8') as f:
            jobj = json.load(f)
            all_keys = jobj.keys()
            for element in d_list:
                if not element in all_keys:
                    jobj[element] = input(f'enter value for {element} :')

        #put the new data in config file
        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(jobj,fp)
        return jobj
    else:
        #if file does not exists
        jobj = dict()
        all_keys = jobj.keys()
        for element in d_list:
            if not element in all_keys:
                jobj[element] = input(f'enter value for {element} :')
        with open(config_file_path,'w',encoding='utf-8') as fp:       
            json.dump(jobj,fp)
        return jobj

create_db_file()



def config_file():
    d_list = ['num_instances','notify_email','recycle_proxy','min_load','max_load','list_country_flags']

    jobj = None
    if sys_platform =='linux':
        config_file_path = 'config.json'
    else:
        config_file_path = os.path.join(Path.home(),'config.json')
    
    if os.path.exists(config_file_path):
        with open(config_file_path,'r',encoding='utf-8') as f:
            jobj = json.load(f)
            all_keys = jobj.keys()
            for element in d_list:
                if not element in all_keys:
                    if 'list' in element:
                        #if list is expected
                        jobj[element] = input(f'list for {element} :' ).split(',')
                    else:
                        jobj[element] = input(f'enter value for {element} :')

        #put the new data in config file
        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(jobj,fp)
        return jobj
    else:
        jobj = dict()
        all_keys = jobj.keys()
        for element in d_list:
            if not element in all_keys:
                if 'list' in element:
                        #if list is expected
                        jobj[element] = input(f'list for {element} :' ).split(',')
                else:
                    jobj[element] = input(f'enter value for {element} :')
        with open(config_file_path,'w',encoding='utf-8') as fp:
            json.dump(jobj,fp)
        return jobj


def pgconnstring():
    if sys_platform == 'linux':
        dbdata_file = 'dbdata.json'
    else:
        dbdata_file = os.path.join(current_path,'dbdata.json')

    connstring = None

    with open(dbdata_file,'r',encoding='utf-8') as f:
        jobj = json.load(f)
        user = jobj['user']
        password = jobj['password']
        host = jobj['host']
        dbname = jobj['dbname']
        connstring = f'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'
    return connstring
