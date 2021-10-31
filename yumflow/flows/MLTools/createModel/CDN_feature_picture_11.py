#for visualizing new data binarized
import shutil
from pprint import pprint
import pandas as pd
import numpy as np
import statistics
import random
import pickle
import json
import csv
import sys
import os
import matplotlib.pyplot as plt

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###################### siah - algorithme NARENJI - CDN_feature_picture_10 with concat-1500 data
def write_csv_file(concat_bool,X_,y_,filename_,server_name_,cdn_header,filewriter_all,filewriter_=0):
    if concat_bool:
        this_i=-1

    for i in range(len(X_)):
        if concat_bool:
            if i!=len(X_)-1:
                if this_i==-1: #akhari nist dar zemn avvali hast

                    temp_=picture_cdn_dict_2(X_[i])
                    # print(temp_)
                    this_i=i
                    row2=[elem for elem in temp_ if elem!=0]
                    continue #chap nakon boro badi
                elif filename_[i]==filename_[this_i]:#akhari nist dar zemn vasate kare

                    temp_=picture_cdn_dict_2(X_[i])

                    row2=row2+[elem for elem in temp_ if elem!=0]
                    continue#chap nakon boro baedi
                else:#akhari nist va akhare kare va bayad chap beshe

                    temp_=picture_cdn_dict_2(X_[i])
                    pass#boro baraye chap

                row2=row2+[0]*((element_size*max_picture_per_cdn)-len(row2))
                row_=dict()
                for j in range(len(cdn_header)):
                    # temp11=row_[cdn_header[j]]
                    #temp22=row2[j]
                    row_[cdn_header[j]]=row2[j]
                row_['label']=y_[this_i]
                row_['server_name']=server_name_[this_i]
                row_['filename']=filename_[this_i]
                if type(filewriter_)!=int:
                    filewriter_.writerow(row_)
                filewriter_all.writerow(row_)
                row2=[elem for elem in temp_ if elem!=0]
                this_i=i

            else:
                if this_i==-1:#akharie hamzaman avvalie

                    temp_=picture_cdn_dict_2(X_[i])

                    this_i_3=i
                    row3=[elem for elem in temp_ if elem!=0]
                elif filename_[i]==filename_[this_i]:

                    temp_=picture_cdn_dict_2(X_[i])
                    this_i_3=this_i
                    row3=row2+[elem for elem in temp_ if elem!=0]
                else:#FAGHAT AKHARIE NA AVVALI

                    temp_=picture_cdn_dict_2(X_[i])

                    row3=[elem for elem in temp_ if elem!=0]
                    this_i_3=i

                row3=row3+[0]*((element_size*max_picture_per_cdn)-len(row3))
                row_=dict()
                for j in range(len(cdn_header)):
                    row_[cdn_header[j]]=row3[j]
                row_['label']=y_[this_i_3]
                row_['server_name']=server_name_[this_i_3]
                row_['filename']=filename_[this_i_3]
                if type(filewriter_)!=int:
                    filewriter_.writerow(row_)
                filewriter_all.writerow(row_)

        else:
            
            row2=picture_cdn_dict_2(X_[i])
            
            




            # print(row2)
            row_=dict()
            for j in range(len(cdn_header)):
                row_[cdn_header[j]]=row2[j]
            row_['label']=y_[i]
            row_['server_name']=server_name_[i]
            row_['filename']=filename_[i]
            if type(filewriter_)!=int:
                filewriter_.writerow(row_)
            filewriter_all.writerow(row_)

def feature_reduction(df,feat_num_length,feat_num_time,feat_num_direction):
    # headers=[]
    out_X=[]
    out_y=[]
    out_filename=[]
    out_server_name=[]
    counter=0
    for b in df.iterrows():
        counter=counter+1
        out_X.append(eval(b[1]['Length'])[0:feat_num_length] + eval(b[1]['Time'])[0:feat_num_time] + eval(b[1]['Direction'])[0:feat_num_direction])
        out_y.append(b[1]['Label'])
        out_filename.append(b[1]['filename'])
        out_server_name.append(b[1]['server_name'])
        if (counter % 100)==0:
            if log_bool:
                print(counter)
    return out_X,out_y,out_filename,out_server_name

