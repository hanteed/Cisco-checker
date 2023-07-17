import os
import webbrowser

# List of IOS & IOS XE prefixes :
# IOS Software : 15/12
# IOS XE Software : 3/16/17

dangerlevel1 = "critical,high"
dangerlevel2 = "critical,high"
IOSprefix = ["15","12"]
outputdirectory = "Output"
firmwarefile = 'firmwares.txt'


def firmwares_check():
        if not os.path.isfile(firmwarefile):
            print(f"File '{firmwarefile}' containing firmware versions not found, creating it...")
            f = open(firmwarefile, "a")
            f.close()
            print(f"File '{firmwarefile}' has been created, please fill out firmware versions.")
            exit()
        else:
            if os.stat(firmwarefile).st_size == 0:
                print(f"File '{firmwarefile}' containing firmware versions seems empty, please fill it.")
                exit()


def ciscocheck():
    firmwares_check()
    global ciscolist
    try:
        ciscolist = [line.strip() for line in open(firmwarefile)]
    except:
        print("An error occured while parsing the file.")
   
    ioslist = []
    iosxelist = []
    filterwords = ["#N/A",""]

    sortedset = set(ciscolist)
    sortedlist = list(sortedset)
    sortedlist.sort()

    for i in range(len(sortedlist)-1):
        sortedlist[i] = sortedlist[i].split(',')[0]
        sortedlist[i] = sortedlist[i].split(' ')[0]
        if sortedlist[i] not in filterwords:
            if sortedlist[i].split(".")[0] in IOSprefix:
                ioslist.append(sortedlist[i])
            else:
                iosxelist.append(sortedlist[i])

    iosset = set(ioslist)
    iossortedlist = list(iosset)
    iossortedlist.sort()

    iosxeset = set(iosxelist)
    iosxesortedlist = list(iosxeset)
    iosxesortedlist.sort()
    
    return iossortedlist,iosxesortedlist


def ciscoexport(firmwarelist,prefix):
    if not os.path.exists(outputdirectory):
        os.makedirs(outputdirectory)

    sublists = [firmwarelist[i:i+50] for i in range(0, len(firmwarelist), 50)]

    for i, sublist in enumerate(sublists):
        filename = f"{outputdirectory}/{prefix}_data_{i+1}.txt"
        with open(filename, 'w') as outfile:
            for firmware in sublist:
                outfile.write(str(firmware) + '\n')
    
    sublist.reverse()
    url = ','.join(sublist)
    return url


def urlforge(OS,versions,impact):
    temp = []

    if OS == "IOS":
        OS = "ios"

    elif OS == "IOSXE":
        OS = "ios_xe"

    impact = impact.split(',')
    for i in impact:
        temp.append(i.capitalize())        
    impact = temp.copy()
    impact = ','.join(impact)

    if impact.capitalize() == "All" or impact.capitalize() == "" or impact.capitalize() == None or impact.capitalize().isspace():
        return "https://sec.cloudapps.cisco.com/security/center/softwarechecker.x?productSelected="+OS+"&selectedMethod=C&platformCode=NA&versionNamesSelected="+versions+"&allAdvisoriesSelectedByTree=N&advisoryType=0&iosBundleId=cisco-sa-20230322-bundle&isFewCheckBoxChecked1=false&isNoneCheckBoxsChecked1=true#~onStep3"
    else:
        return "https://sec.cloudapps.cisco.com/security/center/softwarechecker.x?productSelected="+OS+"&selectedMethod=C&platformCode=NA&versionNamesSelected="+versions+"&allAdvisoriesSelectedByTree=N&advisoryType=0&iosBundleId=cisco-sa-20230322-bundle&impact="+impact+"&isFewCheckBoxChecked1=false&isNoneCheckBoxsChecked1=true#~onStep3"
        

def main():
    res = ciscocheck()
    ios = res[0]
    iosxe = res[1]
    IOSVERSIONS = ciscoexport(ios,"IOS")
    IOSXEVERSIONS = ciscoexport(iosxe,"IOSXE")

    # Levels of dangerousness : Critical,High,Medium,Low
    webbrowser.open(urlforge("IOS",IOSVERSIONS,dangerlevel1),"\n")
    webbrowser.open(urlforge("IOSXE",IOSXEVERSIONS,dangerlevel2))


main()