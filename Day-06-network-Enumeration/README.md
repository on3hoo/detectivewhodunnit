# Nmap Network Enumeration & Attack-Surface Analysis

## Overview

This project documents a practical network reconnaissance and attack-surface analysis experiment performed using **Nmap on Kali Linux** against a deliberately vulnerable **DVWA (Damn Vulnerable Web Application)** Docker lab.

The objective was not to exploit DVWA, but to approach the environment from a reconnaissance perspective and determine:

* Which network services are exposed?
* Which ports are reachable?
* What software is running behind those ports?
* What information can be obtained through service fingerprinting?
* What web resources can be identified?
* How does Docker networking affect the observable attack surface?
* How can an unknown open port be investigated and attributed to the correct process?

> **Disclaimer:** This experiment was performed entirely inside my own isolated cybersecurity lab using DVWA, an intentionally vulnerable application. Only systems you own or have explicit authorization to test should be scanned.

---

## Lab Environment

* **Attacker / Reconnaissance Machine:** Kali Linux VM
* **Target:** DVWA Docker container
* **Web Server:** Apache HTTP Server
* **Database:** MariaDB
* **Primary Tool:** Nmap
* **Supporting Tools:** Docker, `ss`, `lsof`, `ping`

### Network Architecture

DVWA runs inside a Docker container and exposes HTTP internally on:

```text
172.18.0.3:80
```

Docker publishes the application to Kali through:

```text
127.0.0.1:4280 → DVWA:80
```

The MariaDB backend uses TCP/3306 internally but is not published onto the Kali host.

---

## Reconnaissance Methodology

### 1. Docker Environment Inspection

The running containers were first examined using:

```bash
sudo docker ps
```

This identified:

* DVWA web container
* MariaDB database container
* Docker port mappings

A key observation was:

```text
127.0.0.1:4280 -> 80/tcp
```

This indicated that DVWA was published specifically through the Kali host's loopback interface.

---

### 2. Initial Nmap Scan

A basic scan was performed:

```bash
nmap 127.0.0.1
```

The initial scan did not identify DVWA because TCP/4280 was not included among the default commonly scanned ports.

A targeted scan was therefore performed:

```bash
nmap -p 4280 127.0.0.1
```

TCP/4280 was identified as **open**.

This demonstrated that a default Nmap scan does not necessarily discover every exposed TCP service.

---

### 3. Service and Version Detection

Service fingerprinting was performed using:

```bash
nmap -sV -p 4280 127.0.0.1
```

Nmap identified the service as:

```text
4280/tcp open http Apache httpd 2.4.68 ((Debian))
```

This also demonstrated why port numbers alone should not be used to determine which application is actually running.

---

### 4. Nmap Default Script Enumeration

Further enumeration was performed using:

```bash
nmap -sC -sV -p 4280 127.0.0.1
```

Information discovered included:

* Apache HTTP Server
* Debian-based server environment
* DVWA application title
* `login.php`
* `robots.txt`

This moved the investigation from basic port discovery into service and application reconnaissance.

---

### 5. HTTP Enumeration

HTTP-specific reconnaissance was performed using Nmap NSE scripts.

```bash
nmap -sV --script http-title,http-headers -p 4280 127.0.0.1
```

and:

```bash
nmap -sV --script http-enum -p 4280 127.0.0.1
```

Enumeration identified resources including:

```text
/login.php
/robots.txt
```

The login page represents an authentication surface, while `robots.txt` provides additional information useful during application reconnaissance.

---

### 6. Identifying the DVWA Container

The internal Docker IP address was obtained using Docker inspection.

```bash
sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dvwa-dvwa-1
```

The DVWA container was identified as:

```text
172.18.0.3
```

Connectivity was verified using:

```bash
ping -c 4 172.18.0.3
```

The successful replies confirmed network-layer connectivity between Kali and the DVWA container.

---

### 7. Full TCP Port Scan

A complete TCP port scan was performed against the DVWA container:

```bash
nmap -p- 172.18.0.3
```

Only:

```text
80/tcp open http
```

was discovered.

Therefore, the container's directly exposed TCP network-service attack surface was primarily limited to its HTTP service.

---

### 8. Direct DVWA Service Enumeration

The container was enumerated directly using:

```bash
nmap -sC -sV -p 80 172.18.0.3
```

The scan again identified:

* TCP/80
* HTTP
* Apache 2.4.68
* Debian
* DVWA
* `login.php`
* `robots.txt`

---

### 9. OS Fingerprinting

Nmap OS detection was performed using:

```bash
sudo nmap -O 172.18.0.3
```

The resulting network-stack fingerprint indicated a Linux-based system.

Nmap OS detection is fingerprint-based and should therefore be treated as an estimate rather than definitive operating-system identification.

---

## Investigation of Unknown TCP/40399

During a full localhost TCP scan, an additional open port was discovered:

