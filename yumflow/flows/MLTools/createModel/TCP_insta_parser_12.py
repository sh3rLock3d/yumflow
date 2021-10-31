import matplotlib.pyplot as plt
from shutil import copyfile
from scapy.all import *
import numpy as np
import statistics
import datetime
import pyshark
import random
import pickle
import scapy
import json
import time
import csv
import sys
import os
from . import CDN_feature_picture_11
import math


# this function is for sorting sessions by total size of its packets
def session_tls_payload_total_size(session_,packet_goodness_k,session_goodness_k):
    if session_goodness_k[0]==1 or (session_goodness_k[0]==sni_number+2 and sni_number!=0):
        LEN_=0
    elif session_goodness_k[0]==2 and sni_number==0:
        LEN_=0
    elif session_goodness_k[0]>=2 and session_goodness_k[0]<=sni_number+1:
        LEN_=(sni_number+3-session_goodness_k[0])*big_number
    for indd in range(len(session_)):
        p=session_[indd]
        if packet_goodness_k[indd]!=0:
            payload_size=0
            try:
                payload_size = len(p[TCP].payload)
            except:
                payload_size=0
            LEN_+=payload_size
    return LEN_

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def full_duplex(p):
    session_ip_port_name = "Other" #bilateral session ( ip1 <---> ip2 , direction is not important)
    if 'IP' in p:
        if 'TCP' in p:
            session_ip_port_name = str(sorted(["TCP", p[IP].src, str(p[TCP].sport), p[IP].dst, str(p[TCP].dport)],key=str))
        elif 'UDP' in p:
            sesession_ip_port_namess = str(sorted(["UDP", p[IP].src, str(p[UDP].sport), p[IP].dst, str(p[UDP].dport)] ,key=str))
    return session_ip_port_name

def filename_to_label(filename):
    test_state_bool=True
    if "_" in filename:#"_" is delimiter character
        filename_first_part=filename.split("_")[0]
        filename_first_part_without_dot=filename_first_part.replace(".","")
        for char_element in filename_first_part_without_dot:
            if not(char_element>="0" and char_element<="9"):
                test_state_bool=False
                break
    else:
        test_state_bool=False
    if test_state_bool:
        filename="_".join(filename.split("_")[1:])
    reverse_indices_of_filename=list(range(len(filename)))[::-1]

    #before last dot selection
    for index_of_file_name in reverse_indices_of_filename:
        if filename[index_of_file_name]==".":
            break
        index_of_file_name=-1
    if index_of_file_name!=-1: #means that filename does not have any dot from last to first
        filename=filename[:index_of_file_name]
    return filename


def session_split_function(pcaps_location,session_splitter_mode):
    #folder address that csv and codes are in it
    
    home_address=os.path.dirname(os.path.realpath(__file__))
    # home_address=[i.strip('\n') for i in os.popen("pwd")][0]


    #IP of users must be annotated here
    with open(os.path.join(home_address,'config_parameters.json'),'r') as file_:
        config_parameters=json.loads(file_.read())
    # desired_ip=config_parameters['session_splitter']['desired_ip']
    desired_ip=[]

    # session labels of goodness== {0: bad sni || 1: general good sni names of insta that were not in our snis || 2...sni_number+1: our snis || sni_number+2: other sessions detected by ip range of facebook}
    #if delete other general sni: we have just our snis
    #after sni_dict_priority snis, as second order of priority::
    #"1" is all facebook instagram Facebook Instagram substring snis (if delete_other_general_sni==False)
    #after above all sni,as third order of priority, "sni_number+2" is IP range of FB (if not delete_other_general_sni)
    #first order of priority is 2 to sni_number+1
    sni_dict_priority=config_parameters['session_splitter']['sni_dict_priority']
    #it is ip range of facebook discovered
    facebook_ip_range=config_parameters['session_splitter']['facebook_ip_range']
    #public sni of instagram application in False mode of delete_... being one priority
    delete_other_general_sni=config_parameters['session_splitter']['delete_other_general_sni']





    badcdnSNI="xx.fbcdn"

