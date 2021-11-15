#this script is for running all scripts in one script and manage the process of data pipeline
import os
import sys
import json
from . import TCP_insta_parser_12
from . import insta_model
def Create():
    home_address=os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(home_address,'config_parameters.json'),'r') as file_:
        config_parameters=json.loads(file_.read())

    has_train=config_parameters['main']['has_train']
    has_test=config_parameters['main']['has_test']

    change_train_data=config_parameters['main']['change_train_data']
    change_test_data=config_parameters['main']['change_test_data']
    train_data_folder=config_parameters['main']['train_data_folder']
    try:
        test_data_folder=sys.argv[1]
    except:
        test_data_folder=config_parameters['main']['test_data_folder']

    if change_train_data:
            
        csvname_out_all=TCP_insta_parser_12.session_split_function(train_data_folder,"train")
        with open(os.path.join(home_address,"TCP_parser_train.txt"), 'w') as file_to_write:
            print(csvname_out_all,file=file_to_write)
        # #session splitter on test data
    if change_test_data:
        csvname_out_all=TCP_insta_parser_12.session_split_function(test_data_folder,"test")
        with open(os.path.join(home_address,"TCP_parser_test.txt"), 'w') as file_to_write:
            print(csvname_out_all,file=file_to_write)



    read_last_train_files_splitted=config_parameters['main']['read_last_train_files_splitted']
    read_last_test_files_splitted=config_parameters['main']['read_last_test_files_splitted']

    manual_train_data_csv=config_parameters['main']['manual_train_data_csv']
    manual_test_data_csv=config_parameters['main']['manual_test_data_csv']

    if read_last_train_files_splitted:
        with open(os.path.join(home_address,"TCP_parser_train.txt"), 'r') as file_to_read:
            train_data_file_name=str(file_to_read.readline())[:-1]
    else:
        train_data_file_name=manual_train_data_csv

    if read_last_test_files_splitted:
        with open(os.path.join(home_address,"TCP_parser_test.txt"), 'r') as file_to_read:#110 tayii
            test_data_file_name=str(file_to_read.readline())[:-1]
    else:
        test_data_file_name=manual_test_data_csv


    if os.name=="posix":
        python_command="python3 "
    elif os.name=="nt":
        python_command="python "


        # #training Tree models for classification of profiles and training Tree model for classification of Known and Unknown
    if has_train:
            #os.system(python_command+os.path.join(home_address,"insta_model.py")+" "+train_data_file_name+" "+test_data_file_name+" train")
        print('------------------',train_data_file_name)
        insta_model.model_train_exec(train_data_file_name)
            
        # #final test models, always we have test
    result = []
    if has_test:
        file_names,predicted=insta_model.model_test_exec(test_data_file_name)
        for index_temp in range(len(file_names)):
                # print(index_temp,file_names[index_temp],predicted[index_temp])
            result.append([index_temp,file_names[index_temp],predicted[index_temp]])
        return(result)

            