```text
40399/tcp open unknown
```

Rather than assuming that this service belonged to DVWA, host-level investigation was performed.

### Socket Inspection

```bash
sudo ss -ltnp | grep 40399
```

This identified:

```text
127.0.0.1:40399
Process: containerd
PID: 926
```

The result was independently checked using:

```bash
sudo lsof -iTCP:40399 -sTCP:LISTEN
```

Nmap service detection was then performed:

```bash
nmap -sV -p 40399 127.0.0.1
```

Nmap observed an HTTP service exhibiting Go `net/http` behavior.

The investigation therefore determined that TCP/40399 was associated with the local container runtime rather than the DVWA application.

This demonstrated the importance of correlating **network reconnaissance with host-level evidence** before attributing an open port to a particular application.

---

## Interface Exposure Analysis

Kali's available network addresses were identified using:

```bash
hostname -I
```

TCP/4280 was then tested through different interfaces.

The results showed:

| Interface                   | Port | Result   |
| --------------------------- | ---: | -------- |
| `127.0.0.1`                 | 4280 | OPEN     |
| Kali VM network address     | 4280 | FILTERED |
| Docker gateway `172.18.0.1` | 4280 | FILTERED |
| Docker bridge `172.17.0.1`  | 4280 | FILTERED |

These observations are consistent with the Docker configuration:

```text
127.0.0.1:4280 -> 80/tcp
```

DVWA is published specifically through the host loopback interface rather than broadly through all Kali network interfaces.

The DVWA container itself remains directly reachable from Kali through:

```text
172.18.0.3:80
```

---

## Attack-Surface Summary

| Component           | Exposure          | Observation             | Security Significance                    |
| ------------------- | ----------------- | ----------------------- | ---------------------------------------- |
| DVWA                | `172.18.0.3:80`   | HTTP exposed            | Primary application attack surface       |
| Apache              | TCP/80            | Version fingerprinted   | Technology information exposed           |
| DVWA login          | `/login.php`      | Authentication endpoint | Authentication attack surface            |
| robots.txt          | `/robots.txt`     | Discoverable            | Reconnaissance information               |
| Docker host mapping | `127.0.0.1:4280`  | Loopback only           | Restricted host-side exposure            |
| MariaDB             | TCP/3306          | Not host-published      | Backend remains within Docker networking |
| containerd          | `127.0.0.1:40399` | Local HTTP listener     | Container-runtime service, not DVWA      |

---

## Key Findings

The experiment demonstrated that the same application can present different attack surfaces depending on the reconnaissance vantage point.

At the **container level**, DVWA exposes HTTP on TCP/80.

At the **host level**, Docker maps the service to TCP/4280 specifically on the loopback interface.

At the **application level**, HTTP enumeration reveals DVWA, its login endpoint and other web resources.

The experiment also demonstrated that an open port should not automatically be attributed to the target application. TCP/40399 was initially unexplained but was subsequently traced to `containerd` using host-level socket inspection.

---

## Security Recommendations

For real-world containerized applications:

* Expose only services that require network access.
* Bind services to appropriate interfaces instead of all interfaces where possible.
* Avoid publicly exposing database services unless required.
* Restrict management and container-runtime interfaces.
* Keep web servers, container images and dependencies patched.
* Reduce unnecessary server/version information disclosure.
* Apply appropriate authentication and access controls to sensitive endpoints.
* Regularly perform network reconnaissance to identify unintended service exposure.

> DVWA is intentionally vulnerable and should never be exposed to an untrusted or production network.

---

## Limitations

This experiment primarily evaluated the **TCP network attack surface**.

It did not comprehensively assess:

* UDP services
* Web application vulnerabilities
* Authentication vulnerabilities
* Exploitation
* Source-code security
* Container escape vulnerabilities
* Docker daemon security
* Application business logic

Therefore, a limited number of exposed TCP ports should not be interpreted as proof that a system is secure.

---

## Skills Practiced

* Nmap reconnaissance
* TCP port scanning
* Full-port enumeration
* Service/version fingerprinting
* Nmap Scripting Engine (NSE)
* HTTP enumeration
* OS fingerprinting
* Linux socket investigation
* Docker networking
* Process-to-port attribution
* Network-interface analysis
* Attack-surface mapping
* Security findings documentation

---

## Conclusion

This lab demonstrated a structured approach to network reconnaissance rather than simply executing individual Nmap commands.

Starting from an unknown network surface, the experiment identified reachable services, fingerprinted the underlying technologies, enumerated application resources, investigated an unexplained open port, and compared exposure across Docker and host network interfaces.

The primary DVWA network attack surface was identified as its HTTP service on TCP/80 within the Docker network, with Docker publishing the application through TCP/4280 specifically on Kali's loopback interface.

The experiment demonstrates how **Nmap, Docker inspection and Linux host-level networking tools can be combined to build a more accurate picture of a system's real attack surface.**
