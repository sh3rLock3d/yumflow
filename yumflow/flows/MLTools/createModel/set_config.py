import json
import pprint
import re
import os


class SetConfig():
    def __init__(self, isTrain):
        

        home_address=os.path.dirname(os.path.realpath(__file__))

        config_parameters = dict()

        config_parameters['main'] = {
        #must not be _ in foldername basename
            
            'change_train_data': False,#if false read from the csv file name mentioned in TCP_parser_train.txt
            'change_test_data': False,#if false read from the csv file name mentioned in TCP_parser_test.txt

            'has_train': isTrain,
            'has_test': not isTrain,
            
            
        
            'train_data_folder':'./train.csv',

            'test_data_folder':'./test.csv',

            'read_last_train_files_splitted':False,#from file TCP_parser_train newest
            'read_last_test_files_splitted':False,#from file TCP_parser_test newest
            

            'manual_train_data_csv':'train',
            
            
            'manual_test_data_csv':'test',
            
            'output_folder':'final_test'

        }

        config_parameters['session_splitter'] = {
            'delete_other_general_sni':True,
            # 'sni_dict_priority_list': [{"i.instagram":2,"mqtt-mini.facebook":3,"cdn":4,"graph.instagram":5}],
            'sni_dict_priority': {"cdn":2},
            'train_test_val_percent_in_training':[80,20,0],
            'number_of_packet':2000,
            'concat_sessions':False,
            'facebook_ip_range':["102.132.96","102.132.96","103.4.96","129.134.0","129.134.25","129.134.26","129.134.27","129.134.28","129.134.29","129.134.30","129.134.30","129.134.31","129.134.64","129.134.65","129.134.66","129.134.67","129.134.68","129.134.69","129.134.70","157.240.0","157.240.0","157.240.10","157.240.1","157.240.11","157.240.12","157.240.13","157.240.14","157.240.17","157.240.18","157.240.19","157.240.192","157.240.193","157.240.194","157.240.195","157.240.196","157.240.197","157.240.199","157.240.200","157.240.20","157.240.201","157.240.2","157.240.204","157.240.205","157.240.206","157.240.209","157.240.210","157.240.21","157.240.211","157.240.212","157.240.213","157.240.215","157.240.216","157.240.217","157.240.218","157.240.219","157.240.220","157.240.22","157.240.221","157.240.222","157.240.223","157.240.24","157.240.26","157.240.27","157.240.28","157.240.29","157.240.30","157.240.3","157.240.6","157.240.7","157.240.8","157.240.9","173.252.64","173.252.70","173.252.88","173.252.96","179.60.192","179.60.192","179.60.194","179.60.195","185.60.216","185.60.216","185.60.217","185.60.218","185.60.219","185.89.218","185.89.218","185.89.219","204.15.20","31.13.24","31.13.64","31.13.64","31.13.64","31.13.65","31.13.66","31.13.67","31.13.69","31.13.70","31.13.71","31.13.72","31.13.73","31.13.74","31.13.79","31.13.75","31.13.76","31.13.77","31.13.78","31.13.80","66.220.144","66.220.149","66.220.152","66.220.158","66.220.159","66.220.144","69.63.176","69.63.184","69.171.224","69.171.229","69.171.239","69.171.240","69.171.242","69.171.255","74.119.76","69.171.250","31.13.92","31.13.72","195.33.193","185.200.233","213.202.0","157.221.29","157.240.21","213.202.5","3.211.123","81.27.242","157.240.227"],


            ##if type of time in file name is timestamp then time filter type must be zero

            'train_time_filter_type':0,#0 : not filter_all retention, 1: time_window_by_date,2:houre before from now ,3: last pcap time is now in 2
            'train_time_window_start': '20210520132507',#type 1
            'train_time_window_finish':'20210520162106',#type 1
            'train_time_hours_ago':8,#type 2
            # 'train_picked_label':['metro', 'futbol90', 'machinlearning', '_machinelearning', 'mobile_game', 'alidaei', 'neuer', 'ucdcogsci', 'sadrossadati', 'sheykhjafar', 'bitcoin', 'cristiano', 'messi', 'homazadeh', 'salim', 'hrouhani', 'codingtim', 'khamenei', 'bahjat', 'javane', 'python', 'gonahkabireh', 'tehroonnews', 'honarjoha', 'typical', 'jordi', 'gameofthrones', 'soluk', 'fifa21', 'zobakalam', 'koodake', 'rouhani', 'officialpes', 'sport3', 'tarikh', 'khatami', 'fifaworldcup', 'fact', 'khodro45','mobilegame','_machinlearning','mach'][:],
            'train_picked_label':['all'][:],

            #test file name must be like num_label.pcap
            'test_time_filter_type':0,#0 : not filter_all retention, 1: time_window_by_date,2:houre before from now ,3: last pcap time is now in 2
            'test_time_window_start': '20210520132507',#type 1
            'test_time_window_finish':'20210520162106',#type 1
            'test_time_hours_ago':8,#type 2
            'test_picked_label':['all']

        }




        config_parameters['feature_extraction'] = {
            'orange_threshold':450,
            'black_threshold':225,
            'max_picture_per_cdn':700,
            
            'concat_bool':False,
            'just_length_without_time':False,
            'round_length_time':3,


            'concat_pictures_of_sessions_by_time':True,#if concat_bool==False and just_length_without_time==False
            'min_length':1000,
            'max_jpg_byte':126000,
            'time_adjacency':2.0,
            'get_time_of_pictures':False,
            'get_session_number_of_pictures':False,

            ## removing features 
            #preprocessing for test data
            #this config must be totally automatic. a function that its input is 
            #total picture,  , min data
            # if total picture==min: hichi
            # if total pucture
            # 'minimum_total_picture_number_to_activate_removing_from_end':20,#is it by cdn_number
            # 'remove_last_pictures_of_every_session':1,#1,0,2
            # 'remove_last_total':0.2,#
            # 'filter_first_pictures':10000?
        }







        config_parameters['model_train']={

            'verbose_':100,
            


            'test_coeffecient':0.1,#important A in training known unknown model. its knowns 0.38 , 0.5,,,,,0.1,80 . read frin one file bool

            
            
            'roundup_length_equal':100,
            'sort_bool':True,
            'high_to_low_sort_bool':False,
            
            'bin_optimization_bool':True,
            'carachteristic_model':True,
            'offset':[-500,-400,-300,-200,-100,0,+100,+200,+300],
            'thr_bin':0.45,#0
            'value_thr':0.25,#0

            

            'histogram_bin_byte':400,
            'histogram_bin_byte_end':400,
            'bin_overlap_coeff':0,

            #TUNING
            #'z_score_bool':False,
            'other_proba_importance':0.4,
            'zscore_threshold_unknown':1.0,
            
            'thr_distance_for_check_z_score':0.16,
            'zscore_threshold_known':-5,
            'thr_distance_unknown':0.16,
            'thr_min_pic':7,
            # 'augmentation_bool':True,
            'augmentation_coeff':7,#number of data created

            # 'histogram_bin_byte':800,
            # 'histogram_bin_byte_end':800,
            # 'bin_overlap_coeff':0.875,
            
            #3:arabpour histogram
            'all_coeff_one':True,
            'first_importance_of_columns':0.05,
            #2:aghamiri
            'model_distance_number':3,
            
            
            'min_length':2000,
            'max_jpg_byte':66000,
            'big_number':250000,

            'roundup_length':200,
            'train_offset':-200,


            

        #,'saeed','mohamadreza','cat'
            # 'Known_list':['metro', 'futbol90', 'machinlearning', '_machinelearning', 'mobile_game', 'alidaei', 'neuer', 'ucdcogsci', 'sadrossadati', 'sheykhjafar', 'bitcoin', 'cristiano', 'messi', 'homazadeh', 'salim', 'hrouhani', 'codingtim', 'khamenei', 'bahjat', 'javane', 'python', 'gonahkabireh', 'tehroonnews', 'honarjoha', 'typical', 'jordi', 'gameofthrones', 'soluk', 'fifa21', 'zobakalam', 'koodake', 'rouhani', 'officialpes', 'sport3', 'tarikh', 'khatami', 'fifaworldcup', 'fact', 'khodro45','mobilegame','_machinlearning'][:],#[:25],
            'Known_list':['all'],
            # 'Known_list':['xxsadrossadati', 'xxcafebazar', 'xxucdcogsci', 'xxhomazadeh', 'xxgonahkabireh', 'xxfutbol90', 'xxtarikh', 'xxsport3', 'xxpython', 'xxalidaei', 'xxkhatami', 'xxhrouhani', 'xxmetro', 'xxmessi', 'xxsalim', 'xxzobakalam', 'xxjordi', 'xxsheykhjafar', 'xxcristiano', 'xxtypical', 'xxneuer', 'xxofficial_type', 'xxmobile_game', 'xxtehroonnews', 'xxsoluk', 'xxhonarjoha', 'xxkhodro45', 'xxfact', 'xxfifaworldcup', 'xxmachinlearning', 'xx_machinelearning', 'xxkoodake', 'xxfifa_orig', 'xxbahjat', 'xxbitcoin', 'xxkhamenei', 'xxgameofthrones', 'xxcodingtim'],
            
            'number_min_every_bin':5,



            'thr_bin_occurence':0,#between zero and one
            'vis_dimension':2,
            'number_of_labels_to_visualize':40,
            
            'norm_number':1,
            
            
            'thr_distance':0.5,
            'ylim_max':10,
            
            'plots_bool':False,
            'plots_bool_after_preprocessing':False,
            'plot_dpi':30,
            
            

            'main_model_max_depth_grid':[10],
            'main_model_n_estimators_grid':[10],
            'main_model_max_features_grid':['sqrt',None],
            'main_model_criterion_grid':['entropy','gini'],

        }


        config_parameters['model_test']={

        }

        output = json.dumps(config_parameters,sort_keys=False,indent=4)

        output2=""
        i=0
        while i < len(output):
            if output[i]=="[":
                j=output[i:].index("]")+i+1
                for temp_i in list(range(i,j+1)):
                    # print(temp_i,output[temp_i],ord(output[temp_i]))
                    if ord(output[temp_i])!=10 and output[temp_i]!=" ":
                        output2+=output[temp_i]
                i=j+1
            else:
                # print(i,output[i])
                output2+=output[i]
                i+=1

        with open(os.path.join(home_address,'config_parameters.json'), 'w') as outfile:
            print(output2,file=outfile)

                    