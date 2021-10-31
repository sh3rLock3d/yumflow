import json
import sys
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib
import datetime
import pickle
import random
import joblib

import math
import time

import os
import statistics

import warnings
warnings.filterwarnings("ignore")


    



def save_obj(obj, address_ ):
    with open(address_, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(address_ ):
    with open(address_, 'rb') as f:
        return pickle.load(f)


def indices_sort_by_filename_time(file_name_):
    return list(np.argsort(file_name_))

def random_grid_to_max_iter(rg):
    output_=1
    for key_ in rg.keys():
        output_*=len(rg[key_])
    return output_


def split_by_knowing(X,y,file_list,servername_list,Known_list):
    X_Unknown=[]
    y_Unknown=[]
    file_list_Unknown=[]
    servername_list_Unknown=[]

    y_indices=list(range(len(y)))[::-1]
    for y_index in y_indices:
        y_element=y[y_index]
        if not (y_element in Known_list):
            X_Unknown.append(X[y_index])
            y_Unknown.append(y[y_index])
            file_list_Unknown.append(file_list[y_index])
            servername_list_Unknown.append(servername_list[y_index])
            del X[y_index]
            del y[y_index]
            del file_list[y_index]
            del servername_list[y_index]
    return X,y,file_list,servername_list,X_Unknown,y_Unknown,file_list_Unknown,servername_list_Unknown

def roundup(x,roundup_length_,train_offset_):
    if x==0:
        return 0
    x=x+train_offset_
    return int(math.ceil(x / roundup_length_)) * int(roundup_length_)

def round_decimal_list_dict(input_,decimal_digit_number):
    if type(input_)==list:
        output_=[]
        for input_element in input_:
            if type(input_element)==tuple:
                output_.append((input_element[0],round(input_element[1],decimal_digit_number)))
            elif type(input_element)==list:
                output_.append([input_element[0],round(input_element[1],decimal_digit_number)])
            else:
                output_.append(round(input_element,decimal_digit_number))
        return output_
    if type(input_)==dict:
        keys_=list(input_.keys())
        output_=dict()
        for key_index in keys_:
            output_[key_index]=round(input_[key_index],decimal_digit_number)
        return output_


def print_confusion_matrix(confusion_matrix_):
    number_digit_max=max(len(str(np.array(confusion_matrix_).max())),len(str(len(confusion_matrix_))))

    for row_number in range(len(confusion_matrix_)):
        row_=confusion_matrix_[row_number]
        first_row_address_string=" "
        row_to_print="["
        for column_number in range(len(row_)):
            cm_element=str(row_[column_number])
            cm_element=(number_digit_max-len(cm_element))*" "+cm_element
            row_to_print+=cm_element
            if row_number==0:
                column_number_string=str(column_number)
                column_number_string=(number_digit_max-len(column_number_string))*" "+column_number_string
                first_row_address_string+=column_number_string
            if column_number!=len(row_)-1:
                row_to_print+=", "
                if row_number==0:
                    first_row_address_string+=", "
        row_to_print+="] " + str(row_number)

        if row_number==0:
            print(first_row_address_string,file=file_log)
        print(row_to_print,file=file_log)


def delete_and_create_file(file_name_,has_train,train_bool):
    if has_train:
        if train_bool:
            file_=open(file_name_,'w')
            file_.close()
        else:
            pass
    else:
        if train_bool:
            pass
        else:
            file_=open(file_name_,'w')
            file_.close()
    file_=open(file_name_,'a')
    return file_

def histo_by_bins(vector_,bins_):
    list_histo=list()
    for element in bins_:
        bin_first_length=element[0]
        bin_last_length=element[1]
        list_histo.append(sum([1 for vector_element in vector_ if (bin_first_length<=vector_element and vector_element<bin_last_length)]))
    return list_histo
    


def histo_bins_from_numbers(min_length,histogram_bin_byte,histogram_bin_byte_end,max_jpg_byte,big_number,bin_overlap_coeff):
    first_=min_length
    last_=max_jpg_byte
    first_bin=histogram_bin_byte
    last_bin=histogram_bin_byte_end

    number_of_bins=int(float(last_-first_)/(float(first_bin+last_bin)/2.0)-1.0)
    bin_increase_step=int(float(last_bin-first_bin)/float(number_of_bins))

    
    bins_=[]
    bin_first_length=min_length
    bin_size=first_bin
    end_while_boolean=False
    while(not end_while_boolean):
        
        if bin_first_length>=max_jpg_byte:
            end_while_boolean=True
            bin_last_length=big_number
        else:
            bin_last_length=bin_first_length+bin_size


        bins_.append([bin_first_length,bin_last_length])
        
        bin_first_length+=(1-bin_overlap_coeff)*bin_size
        bin_size+=(1-bin_overlap_coeff)*bin_increase_step

    return bins_

def print_csv(file_name_,X_,y_,pcap_names,servernames=[]):

    if len(servernames)!=0:
        for index_sample in range(len(X_)):
            string_to_print=y_[index_sample]+"|"
            for index_data in range(len(X_[index_sample])):
                string_to_print+=str(X_[index_sample][index_data])+"|"
            try:
                string_to_print=string_to_print+pcap_names[index_sample]+"|"+servernames[index_sample]
            except:
                print('error! print csv')
                print(index_sample)
                print(servernames)
                print(pcap_names)
                input()
            print(string_to_print,file=file_name_)
    else:
        for index_sample in range(len(X_)):
            string_to_print=y_[index_sample]+"|"
            for index_data in range(len(X_[index_sample])):
                string_to_print+=str(X_[index_sample][index_data])+"|"
            string_to_print=string_to_print+pcap_names[index_sample]
            print(string_to_print,file=file_name_)


def list_from_dict(this_sample_bins_dict,data_character_label_dict):
    bins_total=list(this_sample_bins_dict.keys())
    
    bins_=list(data_character_label_dict.keys())
    bins_none=bins_total.copy()

    for element_ in bins_:
        if element_ in bins_none:
            bins_none.remove(element_)

    this_list=[]
    for this_bin_index in range(len(bins_total)):
        bin_key_=bins_total[this_bin_index]    
        
        this_list.extend(this_sample_bins_dict[bin_key_])
    
    this_list=sorted(this_list)

    train_list=[]
    for this_bin_index in range(len(bins_)):
        bin_key_=bins_[this_bin_index]    
        train_list.extend(data_character_label_dict[bin_key_])


    

    train_list=sorted(train_list)

    return this_list,train_list


def augment_vector(vector_,min_disappear_bin,max_disappear_bin,min_number_create,max_number_create,offset_list,bins_):
    
    bin_disappear_number=random.randint(min_disappear_bin,max_disappear_bin)

    dic_of_values_in_bins=bin_implement(vector_,bins_)

    list_disappear=list(range(len(bins_)))
    random.shuffle(list_disappear)
    list_disappear=list_disappear[:bin_disappear_number]
    

    for this_bin_index in list_disappear:
        
        bin_key_=get_key_bin(bins_[this_bin_index])

        dic_of_values_in_bins[bin_key_]=[]

    this_list,temp_list=list_from_dict(dic_of_values_in_bins,dict())
    
    create_number=random.randint(min_number_create,max_number_create)
    for num_create in range(create_number):
        temp_random=random.randint(min_length,max_jpg_byte)
        this_list.append(temp_random)

    this_list=sorted(this_list)

    offset_index=random.randint(0,len(offset_list)-1)

    this_list=[element_+offset_list[offset_index] for element_ in this_list]

    return this_list


def digit_number_function(number_):
    if number_==0:
        return 1
    else:
        return math.ceil(math.log10(number_+1))



def bin_implement(vector_,bins_):

    dic_of_values_in_bins=dict()
    for this_bin_index in range(len(bins_)):
        
        first_=bins_[this_bin_index][0]
        last_=bins_[this_bin_index][1]
        bin_key_=get_key_bin(bins_[this_bin_index])
        dic_of_values_in_bins[bin_key_]=[]

        for value_ in vector_:
            if first_<=value_ and value_<last_:
                dic_of_values_in_bins[bin_key_].append(value_)

    return dic_of_values_in_bins



def similarity(X, Y, r=0.1):

    X = np.array(sorted(X))
    Y = np.array(sorted(Y))
    result = 0
    if min(X.size, Y.size) <= 1:
        return 1000
    for i in range(min(X.size, Y.size) - 1):
        if (X[i] <= Y[i] and X[i + 1] <= Y[i + 1]) or (X[i] > Y[i] and X[i + 1] > Y[i + 1]):
            result += abs(X[i] - Y[i]) + abs(X[i + 1] - Y[i + 1])
        else:
            result += ((X[i] - Y[i]) ** 2 + (X[i + 1] - Y[i + 1]) ** 2) / (abs(X[i] - Y[i]) + abs(X[i + 1] - Y[i + 1]))

    return result


def distance_new2(this_list,train_list):
    return float(similarity(this_list,train_list))

def distance_function1(vector_1,vector_2):
    temp_=[vector_1[vector_index]-vector_2[vector_index] for vector_index in range(len(vector_1))]
    if norm_number>1:
        return ((sum([abs(temp_element)**norm_number for temp_element in temp_]))**(1/norm_number))
    elif norm_number==1:
        return (float(sum([abs(temp_element) for temp_element in temp_]))/float(len(temp_)))

def distance_new(this_sample_bins_dict,data_character_label_dict):

    distance_value=0.0

    bins_total=list(this_sample_bins_dict.keys())
    
    bins_=list(data_character_label_dict.keys())
    bins_none=bins_total.copy()


    for element_ in bins_:
        if element_ in bins_none:
            bins_none.remove(element_)


    test_list,train_list=list_from_dict(this_sample_bins_dict,data_character_label_dict)


    if len(test_list)<=config_parameters['model_train']['thr_min_pic']:
        return config_parameters['model_train']['thr_distance_unknown']+0.1
    

    decay_number=1.4

    if len(test_list)>len(train_list):
        
        
        decay_number*=(float(len(test_list))/float(len(train_list))+1.0)/2.0
        
    else:
        decay_number*=1.0


    decay_number_without_train=0.7*decay_number#0.0 or 1.0


    for this_bin_index in range(len(bins_)):
        bin_key_=bins_[this_bin_index]
        this_sample_bins_dict[bin_key_]
        
        if len(this_sample_bins_dict[bin_key_])==0 and len(data_character_label_dict[bin_key_])==0 :
            distance_value+=0.0

        if len(this_sample_bins_dict[bin_key_])==0 and len(data_character_label_dict[bin_key_])!=0 :
            distance_value+=float(len(data_character_label_dict[bin_key_]))

        if len(this_sample_bins_dict[bin_key_])!=0 and len(data_character_label_dict[bin_key_])==0 :
            
            
            if len(this_sample_bins_dict[bin_key_])==1:
                distance_value+=float(len(this_sample_bins_dict[bin_key_]))*0.9*decay_number_without_train
            else:
                distance_value+=float(len(this_sample_bins_dict[bin_key_]))*1.2*decay_number_without_train

        if len(this_sample_bins_dict[bin_key_])!=0 and len(data_character_label_dict[bin_key_])!=0 :

            
            delta_distance=float(len(this_sample_bins_dict[bin_key_])-len(data_character_label_dict[bin_key_]))
            if delta_distance==0.0:
                pass
            elif delta_distance>0.0:
                if delta_distance<=1.0:
                    delta_distance=0.0
                else:
                    pass

            else:
                delta_distance=abs(delta_distance)
                delta_distance/=float(len(this_sample_bins_dict[bin_key_]))
            
            

            distance_value+=delta_distance*decay_number
            




    

    for this_bin_index in range(len(bins_none)):
        bin_key_=bins_none[this_bin_index]
        
        

        if len(this_sample_bins_dict[bin_key_])==0:
            distance_value+=0.0

        
        if len(this_sample_bins_dict[bin_key_])!=0:
            if len(this_sample_bins_dict[bin_key_])==1:
                distance_value+=float(len(this_sample_bins_dict[bin_key_]))*0.7*decay_number_without_train
            else:
                distance_value+=float(len(this_sample_bins_dict[bin_key_]))*1.0*decay_number_without_train

            # distance_value+=0.0
            # distance_value+=float(len(this_sample_bins_dict[bin_key_]))

    # distance_value/=float(len(test_list))
    
    return distance_value/float(len(bins_total))



def distance_new3(this_sample_bins_dict,data_character_label_dict,coeffecient_importance_distance_y_element):
    #TUNING
    distance_value=0.0

    bins_total=list(this_sample_bins_dict.keys())
    
    bins_=list(data_character_label_dict.keys())
    bins_none=bins_total.copy()

    

    for element_ in bins_:
        if element_ in bins_none:
            bins_none.remove(element_)


    test_list,train_list=list_from_dict(this_sample_bins_dict,data_character_label_dict)

    total_len_dict=0.0
    
    sum_coeff=0.0
    for this_bin_index in range(len(bins_)):
        bin_key_=bins_[this_bin_index]
        len_dict=0.0
        for element_ in data_character_label_dict[bin_key_].keys():
            len_dict+=float(data_character_label_dict[bin_key_][element_])

        

        len_dict=float(math.ceil(len_dict-config_parameters['model_train']['value_thr']/2.0))
        total_len_dict+=len_dict

        delta_distance=float(len(this_sample_bins_dict[bin_key_]))-len_dict
        
        

        if len(this_sample_bins_dict[bin_key_])==0 and len(data_character_label_dict[bin_key_])==0 :
            delta_distance_coef=1.0
        
        if len(this_sample_bins_dict[bin_key_])==0 and len(data_character_label_dict[bin_key_])!=0 :
            

            if config_parameters['model_train']['all_coeff_one']:
                delta_distance_coef=1.0
            else:
                if len(data_character_label_dict[bin_key_])==1:
                    delta_distance_coef=1.3
                else:
                    delta_distance_coef=1.8
        if len(this_sample_bins_dict[bin_key_])!=0 and len(data_character_label_dict[bin_key_])==0 :
            
            if config_parameters['model_train']['all_coeff_one']:
                delta_distance_coef=1.0
            else:
                if len(this_sample_bins_dict[bin_key_])==1:
                    delta_distance_coef=1.0
                else:
                    delta_distance_coef=1.6
            
        if len(this_sample_bins_dict[bin_key_])!=0 and len(data_character_label_dict[bin_key_])!=0 :
            if config_parameters['model_train']['all_coeff_one']:
                delta_distance_coef=1.0
            else:
                if delta_distance==0.0:
                    delta_distance_coef=0.0
                elif delta_distance>0.0:
                    if delta_distance<=1.2:
                        delta_distance_coef=0.0
                    else:
                        delta_distance_coef=1.0/float(len(this_sample_bins_dict[bin_key_]))
                else:
                    if -1.2<=delta_distance:
                        delta_distance_coef=0.0
                    else:
                        delta_distance_coef=1.0/float(len(this_sample_bins_dict[bin_key_]))
                    


        delta_distance=abs(delta_distance)
        distance_value+=delta_distance_coef*delta_distance*coeffecient_importance_distance_y_element[bin_key_]
        sum_coeff+=coeffecient_importance_distance_y_element[bin_key_]
    
    for this_bin_index in range(len(bins_none)):
        bin_key_=bins_none[this_bin_index]
        
        
        
        delta_distance=abs(float(len(this_sample_bins_dict[bin_key_])))
        if config_parameters['model_train']['all_coeff_one']:
            delta_distance_coef=1.0
        else:
            delta_distance_coef=float(config_parameters['model_train']['first_importance_of_columns'])
            if len(this_sample_bins_dict[bin_key_])==0:
                delta_distance_coef*=1.0    
            if len(this_sample_bins_dict[bin_key_])!=0:
                if len(this_sample_bins_dict[bin_key_])==1:
                    delta_distance_coef*=1.0
                else:
                    delta_distance_coef*=2.0


        
        distance_value+=delta_distance_coef*delta_distance
        sum_coeff+=float(config_parameters['model_train']['first_importance_of_columns'])


    if len(test_list)<=config_parameters['model_train']['thr_min_pic']:
        return config_parameters['model_train']['thr_distance_unknown']+0.1

    
    if config_parameters['model_train']['all_coeff_one']:
        return distance_value/float(len(bins_))
    else:
        return distance_value/float(sum_coeff)


def plot_bar_of_binns(vector_,color_,mean_vector_,y_0,y_1,bar_title,fig_title,fig_address):
    fig=plt.figure(fig_title)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim([y_0,y_1])
    try:
        ax.set_title(bar_title)
    except:
        pass
    if len(mean_vector_)!=0:
        plt.bar(list(range(len(mean_vector_))),mean_vector_,color="red",alpha=1)  # density=False would make counts
    
    if len(vector_)!=0:
        plt.bar(list(range(len(vector_))),vector_,color=color_,alpha=0.5)  # density=False would make counts

    plt.ylabel('number')
    plt.xlabel('byte bin')
    plt.savefig(fig_address,DPI=plot_dpi)
    del fig
    plt.close()


def get_key_bin(first_last_list):
    return str(first_last_list[0])+"_"+str(first_last_list[1])

def model_train_exec(sysargv1):
    print("train exec")
    #### initialization
    global home_address
    home_address=os.path.dirname(os.path.realpath(__file__))
    
    ### read cli train and test files
    
    base_name_data=sysargv1
    

    ### read and pass config parameters
    global config_parameters
    with open(os.path.join(home_address,'config_parameters.json'),'r') as file_:
        config_parameters=json.loads(file_.read())

    

    ### make zero output folder
    output_folder0=os.path.join(home_address,config_parameters['main']['output_folder'])
    
    #make train or test folder
    output_folder=os.path.join(output_folder0,"train")
    
    ##make directories
    try: os.mkdir(output_folder0)
    except: pass
    try: os.mkdir(output_folder)
    except: pass
    # try: os.mkdir(os.path.join(output_folder,"pngs"))
    # except: pass
    # try: os.mkdir(os.path.join(output_folder,"pngs_after"))
    # except: pass
    
    ###make file log
    log_file_name=os.path.join(output_folder,'train.log')
    global file_log
    
    file_log=delete_and_create_file(log_file_name,config_parameters['main']['has_train'],True)
    
    

    
    try: Known_list=config_parameters['model_train']['Known_list']
    except: Known_list=['all']
    
    
    verbose_number=config_parameters['model_train']['verbose_']
    thr_min_pic=config_parameters['model_train']['thr_min_pic']


    histogram_bin_byte=config_parameters['model_train']['histogram_bin_byte']
    histogram_bin_byte_end=config_parameters['model_train']['histogram_bin_byte_end']

    bin_optimization_bool=config_parameters['model_train']['bin_optimization_bool']
    bin_overlap_coeff=config_parameters['model_train']['bin_overlap_coeff']#must be a division number for max_jpg_byte #for example 250,420,600,900,1000,1260,1500,1800,2250,2800,3150,3600,4500,6300,8400,10500,15000,18000


    roundup_bool=True

    sort_bool=config_parameters['model_train']['sort_bool']
    high_to_low_sort_bool=config_parameters['model_train']['high_to_low_sort_bool']

    

    roundup_length=config_parameters['model_train']['roundup_length']#roundup
    train_offset=config_parameters['model_train']['train_offset']

    max_jpg_byte=config_parameters['model_train']['max_jpg_byte'] # must be divisional by bin_byte #80000

    big_number=config_parameters['model_train']['big_number'] # must be divisional by bin_byte #80000

    categ_threshold=0


    delete_badnumber_bool=False
    min_length=config_parameters['model_train']['min_length'] #-1

    bad_numbers=[]
    
    add_unknown_of_train_to_test=True
    
    #delete_past_unknown_labels_of_test_data_that_were_unknown_in_training_data_of_probability #BECAUSE IN TRAINING OF KNOWN MODEL HAVE BEEN USED; it is for last tree model and now has been expired to be True
    
    delete_train_unknown_labels_from_test_data=False
    
    SAVE_MODEL_BOOL=True
    LOAD_MODEL_BOOL=False

    base_name_data_test=base_name_data        
    test_coeffecient=config_parameters['model_train']['test_coeffecient']




#### loading data train and test
    training_data = pd.read_csv(os.path.join(home_address,base_name_data+'.csv'),delimiter='|',header=0)
    X_train=training_data.loc[:, (training_data.columns!='label') & (training_data.columns!='filename') & (training_data.columns!='server_name')].values.tolist()
    y_train=training_data['label'].tolist()
    list_filename_train=training_data['filename'].tolist()
    list_servername_train=training_data['server_name'].tolist()

    all_Known_list=sorted(list(set(y_train)))

    test_data = pd.read_csv(os.path.join(home_address,base_name_data_test+'.csv'),delimiter='|',header=0)
    X_test=test_data.loc[:, (test_data.columns!='label') & (test_data.columns!='filename') & (test_data.columns!='server_name')].values.tolist()
    y_test=test_data['label'].tolist()
    list_filename_test=test_data['filename'].tolist()
    list_servername_test=test_data['server_name'].tolist()



#### known data and unknown data initialization
    
    #### check status of known list
        
    # print("KNOWN_ALL:",all_Known_list,file=file_log)
    if len(Known_list)>2:
        pass
    elif len(Known_list)==1 and Known_list[0]=='all':
        Known_list=all_Known_list
    else:
        Known_list=all_Known_list

    ### main function to split into known and unknown
    X_train,y_train,list_filename_train,list_servername_train,X_Unknown,y_Unknown,file_list_Unknown,list_servername_Unknown = split_by_knowing(X_train,y_train,list_filename_train,list_servername_train,Known_list)

    ### delete_train_unknown_labels_from_test_data , its always false. it was True in the past model of insta that we train e secon model for detecting unknown from confidency
    if delete_train_unknown_labels_from_test_data:
        Known_list_2=list(set(y_test) - (set(all_Known_list)-set(Known_list)))
        print(Known_list_2)
        Known_list_2=sorted(Known_list_2)
        X_test,y_test,list_filename_test,list_servername_test,X_test_temp_Unknown,y_test_temp_Unknown,file_list_test_temp_Unknown,servername_list_test_temp_Unknown = split_by_knowing(X_test,y_test,list_filename_test,list_servername_test,Known_list_2)

    #adding deleted unknown data from train into test data
    if add_unknown_of_train_to_test: # as unknown tests
        X_test=X_test+X_Unknown
        y_test=y_test+y_Unknown
        list_filename_test=list_filename_test+file_list_Unknown
        list_servername_test=list_servername_test+list_servername_Unknown




#### generate a mapping of dictionary from filename to its label (train)
    dict_filename_to_label=dict()
    for j in range(len(X_train)):
        dict_filename_to_label[list_filename_train[j]]=y_train[j]

#### some general preprocessing like sort, delete badnumber and roundup and ...

    #### at this part of code we delete bad picture numbers. every number must be bigger than min_approved_length and not be in list of bad numbers
    if delete_badnumber_bool:
        for i in range(len(X_train)):
            temp=[]
            for j in X_train[i]:
                if (not(j in bad_numbers)) and j > min_length:
                    temp.append(j)
                else:
                    temp.append(0)
            X_train[i]=temp
        for i in range(len(X_test)):
            temp=[]
            for j in X_test[i]:
                if (not(j in bad_numbers)) and j>min_length:
                    temp.append(j)
                else:
                    temp.append(0)
            X_test[i]=temp

    roundup_length_equal=config_parameters['model_train']['roundup_length_equal']
    #### at this part we sort data of each sample (sort length of pictures), at this time we delete equal number that repeated(roundup for offset of equity)
    if sort_bool:
        for i in range(len(X_train)):
            temp=X_train[i].copy()
            temp=sorted(list(set([roundup(x,roundup_length_equal,0) for x in temp if x!=0])),reverse=high_to_low_sort_bool)
            X_train[i]=temp+(len(X_train[i])-len(temp))*[0]
            if not high_to_low_sort_bool:
                x_temp=[x for x in X_train[i] if x!=0]
                x_temp=x_temp+(len(X_train[i])-len(x_temp))*[0]
                X_train[i]=x_temp

        for i in range(len(X_test)):
            temp=X_test[i].copy()
            temp=sorted(list(set([roundup(x,roundup_length_equal,0) for x in temp if x!=0])),reverse=high_to_low_sort_bool)
            X_test[i]=temp+(len(X_test[i])-len(temp))*[0]

            if not high_to_low_sort_bool:
                x_temp=[x for x in X_test[i] if x!=0]
                x_temp=x_temp+(len(X_test[i])-len(x_temp))*[0]
                X_test[i]=x_temp

    #### round begin with train offset for train data and without offset for test data
    if roundup_bool:
        for i in range(len(X_train)):
            temp=X_train[i].copy()
            X_train[i]=[roundup(j,roundup_length,train_offset) for j in temp]
        for i in range(len(X_test)):
            temp=X_test[i].copy()
            X_test[i]=[roundup(j,roundup_length,0) for j in temp]

    bad_numbers_2=[0]


#### get backup from general preprocessed data to use if neces
    X_train_backup=X_train
    y_train_backup=y_train
    list_filename_train_backup=list_filename_train
    list_servername_train_backup=list_servername_train

#### calculate all label lists
    labels_train=sorted(list(set(y_train)))
    labels_test=sorted(list(set(y_test)))

    all_labels=set(y_train)
    all_labels.update(set(y_test))
    all_labels=sorted(list(all_labels))

#### binning start here
    bins_total=histo_bins_from_numbers(min_length,histogram_bin_byte,histogram_bin_byte_end,max_jpg_byte,big_number,bin_overlap_coeff)
    bins_total=bins_total[:-1]

    bins_=bins_total.copy()


    X_train_all_sorted=[]
    y_train_all_sorted=[]
    list_filename_train_all_sorted=[]
    list_servername_train_all_sorted=[]

    X_test_all_sorted=[]
    y_test_all_sorted=[]
    list_filename_test_all_sorted=[]
    list_servername_test_all_sorted=[]


    total_bins_dict=dict()
    #### bins_ is a list of tuples(2 length list) that first number is beginning of a bin and the last number is the end of the bin
    #### binkey is a string for beeing key of dictionaries that is a string wiht style like this "1200_1400"
    #bin:[1200,1400]  ===>  binkey:"1200_1400"
    max_value_number_per_bin=dict()
    for this_bin_index in range(len(bins_)):
        
        bin_key_=get_key_bin(bins_[this_bin_index])
        
        max_value_number_per_bin[bin_key_]=0

#### label by label 
    for y_element in all_labels:
        
        #### select one label from train

        this_label_indices=[y_train_index for y_train_index in range(len(y_train)) if y_train[y_train_index]==y_element]
        X_train_this_label=[X_train[i] for i in this_label_indices]
        y_train_this_label=[y_train[i] for i in this_label_indices]
        file_name_train_this_label=[list_filename_train[i] for i in this_label_indices]
        servername_train_this_label=[list_servername_train[i] for i in this_label_indices]


        #### sort train by filename date
        temp_indices=indices_sort_by_filename_time(file_name_train_this_label)

        X_train_this_label=[X_train_this_label[i] for i in temp_indices]
        y_train_this_label=[y_train_this_label[i] for i in temp_indices]
        file_name_train_this_label=[file_name_train_this_label[i] for i in temp_indices]
        servername_train_this_label=[list_servername_train[i] for i in temp_indices]


        #### (train)merge labels into each other for get all that labels are behind to each other after another in one file to be print on
        X_train_all_sorted.extend(X_train_this_label)
        y_train_all_sorted.extend(y_train_this_label)
        list_filename_train_all_sorted.extend(file_name_train_this_label)
        list_servername_train_all_sorted.extend(servername_train_this_label)
        
        #### select one label from test
        this_label_indices=[y_test_index for y_test_index in range(len(y_test)) if y_test[y_test_index]==y_element]
        X_test_this_label=[X_test[i] for i in this_label_indices]
        y_test_this_label=[y_test[i] for i in this_label_indices]
        file_name_test_this_label=[list_filename_test[i] for i in this_label_indices]
        servername_test_this_label=[list_servername_test[i] for i in this_label_indices]

        #### sort test by filename date
        temp_indices=indices_sort_by_filename_time(file_name_test_this_label)

        X_test_this_label=[X_test_this_label[i] for i in temp_indices]
        y_test_this_label=[y_test_this_label[i] for i in temp_indices]
        file_name_test_this_label=[file_name_test_this_label[i] for i in temp_indices]
        servername_test_this_label=[list_servername_test[i] for i in temp_indices]

        

        #### (test)merge labels into each other for get all that labels are behind to each other after another in one file to be print on
        X_test_all_sorted.extend(X_test_this_label)
        y_test_all_sorted.extend(y_test_this_label)
        list_filename_test_all_sorted.extend(file_name_test_this_label)
        list_servername_test_all_sorted.extend(servername_test_this_label)

        ############ now we generate a dict for train and test , for every file
        total_bins_dict[y_element]=dict()

        total_bins_dict[y_element]["train"]=dict()#list_of_bin_dics
        total_bins_dict[y_element]["test"]=dict()#list_of_bin_dics

        #### DICT has this structure:  total_bins_dict[label]["train" or "test"][filename][bin_string_name like "1220_1320"] : its a list ultimately
        #### DICT has this structure:  total_bins_dict[label]["train" or "test"][filename][server name(sni)] : its servername string of the file

        #### generate each bin for every train sample for deploy in the dictionary (train)
        for index_train in range(len(X_train_this_label)):
                
            this_sample=X_train_this_label[index_train]
            this_pcap_name=file_name_train_this_label[index_train]
            this_servername=servername_train_this_label[index_train]



            
            #### (train) the main function for binning one sample 
            dic_of_values_in_bins=bin_implement(this_sample,bins_)
            ### (train) set sni
            dic_of_values_in_bins['servername']=this_servername


            #### (print_visualization) (train) for printing we need to correct characters to be very nice below each other in csv that we want to print in it. in this line we consider max bin numbers that are in it                 
            if max_value_number_per_bin[bin_key_]<len(dic_of_values_in_bins[bin_key_]):
                max_value_number_per_bin[bin_key_]=len(dic_of_values_in_bins[bin_key_])

            ## (train)copy the final output of function that is one dic itself into leaves of general dict, and it copied cause if dictionary changed after it , not change total dictionary
            
            total_bins_dict[y_element]["train"][this_pcap_name]=dic_of_values_in_bins.copy()
            
        
        #### generate each bin for every train sample for deploy in the dictionary (test)
        for index_test in range(len(X_test_this_label)):
            
            this_sample=X_test_this_label[index_test]
            this_pcap_name=file_name_test_this_label[index_test]


            this_servername=servername_test_this_label[index_test]
            
            
            #### (test) the main function for binning one sample 
            dic_of_values_in_bins=bin_implement(this_sample,bins_)
            ### (test) set sni
            dic_of_values_in_bins['servername']=this_servername

            ## (test)copy the final output of function that is one dic itself into leaves of general dict, and it copied cause if dictionary changed after it , not change total dictionary
            total_bins_dict[y_element]["test"][this_pcap_name]=dic_of_values_in_bins.copy()


    #### in printing of bins im csv , every bin has max number per it to print(0 or non zero value) that we save in one dictionaty and we plus it with one min parameter that mentioned ind config file
    #bin:[1200,1400]  ===>  binkey:"1200_1400"
    for this_bin_index in range(len(bins_)):

        bin_key_=get_key_bin(bins_[this_bin_index])
        max_value_number_per_bin[bin_key_]=max_value_number_per_bin[bin_key_]+config_parameters['model_train']['number_min_every_bin']
               
    
    #### (print_visualization) for print pretty we should use max of number to calculate max digits of numbers
    max_number_list=[max(temp_element) for temp_element in X_test_all_sorted]
    max_number_list+=[max(temp_element) for temp_element in X_train_all_sorted]
    max_number=max(max_number_list)
    max_digits=digit_number_function(max_number)
   
    
    ####(print_visualization)every bin has a max character number
    max_chars_of_bins=dict()
   
    #### (print_visualization) move on the general bin dfictionary that explanated before , to print pretty for visualization
    #### bins_pcs_train_test_raw.csv
    file_bins_pcs_train_test_raw=delete_and_create_file(os.path.join(output_folder,"bins_pcs_train_test_raw.csv"),config_parameters['main']['has_train'],True)
    headers_=""
    train_test_delimiter=""
    label_delimiter=""
    for y_element in all_labels:

        #### (print_visualization)calculate some parameters for pretty printing 
        for mode_tt in ["train","test"]:
        
            for pcap_name_ in total_bins_dict[y_element][mode_tt].keys():
                
                for this_bin_index in range(len(bins_)):
                    bin_key_=get_key_bin(bins_[this_bin_index])
                    left_zeros=0
                    right_zeros=max_value_number_per_bin[bin_key_]-len(total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_])
                    total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_]=[0]*left_zeros+total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_]+[0]*right_zeros
                    max_chars_of_bins[bin_key_]=max_digits*max_value_number_per_bin[bin_key_]+max_value_number_per_bin[bin_key_]-1
                    max_chars_of_bins[bin_key_]=max([max_chars_of_bins[bin_key_],len(bin_key_)])

                    
        #### (print_visualization)making every row:     
        if y_element==all_labels[0]:
            for this_bin_index in range(len(bins_)):
                bin_key_=get_key_bin(bins_[this_bin_index])
                
                this_label_delimiter="."*max_chars_of_bins[bin_key_]
                
                this_header=bin_key_+" "*(max_chars_of_bins[bin_key_]-len(bin_key_))
                
                if this_bin_index!=0:
                    label_delimiter+="|"
                    
                    headers_+="|"
                label_delimiter+=this_label_delimiter
                headers_+=this_header
            
            headers_+="|file_name|servername"
        #### (print_visualization) printing headers
        print(label_delimiter,file=file_bins_pcs_train_test_raw)
        print(label_delimiter,file=file_bins_pcs_train_test_raw)
        print(label_delimiter,file=file_bins_pcs_train_test_raw)
        print(((y_element+"|")*(len(bins_)+1))[:-1],file=file_bins_pcs_train_test_raw)
        print(headers_,file=file_bins_pcs_train_test_raw)
        #### (print_visualization) row generate and ultimate print every row,bins and label an sni and pcap name
        for mode_tt in ["train","test"]:
        
            for pcap_name_ in total_bins_dict[y_element][mode_tt].keys():
                row_=""
                for this_bin_index in range(len(bins_)):
                    bin_key_=get_key_bin(bins_[this_bin_index])

                    this_bin_str=""

                    for value_index in range(len(total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_])):

                        value_=total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_][value_index]
                        if value_index!=0:
                            this_bin_str+=','
                        digit_number_function(value_)
                        this_bin_str+=(max_digits-digit_number_function(value_))*" "+str(value_)
                    if this_bin_index!=0:
                        row_+="|"
                    row_+=this_bin_str
                row_+="|"+pcap_name_+"|"+total_bins_dict[y_element][mode_tt][pcap_name_]['servername']
                print(row_,file=file_bins_pcs_train_test_raw)
            
            if mode_tt=="train":
                print(train_test_delimiter,file=file_bins_pcs_train_test_raw)
                
                
    ####(print_visualization) print  labels and samples of train and test data normally under each other
    #### pics_train_raw.csv
    #### pics_test_raw.csv
                
    file_histo_train=delete_and_create_file(os.path.join(output_folder,"pics_train_raw.csv"),config_parameters['main']['has_train'],True)
    print_csv(file_histo_train,X_train_all_sorted,y_train_all_sorted,list_filename_train_all_sorted,list_servername_train_all_sorted)

    file_histo_test=delete_and_create_file(os.path.join(output_folder,"pics_test_raw.csv"),config_parameters['main']['has_train'],True)
    print_csv(file_histo_test,X_test_all_sorted,y_test_all_sorted,list_filename_test_all_sorted,list_servername_test_all_sorted)




    #### delete noise of train data in bin general dictionary. delete pictures that are not repeated high frequently and delete bins that are not important

    if bin_optimization_bool:

        bins_freq=[0]*len(bins_)                

        thr_bin=config_parameters['model_train']['thr_bin']
        #### moving in dictionary in all keys
        for y_element in all_labels:

            this_label_pcaps_list=total_bins_dict[y_element]["train"].keys()

            for this_bin_index in range(len(bins_)):
                bin_key_=get_key_bin(bins_[this_bin_index])

                this_bin_proba_for_values=0.0
                for pcap_name_ in this_label_pcaps_list:
                    
                    list_of_values_of_bin=[element_ for element_ in total_bins_dict[y_element]["train"][pcap_name_][bin_key_] if element_!=0]

                    if len(list_of_values_of_bin)>0:
                        this_bin_proba_for_values+=1.0
                
                if len(this_label_pcaps_list)!=0:
                    this_bin_proba_for_values/=float(len(this_label_pcaps_list))

                if this_bin_proba_for_values>thr_bin:
                    bins_freq[this_bin_index]=1
                else:
                    for pcap_name_ in this_label_pcaps_list:
                        total_bins_dict[y_element]["train"][pcap_name_][bin_key_]=[0 for element_ in total_bins_dict[y_element]["train"][pcap_name_][bin_key_]]


        #### set indices to be removed
        bin_remove_indices=[]
        for this_bin_index in range(len(bins_)):
            bin_key_=get_key_bin(bins_[this_bin_index])
            if bins_freq[this_bin_index]==0:
                bin_remove_indices.append(this_bin_index)
            

        bin_remove_indices=bin_remove_indices[::-1]
        
        #### remove bad indices
        
        for this_bin_index in bin_remove_indices:
            bin_key_=get_key_bin(bins_[this_bin_index])
            
            del bins_[this_bin_index]

            for y_element in all_labels:
                for mode_tt in ["train","test"]:
                    for pcap_name_ in total_bins_dict[y_element][mode_tt].keys():
                        # input(pcap_name_)            
                        del total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_]

        #### (print_visualisation) print the new general corrected dictionary of bins exactly like previous
        #### print corrected bins in bins_pcs_train_test_raw_2.csv
        headers_=""
        train_test_delimiter=""
        label_delimiter=""
        file_bins_pcs_train_test_raw=delete_and_create_file(os.path.join(output_folder,"bins_pcs_train_test_raw_2.csv"),config_parameters['main']['has_train'],True)

        for y_element in all_labels:
            for mode_tt in ["train","test"]:
                                
                for pcap_name_ in total_bins_dict[y_element][mode_tt].keys():

                    for this_bin_index in range(len(bins_)):
                        
                        first_=bins_[this_bin_index][0]
                        last_=bins_[this_bin_index][1]
                        bin_key_=get_key_bin(bins_[this_bin_index])

                        

                        max_chars_of_bins[bin_key_]=max_digits*max_value_number_per_bin[bin_key_]+max_value_number_per_bin[bin_key_]-1
                        max_chars_of_bins[bin_key_]=max([max_chars_of_bins[bin_key_],len(bin_key_)])

                        
                        
            if y_element==all_labels[0]:
                for this_bin_index in range(len(bins_)):
                    bin_key_=get_key_bin(bins_[this_bin_index])
                    
                    this_label_delimiter="."*max_chars_of_bins[bin_key_]
                    
                    this_header=bin_key_+" "*(max_chars_of_bins[bin_key_]-len(bin_key_))
                    
                    if this_bin_index!=0:
                        label_delimiter+="|"
                        
                        headers_+="|"
                    label_delimiter+=this_label_delimiter
                    headers_+=this_header
                
                headers_+="|file_name|servername"
            
            print(label_delimiter,file=file_bins_pcs_train_test_raw)
            print(label_delimiter,file=file_bins_pcs_train_test_raw)
            print(label_delimiter,file=file_bins_pcs_train_test_raw)
            print(((y_element+"|")*(len(bins_)+1))[:-1],file=file_bins_pcs_train_test_raw)
            print(headers_,file=file_bins_pcs_train_test_raw)
            for mode_tt in ["train","test"]:
            
                for pcap_name_ in total_bins_dict[y_element][mode_tt].keys():
                    row_=""
                    for this_bin_index in range(len(bins_)):
                        bin_key_=get_key_bin(bins_[this_bin_index])

                        this_bin_str=""

                        for value_index in range(len(total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_])):

                            value_=total_bins_dict[y_element][mode_tt][pcap_name_][bin_key_][value_index]
                            if value_index!=0:
                                this_bin_str+=','
                            digit_number_function(value_)
                            this_bin_str+=(max_digits-digit_number_function(value_))*" "+str(value_)
                        if this_bin_index!=0:
                            row_+="|"
                        row_+=this_bin_str
                    row_+="|"+pcap_name_+"|"+total_bins_dict[y_element][mode_tt][pcap_name_]['servername']
                    print(row_,file=file_bins_pcs_train_test_raw)
                
                if mode_tt=="train":
                    print(train_test_delimiter,file=file_bins_pcs_train_test_raw)

        #### (generate and print_visualization  both) concrete data characteristic
        #### dar inja dadeye charachterisitc kholase ro ke frequency tekrare tool ha dar aan ast ra ke dar
        #### data_character[y_element] misazim az rooye dade train va haminja chappesh mikonim
        if config_parameters['model_train']['carachteristic_model']:

            file_character_train=delete_and_create_file(os.path.join(output_folder,"character_train.csv"),config_parameters['main']['has_train'],True)
            data_character=dict()
            row_="label|"            
            for this_bin_index in range(len(bins_)):
                bin_key_=get_key_bin(bins_[this_bin_index])
                row_+=bin_key_+"|"
            row_+="number_of_pictures|sum_of_bytes|"
            print(row_,file=file_character_train)

            row_=""
            for y_element in labels_train:
                
                row_=y_element+"|"
                data_character[y_element]=dict()

                sum_of_bytes=0
                number_of_pictures=0

                for this_bin_index in range(len(bins_)):
                    
                    first_=bins_[this_bin_index][0]
                    last_=bins_[this_bin_index][1]
                    bin_key_=get_key_bin(bins_[this_bin_index])
                    data_character[y_element][bin_key_]=dict()
                    pcap_number=float(len(list(total_bins_dict[y_element]["train"].keys())))
                    for pcap_name_ in total_bins_dict[y_element]["train"].keys():
                        
                        for element_ in total_bins_dict[y_element]["train"][pcap_name_][bin_key_]:
                            if element_!=0:
                                if not (element_ in data_character[y_element][bin_key_].keys()):
                                    data_character[y_element][bin_key_][element_]=0.0
                                data_character[y_element][bin_key_][element_]+=float(1.0/pcap_number)

                    list_of_elements=list(data_character[y_element][bin_key_].keys())
                    for element_ in list_of_elements:
                        if data_character[y_element][bin_key_][element_]<config_parameters['model_train']['value_thr']:
                            del data_character[y_element][bin_key_][element_]

                    if len(data_character[y_element][bin_key_])>0:
                        number_of_pictures+=1
                        sum_of_bytes+=int(float(first_+last_)/2.0)
                    
                    row_+=str(round_decimal_list_dict(data_character[y_element][bin_key_],2))+"|"
                row_+=str(number_of_pictures)+"|"+str(sum_of_bytes)
                print(row_,file=file_character_train)


            #### REgenerate X_train from corrected general dictionary of bins in order to consideration bin corrections in X_train raw
            X_train=[]
            y_train=[]
            list_filename_train=[]
            list_servername_train=[]
            for y_element in labels_train:
                for pcap_name_ in total_bins_dict[y_element]["train"].keys():
                    pcap_number=float(len(list(total_bins_dict[y_element]["train"].keys())))
                    X_train.append([])
                    for this_bin_index in range(len(bins_total)):
                        this_bin=bins_total[this_bin_index]
                        bin_key_=get_key_bin(this_bin)
                        if this_bin in bins_:
                            for element_ in total_bins_dict[y_element]["train"][pcap_name_][bin_key_]:
                                X_train[-1].append(element_)
                        else:
                            X_train[-1]=X_train[-1]+config_parameters['model_train']['number_min_every_bin']*[0]
                    y_train.append(y_element)
                    list_filename_train.append(pcap_name_)
                    list_servername_train.append(total_bins_dict[y_element]["train"][pcap_name_]['servername'])

            
                


    #### now begin modeling of distances
    
    

    #### in this part we decide about importance of every bin in decision making
    #### it not used in distance calculation now
    #### cause of this parameter is True: config_parameters['model_train']['all_coeff_one']=True
    #### it consider difference of bins but becaUSE OF bad thresholding we turned off this feature
    #### every bin that has more big differentiationability between labels has more score
    coeffecient_importance_distance=dict()
    for y_element in data_character.keys():
        coeffecient_importance_distance[y_element]=dict()
        for bin_key in data_character[y_element].keys():
            
            other_number=0.0
            sigma_proba_others=0.0
            sigma_proba_ours=0.0
            for y_element2 in data_character.keys():
                delta_sigma_others=0.0
                delta_sigma_ours=0.0
                if y_element==y_element2:
                    for element_ in data_character[y_element2][bin_key]:
                        delta_sigma_ours+=data_character[y_element2][bin_key][element_]
                else:
                    for element_ in data_character[y_element2][bin_key]:
                        delta_sigma_others+=data_character[y_element2][bin_key][element_]

                if delta_sigma_others!=0.0:
                    other_number+=1.0

                sigma_proba_ours+=delta_sigma_ours
                sigma_proba_others+=delta_sigma_others

            if config_parameters['model_train']['all_coeff_one']:
                coeffecient_importance_distance[y_element][bin_key]=1.0
            else:
                coeffecient_importance_distance[y_element][bin_key]=float(config_parameters['model_train']['first_importance_of_columns'])

                other_proba_importance=config_parameters['model_train']['other_proba_importance']
                if sigma_proba_ours==0.0:

                    # delta_coef=other_number/(float(len(list(data_character.keys()))))
                    # other_proba_importance=(1+other_proba_importance)/2

                    delta_coef=sigma_proba_others/(float(len(list(data_character.keys()))))
                    delta_coef=(delta_coef+1.0)/2.0
                    delta_coef=(delta_coef+1.0)/2.0

                    coeffecient_importance_distance[y_element][bin_key]+=delta_coef
                else:
                    delta_coef=sigma_proba_ours/(1.0+other_proba_importance*sigma_proba_others)
                    delta_coef=(delta_coef+1.0)/2.0
                    delta_coef=(delta_coef+1.0)/2.0

                    coeffecient_importance_distance[y_element][bin_key]+=delta_coef



    #### in this part we calculate distances for augmentation and do it for next calculation of mean and standard deviation
    #### for analysis of training data in order to set threshold
    #### do augment and print statistic results of it
    distance_list_dict=dict()
    
    print("augmented statictics pattern of labels ",file=file_log)
    print("...................................... ",file=file_log)
    
    for index_ in range(len(X_train_backup)):

        for iteration_augment_number in range(config_parameters['model_train']['augmentation_coeff']):
            #augment_vector(vector_,min_disappear_bin,max_disappear_bin,min_number_create,max_number_create,offset_list,bins_)
            this_list=augment_vector([element_ for element_ in X_train_backup[index_] if element_!=0],0,0,0,0,config_parameters['model_train']['offset'],bins_total)

            this_sample_bins_dict=bin_implement(this_list,bins_total)

            y_element=y_train_backup[index_]

            data_character_label_dict=data_character[y_element]

            test_list,train_list=list_from_dict(this_sample_bins_dict,data_character_label_dict)
            
            if config_parameters['model_train']['model_distance_number']==3:
                dist=distance_new3(this_sample_bins_dict,data_character_label_dict,coeffecient_importance_distance[y_element])
            elif config_parameters['model_train']['model_distance_number']==2:
                dist=distance_new2(this_list,train_list)

            if not (y_element in distance_list_dict.keys()):
                distance_list_dict[y_element]=[]
            distance_list_dict[y_element].append(round(dist,4))



    distance_list_dict_max=dict()
    distance_list_dict_min=dict()
    distance_list_dict_std=dict()
    distance_list_dict_mean=dict()

    distance_list_dict_thr=dict()
    for y_element in labels_train:

        print("________________",file=file_log)
        print(y_element,file=file_log)
        print(distance_list_dict[y_element],file=file_log)
        print(len(distance_list_dict[y_element]),file=file_log)
        distance_list_dict_max[y_element]=max(distance_list_dict[y_element])
        distance_list_dict_min[y_element]=min(distance_list_dict[y_element])
        distance_list_dict_mean[y_element]=statistics.mean(distance_list_dict[y_element])
        distance_list_dict_std[y_element]=statistics.pstdev(distance_list_dict[y_element])




        print("max_dist "+y_element,round(distance_list_dict_max[y_element],3),file=file_log)
        print("min_dist "+y_element,round(distance_list_dict_min[y_element],3),file=file_log)
        print("mean_dist "+y_element,round(distance_list_dict_mean[y_element],3),file=file_log)
        print("std_dist "+y_element,round(distance_list_dict_std[y_element],3),file=file_log)

    z_score_unknown_threshold=config_parameters['model_train']['zscore_threshold_unknown']
    y_test_pred=[[]]*len(y_test)
    
    z_score_known_threshold=config_parameters['model_train']['zscore_threshold_known']
    z_score_unknown_threshold=config_parameters['model_train']['zscore_threshold_unknown']
    distance_threshold=config_parameters['model_train']['thr_distance_unknown']
    

    dict_threshold=dict()
    for y_element in data_character.keys():
        dict_threshold[y_element]=distance_threshold

        
    for index_ in range(len(X_test)):
        print("_______________________________________________________________________",file=file_log)
        print('real:'+y_test[index_]+" "+list_filename_test[index_]+" "+list_servername_test[index_],file=file_log)
        # print('real:'+y_test[index_]+" "+list_filename_test[index_]+" "+list_servername_test[index_])
        print("--------------------",file=file_log)
        min_z_score_dict=dict()
        min_distance_dict=dict()
        min_y_element=""
        min_dist=2*big_number
        min_z=2*big_number
        min_offset=-1
      
        for offset_ in config_parameters['model_train']['offset']:
            
            this_sample_bins_dict=bin_implement([element_+offset_ for element_ in X_test[index_] if element_!=0],bins_total)
            
            for y_element in data_character.keys():
                
                if not (y_element in min_distance_dict.keys()):
                    min_distance_dict[y_element]=dict()
                    min_z_score_dict[y_element]=dict()

                data_character_label_dict=data_character[y_element]
                
                
                test_list,train_list=list_from_dict(this_sample_bins_dict,data_character_label_dict)
                

                # dist=distance_new(this_sample_bins_dict,data_character_label_dict)

                if config_parameters['model_train']['model_distance_number']==3:
                    dist=distance_new3(this_sample_bins_dict,data_character_label_dict,coeffecient_importance_distance[y_element])
                elif config_parameters['model_train']['model_distance_number']==2:
                    dist=distance_new2(this_list,train_list)

                

                radious=distance_list_dict_std[y_element]
                # radious=distance_list_dict_max[y_element]
                # radious=(distance_list_dict_max[y_element]+distance_list_dict_max[y_element])/2.0

                zscore=(dist-distance_list_dict_mean[y_element])/radious
                
                min_distance_dict[y_element][offset_]=round(dist,3)
                min_z_score_dict[y_element][offset_]=round(zscore,3)

                print(list_filename_test[index_] + " from " + y_element+" @OFFSET {}".format(offset_),file=file_log)

                print("*******dist={}".format(dist),file=file_log)
                print("*******zscore={}".format(zscore),file=file_log)
                print("   test :",test_list,file=file_log)
                print("   train:",train_list,file=file_log)
                

                
                # input()

            
                if min_distance_dict[y_element][offset_]<min_dist :
                    min_y_element=y_element
                    min_dist=min_distance_dict[y_element][offset_]
                    min_z=min_z_score_dict[y_element][offset_]
                    min_offset=offset_


        
        this_sample_bins_dict=bin_implement([element_+min_offset for element_ in X_test[index_] if element_!=0],bins_total)
        temp_test_list=[]

        for this_bin_index in range(len(bins_total)):

            this_bin=bins_total[this_bin_index]

            bin_key_=get_key_bin(bins_total[this_bin_index])
                
            if this_bin in bins_:
                # input("THERE")
                max_value_of_bin=max_value_number_per_bin[bin_key_]
            else:
                max_value_of_bin=config_parameters['model_train']['number_min_every_bin']
            
            this_sample_bins_dict[bin_key_]=this_sample_bins_dict[bin_key_][:max_value_of_bin]
            this_sample_bins_dict[bin_key_]=this_sample_bins_dict[bin_key_]+[0]*(max_value_of_bin-len(this_sample_bins_dict[bin_key_]))
            temp_test_list.extend(this_sample_bins_dict[bin_key_])
        
      
        
        X_test[index_]=temp_test_list.copy()


        for y_element in data_character.keys():
            print("      distance,zscore from {} @min_offset {} = {},{}".format(y_element,min_offset,min_distance_dict[y_element][min_offset],min_z_score_dict[y_element][min_offset]),file=file_log)
        print("--------------------",file=file_log)

        
        if (min_dist>dict_threshold[y_element] or min_z>z_score_unknown_threshold) and min_z>z_score_known_threshold:
            print('real: {} '.format(list_filename_test[index_]),"_ predicted: UNKNOWN({}) , offset {} , distance {} , zscore {}".format(min_y_element,min_offset,min_dist,min_z),file=file_log)
            y_test_pred[index_]=["Unknown",min_y_element,min_dist]
        else:
            print('real: {} '.format(list_filename_test[index_]),"_ predicted: {} , offset {} , distance {} , zscore {}".format(min_y_element,min_offset,min_dist,min_z),file=file_log)
            y_test_pred[index_]=["Known",min_y_element,min_dist]
            
                
    

    if True:
        dict_threshold=dict()
        for y_element in all_labels:
            indices_y_element=[index for index in range(len(y_test)) if y_test[index]==y_element]
            list_good_distances=[]
            for index in indices_y_element:
                if y_test[index]==y_test_pred[index][1]:
                    if y_test_pred[index][0]=="Known":
                        list_good_distances.append(y_test_pred[index][2])
            #dict_threshold[y_element]=max(list_good_distances)+0.01
            
            # dict_threshold[y_element]=statistics.mean(list_good_distances)+ 1.5*statistics.pstdev(list_good_distances)
            
            dict_threshold[y_element]=(max(list_good_distances)+statistics.mean(list_good_distances))/2.0

        save_obj([data_character,dict_threshold,max_value_number_per_bin,distance_list_dict_mean,distance_list_dict_std], os.path.join(output_folder0,"insta_trained_model.txt"))
    
    
