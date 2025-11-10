# Write Up
## Material
* A Binary File

## Walkthrough
Open the binary file in `IDA`

<img width="2554" height="1421" alt="image" src="https://github.com/user-attachments/assets/4a6c98ba-0429-4525-acfb-dc720022c7de" />

Open it in pseudocode

<img width="2175" height="1020" alt="image" src="https://github.com/user-attachments/assets/db363a1c-54dc-44c6-b518-e472d27238dc" />

What i know is it `check_flag` function, then return for me if it's correct or not. Go to the `check_flag` function and check their pseudocode

<img width="1659" height="974" alt="image" src="https://github.com/user-attachments/assets/5f8b5eef-8e33-4030-bd88-315fb68de65b" />

look like we can obtain some informaition. First is it do a xor to obtain the flag

```
initial_key ^ (unsigned __int8)s[i]) != *((_BYTE *)v2 + i
```

it goes 18 bytes, and get value from `v2`. But the total bytes from `v2` = 16, and look at this line
```
  _DWORD v2[4]; // [esp+2h] [ebp-26h]
  __int16 v3; // [esp+12h] [ebp-16h]
```
it craft `v2` with 16 bytes and `v3` with 2 bytes, in a total of 18 bytes. Let's check initial key

<img width="967" height="323" alt="image" src="https://github.com/user-attachments/assets/5a3ff3cd-2af0-452a-83f4-7f6cc612b287" />

So initial key = `66` or `0x42`. Crafting a script to solve it
```
import struct

v2 = [-149475292, -823739183, 1060455757, -1748967140]
v3 = -32317

expected = b''.join(struct.pack('<i', x) for x in v2) + struct.pack('<h', v3)

def recover(initial_key):
    key = initial_key
    s = []
    for b in expected:
        s.append(key ^ b)
        key = (key + 26) & 0xFF
    return bytes(s)

print(recover(0x42).decode('ascii'))  
```
which to craft v2 and v3 to a struct, call a list and do the xor with the key = 0x42, increment by 26 each step

<img width="1830" height="579" alt="image" src="https://github.com/user-attachments/assets/ed3c2ef7-0828-42e6-8d5a-506dce15127a" />

test

<img width="909" height="351" alt="image" src="https://github.com/user-attachments/assets/e6adeef2-e409-4935-96d2-dc39f016bac5" />

Flag: `flag{x86_is_fun_!}`
