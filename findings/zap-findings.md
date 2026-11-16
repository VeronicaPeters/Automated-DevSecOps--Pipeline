# OWASP ZAP DAST Findings

## 1. Assessment Overview

This document records the results of an automated Dynamic Application Security Testing (DAST) assessment performed against the deliberately vulnerable Flask application in the Automated DevSecOps Pipeline project.

The assessment used OWASP ZAP to identify potential security weaknesses by sending HTTP requests to the running application and analyzing its responses.

| Attribute | Details |
|---|---|
| Tool | OWASP ZAP |
| Assessment type | Dynamic Application Security Testing (DAST) |
| Target application | Vulnerable Flask application |
| Target URL | `http://localhost:5001` |
| Scan configuration | `.zap/zap-plan.yaml` |
| Report format | Traditional HTML |
| Report location | `.zap/reports/zap-report.html` |
| Total alert types | 5 |
| Total alert instances | 16 |

The application was assessed locally within the CI environment. The `localhost` address in the report refers to the application running in the pipeline environment, not a publicly deployed production application.

## 2. Assessment Scope and Configuration

The ZAP assessment was configured through `.zap/zap-plan.yaml` and executed using the official OWASP ZAP Docker image.

### 2.1 Configured endpoints

The requestor job sent GET requests to four application endpoints:

| Endpoint | HTTP Method | Request |
|---|---|---|
| Login | GET | `/login` |
| Admin users | GET | `/admin/users` |
| Search | GET | `/search?username=test` |
| Password reset | GET | `/reset-password?email=test@example.com` |

These requests provided ZAP with responses to inspect during the assessment.

### 2.2 Scan configuration

The scan plan included the following stages:

| Stage | Configuration |
|---|---|
| Requestor | Sends configured GET requests to the four endpoints |
| Passive scanning | Waits for a maximum of 1 minute |
| Active scanning | Targets `/login` within the configured application context |
| Active scan strength | Medium |
| Active scan threshold | Medium |
| Maximum active scan duration | 2 minutes |
| Reporting | Generates a traditional HTML report |

**Important scope distinction:** Although four endpoints were explicitly requested, the active scan job was configured to target `/login` only. The other endpoints were available for passive inspection through their request and response traffic. The findings should therefore not be interpreted as evidence that all four endpoints received equivalent active attack testing.

## 3. Assessment Results Summary

The ZAP report identified five alert types, with 16 total instances across the application.

| Finding | Severity | Instances |
|---|---|---:|
| Content Security Policy (CSP) Header Not Set | Medium | 3 |
| Missing Anti-clickjacking Header | Medium | 3 |
| Server Leaks Version Information via "Server" HTTP Response Header Field | Low | 4 |
| X-Content-Type-Options Header Missing | Low | 4 |
| Information Disclosure - Sensitive Information in URL | Informational | 2 |
| **Total** | **2 Medium, 2 Low, 1 Informational** | **16** |

The results primarily identify missing HTTP security headers and information disclosure through response headers and URL parameters.

## 4. Detailed Findings

### 4.1 Content Security Policy (CSP) Header Not Set

**Severity:** Medium  
**Instances:** 3

#### Description

The application responses did not include a Content Security Policy (CSP) header.

CSP is a browser-enforced security policy that allows an application to define which sources are permitted to load resources such as scripts, stylesheets, images and other content.

Without an appropriate CSP, the browser has fewer restrictions on the sources from which content can be loaded. This can reduce the application's ability to mitigate certain attacks, including some cross-site scripting (XSS) and content-injection scenarios.

#### Affected Endpoints

| Endpoint | HTTP Method |
|---|---|
| `/login` | GET |
| `/reset-password?email=test@example.com` | GET |
| `/search?username=test` | GET |

#### Evidence

ZAP reported that the `Content-Security-Policy` response header was not set on the three affected endpoints.

#### Potential Security Impact

The absence of CSP removes an additional browser-enforced layer of protection against unauthorized content execution and loading.

If an injection vulnerability exists elsewhere in the application, a properly configured CSP may help limit the impact by restricting the sources from which executable content can be loaded.

The finding does not establish that an XSS vulnerability was successfully exploited.

#### Recommendation

Implement a Content Security Policy through the application or web server.

The policy should explicitly define trusted sources for scripts, stylesheets, images, and other resources. Avoid unnecessarily permissive directives such as unrestricted `*` sources or `'unsafe-inline'` where safer alternatives are practical.

A restrictive policy should be tested against the application's actual resource requirements before enforcement.

---

### 4.2 Missing Anti-clickjacking Header

**Severity:** Medium  
**Instances:** 3  
**CWE:** CWE-1021  
**ZAP Plugin ID:** 10020

#### Description

ZAP identified that the application responses did not include an effective anti-clickjacking protection mechanism.

Clickjacking occurs when an attacker tricks a user into interacting with an application through an embedded or disguised interface, often by placing the legitimate application inside a malicious webpage using an iframe.