def model_test_exec(sysargv2):
    print("test exec")
    #### initialization
    global home_address
    home_address=os.path.dirname(os.path.realpath(__file__))
    
    ### read cli train and test files
    
    
    base_name_data_test=sysargv2

    ### read and pass config parameters
    global config_parameters
    with open(os.path.join(home_address,'config_parameters.json'),'r') as file_:
        config_parameters=json.loads(file_.read())

    

    ### make zero output folder
    output_folder0=os.path.join(home_address,config_parameters['main']['output_folder'])
    
    #make train or test folder
    output_folder=os.path.join(output_folder0,"test")
    
    ##make directories
    try: os.mkdir(output_folder0)
    except: pass
    try: os.mkdir(output_folder)
    except: pass

    ###make file log
    log_file_name=os.path.join(output_folder,'output_prediction.log')
    global file_log
    
    file_log=delete_and_create_file(log_file_name,config_parameters['main']['has_train'],False)
    
    

    
    try: Known_list=config_parameters['model_train']['Known_list']
    except: Known_list=['all']
    
    
    verbose_number=config_parameters['model_train']['verbose_']
    thr_min_pic=config_parameters['model_train']['thr_min_pic']


    histogram_bin_byte=config_parameters['model_train']['histogram_bin_byte']
    histogram_bin_byte_end=config_parameters['model_train']['histogram_bin_byte_end']

    bin_optimization_bool=config_parameters['model_train']['bin_optimization_bool']
    bin_overlap_coeff=config_parameters['model_train']['bin_overlap_coeff']#must be a division number for max_jpg_byte #for example 250,420,600,900,1000,1260,1500,1800,2250,2800,3150,3600,4500,6300,8400,10500,15000,18000


    roundup_bool=True

    sort_bool=config_parameters['model_train']['sort_bool']
    high_to_low_sort_bool=config_parameters['model_train']['high_to_low_sort_bool']

    

    roundup_length=config_parameters['model_train']['roundup_length']#roundup
    train_offset=config_parameters['model_train']['train_offset']

    max_jpg_byte=config_parameters['model_train']['max_jpg_byte'] # must be divisional by bin_byte #80000

    big_number=config_parameters['model_train']['big_number'] # must be divisional by bin_byte #80000

    categ_threshold=0


    delete_badnumber_bool=False
    min_length=config_parameters['model_train']['min_length'] #-1

    bad_numbers=[]
    
    add_unknown_of_train_to_test=False
    
    #delete_past_unknown_labels_of_test_data_that_were_unknown_in_training_data_of_probability #BECAUSE IN TRAINING OF KNOWN MODEL HAVE BEEN USED; it is for last tree model and now has been expired to be True
    
    delete_train_unknown_labels_from_test_data=False
    
    SAVE_MODEL_BOOL=False
    LOAD_MODEL_BOOL=True
    
