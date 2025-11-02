# Crackme 6

## Objective
* Remove the starting Nag Screen
* When the button Re-Check is clicked, a pop-up messagebox appears and you should set it to say “Thank you for registering this software”
* Set the Status box text to: “Clean crack! Good Job!”

<img width="1835" height="1238" alt="image" src="https://github.com/user-attachments/assets/c26e06cb-d839-4656-aabb-f80836937797" />

## Write up
Doing as always

<img width="1822" height="1000" alt="image" src="https://github.com/user-attachments/assets/952bbcac-27b6-411c-ba9a-ef8b54f3cc15" />

<img width="700" height="689" alt="image" src="https://github.com/user-attachments/assets/ad6ee332-46f0-4219-8da6-38a01c848113" />

Open it in `IDA`

<img width="2543" height="1508" alt="image" src="https://github.com/user-attachments/assets/bdc1cfc3-8eb8-431c-b734-bb3a0c79947b" />

In the `start` function, we can't see anything about nag. Go to `DialogueFunc`

<img width="1991" height="895" alt="image" src="https://github.com/user-attachments/assets/5829012a-9e2e-4898-afb3-951e3fda7d03" />

First, i will deal with the nag

<img width="1750" height="1009" alt="image" src="https://github.com/user-attachments/assets/2ef43e52-5428-4d82-a8f6-f82aadc9071d" />

convert
```
jz      short loc_401096
```
to
```
jmp     short loc_4010BD
```
this will lead directly to the clean crack and remove the nag. I will deal with the re-check button

<img width="2027" height="851" alt="image" src="https://github.com/user-attachments/assets/a1b3f8bb-778e-43d3-ba8e-74f02f9f5b7e" />

As in this function, it will directly go to the `nag not removed` dialogue when we click on the check button.

convert
```
jz      short loc_401117
```
to
```
jmp     short loc_401128
```

<img width="2053" height="974" alt="image" src="https://github.com/user-attachments/assets/97d2f709-acd2-4d21-80a7-51e2acc47143" />

Patch the program and test it

<img width="535" height="540" alt="image" src="https://github.com/user-attachments/assets/4e201a46-45e1-4843-8bac-4a98654f356b" />

<img width="734" height="728" alt="image" src="https://github.com/user-attachments/assets/0b63568d-4d95-42ec-a72c-13758f2ac0ed" />