def picture_cdn_dict_2(row_):
    row_out=[0]*element_size*max_picture_per_cdn
    length_=row_[0:cdn_feature_number]
    time_=row_[1*cdn_feature_number:2*cdn_feature_number]
    direction_=row_[2*cdn_feature_number:3*cdn_feature_number]
    index_=[]
    index_exception=[]
    baias=0
    max_time_sequential_inner_packets=0.010 #FOR CALCULATING ADJACENCY

    inner_packets_indices=[j for j in range(cdn_feature_number) if direction_[j]==-2 or direction_[j]==-12]
    temp_list=[time_[inner_packets_indices[j_index+1]]-time_[inner_packets_indices[j_index]] for j_index in range(len(inner_packets_indices[:-1]))]
    temp_list2=[t for t in temp_list if t<max_time_sequential_inner_packets]

    try:
        mean_time_beetween_sequential_oranges_yellows = statistics.mean(temp_list2)
        try:
            stdev_time_beetween_sequential_oranges_yellows = statistics.stdev(temp_list2)
        except:
            pass
        index_=[]
        # adjacency_time=mean_time_beetween_sequential_oranges_yellows-stdev_time_beetween_sequential_oranges_yellows/2
        # adjacency_time=mean_time_beetween_sequential_oranges_yellows*6 #fasele ziade agar az in bishtar bashe

        black_adjacency_time=mean_time_beetween_sequential_oranges_yellows*9
        green_adjacency_time=mean_time_beetween_sequential_oranges_yellows*9

    except:
        pass


    black_indices  = [j for j in range(cdn_feature_number) if direction_[j]==-2  and length_[j] >  black_threshold  ] #BIG   INNER TLS
    #green_indeces  = [j for j in range(cdn_feature_number) if direction_[j]==-2  and length_[j] <= black_threshold  ] #SMALL INNER TLS
    # orange_indices = [j for j in range(cdn_feature_number) if direction_[j]==-12 and length_[j] >  orange_threshold ] #BIG   INNER TCP
    # yellow_indices = [j for j in range(cdn_feature_number) if direction_[j]==-12 and length_[j] <= orange_threshold ] #SMALL INNER TCP

    
    PROBABILITY_START_FINISH_OF_PICTURES=[0]*len(black_indices)
    #big + for begin black
    #small - for end black
    #0 for not good black, Auxiliary black
    black_list_j_indices=list(range(len(black_indices)))

    # for j_index in black_list_j_indices:
    #     j=black_indices[j_index]

    # for j_index in black_list_j_indices[:-1]:
    #     j1=black_indices[j_index]
    #     j2=black_indices[j_index+1]

    # for j_index in black_list_j_indices[:-1]:
    #     j1=black_indices[j_index]
    #     j2=black_indices[j_index+1]
    #     for temp_j in range(j1+1,j2):
    # print("bbb,",black_list_j_indices)
    for j_index in black_list_j_indices[:-1]:
        j1=black_indices[j_index]
        j2=black_indices[j_index+1]
        for temp_j in range(j1+1,j2):
            if direction_[temp_j]==-12 and length_[temp_j] > orange_threshold:
                PROBABILITY_START_FINISH_OF_PICTURES[j_index]+=0.01
                PROBABILITY_START_FINISH_OF_PICTURES[j_index+1]+=-0.01

    temp1=[black_indices[j_index] for j_index in black_list_j_indices if PROBABILITY_START_FINISH_OF_PICTURES[j_index]>=0.01]
    temp2=[black_indices[j_index] for j_index in black_list_j_indices if PROBABILITY_START_FINISH_OF_PICTURES[j_index]<=-0.01]
    temp_total=sorted(temp1+temp2)
    temp_total_str=[]
    for u in temp_total:
        if u in temp1:
            temp_total_str.append("("+str(u))
        else:
            temp_total_str.append(str(u)+")")
    for u in range(len(temp_total_str)):
        if temp_total_str[u][0]=="(":
            for uu in range(u+1,len(temp_total_str)):
                try:
                    if temp_total_str[uu][-1]==")":
                        index_.append([int(temp_total_str[u][1:]),int(temp_total_str[uu][:-1])])
                        try:
                            if temp_total_str[uu+1][-1]==")":
                                index_.append([int(temp_total_str[u][1:]),int(temp_total_str[uu+1][:-1])])
                                index_exception.append([int(temp_total_str[u][1:]),int(temp_total_str[uu+1][:-1])])
                        except:
                            pass
                        break
                except:
                    break
                    pass
    if 'black_adjacency_time' in locals():
        for j_index in black_list_j_indices[0:-1]:
            try:
                j1=black_indices[j_index]
                j2=black_indices[j_index+1]
                if PROBABILITY_START_FINISH_OF_PICTURES[j_index]==0:
                    if time_[j2]-time_[j1]<black_adjacency_time:
                        for uu in range(len(index_)):
                            if index_[uu][0]==j2:
                                index_[uu][0]=j1
                                break
            except:
                pass
    if 'black_adjacency_time' in locals():
        for t in range(len(index_)-1):
            taghir_bool=False
            ind1=index_[t][0]
            ind2=index_[t][1]
            temp_=list(range(ind1,ind2+1))[::-1]
            for j in temp_:
                if direction_[j]==-12:
                    if time_[ind2]-time_[j]>black_adjacency_time:
                        taghir_bool=True
                    break
        try:
            ind1_=index_[t+1][0]
            ind2_=index_[t+1][1]
            if taghir_bool and ind1!=ind1_:
                if time_[ind1_]-time_[ind2]<=black_adjacency_time:
                    index_[t+1][0]=ind2
                    index_[t][1]=j
        except:
            pass
    index_=index_+index_exception
    index_=sorted(index_, key=lambda l: l[0])
    
    for t in range(len(index_)):
        ind1=index_[t][0]
        ind2=index_[t][1]

        ind1_OK_bool=False
        for index_temp in range(0,ind1):
            if direction_[index_temp]==2:
                ind1_OK_bool=True
                break

        if not ind1_OK_bool:
            for index_temp in range(ind1,cdn_feature_number):
                if direction_[index_temp]==2:
                    ind1=index_temp
                    break

        SUM=0

        for j in range(ind1,ind2+1):
            if direction_[j]==-12 or direction_[j]==-2:
                SUM+=length_[j]


        if element_size==2:

            

            try:

                row_out[t*element_size]=round(time_[ind1],config_parameters['feature_extraction']['round_length_time'])
                
                row_out[t*element_size+1]=SUM
            except:
                
                if log_bool:
                    print("error",t*element_size, ind1)
        elif element_size==1:
            try:
                row_out[t*element_size]=SUM
            except:
                if log_bool:
                    print("error",t*element_size, ind1)


    if sum(row_out)==0:
        if log_bool:
            print("zero response")
    else:
        pass
    return row_out