#### load model threshold

    model_=load_obj(os.path.join(output_folder0,"insta_trained_model.txt"))
    
    data_character=model_[0]
    dict_threshold=model_[1]
    max_value_number_per_bin=model_[2]
    distance_list_dict_mean=model_[3]
    distance_list_dict_std=model_[4]
    # print(dict_threshold)
#### loading data test

    all_Known_list=sorted(list(set(dict_threshold.keys())))
    # print(all_Known_list)
    # input()

    test_data = pd.read_csv(os.path.join(home_address,base_name_data_test+'.csv'),delimiter='|',header=0)
    X_test=test_data.loc[:, (test_data.columns!='label') & (test_data.columns!='filename') & (test_data.columns!='server_name')].values.tolist()
    y_test=test_data['label'].tolist()
    list_filename_test=test_data['filename'].tolist()
    list_servername_test=test_data['server_name'].tolist()



#### known data and unknown data initialization
    
    #### check status of known list
        
    # print("KNOWN_ALL:",all_Known_list,file=file_log)
    if len(Known_list)>2:
        pass
    elif len(Known_list)==1 and Known_list[0]=='all':
        Known_list=all_Known_list
    else:
        Known_list=all_Known_list

    

    ### delete_train_unknown_labels_from_test_data , its always false. it was True in the past model of insta that we train e secon model for detecting unknown from confidency
    if delete_train_unknown_labels_from_test_data:
        Known_list_2=list(set(y_test) - (set(all_Known_list)-set(Known_list)))
        print(Known_list_2)
        Known_list_2=sorted(Known_list_2)
        X_test,y_test,list_filename_test,list_servername_test,X_test_temp_Unknown,y_test_temp_Unknown,file_list_test_temp_Unknown,servername_list_test_temp_Unknown = split_by_knowing(X_test,y_test,list_filename_test,list_servername_test,Known_list_2)

    #adding deleted unknown data from train into test data
    if add_unknown_of_train_to_test: # as unknown tests
        X_test=X_test+X_Unknown
        y_test=y_test+y_Unknown
        list_filename_test=list_filename_test+file_list_Unknown
        list_servername_test=list_servername_test+list_servername_Unknown






