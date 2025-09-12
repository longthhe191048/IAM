# LAB 1: Setting Up Environment
## Requirement
- kali linux
- Win2008Malware.7z

## pre-Lab knowledge
- This lab will be focusing on running Inetsim as an **dns** and **HTTP** service
- Inetsim: a software allows to simulate common internet services in a lab enviroment.
- This can help us to analyze behavior of unknown malware
Some of the service it can replicate:

| Dịch vụ | Cổng | Giao thức  |
|---------|------|------------|
| dns     | 53   | udp/tcp    |
| http    | 80   | tcp        |
| https   | 8443 | tcp        |
| smtp    | 25   | tcp        |
| irc     | 6667 | tcp        |
| smtps   | 465  | tcp        |
| ntp     | 123  | udp        |
| pop3    | 110  | tcp        |
| finger  | 79   | tcp        |
| syslog  | 514  | udp        |
| tftp    | 69   | udp        |
| pop3s   | 995  | tcp        |
| time    | 37   | tcp        |
| ftp     | 21   | tcp        |
| ident   | 113  | tcp        |
| ftps    | 990  | tcp        |
| daytime | 13   | tcp/udp    |
| echo    | 7    | tcp/udp    |
| discard | 9    | tcp/udp    |
| quotd   | 17   | tcp/udp    |
| chargen | 19   | tcp/udp    |
| dummy   | 1    | tcp/udp    |

## Topology
```
(Isolated lab network, e.g., Host-Only)

┌────────────────────────────┐            DNS + all services → Kali
│  Windows Server 2008       │  DNS: 192.168.109.133  ─────────────▶
│  (Target / Client)         │                                    ┌───────────────────────┐
│  IP: 192.168.109.X/24      │◀────────── all traffic (HTTP/FTP/…)│  Kali Linux           │
└────────────────────────────┘                                    │  IP: 192.168.109.133  │
                                                                  │  INetSim              │
                                                                  └───────────────────────┘

```
## Lab walkthrough and explaination
1. Start the `kali` VM and set it's [network mode](https://github.com/longthhe191048/IAM/blob/main/Lab_01/Network_Mode_VMware.md) to NAT or bridge. I prefer for NAT because we just need both of our VMs can connect to each other.

<img width="2879" height="1800" alt="image" src="https://github.com/user-attachments/assets/ee02928d-3b6d-427d-80bc-63d2a31a57f0" />


2. We will need to check if `kali` has an ip address. We will use `ip a` or `ifconfig`

 <img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/60c32142-fb7e-4e3b-91ea-40941861eebe" />

My `kali` ip: `192.168.109.133`
**NOTE**: if it doesn't have an ip address, you can use this command to get one using DHCP `dhclient`

3. I will configure **Inetsim** with it's configuration file. You can use any text editor as you like. I will use `vim` as my text editor. `vim /etc/inetsim/inetsim.conf`.

<img width="2880" height="1797" alt="image" src="https://github.com/user-attachments/assets/35b522c4-9534-4900-a388-62d5c2c33023" />

**NOTE**
- You might need root permission
- You might want to make a copy of the configuration file if anything went wrong: `cp /etc/inetsim/inetsim.conf /etc/inetsim/inetsim.conf.old`

4. We will need to add some line into configuration file.
- `service_bind_address 0.0.0.0`: it will listen on all available network interfaces
- `dns_default_ip [kali ip]`: to set default IP address to return in DNS replies. In this case, it will be `dns_default_ip 192.168.109.133`

After that `save / write` and `exit / quit`

<img width="2880" height="1683" alt="image" src="https://github.com/user-attachments/assets/0e964f37-ea7b-40ed-ac34-d7395d1328ce" />

5. We can start it directly or using **inetsim** as a service.
- Service: `systemctl start inetsim.service` (root permission needed)
- Directly: `inetsim`(root permission needed)
I prefer do it directly so we can look at the output in the terminal
<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/668c30dc-deca-427e-8216-70f2077045c1" />

6. it's look like we encounter trouble as it said
`Can't locate object method "main_loop" via package "Net::DNS::Nameserver" at /usr/share/perl5/INetSim/DNS.pm line 69.
`
After researching it, i found that Net::DNS after 1.37 has some error to inetsim.

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/3a6dcb96-b36b-4b79-b246-482c51b53665" />

So i will check mine with command`perl -MNet::DNS -e 'print "$Net::DNS::VERSION\n"'`

<img width="2880" height="1791" alt="image" src="https://github.com/user-attachments/assets/e40ea57e-d09b-4a3c-afa0-ad12f2de7605" />

Mine was `1.50` so i will downgrade it. In the post i have found, there are 2 ways to do it.

**cpan** -- video version
```
cpan                                              # or "perl -MCPAN -e shell"
cpan[1]>force get NLNETLABS/Net-DNS-1.37.tar.gz   # replace version if needed
cpan[2]>install NLNETLABS/Net-DNS-1.37.tar.gz
cpan[3]>exit
```

**package install** -- image version
```
wget https://cpan.metacpan.org/authors/id/N/NL/NLNETLABS/Net-DNS-1.37.tar.gz
tar xzf Net-DNS-1.37.tar.gz && cd Net-DNS-1.37
perl Makefile.PL
make
make test
sudo make install
```

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/9dd0e0d1-3e54-4a45-b420-c41911c28f89" />

After doing it, let's check the version again

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/9dfe3a18-d63c-4180-a0ec-6f8bec9eb33f" />

Then restart **inetsim**

<img width="2869" height="1695" alt="image" src="https://github.com/user-attachments/assets/88112de3-1d02-423a-8fa0-98813118452a" />

7. Go to `win2008` and make sure it's network mode is NAT

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/d076b614-fc3f-4dd2-89eb-9283edc129fd" />

and confirm it by checking ip in command prompt. `ipconfig`

<img width="2877" height="1799" alt="image" src="https://github.com/user-attachments/assets/2fc450f2-c02e-4b6d-93c2-e5211a8c47cf" />

8. We will set it DNS server to our `kali` VM. This can be done by open start > Control Panel > Network and Internet > Network and Sharing center >  Manage network connections

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/8dcae718-132c-4c02-aeb9-eb3dfebf85a2" />

By choosing the adapter that are connect to NAT network > properties > internet protocol version 4

<img width="2880" height="1789" alt="image" src="https://github.com/user-attachments/assets/b05f4b51-adec-464b-be56-0e196b3abdd5" />

Enable use the following dns server address and type `kali` ip address in it

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/36273d7e-da46-4fda-800e-232e6f9e1dfa" />

Everything is done. We will now checking the result

<img width="2880" height="1800" alt="image" src="https://github.com/user-attachments/assets/9b1d0edc-4983-4d5d-b720-14f3ce1301b2" />

## Scripted version - automated
```
wget https://raw.githubusercontent.com/longthhe191048/IAM/main/Lab_01/autorun.sh
chmod +x autorun.sh
sudo ./autorun.sh
```
## Video POC

https://github.com/user-attachments/assets/94e79d6b-3122-4acc-956b-8bae871cbcc5

## Reference
- [Reddit](https://www.reddit.com/r/MalwareAnalysis/comments/1iise7n/inetsim_set_up/)
- [inetsim.conf manual](https://manpages.debian.org/testing/inetsim/inetsim.conf.5.en.html)
