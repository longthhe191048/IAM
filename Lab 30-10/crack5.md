# Crackme 5
## objective
* Enter your first name.
* Crack the software to find a valid serial key for your firstname

<img width="1731" height="1030" alt="image" src="https://github.com/user-attachments/assets/ab2a0b60-5fe8-4ef2-89af-02fbce448164" />

## Writeup
Create a backup and run the program

<img width="1867" height="1056" alt="image" src="https://github.com/user-attachments/assets/c973aa7a-f765-4167-9de2-3371941cefb8" />

<img width="678" height="531" alt="image" src="https://github.com/user-attachments/assets/ab638849-7be4-4920-a33a-178a747596c5" />

Typing my name into `first name` and `serial key`

<img width="777" height="531" alt="image" src="https://github.com/user-attachments/assets/33e6ca7f-bfa7-4325-8cc3-9d7b3563cecb" />

Open the program in `IDA`

<img width="2542" height="1509" alt="image" src="https://github.com/user-attachments/assets/b9ca9e34-a558-40f8-8739-0032517a2254" />

There is nothing special in `WinMain`, continue to `DialogueFunc`

<img width="2049" height="954" alt="image" src="https://github.com/user-attachments/assets/19423350-7258-4503-87f2-e9ec0a55af90" />

As we can see here is how it obtain the serial key

**Format**
```
firstname-<year+1234><month><day>
```
My current time when doing this writeup

<img width="856" height="329" alt="image" src="https://github.com/user-attachments/assets/c3124d97-1cd1-45d5-ab89-3d55be770258" />

So i can craft a serial key like: `wdchocopie-3259112`

<img width="1125" height="677" alt="image" src="https://github.com/user-attachments/assets/59a9f8d2-10aa-4dcf-98b8-ba5f5df12e08" />
