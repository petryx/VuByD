## Vuln by Design

This project was inspired by (https://github.com/erev0s/VAmPI][https://github.com/erev0s/VAmPI] a very good project to study API vulnerabilities.
Thanks, @erev0s for the amazing project.

In this project, I tried to build BugBounty style because almost all web apps use a background API. Made some modifications, inserted new vulnerabilities based on (Owasp API Security Top 10 2019) [https://owasp.org/www-project-api-security/]
This project has not yet been completed. The following vulnerabilities are already implemented:

- API1: 2019 Broken object level authorization
- API2: 2019 Broken authentication 
- API5: 2019 Broken function level authorization 
- API6: 2019 Mass Assignment
- API7: 2019 — Security misconfiguration
- API8: 2019 injection
- Regular expression Denial of Service
- And more ...

## Learning Path

The main objective of this project is to improve your skills, so I suggest the following path:
    - Try to enumerate API endpoints using available security tools. If that doesn't work, create a custom wordlist;
    - Discover how to exploit each of the vulnerabilities, manually and with automated tools;
    - Describe all steps to reach the goals;
    - Please share your write-up.

## How to run

### Clone the Repo

```bash

$ git clone 
```

## Note

Don't put this project on the internet, run it locally. This project is extremely insecure by design.