#### some general preprocessing like sort, delete badnumber and roundup and ...

    #### at this part of code we delete bad picture numbers. every number must be bigger than min_approved_length and not be in list of bad numbers
    if delete_badnumber_bool:
        for i in range(len(X_train)):
            temp=[]
            for j in X_train[i]:
                if (not(j in bad_numbers)) and j > min_length:
                    temp.append(j)
                else:
                    temp.append(0)
            X_train[i]=temp
        for i in range(len(X_test)):
            temp=[]
            for j in X_test[i]:
                if (not(j in bad_numbers)) and j>min_length:
                    temp.append(j)
                else:
                    temp.append(0)
            X_test[i]=temp

    roundup_length_equal=config_parameters['model_train']['roundup_length_equal']
    #### at this part we sort data of each sample (sort length of pictures), at this time we delete equal number that repeated(roundup for offset of equity)
    if sort_bool:
        
        for i in range(len(X_test)):
            temp=X_test[i].copy()
            temp=sorted(list(set([roundup(x,roundup_length_equal,0) for x in temp if x!=0])),reverse=high_to_low_sort_bool)
            X_test[i]=temp+(len(X_test[i])-len(temp))*[0]

            if not high_to_low_sort_bool:
                x_temp=[x for x in X_test[i] if x!=0]
                x_temp=x_temp+(len(X_test[i])-len(x_temp))*[0]
                X_test[i]=x_temp

    #### round begin with train offset for train data and without offset for test data
    if roundup_bool:
        
        for i in range(len(X_test)):
            temp=X_test[i].copy()
            X_test[i]=[roundup(j,roundup_length,0) for j in temp]

    bad_numbers_2=[0]



