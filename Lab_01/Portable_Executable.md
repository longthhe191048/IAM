<!-- TOC --><a name="portable-executable-pe"></a>
# Portable Executable (PE)
<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Portable Executable (PE)](#portable-executable-pe)
   * [Definition](#definition)
   * [Structure overview](#structure-overview)
      + [DOS Header](#dos-header)
      + [DOS STUB](#dos-stub)
      + [NT HEADER](#nt-header)
      + [Sections](#sections)
   * [Example of PE](#example-of-pe)
      + [Requirement](#requirement)
      + [Overview](#overview)
      + [Structure](#structure)
      + [DOS Header](#dos-header-1)
      + [DOS Stub](#dos-stub-1)
      + [NT Header ](#nt-header-1)
         - [Signature](#signature)
         - [File Header](#file-header)
         - [Optional Header](#optional-header)
         - [Section Header](#section-header)
   * [Reference](#reference)

<!-- TOC end -->



<!-- TOC --><a name="definition"></a>
## Definition
- PE = Portable executable
- File format for executables used in Windows operating systems
- Some file extension: `.EXE`\(executable\), `.DLL` \(32 bit\)\(dynamic links libraries\),`.COM`,`.NET`, `.CPL`,...etc
- PE file = data structure has holds information for OS loader \(part of the operating system that reads a program from secondary storage, loads it into main memory\) to load executable into main memory and execute it

---
<!-- TOC --><a name="structure-overview"></a>
## Structure overview
```
+-------------------+
| DOS Header        |-------------
+-------------------+            |
| DOS Stub          |            |
+-------------------+            |
| NT Headers        |            |
| - PE signature    |          HEADER
| - File Header     |            |
| - Optional Header |            |
+-------------------+            |
| Section Table     |-------------
+-------------------+
| Section 1         |-------------
+-------------------+            |
| Section 2         |            |
+-------------------+            |
| Section 3         |            |
+-------------------+          SECTION
| Section 4         |            |
+-------------------+            |
| ...               |            |
+-------------------+            |
| Section n         |-------------
+-------------------+
```

**NOTE**
- Divide in 2 main part:
  - **header**: header contains metadata about the file itself
  - **Section**:  sections of the file, each of which contains useful information
<!-- TOC --><a name="dos-header"></a>
### DOS Header

Every PE file starts with a 64-bytes-long structure called the DOS header, it’s what makes the PE file an MS-DOS executable

Example of DOS Header
```
typedef struct _IMAGE_DOS_HEADER {      // DOS .EXE header
    WORD   e_magic;                     // Magic number
    WORD   e_cblp;                      // Bytes on last page of file
    WORD   e_cp;                        // Pages in file
    WORD   e_crlc;                      // Relocations
    WORD   e_cparhdr;                   // Size of header in paragraphs
    WORD   e_minalloc;                  // Minimum extra paragraphs needed
    WORD   e_maxalloc;                  // Maximum extra paragraphs needed
    WORD   e_ss;                        // Initial (relative) SS value
    WORD   e_sp;                        // Initial SP value
    WORD   e_csum;                      // Checksum
    WORD   e_ip;                        // Initial IP value
    WORD   e_cs;                        // Initial (relative) CS value
    WORD   e_lfarlc;                    // File address of relocation table
    WORD   e_ovno;                      // Overlay number
    WORD   e_res[4];                    // Reserved words
    WORD   e_oemid;                     // OEM identifier (for e_oeminfo)
    WORD   e_oeminfo;                   // OEM information; e_oemid specific
    WORD   e_res2[10];                  // Reserved words
    LONG   e_lfanew;                    // File address of new exe header
  } IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER;
```
**NOTE**
- `e_magic`:
  - First member of DOS Header
  - WORD = 2 bytes
  - fixed value = `0x5A4D` \(`MZ` in ASCII`\)
  - Signature that make file as MS-DOS executable
- `e_lfanew`
  - last member of DOS Header
  - Store Offset of PE Header
  - Tell where to look for the file header

<!-- TOC --><a name="dos-stub"></a>
### DOS STUB
The DOS stub is an MS-DOS program that prints an error message saying that the executable is not compatible with DOS then exits.

<!-- TOC --><a name="nt-header"></a>
### NT HEADER
Contains 3 main parts:
- **PE Signature**: A 4-byte signature that identifies the file as a PE file.
- **File Header**: A standard [`COFF` File Header](https://wiki.osdev.org/COFF). It holds some information about the PE file
- **Optional Header**: This header provides important information to the OS loader.
<!-- TOC --><a name="sections"></a>
### Sections
Sections are where the actual contents of the file are stored, these include things like data and resources that the program uses, and also the actual code of the program, there are several sections each one with its own purpose.

<!-- TOC --><a name="example-of-pe"></a>
## Example of PE

<!-- TOC --><a name="requirement"></a>
### Requirement
- Any type of PE file. I will use `Exterro_FTK_Imager_(x64)-4.7.3.81.exe` as an example
- [PE Bear](https://github.com/hasherezade/pe-bear/releases)

<!-- TOC --><a name="overview"></a>
### Overview

<img width="949" height="689" alt="image" src="https://github.com/user-attachments/assets/b94b7a93-d9af-4ded-bbfd-ac11adb03e67" />

<!-- TOC --><a name="structure"></a>
### Structure

<img width="257" height="395" alt="image" src="https://github.com/user-attachments/assets/d8d05841-016b-4829-b012-50cca1c64738" />

<!-- TOC --><a name="dos-header-1"></a>
### DOS Header

`e_magic`: start with 4D5A

`e_lfanew`: \(offset `3C`\) has value `108`. Follow to find start of NT header

<img width="953" height="683" alt="image" src="https://github.com/user-attachments/assets/10ab66d9-1f27-43ba-a924-21f7b31850d3" />

<img width="945" height="678" alt="image" src="https://github.com/user-attachments/assets/fec27add-149f-43bc-828b-6dc5f328f928" />

NT header

<img width="945" height="674" alt="image" src="https://github.com/user-attachments/assets/6f39adbb-99f6-41de-83dd-0cb004bce0c6" />

<!-- TOC --><a name="dos-stub-1"></a>
### DOS Stub

<img width="1905" height="328" alt="image" src="https://github.com/user-attachments/assets/68acb202-9a79-4ca6-a6fa-ca9d3e9814bd" />

Default message: “This program cannot be run in DOS mode.”

<img width="827" height="182" alt="image" src="https://github.com/user-attachments/assets/329b1f67-039d-4b9b-a4d7-2024aa0104e2" />

<!-- TOC --><a name="nt-header-1"></a>
### NT Header 

<!-- TOC --><a name="signature"></a>
#### Signature

<img width="1501" height="291" alt="image" src="https://github.com/user-attachments/assets/94daf045-e325-4065-b1aa-8f6a0ce5fd2f" />

<!-- TOC --><a name="file-header"></a>
#### File Header

<img width="1920" height="350" alt="image" src="https://github.com/user-attachments/assets/58921f00-026f-4247-bf4e-afecc7ceee68" />

<img width="1588" height="251" alt="image" src="https://github.com/user-attachments/assets/440f0b51-f63e-4b67-916a-e7036bddc1d2" />

**NOTE**
- Machine: This is a number that indicates the type of machine (CPU Architecture) the executable is targeting.
- NumberOfSections: This field holds the number of sections (or the number of section headers aka. the size of the section table.).
- TimeDateStamp: A unix timestamp that indicates when the file was created
- PointerToSymbolTable and NumberOfSymbols: These two fields hold the file offset to the COFF symbol table and the number of entries in that symbol table
- SizeOfOptionalHeader: The size of the Optional Header.
- Characteristics: A flag that indicates the attributes of the file

<!-- TOC --><a name="optional-header"></a>
#### Optional Header

<img width="1920" height="1036" alt="image" src="https://github.com/user-attachments/assets/97ef6dde-c0bc-41cd-b354-9191e7b08489" />


<!-- TOC --><a name="section-header"></a>
#### Section Header

<img width="1920" height="673" alt="image" src="https://github.com/user-attachments/assets/9b3d61a8-b2cd-4bd5-b5f1-d0ec14e1a05e" />

- .text: Contains the executable code of the program.
- .data: Contains the initialized data.
- .rdata: Contains read-only initialized data.
- .reloc: Contains image relocation information.
- .rsrc: Contains resources used by the program, these include images, icons or even embedded binaries.

--> official document: [PE Format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format)

---
<!-- TOC --><a name="reference"></a>
## Reference
- [Tìm hiểu về PE file – P1](https://phamcongit.wordpress.com/2017/07/06/tim-hieu-ve-pe-file-p1/)
- [A dive into the PE file format](https://0xrick.github.io/win-internals/pe2/)
