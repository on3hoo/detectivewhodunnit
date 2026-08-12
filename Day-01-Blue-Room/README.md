# Day 01 — TryHackMe Blue Room

## Focus

Nmap, SMB, MS17-010, EternalBlue and Metasploit.

## Objective

Learn basic reconnaissance, service enumeration, vulnerability identification and exploitation in an authorized TryHackMe lab.

## Tools

- Nmap
- Metasploit
- Meterpreter
- TryHackMe

## What I Did

1. Identified the target IP.
2. Scanned the target using Nmap.
3. Identified TCP 445 as `microsoft-ds` / SMB.
4. Checked for the MS17-010 vulnerability.
5. Used Metasploit to exploit EternalBlue.
6. Established a Meterpreter session.
7. Verified SYSTEM-level privileges.
8. Located the flags.

## Key Concepts Learned

- Nmap scanning
- SMB
- TCP 445
- MS17-010
- EternalBlue
- Metasploit
- Meterpreter
- Windows SYSTEM privileges

## Key Takeaway

This lab demonstrated how network enumeration can identify exposed services and how known vulnerabilities can be investigated in an authorized environment.
