# Crack me 1 Writeup
## Objective
* Find the serial key and enter in the textbox
* Patch the file to always show the Congrats message when button Check is clicked

<img width="1888" height="1296" alt="image" src="https://github.com/user-attachments/assets/09d268f7-89ae-4f0e-9e4c-16ebe7fee320" />

## Writeup
Fristly, i installed the challenge file, make a backup and run it

<img width="2221" height="1200" alt="image" src="https://github.com/user-attachments/assets/c3f5111c-f3aa-4991-9172-51defcae25d8" />

<img width="600" height="474" alt="image" src="https://github.com/user-attachments/assets/da0bc3d5-f632-483c-9962-6b538e644b12" />

As we can see, they prompt for a serial key, i will tried to type in something

<img width="779" height="487" alt="image" src="https://github.com/user-attachments/assets/52f0ae3b-1417-474d-9f69-c92ee6b8a7a0" />

So we need to find correct key for it, let's look at the program in `IDA`

<img width="2549" height="1471" alt="image" src="https://github.com/user-attachments/assets/342d662c-8aa4-43e0-9a93-f24360802ab8" />

I first look through in the `DialogueFunc` because it might contain something about the message that we saw earlier

<img width="1666" height="585" alt="image" src="https://github.com/user-attachments/assets/1cf237a1-3795-4323-ad8c-f452a18d92bb" />

And in the first part, i need to find what is the serial key, so i look clearly in the function and see this

<img width="1030" height="570" alt="image" src="https://github.com/user-attachments/assets/e64cbf91-1117-463d-bdf1-20f50d4ffbf2" />

After putting `cr4ckingL3ssons` in `ecx`, it will try to do `strcmp`. Let's look at pseudocode

<img width="1361" height="927" alt="image" src="https://github.com/user-attachments/assets/6aff0732-9c16-4a46-8874-006d115e5b78" />

So it actually a serial key. Test in the prgram

<img width="1417" height="849" alt="image" src="https://github.com/user-attachments/assets/5083c9cd-0803-4af9-8954-bfead135c890" />

Back to the `IDA`, i will try to patch the program. I saw at the funtion were it determind which message will be shown.

<img width="1576" height="426" alt="image" src="https://github.com/user-attachments/assets/0250cc7e-0a7f-49e9-82f7-ba79a76b44a5" />

So to work with the next objective, we have 2 ways:
* Changing the logical so `ZF = 1`, and the `jnz` won't work
* Changing text in `loc_401154:` so it the same with correct answer

I will do it in the first way. i modified this line 
```
test    eax, eax
```
to 
```
xor     eax, eax
```
as this will do a `xor` to itself, which the result = 0, will lead `ZF = 1`, which not trigger the `jnz` instruction  

<img width="532" height="216" alt="image" src="https://github.com/user-attachments/assets/b94fda20-f640-4c25-9e78-e061ff33f3fb" />

Checking after patching

<img width="1448" height="634" alt="image" src="https://github.com/user-attachments/assets/99d5abc5-1174-453e-90c9-aae38eacbf4a" />

