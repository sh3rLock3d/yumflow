import os
import shutil
import time

pcaps_location="C:\\Users\\user\\Desktop\\data\\archive"
target_location="C:\\Users\\user\\Desktop\\data\\new_archive"

lst=[ filename.replace("(copy)","") for filename in os.listdir(pcaps_location) if os.path.isdir(os.path.join(pcaps_location, filename)) ]


try:
    os.makedirs(target_location)
except:
    pass

for filename in lst:
    try:
        pcap_file_name  =os.path.join(pcaps_location,filename , "packets.pcap")
        new_name=os.path.basename(os.path.normpath(filename))
        ind=new_name.index('-')

        label = new_name[:ind]
        datetime_=new_name[ind+1:]

        time_string = time.mktime(time.strptime(datetime_,"%Y-%m-%d-%H-%M-%S"))



        new_name=str(time_string)+"_"+label+".pcap"
        target_file_name=os.path.join(target_location , new_name)
        shutil.move(pcap_file_name, target_file_name)

        ####png
        search_char_index_list=[i for i in range(len(datetime_)) if datetime_[i]=='-']

        i1=search_char_index_list[-2]
        i2=search_char_index_list[-1]
        datetime_2=datetime_[0:i1] +datetime_[i1+1:i2] + datetime_[i2+1:]

        shutil.move(os.path.join(pcaps_location,filename , datetime_2+'_800x600_scrot.png'), target_file_name.replace(".pcap",".png"))
    except:
        print(filename," error")
