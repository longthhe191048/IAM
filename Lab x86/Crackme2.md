# Crack me 2 Write up
## Objective
* Without patching, Register it to your name.

## Write up
Fristly, i installed the challenge file, make a backup and run it

<img width="1974" height="1044" alt="image" src="https://github.com/user-attachments/assets/4bc08aee-2ec4-4188-80c4-00f47770ea7d" />

<img width="697" height="383" alt="image" src="https://github.com/user-attachments/assets/9d2aa826-5c0f-48c0-8410-d0650649821b" />

Open in `IDA`, look at the `WinMain` Function

<img width="1333" height="723" alt="image" src="https://github.com/user-attachments/assets/4cae3c8d-0fe5-4898-8d88-53bcf360f75b" />

Overhere, we can see it call `CreateFileA`, calling name `"keyfile.txt"`.

<img width="1191" height="791" alt="image" src="https://github.com/user-attachments/assets/2c83ae6a-cce4-4676-92de-b76fe67914cc" />

Look at the bottom, we can see it calling string from `keyfile.txt` and set it as register name. Let's test it

<img width="2184" height="1219" alt="image" src="https://github.com/user-attachments/assets/ba10cf68-1a89-44cf-acb0-ffcd420b6931" />
