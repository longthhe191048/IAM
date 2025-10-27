# Crack me 3 Write up
## Objective 
* Remove the 2 nag screens – one at startup and one at close of program.
* In the About screen – change status to Registered.
<img width="1252" height="1222" alt="image" src="https://github.com/user-attachments/assets/5a17e1d8-73c1-4b4e-ba49-c97d4ae01ede" />

## Write up
Fristly, i installed the challenge file, make a backup and run it

<img width="2022" height="1100" alt="image" src="https://github.com/user-attachments/assets/4301f2f7-719f-4531-9707-8cf78a9e003d" />

<img width="2088" height="1130" alt="image" src="https://github.com/user-attachments/assets/da55216d-29a7-4ad8-948f-bbb70a15a2e3" />

<img width="1108" height="688" alt="image" src="https://github.com/user-attachments/assets/9002090d-c615-455e-8f86-d45c647e42af" />

<img width="1144" height="555" alt="image" src="https://github.com/user-attachments/assets/84176c9c-115c-45d9-9a0d-50b6d5d1274e" />

Open it in `IDA` and look at `WinMain`

<img width="2553" height="1438" alt="image" src="https://github.com/user-attachments/assets/6d8bd1a6-c7ed-49db-ba62-ae0a5fa83a1a" />

We saw it do a `CreateDialogueParamA`, after that calling the opening nag. I found that we can skip it by modified `jnz` to `jz`
```
jz     short loc_401044
```
<img width="1436" height="896" alt="image" src="https://github.com/user-attachments/assets/2eb95d3b-ff47-4014-8a49-a5d6209b79da" />

Go to `DialogueFunc`, we see it call `closing nag` and checking register status

<img width="2554" height="1517" alt="image" src="https://github.com/user-attachments/assets/ac4caf27-f72a-4095-b96a-a81fdb90b125" />

First, i will deal the register status by changing `jz` instruction to `jnz` as it will be the opposite of original instruction

```
jnz      short loc_4010EC
```

<img width="922" height="370" alt="image" src="https://github.com/user-attachments/assets/09ecd5fa-3bd2-4dae-9981-e28e6fd6d000" />

Now let work around with the `closing nag`

<img width="952" height="425" alt="image" src="https://github.com/user-attachments/assets/5d1d6f01-117b-4c6e-8a77-c67cd2e6943c" />

As in the `closing nag`, it already call `PostQuitMessage` from [WinAPI32](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-postquitmessage), which request to terminate the program. I will use `nop` instruction to bypass all of them

Original instruction
```
loc_4010FF:             ; nCmdShow
push    0
push    hWnd            ; hWnd
call    ds:ShowWindow
push    0               ; uType
push    offset aClosingNag ; "Closing Nag"
push    offset Text     ; "I am a nag screen\nPlease remove me."
push    0               ; hWnd
call    ds:MessageBoxA
push    0               ; nExitCode
call    ds:PostQuitMessage
```

Modified Instruction
```
loc_4010FF:
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
push    0               ; nExitCode
call    ds:PostQuitMessage
```

<img width="485" height="783" alt="image" src="https://github.com/user-attachments/assets/eafc77b4-986b-4f48-a28d-f231c73a2c0e" />


Patch the program and run it

<img width="1148" height="640" alt="image" src="https://github.com/user-attachments/assets/849a6764-cd13-4f66-9b12-5e98b5463243" />