#in order to inject one folder addresses into session splitter
# pcaps_location=sys.argv[1]
# session_splitter_mode=sys.argv[2]

    if session_splitter_mode=="train":
        train_percent=config_parameters['session_splitter']['train_test_val_percent_in_training'][0]
        test_percent=config_parameters['session_splitter']['train_test_val_percent_in_training'][0]



        



        valid_percent=100-train_percent-test_percent


        time_filter_type=config_parameters['session_splitter']['train_time_filter_type']
        time_window_start=config_parameters['session_splitter']['train_time_window_start']
        time_window_finish=config_parameters['session_splitter']['train_time_window_finish']
        time_hours_ago=config_parameters['session_splitter']['train_time_hours_ago']
        picked_label=config_parameters['session_splitter']['train_picked_label']


    elif session_splitter_mode=="test":
        train_percent=100
        test_percent=0
        valid_percent=100-train_percent-test_percent

        time_filter_type=config_parameters['session_splitter']['test_time_filter_type']
        time_window_start=config_parameters['session_splitter']['test_time_window_start']
        time_window_finish=config_parameters['session_splitter']['test_time_window_finish']
        time_hours_ago=config_parameters['session_splitter']['test_time_hours_ago']
        picked_label=config_parameters['session_splitter']['test_picked_label']

    global sni_number

    #for split cdn sessions into train, test and validation parts by random . all cdn sessions of a visit can be in one part


    #for setting batch size and maximum length of packets of any cdn session
    number_of_packet=config_parameters['session_splitter']['number_of_packet']

    #visualization parameters
    visualization_bool = False
    number_string_char=7
    imshow_bool=False
    if not visualization_bool:
        imshow_bool=False
    visualization_len=35
    row_number_total=8
    column_number_total=6

    session_picked_0=[]#0,1,2,....
    session_number_picked=1000 # after sort

    concat_sessions=config_parameters['session_splitter']['concat_sessions']
    #False#in packet level for cdn sessions

    global big_number
    big_number=1000000

    just_application_data=False
    PDU_TCP_bool=True
    PDU_TCP_bool_length=0
    PDU_SUM_BOOL=False




    picture_label_number=dict()
    fig_number_total_till_now=0

    sni_list=list(sni_dict_priority.keys())

    sni_number= len(sni_list)

    

    list_of_filenames=[ name for name in os.listdir(pcaps_location) if (not os.path.isdir(os.path.join(pcaps_location, name)) and name[-5:]=='.pcap') ]

    

    # print(list_of_filenames)
    # input("DEBUG")

    end_check=set(list_of_filenames)
    list_of_filenames.sort()
    if len(picked_label)==1:
        if picked_label[0]=='all':
            pass
        else:
            list_of_filenames=[name for name in list_of_filenames if filename_to_label(name) in picked_label]        
    else:
        list_of_filenames=[name for name in list_of_filenames if filename_to_label(name) in picked_label]
    
    
    
    # datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y%m%d%H%M%S')
    

    if time_filter_type!=0:

        dates_=[]
        remove_indices=[]
        for name_index in range(len(list_of_filenames)):
            try:
                dates_.append(datetime.datetime.strptime(list_of_filenames[name_index].split("_")[0], '%Y%m%d%H%M%S'))
            except:
                # remove_indices.append(name_index)
                dates_.append(list_of_filenames[name_index].split("_")[0])#str type date

        # remove_indices=remove_indices[::-1]
        # for name_index_to_remove in remove_indices:
        #     del list_of_filenames[name_index_to_remove]
        #     del dates_[name_index_to_remove]


        if time_filter_type==1:
            time_window_start=datetime.datetime.strptime(time_window_start, '%Y%m%d%H%M%S')
            time_window_finish=datetime.datetime.strptime(time_window_finish, '%Y%m%d%H%M%S')

            tt=time_window_finish.strftime('%Y%m%d%H%M')+'-'+time_window_start.strftime('%Y%m%d%H%M')

        elif time_filter_type==2:
            strfinish=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            
            time_window_finish=datetime.datetime.strptime(strfinish, '%Y%m%d%H%M%S')
            
            hours_ago=math.floor(float(time_hours_ago))
            minutes_ago=int((float(time_hours_ago)-float(math.floor(float(time_hours_ago))))*60.0)
            time_window_start=time_window_finish-datetime.timedelta(hours=hours_ago, minutes=minutes_ago)
            
            tt=time_window_finish.strftime('%Y%m%d%H%M')+'-'+str(hours_ago)+'hours'

        elif time_filter_type==3:
            
            
            time_window_finish=max([dates_element in dates_ for dates_element in dates_ if type(dates_element)==datetime.datetime])
            
            hours_ago=math.floor(float(time_hours_ago))
            minutes_ago=int((float(time_hours_ago)-float(math.floor(float(time_hours_ago))))*60.0)
            time_window_start=time_window_finish-datetime.timedelta(hours=hours_ago, minutes=minutes_ago)
            
            tt=time_window_finish.strftime('%Y%m%d%H%M')+'-'+str(hours_ago)+'hours'



        new_list_of_filenames=[]
        for index_num in range(len(dates_)):
            try:
                if time_window_start<=dates_[index_num] and dates_[index_num]<=time_window_finish:
                    new_list_of_filenames.append(list_of_filenames[index_num])
            except:#str type date
                new_list_of_filenames.append(list_of_filenames[index_num])

        list_of_filenames=new_list_of_filenames


    else:

        tt=datetime.datetime.today().strftime('%Y%m%d%H%M')+'-allretention'
    

    try:
        suffix_file=tt +'_'+sni_list[0] +'_' + 'not'*(not just_application_data) + "justapplicationdata_"+'not'*(not PDU_TCP_bool)+'PDU-TCP'+PDU_TCP_bool*('_'+'un'*(not PDU_SUM_BOOL) + 'summedPDU' )
    except:
        suffix_file=tt +'_' + 'not'*(not just_application_data) + "justapplicationdata_"+'not'*(not PDU_TCP_bool)+'PDU-TCP'+PDU_TCP_bool*('_'+'un'*(not PDU_SUM_BOOL) + 'summedPDU' )

    suffix_file=os.path.basename(pcaps_location)+"_"+suffix_file



    suffix_file+='_'+str(len(list_of_filenames))+"-pcapfiles"

    load_layer("tls")

    ########TCP initialization
    csvfile_TCP=open(os.path.join(home_address,suffix_file+'_train_'+str(number_of_packet)+'-packet_TCP.csv'), 'w')
    testfile_TCP=open(os.path.join(home_address,suffix_file+'_test_'+str(number_of_packet)+'-packet_TCP.csv'), 'w')
    validfile_TCP=open(os.path.join(home_address,suffix_file+'_val_'+str(number_of_packet)+'-packet_TCP.csv'), 'w')

    allfile=open(os.path.join(home_address,suffix_file+'_train_'+str(number_of_packet)+'-packet_TCP_all.csv'), 'w')

    # fieldnames_TCP = ['Length_TLS2', 'Time_TLS2', 'Direction_TLS2','Length_TLS3', 'Time_TLS3', 'Direction_TLS3', 'Label','filename',]
    fieldnames_TCP = ['Length', 'Time', 'Direction','Type','server_name','Label','filename']
    tls_flag2=0
    tls_flag3=0

    filewriter_train_TCP = csv.DictWriter(csvfile_TCP, fieldnames=fieldnames_TCP, delimiter='|',lineterminator='\n')
    filewriter_test_TCP = csv.DictWriter(testfile_TCP, fieldnames=fieldnames_TCP, delimiter='|',lineterminator='\n')
    filewriter_valid_TCP = csv.DictWriter(validfile_TCP, fieldnames=fieldnames_TCP, delimiter='|',lineterminator='\n')

    allfilewriter=csv.DictWriter(allfile, fieldnames=fieldnames_TCP, delimiter='|',lineterminator='\n')

    filewriter_train_TCP.writeheader()
    filewriter_test_TCP.writeheader()
    filewriter_valid_TCP.writeheader()

    allfilewriter.writeheader()
    
    for filename in list_of_filenames:
        try:
            rnd = random.randint(1, 100)

            pcap_file_name = os.path.join(pcaps_location,os.path.join(filename))

            label = filename_to_label(filename)

            packets = rdpcap(pcap_file_name)

            if len(packets)==0:
                continue
            base_pkt_time = packets[0].time
            global i
            i = 0

            packet_relativetime = number_of_packet*[0]
            packet_direction = number_of_packet*[0]
            packet_length = number_of_packet*[0]
            packet_Type= number_of_packet*[0]

            last_packet_protocol_type="TCP"
            sessions_=packets.sessions(full_duplex)
            sessions_keys=list(sessions_.keys())
            session_goodness=dict()
            packet_goodness=dict()

            for j in range(len(sessions_keys)):
                message=""
                this_session_key=sessions_keys[j]
                sessions_[this_session_key]=sorted(sessions_[this_session_key], key=lambda ts: ts.time-base_pkt_time)
                this_session=sessions_[this_session_key]
                packet_goodness[this_session_key]=[0]*len(this_session)
                good_session_type=[0,''] # 0:bad session, 1:good session, 2:TLS1.2, 3:TLS1.3
                indexx=list(range(len(this_session)))
                probable_future_good_packet_index=[]
                for k in indexx:
                    packet=this_session[k]
                    good_packet=0
                    if TCP in packet:
                        if  (packet[TCP].sport == 443) or (packet[TCP].dport == 443) :

                            FLAGS_=packet.sprintf('%TCP.flags%')
                            if not 'R' in FLAGS_:

                                if TLS in packet :
                                    dest_ip=packet[IP].dst
                                    src_ip=packet[IP].src


                                    if ServerName in packet[TLS]:

                                        servername_=str(packet[TLS][ServerName].servername)

                                        for temp_key_index in range(len(sni_list)):
                                            temp_key=sni_list[temp_key_index]

                                            if (temp_key in servername_) and (good_session_type[0]==0 or good_session_type[0]==1 or good_session_type[0]==sni_number+2) and ( not ( badcdnSNI in servername_ ) ):
                                                desired_ip.append(src_ip)
                                                good_session_type[0]=sni_dict_priority[temp_key]
                                                good_session_type[1]=servername_+'_'+dest_ip

                                        if not delete_other_general_sni:
                                            if (('facebook' in servername_) or ('instagram' in servername_) or ('Facebook' in servername_) or ('Instagram' in servername_)) and (good_session_type[0]==0 or good_session_type[0]==sni_number+2):
                                                good_session_type[0]=1
                                                good_session_type[1]=servername_+'_'+dest_ip


                                    src_ip=src_ip[:src_ip.rfind('.')]
                                    dest_ip=dest_ip[:dest_ip.rfind('.')]

                                    if not delete_other_general_sni:
                                        if (src_ip in facebook_ip_range or dest_ip in facebook_ip_range) and (good_session_type[0]==0):
                                            if (just_application_data and (packet[TLS].type==23 or packet[TLS].type==22 or packet[TLS].type==20)) or (not just_application_data):
                                                good_session_type[0]=sni_number+2
                                                good_session_type[1]=src_ip+"_"+dest_ip

                                    ############################### set packet goodness
                                    if not ServerName in packet[TLS]:
                                        if (just_application_data and (packet[TLS].type==23 or packet[TLS].type==22 or packet[TLS].type==20)) or (not just_application_data): #23 app data, 22server hello, 20 cypher change spec
                                            good_packet=good_session_type[0]
                                    else:
                                        if (just_application_data and (packet[TLS].type==23 or packet[TLS].type==22 or packet[TLS].type==20)) or (not just_application_data): #23 app data, 22server hello, 20 cypher change spec
                                            good_packet=good_session_type[0]
                                else :
                                    non_TLS_bool=False
                                    if (PDU_TCP_bool and good_session_type[0]!=0): #( ghablan yek TLS e khoob aghallan dide shode) for PDU
                                        if (sum(packet_goodness[this_session_key][0:k])>0):
                                            non_TLS_bool=True

                                    non_TLS_bool=False
                                    if (PDU_TCP_bool and good_session_type[0]!=0): #( ghablan yek TLS e khoob aghallan dide shode) for PDU
                                            non_TLS_bool=True

                                    if non_TLS_bool:
                                        payload_size=0
                                        try:
                                            payload_size = len(packet[TCP].payload)
                                        except:
                                            payload_size=0


                                        if 'A' in FLAGS_:
                                            if payload_size>PDU_TCP_bool_length:
                                                if 'P' in FLAGS_:
                                                    good_packet=good_session_type[0]+10 #PDU
                                                else:
                                                    good_packet=good_session_type[0]+10 # PDU
                                            else:
                                                good_packet=good_session_type[0]+100 #ACK
                                        else:
                                            if payload_size>PDU_TCP_bool_length:
                                                good_packet=good_session_type[0]+10 #PDU
                                            else:
                                                good_packet=good_session_type[0]+100 #ACK ot TLS

                    packet_goodness[this_session_key][k]=good_packet
                if good_session_type[0]==0:
                    del sessions_[this_session_key]
                    del packet_goodness[this_session_key]
                else:
                    session_goodness[this_session_key]=good_session_type
            good_keys=sorted(sessions_, key=lambda k: session_tls_payload_total_size(sessions_[k],packet_goodness[k],session_goodness[k]), reverse=True)
            session_picked=session_picked_0
            if session_picked==[]:
                good_session_numbers=min(session_number_picked,len(good_keys))
                session_picked=list(range(good_session_numbers))
            try:
                end_check.remove(filename)
            except:
                pass
            bool_end=True
            for f_element in end_check:
                if label in f_element:
                    bool_end=False
                    break
                else:
                    pass
            continue_file=True
            for j in session_picked:
                if not continue_file:
                    break
                else:
                    pass
                this_session_key=good_keys[j]
                this_session=sessions_[this_session_key]
                PDU_started_bool=False
                direction_reserved=0
                type_reserved=0
                length_reserved=0
                time_reserved=0
                servername_=session_goodness[this_session_key][1]

                for k in range(len(this_session)):
                    packet=this_session[k]
                    next_good_pcap_index=-1
                    for temp_ind in list(range(k+1,len(this_session))):
                        if packet_goodness[this_session_key][temp_ind]!=0:
                            next_good_pcap_index=temp_ind
                            break
                    if packet_goodness[this_session_key][k]!=0:
                        direction =-1
                        if IP in packet:
                            if packet[IP].src in desired_ip :
                                direction = 1
                        elif IPv6 in packet:
                            if packet[IPv6].src in desired_ip :
                                direction = 1

                        payload_size=0
                        # try:
                        #     payload_size = len(packet[TLS].payload)
                        #     ##gahi ziad bayad bashad amma sefr mishavad mesle 14.620661 file 2.0_aghamiri.pcap. haman [TCP].payload behtar bood ,sad rahmat behesh, injaa moshkele jeddi darim bayad berim rooye KASHEF
                        #     print("OK_1")
                        #     print("+++++++++++++++t=",float(packet.time)-float(base_pkt_time))
                        #     print("+++++++++++++++",payload_size)
                        # except:
                        #     print("  NO_1")
                        #     try:
                        #         input()
                        #         payload_size = len(packet[TCP].payload)
                        #         print("    YES_1")
                        #         print("------------",filename)
                        #         print("----------t=",float(packet.time)-float(base_pkt_time))
                        #         print("------------",payload_size)
                        #         #this state is for TLS: server hello, change cypher spec, encrypted handshake message
                        #         #this state is for TLS: encrypted handshake message, application data , application data , application data
                        #         #this state is for TCP: TCP with payload not pdu(good to sum)
                        #         #this state is for TCP: TCP with payload pdu(good to sum)
                        #     except:
                        #         payload_size=0
                        #         #this state is for TLS: server hello, change cypher spec, encrypted handshake message
                        #         # print("      NO__21")
                        #         #
                        #         # print("      ",len(packet[TCP].load))

                        try:
                            payload_size = len(packet[TCP].payload)
                        except:
                            payload_size=0

                        if TLS in packet:
                            if next_good_pcap_index!=-1: #next good packet existence estatement
                                if (packet_goodness[this_session_key][k]+10==packet_goodness[this_session_key][next_good_pcap_index]):# TLS -> TCP ( avvale bolook)
                                    PDU_started_bool=True
                                    type_reserved=(packet[TLS].type)+1000
                                    length_reserved=payload_size
                                    # time_reserved=(float(packet.time)-float(this__session[0].time))
                                    time_reserved=(float(packet.time)-float(base_pkt_time))
                                    direction_reserved=(packet_goodness[this_session_key][k])*direction
                                    if not PDU_SUM_BOOL: # nabayad jam zad, bayad darja nevesht
                                        packet_Type[i] = packet[TLS].type
                                        packet_length[i] = payload_size
                                        packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                        packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                        i +=1
                                else: # TLS -> TLS
                                    packet_Type[i] = packet[TLS].type
                                    packet_length[i] = payload_size
                                    packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                    packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                    i +=1
                            else:   # TLS Tamam --> benevis (not existence of next good packet in this session)
                                packet_Type[i] = packet[TLS].type
                                packet_length[i] = payload_size
                                packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                i +=1
                        else: #TCP must exit then!!!!
                            if PDU_started_bool and PDU_TCP_bool:
                                if next_good_pcap_index!=-1:  # TLS->TCP->...->"TCP"-> one good packet
                                    if (packet_goodness[this_session_key][k]==packet_goodness[this_session_key][next_good_pcap_index]): #TLS->TCP->...->"TCP"-> TCP : default:nanevis
                                        length_reserved+=payload_size
                                        if not PDU_SUM_BOOL:
                                            packet_Type[i] = type_reserved # tak tcp
                                            packet_length[i] = payload_size
                                            packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                            packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                            i +=1
                                    else: #TLS->TCP->...->"TCP"-> TLS
                                        length_reserved+=payload_size
                                        if not PDU_SUM_BOOL:
                                            packet_Type[i] = type_reserved # tak tcp
                                            packet_length[i] = payload_size
                                            packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                            packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                            i +=1
                                        else:
                                            packet_Type[i] = type_reserved
                                            packet_length[i] = length_reserved
                                            packet_relativetime[i] = time_reserved
                                            packet_direction[i] = direction_reserved
                                            i +=1
                                        PDU_started_bool=False
                                        direction_reserved=0
                                        type_reserved=0
                                        length_reserved=0
                                        time_reserved=0
                                else: #TLS->TCP->...->"TCP" | tamam
                                    length_reserved+=payload_size
                                    if not PDU_SUM_BOOL:
                                        packet_Type[i] = type_reserved # tak tcp
                                        packet_length[i] = payload_size
                                        packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                        packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                        i +=1
                                    else:
                                        packet_Type[i] = type_reserved
                                        packet_length[i] = length_reserved
                                        packet_relativetime[i] = time_reserved
                                        packet_direction[i] = direction_reserved
                                        i +=1
                                    PDU_started_bool=False
                                    direction_reserved=0
                                    type_reserved=0
                                    length_reserved=0
                                    time_reserved=0
                            else: # | TCP -> *
                                packet_Type[i] = 246 # tak tcp
                                packet_length[i] = payload_size
                                packet_relativetime[i] =  (float(packet.time)-float(base_pkt_time))
                                packet_direction[i] = (packet_goodness[this_session_key][k])*direction
                                i +=1
                                direction_reserved=0
                                type_reserved=0
                                length_reserved=0
                                time_reserved=0

                    if concat_sessions:
                        next_sample_bool=(i == number_of_packet) or ((j==session_picked[len(session_picked)-1]) and (next_good_pcap_index==-1) )
                    else:
                        next_sample_bool= (i==number_of_packet)or(next_good_pcap_index==-1)
                    if next_sample_bool:
                        if rnd <= train_percent:
                            if last_packet_protocol_type=="TCP":
                                filewriter_train_TCP.writerow({'Length': packet_length, 'Time': packet_relativetime,'Direction': packet_direction, 'Type':packet_Type,'server_name':servername_, 'Label': label, 'filename':filename})
                        elif (rnd > train_percent ) and (rnd <= train_percent+test_percent):
                            if last_packet_protocol_type=="TCP":
                                filewriter_test_TCP.writerow(
                                    {'Length': packet_length, 'Time': packet_relativetime, 'Direction': packet_direction, 'Type':packet_Type, 'server_name':servername_, 'Label': label, 'filename':filename})
                        else:
                            if last_packet_protocol_type=="TCP":
                                filewriter_valid_TCP.writerow(
                                    {'Length': packet_length, 'Time': packet_relativetime, 'Direction': packet_direction, 'Type':packet_Type, 'server_name':servername_,'Label': label, 'filename':filename})
                        if last_packet_protocol_type=="TCP":
                                allfilewriter.writerow(
                                    {'Length': packet_length, 'Time': packet_relativetime, 'Direction': packet_direction, 'Type':packet_Type, 'server_name':servername_,'Label': label, 'filename':filename})
                        if visualization_bool and rnd <= train_percent:
                            folder__=os.path.join(home_address, suffix_file)
                            try:
                                os.mkdir(folder__)
                            except:
                                pass
                            f_name=os.path.join(folder__,label+'.txt')

                            with open(f_name, 'a') as ff:
                                print(label,filename,file=ff)
                                print(" ",file=ff)
                                my_formatted_list = [str(x) for x in packet_length[:visualization_len] ]
                                my_formatted_list = [x+' '*(number_string_char-len(x)) for x in my_formatted_list]
                                print(my_formatted_list,file=ff)

                                my_formatted_list = [ '%.2f' % elem for elem in packet_relativetime[:visualization_len] ]
                                my_formatted_list = [x+' '*(number_string_char-len(x)) for x in my_formatted_list]
                                print(my_formatted_list,file=ff)

                                my_formatted_list = [ str(elem).replace('-','$') for elem in packet_direction[:visualization_len] ]
                                my_formatted_list = [x+' '*(number_string_char-len(x)) for x in my_formatted_list]
                                print(my_formatted_list,file=ff)

                                my_formatted_list = [ str(elem) for elem in packet_Type[:visualization_len] ]
                                my_formatted_list = [x+' '*(number_string_char-len(x)) for x in my_formatted_list]
                                print(my_formatted_list,file=ff)

                                print(" ",file=ff)

                            if imshow_bool:
                                plt.rc('font', size=3)
                                if not label in picture_label_number.keys():
                                    fig_number_total_till_now+=1
                                    picture_label_number[label]=[1,[fig_number_total_till_now]]
                                else:
                                    picture_label_number[label][0]+=1
                                    if picture_label_number[label][0]>column_number_total*row_number_total:
                                        fig_number_total_till_now+=1
                                        picture_label_number[label][1].append(fig_number_total_till_now)
                                        picture_label_number[label][0]=1

                                row_number=((picture_label_number[label][0]-1)//column_number_total)+1
                                col_number=((picture_label_number[label][0]-1)%column_number_total)+1

                                #now is time to imshow
                                image_matrix=[]

                                temp_list=packet_length[:visualization_len]
                                # std_=statistics.stdev(temp_list)
                                # mean_=statistics.mean(temp_list)
                                std_=500
                                mean_=500

                                if std_==0.0:
                                    temp_list2=temp_list
                                else:
                                    temp_list2=[2*(float(temp_element)-mean_)/std_ for temp_element in temp_list]
                                image_matrix.append(temp_list2)
                                image_matrix.append(temp_list2)

                                temp_list=packet_relativetime[:visualization_len]
                                # std_=statistics.stdev(temp_list)
                                # mean_=statistics.mean(temp_list)
                                std_=0.5
                                mean_=0.5
                                if std_==0.0:
                                    temp_list2=temp_list
                                else:
                                    temp_list2=[1.1*(float(temp_element)-mean_)/std_ for temp_element in temp_list]
                                image_matrix.append(temp_list2)

                                temp_list=packet_direction[:visualization_len]
                                # std_=statistics.stdev(temp_list)
                                # mean_=statistics.mean(temp_list)
                                std_=5
                                mean_=0
                                if std_==0.0:
                                    temp_list2=temp_list
                                else:
                                    temp_list2=[0.75*(float(temp_element)-mean_)/std_ for temp_element in temp_list]
                                image_matrix.append(temp_list2)

                                image_matrix_2=np.array(image_matrix)

                                fig=plt.figure(picture_label_number[label][1][-1])

                                fig.add_subplot(row_number_total,column_number_total,picture_label_number[label][0])

                                # fig, axs = plt.subplots(2, 2, subplot_kw=dict(polar=True))
                                plt.imshow(image_matrix_2)
                                #titling subplot and close fig if required
                                # temp_str=str((len(picture_label_number[label][1])-1)*column_number_total*row_number_total+picture_label_number[label][0])+" "+str(picture_label_number[label][0])
                                temp_str=str(len(picture_label_number[label][1]))+" "+str(picture_label_number[label][0])
                                temp_str+=' '+filename
                                plt.title(temp_str,size=3)

                        if visualization_bool and imshow_bool :
                            if (picture_label_number[label][0]==column_number_total*row_number_total or bool_end): # ignor rnd<train in end_bool when last file is for test in order to close fig
                                fig.savefig(os.path.join(folder__,label+' '+str(len(picture_label_number[label][1]))), dpi=800)
                                plt.close(fig)
                        i = 0
                        packet_relativetime = number_of_packet*[0]
                        packet_direction = number_of_packet*[0]
                        packet_length = number_of_packet*[0]
                        packet_Type= number_of_packet*[0]
                        if concat_sessions:
                            continue_file=False
                            break
                        else:
                            break
        except:
            print("    error___",filename)
            pass
    try:
        plt.close('all')
    except:
        pass
    csvfile_TCP.close()
    testfile_TCP.close()
    validfile_TCP.close()
    allfile.close()
    # save_object(lss,'FILE_FOR_DEBUG.pkl')

    tempstr0=suffix_file+'_train_'+str(number_of_packet)+'-packet_TCP_all.csv'
    tempstr1=os.path.join(home_address,"raw_"+tempstr0.split("_")[0]+".csv")
    tempstr0=os.path.join(home_address,suffix_file+'_train_'+str(number_of_packet)+'-packet_TCP_all.csv')
    copyfile(tempstr0, tempstr1)

    #feature_extractor_function
    csvname_in=suffix_file+'_train_'+str(number_of_packet)+'-packet_TCP.csv'
    csvname_out_all=CDN_feature_picture_11.feature_extractor_function(home_address,number_of_packet,csvname_in)

    
    

    return csvname_out_all
