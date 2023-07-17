
# CISCO Checker

This project aims at helping cybersecurity teams to establish vulnerability reports about their CISCO switches (it only concerns IOS and IOS XE firmwares but it can be changed pretty quickly). It can be a good alternative if you don't have access to the CISCO OpenVuln API.
## Run Locally

Clone the project

```bash
  git clone https://github.com/hanteed/cisco-checker
```

Go to the project directory

```bash
  cd cisco-checker
```

Run the code

```bash
  python3 cisco.py
```

## Documentation

The project will take an file in input corresponding to the versions wich are going to be exported, each version has to be written on a single line (the file can contain duplicates and will filter useless information). After executing the code, a log folder "Output" will be created, containing the different versions of the firmwares (IOS & IOS XE) in files of 50 lines maximum. The program will also forge and open URLs in which the versions will be written so you can directly export all data without having to fill in every version by hand (you will just be asked to complete the captcha if prompted), you can edit the levels of dangerosity you want to be applied (Critical,High,Medium,Low) at the beginning of the program. 

Firmware file example :

```
17.3.4b
17.3.4b
17.3.5
17.3.5
15.2(2)E8
17.3.5
16.3.6
17.3.4
#N/A
17.3.4
17.3.4
15.2(7)E5
15.2(7)E5
15.2(7)E
15.2(7)E, RELEASE SOFTWARE (fc3)
```