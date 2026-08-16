# Day 4 – Kali Linux Homelab Setup

##  Objective

Set up a Kali Linux cybersecurity lab with essential penetration-testing, network-analysis, password-cracking, and digital-forensics tools, and deploy DVWA as a safe vulnerable web application for practice.

---

##  Lab Setup

```text
                    Host Computer
                         │
                         ▼
                    Kali Linux VM
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Security        Forensics         Docker
      Tools            Tools              │
        │                │                ▼
   Nmap, Burp,       Wireshark,        DVWA
   Gobuster,         Autopsy           Vulnerable
   John, Hashcat                        Web App
```

---

## 🛠️ Tools Installed

| Tool            | Purpose                                     |
| --------------- | ------------------------------------------- |
| Nmap            | Network scanning and enumeration            |
| Wireshark       | Network traffic analysis                    |
| Burp Suite      | Web application security testing            |
| Gobuster        | Web directory enumeration                   |
| John the Ripper | Password/hash cracking                      |
| Hashcat         | Password/hash cracking                      |
| Autopsy         | Digital forensics                           |
| Docker          | Running applications in isolated containers |
| DVWA            | Intentionally vulnerable web application    |

---

##  DVWA Setup

DVWA (Damn Vulnerable Web Application) is a deliberately vulnerable web application used to safely practice web-security concepts.

### Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

### Start Docker

```bash
sudo systemctl enable --now docker
```

### Download DVWA

```bash
git clone https://github.com/digininja/DVWA.git
```

### Enter the DVWA directory

```bash
cd ~/DVWA
```

### Install Docker Compose

```bash
sudo apt install docker-compose -y
```

### Start DVWA

```bash
sudo docker-compose up -d
```

### Check running containers

```bash
sudo docker ps
```

### Access DVWA

Open the following in the Kali browser:

```text
http://127.0.0.1:4280
```

Default credentials:

```text
Username: admin
Password: password
```

---

##  What I Learned

* Set up and configured a Kali Linux cybersecurity environment.
* Installed common penetration-testing and digital-forensics tools.
* Learned the basic purpose of Docker and containers.
* Deployed DVWA using Docker Compose.
* Understood the difference between a security workstation and a vulnerable target.
* Created a safe environment for practicing web-security and penetration-testing techniques.

---

##  Future Lab Activities

The lab will be used for:

* Nmap reconnaissance
* Network enumeration
* Burp Suite testing
* Gobuster directory enumeration
* SQL Injection
* Cross-Site Scripting (XSS)
* Authentication testing
* Wireshark traffic analysis
* Password/hash cracking
* Digital forensics
* Vulnerability assessment
* Penetration-testing exercises

A Metasploitable VM may be added later as a second intentionally vulnerable target for broader network and system-security testing.

---

##  Safety

DVWA and other intentionally vulnerable systems should only be run in an isolated lab environment and tested only by the authorized user.

Do not expose intentionally vulnerable machines or applications to the public internet or networks you do not control.

---

##  Conclusion

The Kali Linux homelab has been successfully established as the foundation for the 30-day Digital Forensics and Cybersecurity Speedrun. Kali provides the security and forensic tools, while Docker provides an isolated environment for running DVWA as a vulnerable target. This setup enables practical learning through controlled experiments rather than relying only on theoretical concepts.