def feature_extractor_function(home_address,number_of_packet,csvname_in):
    global log_bool
    log_bool=False

    global config_parameters
    with open(os.path.join(home_address,'config_parameters.json'),'r') as file_:
        config_parameters=json.loads(file_.read())

    global cdn_feature_number
    cdn_feature_number=number_of_packet

    global orange_threshold
    #DEFINITION OF BIG AND SMALL LENGTH OF INNER TCP PACKET BETWEEN ORANGE OR YELLOW
    orange_threshold=config_parameters['feature_extraction']['orange_threshold']

    global black_threshold
    #DEFINITION OF BIG AND SMALL LENGTH OF INNER TLS PACKET BETWEEN BLACK OR GREEN
    black_threshold = config_parameters['feature_extraction']['black_threshold']

    global max_picture_per_cdn
    max_picture_per_cdn=config_parameters['feature_extraction']['max_picture_per_cdn']
    global element_size
    if config_parameters['feature_extraction']['just_length_without_time']:
        element_size=1
    else:
        element_size=2
    concat_bool=config_parameters['feature_extraction']['concat_bool']

    #for visualization concat_bool must be False and element size must be 2  and has time
    #TODO it have to evolve and extend to just concat_bool True
    #element_size==1

    feat_num_length=cdn_feature_number # < 180
    feat_num_time=cdn_feature_number # < 180
    feat_num_direction=cdn_feature_number # < 180
    feat_num_type=0
    all_feat_num=feat_num_length+feat_num_time+feat_num_direction


    decimal_encoder_bool=False
    onehot_encoder_bool=False
    binary_encoder_bool=False
    feat_num_length=cdn_feature_number


    base_name_data=csvname_in[:-4]
    base_name_data_test=base_name_data.replace("train","test")
    base_name_data_val=base_name_data.replace("train","val")

    # lss=dict()

    training_data = pd.read_csv(os.path.join(home_address,base_name_data+'.csv'),delimiter='|',header=0)
    X_train,y_train,filename_train,server_name_train = feature_reduction(training_data,feat_num_length,feat_num_time,feat_num_direction)


    test_data = pd.read_csv(os.path.join(home_address,base_name_data_test+'.csv'),delimiter='|',header=0)
    X_test,y_test,filename_test,server_name_test = feature_reduction(test_data,feat_num_length,feat_num_time,feat_num_direction)
    try:
        validation_data = pd.read_csv(os.path.join(home_address,base_name_data_val+'.csv'),delimiter='|',header=0)
        X_val,y_val,filename_val,server_name_val = feature_reduction(validation_data,feat_num_length,feat_num_time,feat_num_direction)
    except:
        pass





    #_____________________________
    if log_bool:
        print(base_name_data)




    #for just length :1 , time and length:2
    if element_size==2:
        cdn_header0=["picture_"+str(i+1)+"_time" for i in list(range(max_picture_per_cdn))]
    # cdn_header1=["picture_"+str(i+1)+"_req_length" for i in list(range(max_picture_per_cdn))]
    cdn_header2=["picture_"+str(i+1)+"_size" for i in list(range(max_picture_per_cdn))]
    # cdn_header3=["picture_"+str(i+1)+"_duration_time" for i in list(range(max_picture_per_cdn))]
    # cdn_header4=["picture_"+str(i+1)+"_download_rate" for i in list(range(max_picture_per_cdn))]
    # #cdn_header5=["picture_"+str(i+1)+"_response_ping_time" for i in list(range(max_picture_per_cdn))]
    # cdn_header5=["picture_"+str(i+1)+"_last_res_length" for i in list(range(max_picture_per_cdn))]


    cdn_header=[]
    for i in list(range(max_picture_per_cdn)):
        if element_size==2:
            cdn_header.append(cdn_header0[i])#time
        # cdn_header.append(cdn_header1[i])#req length
        cdn_header.append(cdn_header2[i])#size
        # cdn_header.append(cdn_header3[i])
        # cdn_header.append(cdn_header4[i])
        # #cdn_header.append(cdn_header5[i])
        # cdn_header.append(cdn_header5[i])



    fieldnames = cdn_header + ['server_name','label','filename']




    # lss=load_object(os.path.join(home_address,base_name_data+'.pkl'))

    #
    base_name_data=csvname_in[:-4]+'_dec___'+str(cdn_feature_number)+'length'
    base_name_data_test=base_name_data.replace("train","test")
    try:
        base_name_data_val=base_name_data.replace("train","val")
    except:
        pass
    #
    trainfile_TCP=open(os.path.join(home_address,base_name_data+'_cdnfeaturepicture_train.csv'), 'w')
    testfile_TCP=open(os.path.join(home_address,base_name_data_test+'_cdnfeaturepicture_test.csv'), 'w')
    try:
        validfile_TCP=open(os.path.join(home_address,base_name_data_val+'_cdnfeaturepicture_val.csv'), 'w')
    except:
        pass

    allfile=open(os.path.join(home_address,base_name_data+'_cdnfeaturepicture_train_all.csv'), 'w')
    #
    filewriter_train_TCP = csv.DictWriter(trainfile_TCP, fieldnames=fieldnames, delimiter='|',lineterminator='\n')
    filewriter_test_TCP  = csv.DictWriter(testfile_TCP , fieldnames=fieldnames, delimiter='|',lineterminator='\n')
    try:
        filewriter_valid_TCP = csv.DictWriter(validfile_TCP, fieldnames=fieldnames, delimiter='|',lineterminator='\n')
    except:
        pass

    filewriter_all = csv.DictWriter(allfile, fieldnames=fieldnames, delimiter='|',lineterminator='\n')
    #
    filewriter_train_TCP.writeheader()
    filewriter_test_TCP.writeheader()
    try:
        filewriter_valid_TCP.writeheader()
    except:
        pass

    filewriter_all.writeheader()

    pd.options.display.max_columns= None
    pd.options.display.max_rows= None




    # element_size==1 and
    #TODO
    # print(X_train[0])
    # input()
    write_csv_file(concat_bool,X_train,y_train,filename_train,server_name_train,cdn_header,filewriter_all,filewriter_train_TCP)
    try:
        write_csv_file(concat_bool,X_test,y_test,filename_test,server_name_test,cdn_header,filewriter_all,filewriter_test_TCP)
        write_csv_file(concat_bool,X_val,y_val,filename_val,server_name_val,cdn_header,filewriter_all,filewriter_val_TCP)
    except:
        pass

    allfile.close()

    tempstr0=base_name_data+'_cdnfeaturepicture_train_all.csv'
    tempstr1=tempstr0.split("_")[0]+".csv"

    shutil.copyfile(os.path.join(home_address,tempstr0), os.path.join(home_address,tempstr1))
    csvname_out_all=tempstr0[:-4]
    
    # return csvname_out_all




    if not config_parameters['feature_extraction']['concat_pictures_of_sessions_by_time']:
        return csvname_out_all
    else:

        
        #TODO
        #for on pcaps - group by by pcap name and the execute alegorithme
        
        get_session_number_of_pictures=config_parameters['feature_extraction']['get_session_number_of_pictures']
        get_time_of_pictures=config_parameters['feature_extraction']['get_time_of_pictures']

        header_concat_by_time=[]
        r_out_0=dict()
        

        for picture_number in range(max_picture_per_cdn):
            temp_list= ['picture_{}_sessionnum'.format(picture_number+1)]*get_session_number_of_pictures
            temp_list+=['picture_{}_time'.format(picture_number+1)]*get_time_of_pictures
            temp_list+=['picture_{}_size'.format(picture_number+1)]*True

            for j in temp_list:
                r_out_0[j]=0
            header_concat_by_time.extend(temp_list)


        


        header_concat_by_time.extend(['server_name','label','filename'])
        r_out_0['server_name']=''
        r_out_0['label']=''
        r_out_0['filename']=''


        csvname_out_all=base_name_data+'_cdnfeaturepicture_train_all_concat_by_time'

        file_concat_by_time=open(os.path.join(home_address,csvname_out_all+'.csv'), 'w')
        filewriter_concat_by_time = csv.DictWriter(file_concat_by_time, fieldnames=header_concat_by_time, delimiter='|',lineterminator='\n')
        filewriter_concat_by_time.writeheader()


        X_train.extend(X_test)
        X_train.extend(X_val)
        y_train.extend(y_test)
        y_train.extend(y_val)
        filename_train.extend(filename_test)
        filename_train.extend(filename_val)
        server_name_train.extend(server_name_test)
        server_name_train.extend(server_name_val)
        
        
        filename_train_set=sorted(list(set(filename_train)))

        for this_file_name in filename_train_set:
            data_indexes=[this_index for this_index in range(len(filename_train)) if filename_train[this_index]==this_file_name]
            
            this_X_train=[X_train[this_index] for this_index in data_indexes]
            this_y_train=[y_train[this_index] for this_index in data_indexes]
            this_filename_train=[filename_train[this_index] for this_index in data_indexes]
            this_server_name_train=[server_name_train[this_index] for this_index in data_indexes]


            X_concat_by_time=[]#in bayad sakhte beshe
            y_concat_by_time=[]
            server_name_concat_by_time=[]
            filename_concat_by_time=[]

            all_pictures=[]

            for this_session_number in range(len(this_X_train)):
                # print("****************************************")

                row2=picture_cdn_dict_2(this_X_train[this_session_number])
                






                
                for element_index in range(len(row2)):

                    element_ = row2[element_index]

                    # print(element_)
                    # input()
                    if (element_index%2)==0:
                        this_time   = element_


                    elif (element_index%2)==1:

                        this_length = element_
                        

                        if this_length!=0 or this_time!=0:

                            if this_length>=config_parameters['feature_extraction']['min_length']:
                                if this_length<=config_parameters['feature_extraction']['max_jpg_byte']:
                                    all_pictures.append([this_session_number,this_time,this_length])
                            # print("___")
                            # print("this_session_number",type(this_session_number),this_session_number)
                            # print("this_time",type(this_time),this_time)
                            # print("this_length",type(this_length),this_length)
                        else:
                            break

            all_pictures = sorted(all_pictures, key=lambda x: x[1],reverse=False)
            
            # print(all_pictures)

            

            

            time_adjacency=config_parameters['feature_extraction']['time_adjacency']
            session_begin_end_index_lists=[]

            


            # print(this_filename_train[0])

            if len(all_pictures)==0:
                pass
                # input("salam0")
            elif len(all_pictures)==1:
                session_begin_end_index_lists.append([0,0])

                # input("salam1")
            else:
                # input("salam2")
                last_index=-1
                for this_picture_index in range(len(all_pictures)):

                    this_session_number=all_pictures[this_picture_index][0]
                    this_time=all_pictures[this_picture_index][1]
                    this_length=all_pictures[this_picture_index][2]


                    if this_picture_index==len(all_pictures)-1:
                        discrete_detection=True
                    else:
                        if abs(all_pictures[this_picture_index][1]-all_pictures[this_picture_index+1][1])<time_adjacency:
                            discrete_detection=False
                        else:
                            discrete_detection=True
                    
                    
                    if discrete_detection:

                        if last_index==-1:
                            session_begin_end_index_lists.append([this_picture_index,this_picture_index])
                            last_index=-1
                        else:
                            session_begin_end_index_lists.append([last_index,this_picture_index])
                            last_index=-1
                    else:
                        if last_index==-1:
                            last_index=this_picture_index
                        else:
                            pass

                for index_ in session_begin_end_index_lists:
                    r_out_this=r_out_0.copy()
                    begin_index=index_[0]
                    end_index=index_[1]
                    # print("(     ,       )")
                    # print(begin_index,end_index)
                    # print(all_pictures[begin_index][1],all_pictures[end_index][1])




                    for index_2 in range(begin_index,end_index+1):
                        index_3=index_2-begin_index
                        # print(index_2)
                        # print(index_3)
                        

                        if get_session_number_of_pictures:
                            r_out_this['picture_{}_sessionnum'.format(index_3+1)]=all_pictures[index_2][0]
                        if get_time_of_pictures:
                            r_out_this['picture_{}_time'.format(index_3+1)]=all_pictures[index_2][1]
                        if True:
                            r_out_this['picture_{}_size'.format(index_3+1)]=all_pictures[index_2][2]

                        
                    first_session_number=all_pictures[begin_index][0]

                    r_out_this['label']=this_y_train[first_session_number]
                    r_out_this['server_name']=this_server_name_train[first_session_number]
                    r_out_this['filename']=this_filename_train[first_session_number]

                    filewriter_concat_by_time.writerow(r_out_this)





        # plt.figure()
        # plt.scatter([tt[1] for tt in all_pictures],[0]*len([tt[1] for tt in all_pictures]))
        # plt.show()
        # plt.close()  
        





        
        
        # write_csv_file(False,X_concat_by_time,y_concat_by_time,filename_concat_by_time,server_name_concat_by_time,header_concat_by_time,filewriter_concat_by_time,0)


        return csvname_out_all
