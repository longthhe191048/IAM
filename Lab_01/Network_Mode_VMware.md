

# Network mode - vmware
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Network mode - vmware](#network-mode---vmware)
   * [Bridged](#bridged)
   * [NAT - Network Address Translation](#nat---network-address-translation)
   * [Host only](#host-only)
   * [Custom \(VMnet0-9\)](#custom-vmnet0-9)
   * [Test with vmware](#test-with-vmware)
   * [Reference](#reference)

<!-- TOC end -->
There are 3 main type of network connection:
- Bridged
- NAT
- Host Only

<img width="752" height="405" alt="image" src="https://github.com/user-attachments/assets/302d7328-e30b-4acb-88b9-7e4292807e53" />

<img width="426" height="355" alt="image" src="https://github.com/user-attachments/assets/e7f431ee-2748-4724-a388-47d6e64803b7" />

<img width="1132" height="287" alt="image" src="https://github.com/user-attachments/assets/7c3db3ab-4fac-4be2-9f55-ca6436589d11" />


## Bridged
- Use physical network adapter
- Use case: when VM needs to have IP address and can be accessible from another computer with the same network
- VMnet0

## NAT - Network Address Translation
- The host computer acts as a gateway, sharing a single network identity
- The VM has an IP address on a private network created by the host, and all traffic from the VM is translated to appear as if it came from the host
- Use case: When you want the VM to access external network resources but don't want it to be directly visible or accessible from the external network.
- VMnet8

## Host only
- Creates a private virtual network that connects only the host and its virtual machines.
- Use case: When you need an internal test network.
- VMnet1

## Custom \(VMnet0-9\)
- User-defined networks for advanced scenarios.
- Use case: When you need multiple VMs in a lab setup.

## Test with vmware

<img width="1920" height="1042" alt="image" src="https://github.com/user-attachments/assets/ee8cf634-bdc5-4254-8db3-b0fe34ed1973" />

<img width="1920" height="1045" alt="image" src="https://github.com/user-attachments/assets/a7d2e928-f4a6-44f0-9b19-c2fc7f61db48" />

<img width="1920" height="1041" alt="image" src="https://github.com/user-attachments/assets/bd70718d-dab6-43cf-a9e1-3205bd0743f0" />

## Reference
[Understanding VMware Network Adapters | Bridged, NAT, Host-Only, and Custom Networks with Real-World Examples](https://www.webasha.com/blog/understanding-vmware-network-adapters-bridged-nat-host-only-and-custom-networks-with-real-world-examples)