Without appropriate framing restrictions, an application may be exposed to unauthorized embedding by other websites.

#### Affected Endpoints

| Endpoint | HTTP Method |
|---|---|
| `/login` | GET |
| `/reset-password?email=test@example.com` | GET |
| `/search?username=test` | GET |

#### Evidence

The ZAP report identified the missing `X-Frame-Options` response header on the three affected endpoints.

The report recommends implementing either:

- An `X-Frame-Options` response header; or
- A Content Security Policy containing the `frame-ancestors` directive.

#### Potential Security Impact

If an application can be embedded by an untrusted website, an attacker may attempt to manipulate how users interact with the application.

For example, a malicious page could position an invisible or disguised application interface over another element, potentially tricking users into performing unintended actions.

The finding identifies missing protection; it does not demonstrate a successful clickjacking attack.

#### Recommendation

Implement an appropriate anti-framing policy.

For applications that should never be embedded, use:

`X-Frame-Options: DENY`

Alternatively, a Content Security Policy can enforce the same restriction through:

`Content-Security-Policy: frame-ancestors 'none'`

If legitimate same-origin framing is required, select a policy that supports that requirement without allowing untrusted external websites to embed the application.

---

### 4.3 Server Leaks Version Information via "Server" HTTP Response Header Field

**Severity:** Low  
**Instances:** 4  
**CWE:** CWE-497  
**ZAP Plugin ID:** 10036

#### Description

The application disclosed server and framework version information through its HTTP `Server` response header.

ZAP identified the following value:

`Werkzeug/3.1.8 Python/3.12.16`

This information reveals details about the technologies used to run the application.

#### Affected Endpoints

| Endpoint | HTTP Method |
|---|---|
| `/admin/users` | GET |
| `/login` | GET |
| `/reset-password?email=test@example.com` | GET |
| `/search?username=test` | GET |

#### Evidence

The HTTP response headers exposed:

`Server: Werkzeug/3.1.8 Python/3.12.16`

The same version information was identified across all four endpoints.

#### Potential Security Impact

Disclosing server and framework versions provides attackers with additional information about the application's technology stack.

An attacker could use the disclosed versions to research known weaknesses, identify potentially relevant vulnerabilities, and tailor further reconnaissance.

However, version disclosure alone does not establish that the identified software versions contain an exploitable vulnerability.

#### Recommendation

Configure the application or web server to suppress the `Server` response header or replace detailed version information with a generic value.

Avoid unnecessarily disclosing framework and runtime versions in externally accessible HTTP responses.

---

### 4.4 X-Content-Type-Options Header Missing

**Severity:** Low  
**Instances:** 4  
**CWE:** CWE-693  
**WASC ID:** 15  
**ZAP Plugin ID:** 10021

#### Description

ZAP identified that the application responses did not include the `X-Content-Type-Options` security header with the recommended value of `nosniff`.

This header instructs supported browsers not to perform MIME-type sniffing, where a browser attempts to determine the content type of a response independently of its declared `Content-Type`.

Without this protection, certain browsers may interpret response content differently from the content type specified by the application.

#### Affected Endpoints

| Endpoint | HTTP Method |
|---|---|
| `/admin/users` | GET |
| `/login` | GET |
| `/reset-password?email=test@example.com` | GET |
| `/search?username=test` | GET |

#### Evidence

The ZAP report identified the missing `X-Content-Type-Options` header across all four endpoints.

The report recommends setting the header to:

`X-Content-Type-Options: nosniff`

#### Potential Security Impact

MIME sniffing can cause browsers to interpret content in a way that differs from the declared content type.

Depending on the content being served and the browser's behavior, this may introduce additional exposure to certain content-injection scenarios.

The absence of this header does not, by itself, prove that malicious content can be executed.

#### Recommendation

Configure the application or web server to include the following response header consistently:

`X-Content-Type-Options: nosniff`

Also ensure that appropriate `Content-Type` values are returned for application responses, including error pages.

---

### 4.5 Information Disclosure - Sensitive Information in URL

**Severity:** Informational  
**Instances:** 2

#### Description

ZAP identified values in URL query strings that its sensitive-information detection rule classified as potentially sensitive.

Information placed in URL parameters may be exposed through browser history, server logs, caching systems, monitoring tools, and HTTP referrer information, depending on the application and infrastructure configuration.

#### Affected Endpoints and Evidence

| Endpoint | Parameter | Observed Value |
|---|---|---|
| `/reset-password?email=test@example.com` | `email` | `test@example.com` |
| `/search?username=test` | `username` | `test` |

#### Potential Security Impact

The password reset endpoint places an email address in the URL query string.

Email addresses are personal information and may be retained in browser history, application logs, proxy logs, and other systems that record requested URLs.

The search endpoint also places a username in the URL. Whether this presents a meaningful confidentiality concern depends on the sensitivity of usernames within the application's context.

**Assessment clarification:** This finding does not demonstrate that a password, authentication token, or other credential was exposed. ZAP flagged the email and username values in the query strings as potentially sensitive information.

