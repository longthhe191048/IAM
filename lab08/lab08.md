# Lab08
## Objective
* Basic static Analysis Technique
* Basic dynamic Analysis Technique

## Requirement
* Any windows vm's
* Kali linux vm's that already setup inetsim
* windows server 2008
* lab01 folder

## Lab walkthrough
### Basic Static technique
#### Lab01-01.exe

Uploading `Lab01-01.exe` and `Lab01-01.dll` to [Hybrid Analysis](https://www.hybrid-analysis.com/)

<img width="1920" height="1080" alt="dll" src="https://github.com/user-attachments/assets/6c43e652-0574-43ea-9dd1-d46e2a1044b3" />

<img width="1920" height="1080" alt="exe" src="https://github.com/user-attachments/assets/35339796-c844-43e4-a25a-e89f6ab6d11a" />

Look at the incident respond tab:

<img width="1237" height="354" alt="image" src="https://github.com/user-attachments/assets/b42e0954-d4d9-48f2-8d7d-927a893ce96c" />

<img width="1121" height="311" alt="image" src="https://github.com/user-attachments/assets/84087694-1610-4d11-9fd2-ff873269c797" />

Use `PE-Bear` to see the PE File. For lab requirement, just find the `Timestamp`

<img width="1917" height="1080" alt="image" src="https://github.com/user-attachments/assets/56482845-246c-4287-b549-28332cf2d32a" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3540aea8-eb0e-4022-a06e-8002e6f0445a" />

Look at `import` section

<img width="1345" height="335" alt="image" src="https://github.com/user-attachments/assets/d86ecb25-c633-48a4-9658-366bb6833194" />

<img width="1301" height="323" alt="image" src="https://github.com/user-attachments/assets/e1b7691b-9912-4b3b-b299-d7a5fcbd819c" />

for the `dll` file, it create a process, `exe` file is creating a file

Look at `Strings` section

<img width="1304" height="646" alt="image" src="https://github.com/user-attachments/assets/88b8a92b-9169-4c24-90b7-c9e1b9137c68" />

<img width="1290" height="615" alt="image" src="https://github.com/user-attachments/assets/e206a6e8-fb27-4bd5-a016-f2db28d94c15" />

We've gather some data: the `exe` file will run `dll` file, it should do something with the ip `127.26.152.13`

Examine `diasm` and using `PEid` to gather some info

<img width="1912" height="1080" alt="image" src="https://github.com/user-attachments/assets/115d834f-02d7-4eb3-961f-c61a4119822e" />

Examine `exe` file with `Dependency walker`. Dependency walker is a tools to show which DLLs it depends on and whether anything is missing or mismatched

<img width="1182" height="647" alt="image" src="https://github.com/user-attachments/assets/49cdc784-46f5-40e4-9cb4-07107ff528dd" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/df0ae437-da2a-40c0-b938-8eca27c37faf" />

Examine `dll` file with `Dependency walker`

<img width="1916" height="1072" alt="image" src="https://github.com/user-attachments/assets/82685da1-70d3-47bc-bd93-c609c00877b7" />

We can see it perform networking task such as `accept`, `bind`, `connect`

#### Lab01-02.exe

Uploading `Lab01-02.exe` to [Hybrid Analysis](https://www.hybrid-analysis.com/)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ce3d6feb-f2b1-4dc0-80e1-1515823a5aa8" />

<img width="1161" height="409" alt="image" src="https://github.com/user-attachments/assets/2e89ea76-16cb-421a-ab79-7811e7dae892" />

View in `PE-bear`

<img width="1916" height="1077" alt="image" src="https://github.com/user-attachments/assets/92afa939-51bf-4a29-bc71-1c011bfb94a2" />

<img width="1920" height="1079" alt="image" src="https://github.com/user-attachments/assets/7bcaa026-3ab4-43f5-a542-cafc2725fb77" />

<img width="1878" height="1062" alt="image" src="https://github.com/user-attachments/assets/75c19d6e-560c-40fc-94cf-14850cd94e7b" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/9daa0f88-860c-4a68-8383-4508631f9cf4" />

As we look through everything in the `import` section, we can see it `Create Service`, `open to internet`

Look in `String`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3d5c4aee-4540-44b8-b0a3-fb3227183bbb" />

we could see some http url in string section. Open `PEid`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bf12d46e-bdd6-499f-bc07-782c319b98d9" />

We could see that in `EP section`, it said `UPX1`, so it's not a real code. We will unpack it

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3fbd090f-9bc6-4bfb-8933-2f3b5833efb5" />

Checking with `PEid`

<img width="502" height="298" alt="image" src="https://github.com/user-attachments/assets/84717e8f-b7f5-42a0-908a-fac1146446c1" />

Look again in `PE-bear` with the unpacked `exe`

<img width="1918" height="1067" alt="image" src="https://github.com/user-attachments/assets/1782c183-7cd2-46cc-8c12-fdef74fef03c" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2a328e32-b069-4bce-addd-630364ca0c7d" />

<img width="1917" height="1079" alt="image" src="https://github.com/user-attachments/assets/4165b38f-5b14-489a-a5b1-ce0e7787c3e8" />

<img width="1917" height="1078" alt="image" src="https://github.com/user-attachments/assets/a27f1167-dd71-4fcd-978e-444749888202" />

Back in `Strings` section

<img width="1918" height="1074" alt="image" src="https://github.com/user-attachments/assets/f5e31fd9-d8a2-419d-86e8-c311e5669d30" />

So it create connection to `http://www.malwareanalysisbook.com`

### Basic Dynamic technique

Look at `Lab03-01.exe` in `Pe-bear`

<img width="1920" height="1077" alt="image" src="https://github.com/user-attachments/assets/55de1e72-ede9-4ba3-bbee-76e78dc33ed4" />

<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/5d605264-cbf9-449f-8004-8d96af8c634c" />

We could not see anything special in `import` section but various stuff in `Strings` section where it also doing something with `www.practicalmalwareanalysis.com` and Registry. Now we will run a dynamic analysis. I will run `inetsim` on kali linux and set it dns Ref: [lab01](https://github.com/longthhe191048/IAM/blob/main/Lab_01/Lab01.md)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3b3d5f60-3edc-4267-9248-ac150fa9a897" />

<img width="1584" height="911" alt="image" src="https://github.com/user-attachments/assets/c3baa01e-20c0-4b6f-94fd-9558f99bf42b" />

<img width="1914" height="1068" alt="image" src="https://github.com/user-attachments/assets/0703bb7a-3451-4aa9-8c22-267ef66868e3" />

Open `wireshark`, `Process monitor`, `Process Explorer`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/406ae91d-7801-4b53-8c41-aa24ccf64413" />

Now run the file. In the `Process Explorer`, navigate to `explorer.exe`

<img width="1329" height="682" alt="image" src="https://github.com/user-attachments/assets/19a60232-70d5-403c-975a-b797e1d7abcc" />

<img width="763" height="472" alt="image" src="https://github.com/user-attachments/assets/76256552-9fce-4d72-b983-2bde413b89e9" />

Scroll down, we can see ws2_32.dll, which has function of network

<img width="756" height="302" alt="image" src="https://github.com/user-attachments/assets/ccffbe94-6a6c-4860-9af9-6bec3a9e246f" />

Go to `process monitor`

<img width="897" height="553" alt="image" src="https://github.com/user-attachments/assets/7284312a-704c-438f-91be-7fa871c2ea3f" />

After a quick glance, we can see at least 3 suspicious operation: `Write File`, `RegSetValue`, `TCP send`. Let's filter them

<img width="1917" height="1078" alt="image" src="https://github.com/user-attachments/assets/9f3a860c-9190-4a7c-8e07-ad48ea11b3bc" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f405c453-bc43-48a9-a80e-da24e4cc06d3" />

<img width="1920" height="1076" alt="image" src="https://github.com/user-attachments/assets/78f6a673-e72d-4636-9ef1-f2b82293e3c0" />

Open `Wireshark`

<img width="1920" height="1076" alt="image" src="https://github.com/user-attachments/assets/cd7f40e5-30cc-421b-87e3-d50a3e4ed879" />

`inetsim` log

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/837f64a4-92e7-45e3-a3de-f13bea2c2a59" />



