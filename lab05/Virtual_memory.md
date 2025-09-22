#  Virtual memory
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Virtual memory](#virtual-memory)
   * [What is virtual memory](#what-is-virtual-memory)
   * [Characteristic](#characteristic)
      + [Physical memory](#physical-memory)
      + [Virtual memory](#virtual-memory-1)
   * [Why do we need virtual memory](#why-do-we-need-virtual-memory)
      + [Not enough memory](#not-enough-memory)
      + [Memory fragmentation](#memory-fragmentation)
      + [Security](#security)
   * [Additional detail: Optional header](#additional-detail-optional-header)
   * [Reference](#reference)

<!-- TOC end -->
## What is virtual memory
* Definition: Virtual memory is a memory management technique used by operating systems to give the appearance of a large, continuous block of memory to applications, even if the physical memory (RAM) is limited and not necessarily allocated in contiguous manner
* Simplified: Virtual memory is a **memory managerment** technique use by OS to make a computer appear to have more memory than it physically does

<img width="646" height="435" alt="image" src="https://github.com/user-attachments/assets/248d405a-035f-40fa-9102-cee71a6f312f" />

## Characteristic
### Physical memory
* Main memory - hardware - RAM

### Virtual memory
* Abstract layer - created by operating system
* operating system use to manage process memory
* Processes can only access virtual memory
* Operating system will mapping virtual memory -> physical memory

## Why do we need virtual memory
Virtual memory concept was invented to solve problems:
* Not enough memory
* Memory fragmentation
* Security

### Not enough memory
By using virtual memory, only part of a program is kept in RAM at a time. When more data is needed than RAM can hold, the operating system swaps some pages out to disk (swap space), and brings in the needed pages.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/48914129-0efe-45b4-a46d-7969bb2f28cc" />

### Memory fragmentation
* Virtual memory divides both physical RAM and process memory into small fixed-size blocks called pages (usually 4 KB).
* When a program requests memory, it doesn’t need one large continuous block. Its pages can be scattered all over physical RAM.
* Everything will be keeping track by page table

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1fbfb8a8-b6e2-49e5-8bdd-00d3efa39c33" />

### Security
By using mapping them to corresponding physical address, it would't override each other.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1c360361-f37b-4bd3-a284-fa8dfc51fcd9" />

## Additional detail: Optional header
* BaseOfCode: RVA (related virtual address) of start of the code section when the file is loaded into memory
* ImageBase: It is the address in virtual memory where the executable should be loaded at
* AddressOfEntryPoint: RVA of entry point. Entry point is a pointer to the entry point function, relative to the image base address. It points to the instruction where execution starts
* SizeOfStack:
  * Reserve: the address space is allocated within the process that requested it
  * Commit: mapping that address space to the physical memory so that it can be used.
## Reference
* [Fundamental of virtual memory](https://nghiant3223.github.io/2025/05/29/fundamental_of_virtual_memory.html)
* [Virtual memory in operating system](https://www.geeksforgeeks.org/operating-systems/virtual-memory-in-operating-system/)
* [but, what is a virtual memory](https://www.youtube.com/watch?v=A9WLYbE0p-I)
* [What are PE](https://jumpcloud.com/it-index/what-are-pe-portable-executable-files#:~:text=Entry%20Point%3A%20The%20memory%20address,using%20the%20Portable%20Executable%20format)
* [Dive into pe format](https://0xrick.github.io/win-internals/pe4/)
* [About the entry point of PE in Windows](https://stackoverflow.com/questions/3745672/about-the-entry-point-of-pe-in-windows)
* [What's the difference between reserved and committed memory?](https://stackoverflow.com/questions/2440434/whats-the-difference-between-reserved-and-committed-memory)
