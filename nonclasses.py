"""
maybe
import json
import csv
"""

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'

connected_phones={}
switch_boards={}
connected_switchboards={}
parent_switches={}

def find(area):
    if parent_switches[area]==0:
        return area
    parent_switches[area]=find(parent_switches[area])
    return parent_switches[area]


def connect_switchboards(area_1, area_2):
    if area_1 not in switch_boards:
        print(area_1," This area code does not exists.")
    elif area_2 not in switch_boards:
        print(area_2," This area code does not exists.")
    else:
        one=find(area_1)
        two=find(area_2)
        if one==two:
            print("Already connected")
        else:
            parent_switches[two]=one       
            connected_switchboards[area_1].append(area_2)
            connected_switchboards[area_2].append(area_1)



def add_switchboard(area_code):
    if area_code in switch_boards:
        print(area_code, " ,This Area Code is already exists.")
    else:
        switch_boards[area_code]=[]
        parent_switches[area_code]=0
        connected_switchboards[area_code]=[]


def add_phone(area_code, phone_number):
    if phone_number in switch_boards[area_code]:
        print(phone_number," ,This phone number already exists.")
    else:
        switch_boards[area_code].append(phone_number)


def save_network(file_name):
    f=open(file_name,"w")
    switch_size=str(len(switch_boards))+"\n"
    f.write(switch_size)
    for switchboard in switch_boards:
        area=str(switchboard)+":"
        f.write(area)
        for phone in switch_boards[switchboard]:
            ph=str(phone)+","
            f.write(ph)
        f.write("\n")
    conn_switch_size=str(len(connected_switchboards))+"\n"
    f.write(conn_switch_size)
    for switchboard in connected_switchboards:
        area=str(switchboard)+":"
        f.write(area)
        for other in connected_switchboards[switchboard]:
            oth=str(other)+","
            f.write(oth)
        f.write("\n")
    parent_switches_size=str(len(parent_switches))+"\n"
    f.write(parent_switches_size)
    for switchboard in parent_switches:
        s=str(switchboard)+":"+str(parent_switches[switchboard])+"\n"
        f.write(s)


def load_network(file_name):
    """
    :param file_name: the name of the file to load.
    :return: you must return the new switchboard network.  If you don't, then it won't load properly.
    """
    connected_switchboards.clear()
    switch_boards.clear()
    connected_phones.clear()
    parent_switches.clear()
    with open(file_name,"r") as f:
        FILE=[]
        for line in f:
            FILE.append(line)
        print(FILE)
        switchboards=int(FILE[0])
        for switchboard in range(1,switchboards+1):
            s=""
            i=0
            while FILE[switchboard][i]!=":":
                s+=FILE[switchboard][i]
                i+=1
            switch_boards[int(s)]=[]
            ph=""
            for i in range(i+1,len(FILE[switchboard])):
                if FILE[switchboard][i]==",":
                    switch_boards[int(s)].append(int(ph))
                    ph=""
                else:
                    ph+=FILE[switchboard][i]
        conn_switchs=int(FILE[switchboards+1])
        for switchboard in range(switchboards+2,switchboards+2+conn_switchs):
            s=""
            i=0
            while FILE[switchboard][i]!=":":
                s+=FILE[switchboard][i]
                i+=1
            oth=""
            connected_switchboards[int(s)]=[]
            for i in range(i+1,len(FILE[switchboard])):
                if FILE[switchboard][i]==",":
                    connected_switchboards[int(s)].append(int(oth))
                    oth=""
                else:
                    oth+=FILE[switchboard][i]
        
        parent=int(FILE[switchboards+conn_switchs+2])
        ind=switchboards+conn_switchs+3
        for switchboard in range(ind,ind+parent):
            s=""
            i=0
            while FILE[switchboard][i]!=":":
                s+=FILE[switchboard][i]
                i+=1
            oth=""
            for i in range(i+1,len(FILE[switchboard])):
                oth+=FILE[switchboard][i]
            parent_switches[int(s)]=int(oth)

def start_call(start_area, start_number, end_area, end_number):
    if start_area not in switch_boards:
        print(start_area," ,This area does not exists.")
    elif start_number not in switch_boards[start_area]:
        print(start_number," , This number does not exists.")
    elif end_area not in switch_boards:
        print(end_area," ,This area does not exists.")
    elif end_number not in switch_boards[end_area]:
        print(end_number," , This number does not exists.")
    elif find(start_area)!=find(end_area):
        print(start_area,"-",start_number," and ",end_area,"-",end_number," were not connected.")
    else:
        print(start_area,"-",start_number," and ",end_area,"-",end_number," are now connected.")
        connected_phones[start_number]=[end_area,start_number]
        connected_phones[end_number]=[start_area,start_number]


def end_call(start_area, start_number):
    if start_area not in switch_boards:
        print(start_area," ,This area does not exists.")
    elif start_number not in switch_boards[start_area]:
        print(start_number," , This number does not exists.")
    elif start_number not in connected_phones:
        print("Unable to disconnect.")
    else:
        other=connected_phones[start_number]
        del connected_phones[start_number]
        del connected_phones[other[1]]
        print("Hanging up...\nConnection Terminated.")


def display():
    for switchboard in switch_boards:
        print("Switchboard with area code: ",switchboard)
        print("\tTrunk lines are: ")
        if len(connected_switchboards[switchboard])!=0:
            for connections in connected_switchboards[switchboard]:
                print("\t\tTrunk line connection to: ",connections)
        print("\tLocal phone numbers are: ")
        for phone in switch_boards[switchboard]:
            if phone in connected_phones:
                print("\t\tPhone with number: ",phone," is connected to ",connected_phones[phone][0],"-",connected_phones[phone][1])
            else:
                print("\t\tPhone with number: ",phone," is not in use.")
        
    


if __name__ == '__main__':
    # switchboards = None  # probably {} or []
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            connect_switchboards(area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            add_switchboard(int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))
            add_phone(area_code, phone_number)
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            save_network(split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))
            start_call(src_area_code, src_number, dest_area_code, dest_number)

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))
            end_call(area_code, number)

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            display()

        s = input('Enter command: ')
