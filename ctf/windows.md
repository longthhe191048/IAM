# Write Up
## Material
* Challenge provides: an .EXE file

## Walkthrough 
I first open the challenge in ida

<img width="2547" height="1522" alt="image" src="https://github.com/user-attachments/assets/c87ff72c-6129-4f55-b0b2-8671051ebc0a" />

At the start of the program, it point to another function, follow that

<img width="2553" height="1420" alt="image" src="https://github.com/user-attachments/assets/7d6e0074-80f5-48dd-b63d-feba93add979" />

open pseudocode of them

<img width="1040" height="1003" alt="image" src="https://github.com/user-attachments/assets/bcf7ff68-ddde-4680-883a-9f6ec2b35cef" />

It call 
```
v0 = sub_401360(dword_4E4004);
```
and also give us return value after exit, this should be our main function. let's follow to `sub_401360`

<img width="2557" height="1429" alt="image" src="https://github.com/user-attachments/assets/f3300f62-3871-413d-b46d-a4adaa6a0a34" />

Here, i notice 2 thing: 
* This program will check if our input is the flag

<img width="1314" height="368" alt="image" src="https://github.com/user-attachments/assets/d6aa8817-d23f-4752-a3f2-59394823e6be" />

<img width="1456" height="604" alt="image" src="https://github.com/user-attachments/assets/c64de85c-0bb2-46f0-82af-e943153ed689" />

* And most of other case in the switch is to craft the flag, if wrong go to `case 99`

<img width="1159" height="507" alt="image" src="https://github.com/user-attachments/assets/4f166ea9-9c0e-4f91-a923-72f4b6a5aa6b" />

The way it craft after 28 switches is
```
            LOBYTE(v34) = v49 ^ *(_BYTE *)sub_4BCF00(27);
            if ( (_BYTE)v34 == *(_BYTE *)sub_4B894C(27) )
              v30 = 100;
            else
              v30 = 99;
```
traceback to `v34`, we can see this

<img width="1056" height="475" alt="image" src="https://github.com/user-attachments/assets/3ff9d417-cbf8-437c-90d9-8103d4d06e93" />

So `v34` is to store the address of `v45`

As we can understand, each switch will go to the corressponding position from `v45`, xor it with `-52`. I will extract their value, make it xor with `-52` or `0xCC`.

```
signed = [
 -118, 0x80, -115, -117, -73, -113, -118, -117,
 -109, -8, -94, -88, -109, -8, -94, -72,
 -3, -109, -120, -82, -85, -109, -98, -4,
 -81, -89, -106, -79
]
key = 0xCC

flag = bytes([(b & 0xFF) ^ key for b in signed])
print(flag.decode('ascii'))
```

<img width="2534" height="1438" alt="image" src="https://github.com/user-attachments/assets/76615c32-7de4-4707-abfd-e47b018044fc" />

Testing the flag

<img width="1251" height="498" alt="image" src="https://github.com/user-attachments/assets/b66f2fab-0125-439e-a59a-5efc3ebdedca" />

FLAG: `FLAG{CFG_4nd_4nt1_Dbg_R0ckZ}`