#### binning start here
    bins_total=histo_bins_from_numbers(min_length,histogram_bin_byte,histogram_bin_byte_end,max_jpg_byte,big_number,bin_overlap_coeff)
    bins_total=bins_total[:-1]

    bins_=bins_total.copy()



    
    
    

    #### in this part we decide about importance of every bin in decision making
    #### it not used in distance calculation now
    #### cause of this parameter is True: config_parameters['model_train']['all_coeff_one']=True
    #### it consider difference of bins but becaUSE OF bad thresholding we turned off this feature
    #### every bin that has more big differentiationability between labels has more score
    coeffecient_importance_distance=dict()
    for y_element in data_character.keys():
        coeffecient_importance_distance[y_element]=dict()
        for bin_key in data_character[y_element].keys():
            
            other_number=0.0
            sigma_proba_others=0.0
            sigma_proba_ours=0.0
            for y_element2 in data_character.keys():
                delta_sigma_others=0.0
                delta_sigma_ours=0.0
                if y_element==y_element2:
                    for element_ in data_character[y_element2][bin_key]:
                        delta_sigma_ours+=data_character[y_element2][bin_key][element_]
                else:
                    for element_ in data_character[y_element2][bin_key]:
                        delta_sigma_others+=data_character[y_element2][bin_key][element_]

                if delta_sigma_others!=0.0:
                    other_number+=1.0

                sigma_proba_ours+=delta_sigma_ours
                sigma_proba_others+=delta_sigma_others

            if config_parameters['model_train']['all_coeff_one']:
                coeffecient_importance_distance[y_element][bin_key]=1.0
            else:
                coeffecient_importance_distance[y_element][bin_key]=float(config_parameters['model_train']['first_importance_of_columns'])

                other_proba_importance=config_parameters['model_train']['other_proba_importance']
                if sigma_proba_ours==0.0:

                    # delta_coef=other_number/(float(len(list(data_character.keys()))))
                    # other_proba_importance=(1+other_proba_importance)/2

                    delta_coef=sigma_proba_others/(float(len(list(data_character.keys()))))
                    delta_coef=(delta_coef+1.0)/2.0
                    delta_coef=(delta_coef+1.0)/2.0

                    coeffecient_importance_distance[y_element][bin_key]+=delta_coef
                else:
                    delta_coef=sigma_proba_ours/(1.0+other_proba_importance*sigma_proba_others)
                    delta_coef=(delta_coef+1.0)/2.0
                    delta_coef=(delta_coef+1.0)/2.0

                    coeffecient_importance_distance[y_element][bin_key]+=delta_coef



    z_score_unknown_threshold=config_parameters['model_train']['zscore_threshold_unknown']
    y_test_pred=[[]]*len(y_test)
    
    z_score_known_threshold=config_parameters['model_train']['zscore_threshold_known']
    z_score_unknown_threshold=config_parameters['model_train']['zscore_threshold_unknown']
    distance_threshold=config_parameters['model_train']['thr_distance_unknown']

    
        
    for index_ in range(len(X_test)):
        print("_______________________________________________________________________",file=file_log)
        print('real:'+y_test[index_]+" "+list_filename_test[index_]+" "+list_servername_test[index_],file=file_log)
        # print('real:'+y_test[index_]+" "+list_filename_test[index_]+" "+list_servername_test[index_])
        print("--------------------",file=file_log)
        min_z_score_dict=dict()
        min_distance_dict=dict()
        min_y_element=""
        min_dist=2*big_number
        min_z=2*big_number
        min_offset=-1
      
        for offset_ in config_parameters['model_train']['offset']:
            
            this_sample_bins_dict=bin_implement([element_+offset_ for element_ in X_test[index_] if element_!=0],bins_total)
            
            for y_element in data_character.keys():
                
                if not (y_element in min_distance_dict.keys()):
                    min_distance_dict[y_element]=dict()
                    min_z_score_dict[y_element]=dict()

                data_character_label_dict=data_character[y_element]
                
                
                test_list,train_list=list_from_dict(this_sample_bins_dict,data_character_label_dict)
                

                # dist=distance_new(this_sample_bins_dict,data_character_label_dict)

                if config_parameters['model_train']['model_distance_number']==3:
                    dist=distance_new3(this_sample_bins_dict,data_character_label_dict,coeffecient_importance_distance[y_element])
                elif config_parameters['model_train']['model_distance_number']==2:
                    dist=distance_new2(this_list,train_list)

                
                zscore=(dist-distance_list_dict_mean[y_element])/distance_list_dict_std[y_element]
                
                
                min_distance_dict[y_element][offset_]=round(dist,3)
                min_z_score_dict[y_element][offset_]=round(zscore,3)
                
                print(list_filename_test[index_] + " from " + y_element+" @OFFSET {}".format(offset_),file=file_log)

                print("*******dist={}".format(dist),file=file_log)
                print("*******zscore={}".format(zscore),file=file_log)
                print("   test :",test_list,file=file_log)
                print("   train:",train_list,file=file_log)
                

                
                # input()

                
                if min_distance_dict[y_element][offset_]<min_dist :
                    min_y_element=y_element
                    min_dist=min_distance_dict[y_element][offset_]
                    min_z=min_z_score_dict[y_element][offset_]
                    min_offset=offset_


        
        this_sample_bins_dict=bin_implement([element_+min_offset for element_ in X_test[index_] if element_!=0],bins_total)
        temp_test_list=[]

        for this_bin_index in range(len(bins_total)):

            this_bin=bins_total[this_bin_index]

            bin_key_=get_key_bin(bins_total[this_bin_index])
                
            if this_bin in bins_:
                # input("THERE")
                max_value_of_bin=max_value_number_per_bin[bin_key_]
            else:
                max_value_of_bin=config_parameters['model_train']['number_min_every_bin']
            
            this_sample_bins_dict[bin_key_]=this_sample_bins_dict[bin_key_][:max_value_of_bin]
            this_sample_bins_dict[bin_key_]=this_sample_bins_dict[bin_key_]+[0]*(max_value_of_bin-len(this_sample_bins_dict[bin_key_]))
            temp_test_list.extend(this_sample_bins_dict[bin_key_])
        
      
        
        X_test[index_]=temp_test_list.copy()


        for y_element in data_character.keys():
            print("      distance,zscore from {} @min_offset {} = {},{}".format(y_element,min_offset,min_distance_dict[y_element][min_offset],min_z_score_dict[y_element][min_offset]),file=file_log)
        print("--------------------",file=file_log)

        if (min_dist>dict_threshold[y_element] or min_z>z_score_unknown_threshold) and min_z>z_score_known_threshold:
            print('real: {} '.format(list_filename_test[index_]),"_ predicted: UNKNOWN({}) , offset {} , distance {} , zscore {}".format(min_y_element,min_offset,min_dist,min_z),file=file_log)
            y_test_pred[index_]=["Unknown",min_y_element,min_dist]
        else:
            print('real: {} '.format(list_filename_test[index_]),"_ predicted: {} , offset {} , distance {} , zscore {}".format(min_y_element,min_offset,min_dist,min_z),file=file_log)
            y_test_pred[index_]=["Known",min_y_element,min_dist]
                
    return y_test,y_test_pred
    

    
        
        
    

if __name__ == "__main__":
    
    
    if sys.argv[3]=="train":
        model_train_exec(sys.argv[1])
    if sys.argv[3]=="test":
        model_test_exec(sys.argv[2])
    


            