#### Recommendation

Avoid transmitting sensitive information through URL query parameters when it is not necessary.

For the password reset workflow, use an HTTP POST request and transmit the email address in the request body rather than the URL.

Review the search functionality to determine whether usernames are considered sensitive in the application's context. If they are, consider an alternative request design that does not expose them in the URL.

---

## 5. Remediation Considerations

The findings highlight several improvements that can be implemented centrally through application response configuration.

| Finding | Recommended Remediation |
|---|---|
| Missing CSP | Implement an appropriately restrictive Content Security Policy |
| Missing anti-clickjacking protection | Configure `X-Frame-Options` or CSP `frame-ancestors` |
| Server version disclosure | Suppress or generalize the `Server` response header |
| Missing X-Content-Type-Options | Set `X-Content-Type-Options: nosniff` |
| Sensitive information in URLs | Move sensitive values to request bodies where appropriate |

### Remediation Status

No remediation is recorded as completed or verified in this assessment document.

The recommendations above represent proposed corrective actions. Each change should be implemented and validated through a subsequent scan or appropriate manual testing.

A successful pipeline execution should not be interpreted as evidence that these findings have been resolved.

## 6. CI/CD Pipeline Integration

OWASP ZAP is integrated into the project's GitHub Actions workflow as the DAST stage.

The pipeline uses the Docker image:

`ghcr.io/zaproxy/zaproxy:stable`

The scan is executed using the configured automation plan:

`zap.sh -cmd -autorun /zap/wrk/.zap/zap-plan.yaml`

After execution, ZAP generates the traditional HTML report at:

`.zap/reports/zap-report.html`

The workflow uploads the report as a GitHub Actions artifact named:

`zap-dast-report`

This makes the assessment output available for review after the pipeline run.

### Pipeline Enforcement

The current ZAP integration is configured for report generation rather than enforcement.

There is no explicit ZAP severity-based threshold configured to fail the pipeline when findings are detected.

Consequently, a successful workflow run does not mean that the application has no DAST findings. The report must be reviewed separately to identify and assess detected issues.

## 7. Assessment Limitations

The results should be interpreted in the context of the configured scan scope and execution limits.

The following limitations apply:

1. **Limited active scan coverage:** The active scan job explicitly targeted `/login`. The other three configured endpoints were requested and available for passive inspection, but were not individually configured as active scan targets.

2. **Short scan duration:** The active scan was limited to two minutes, while passive scanning was configured to wait for a maximum of one minute. This limits the depth of testing that could be performed.

3. **No authenticated scan configuration:** The supplied scan plan does not configure an authenticated session. Therefore, the assessment does not establish coverage of functionality that requires authenticated access.

4. **Limited endpoint coverage:** Only four endpoints were explicitly included in the requestor job. Other application routes, input combinations, and application workflows may not have been assessed.

5. **No severity-based pipeline gate:** ZAP findings do not currently fail the workflow based on severity. Pipeline success is therefore not equivalent to a clean DAST assessment.

6. **Automated testing limitations:** Automated DAST cannot replace manual security testing, authorization testing, business logic assessment, or comprehensive API security testing.

The absence of a finding should not be interpreted as proof that a particular vulnerability does not exist.

## 8. Conclusion

The OWASP ZAP assessment identified 16 alert instances across five alert types in the vulnerable Flask application.

The findings included missing browser security headers, disclosure of server version information, and potentially sensitive values transmitted through URL query parameters.

The assessment demonstrates how DAST can be integrated into a CI/CD pipeline to inspect a running application and generate security findings that complement other testing stages.

Within this project, ZAP provides dynamic security testing alongside:

- Gitleaks for secret detection.
- Semgrep for static application security testing.
- pip-audit for Python dependency vulnerability detection.
- Trivy for container image vulnerability scanning.

Together, these tools provide security checks across different stages of the application lifecycle. However, each tool has a defined scope, and their results must be interpreted alongside manual review and further validation.

**Overall assessment:** ZAP successfully generated a DAST report and identified security weaknesses in the running application. The findings provide a basis for remediation and subsequent validation, but the current scan does not establish that the application is free from vulnerabilities.

---

## 9. References

- OWASP ZAP Alerts: https://www.zaproxy.org/docs/alerts/
- OWASP Security Headers: https://owasp.org/www-community/Security_Headers
- ZAP Missing Anti-clickjacking Header (10020): https://www.zaproxy.org/docs/alerts/10020/
- ZAP X-Content-Type-Options Header Missing (10021): https://www.zaproxy.org/docs/alerts/10021/
- ZAP Server Leaks Version Information (10036): https://www.zaproxy.org/docs/alerts/10036/
- CWE-1021: https://cwe.mitre.org/data/definitions/1021.html
- CWE-497: https://cwe.mitre.org/data/definitions/497.html
- CWE-693: https://cwe.mitre.org/data/definitions/693.html
