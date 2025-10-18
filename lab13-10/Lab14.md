# Lab 14
## Objective
* Understanding ADS (Alternate Data Stream)
* Hide data in ADS
* Using TSK or Autopsy to detect
* Understanding SIA, FNA

## Pre-Lab Knowledge
### ADS
* ADS (Alternative Data Stream) are feature of Windows NTFS file system where in a file can have multiple Data Stream.
* Each stream can contain multiple data such as metadata, additional information

### SIA
* SIA or Standard Information attribute
* is the way system views the file.
* Store metadata of the file

### FNA
* FNA or File Name Attribute
* is the way directory see the file.
* Tracks name, location, and size

## Lab walkthrough
### Create a ADS with a file
First i will create a file name `a.txt`

<img width="2876" height="1800" alt="image" src="https://github.com/user-attachments/assets/8cdcdec9-1acd-43c5-82e2-d6c8f306604f" />

Then create ADS with `:`, EX: `a.txt:secret.txt`

<img width="2799" height="1089" alt="image" src="https://github.com/user-attachments/assets/951ceaf9-3938-4e2e-934a-a9abe3322495" />

We can view it by using 
```
more < a.txt:secret.txt
```
<img width="1255" height="323" alt="image" src="https://github.com/user-attachments/assets/0d945980-7bdd-46b1-8fd1-c8000da1d46e" />

I also has my work on what ADS can do [here](https://github.com/longthhe191048/IAM/blob/main/win32api/Extra.md)
### Detect ADS
After working with ADS, we would wonder if there is any ways to find if file has multiple datastream? i will create more ADS for `a.txt` for now so we can see the example

<img width="1124" height="269" alt="image" src="https://github.com/user-attachments/assets/b0ca9536-719f-4382-b4c2-57144141d46f" />

We can find if file has multiple ADS and their names by using this command in powwershell
```
Get-Item -LiteralPath 'a.txt' -Stream *
```

<img width="2038" height="1486" alt="image" src="https://github.com/user-attachments/assets/6c4515c3-4b00-4e81-b564-078cafaad07b" />

## Reference
[Alternate Data Streams: A Complete Overview](https://www.ninjaone.com/blog/alternate-data-streams/)
[File System Date](https://www.sciencedirect.com/topics/computer-science/file-system-date)
[Detecting timestamp changing utilities](https://www.forensickb.com/2009/02/detecting-timestamp-changing-utlities.html)
