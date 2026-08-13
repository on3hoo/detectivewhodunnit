# Day 02 — Python Port Scanner

## Overview

A simple Python-based port scanner built from scratch to understand how port scanning works.

The scanner takes a target IP address as a command-line argument, attempts to connect to ports on the target, and displays only the ports that are found to be open.

## Objective

* Understand the purpose of a port scanner.
* Learn how network ports can be tested for accessibility.
* Practice Python scripting and command-line execution.
* Understand the relationship between IP addresses, ports, and network services.

## Tools

* Python
* Python IDLE
* Windows Command Prompt
* Home router / local network gateway

## How It Works

The scanner:

1. Accepts a target IP address from the command line.
2. Attempts to connect to the specified ports on the target.
3. Determines whether the connection succeeds.
4. Prints only the ports identified as open.

## Usage

Run the script from Command Prompt:

```bash
python3 portscanner.py <target-ip>
```

Example:

```bash
python3 portscanner.py <gateway-ip>
```

The target used during testing was the local gateway IP address of my home network.

## Example Output

```text
Open port: <port>
Open port: <port>
...
```

Only open ports are displayed.

## Key Concepts Learned

* IP addresses
* TCP ports
* Open and closed ports
* Network services
* Port scanning
* Python socket/network programming
* Command-line arguments
* Basic network reconnaissance

## Safety

The scanner was tested only against my own home network gateway. Port scanning should only be performed against systems and networks that you own or have explicit permission to test.

## Takeaway

This project provided a practical introduction to network reconnaissance by building a basic port scanner instead of relying on an existing security tool such as Nmap.
