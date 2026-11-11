# Trivy Container Vulnerability Scan

## Scan Overview

- **Tool:** Trivy
- **Target image:** `vulnerable-app`
- **Base image OS:** Debian 13.7
- **Scan type:** Container image vulnerability scan
- **Scanner:** Vulnerability scanner
- **Report source:** Latest successful GitHub Actions workflow run
- **Date:** 11 November 2026

## Scan Results

Trivy identified vulnerabilities in both the operating system packages and Python packages contained in the image.

### 1. Operating System Vulnerabilities

| Severity | Findings |
|---|---:|
| Critical | 0 |
| High | 49 |
| Medium | 75 |
| Low | 65 |
| Unknown | 15 |
| **Total** | **204** |

### 2. Python Package Vulnerabilities

| Severity | Findings |
|---|---:|
| Critical | 1 |
| High | 5 |
| Medium | 2 |
| Low | 1 |
| **Total** | **9** |

### 3. Notable Python Package Findings

| Package | Installed Version | Vulnerability | Severity | Fixed Version |
|---|---|---|---|---|
| certifi | 2026.6.17 | GHSA-6q48-6c7w-9gw2 | Critical | 2026.10.18 |
| msgpack | 1.1.2 | CVE-2026-114613 | High | 1.2.3 |
| msgpack | 1.1.2 | GHSA-6v7p-g79w-8964 | High | 1.2.1 |
| setuptools | 70.3.0 | CVE-2025-47273 | High | 78.1.1 |
| setuptools | 70.3.0 | CVE-2026-59890 | Medium | 83.0.0 |
| setuptools | 70.3.0 | GHSA-xmj3-9gf7-h52w | Low | 84.1.0 |
| urllib3 | 2.7.0 | CVE-2026-97687 | High | 2.8.0 |
| urllib3 | 2.7.0 | CVE-2026-97689 | High | 2.8.0 |
| urllib3 | 2.7.0 | CVE-2026-97688 | Medium | 2.8.0 |

## Findings and Observations

1. The image contained 204 operating system vulnerabilities, including 49 High-severity findings.
2. Trivy identified 9 Python package vulnerabilities, including one Critical and five High-severity findings.
3. The Python findings included vulnerabilities affecting certifi, msgpack, setuptools and urllib3.
4. Trivy provided fixed-version information for the listed Python findings, which can guide dependency updates and remediation.
5. The operating system findings require separate review because they originate from packages in the Debian base image.

## Comparison with pip-audit

The pipeline's `pip-audit` scan reported no known vulnerabilities in the dependencies listed in `requirements.txt`, while Trivy identified vulnerabilities in Python packages present in the built image.

These results are not necessarily contradictory: the tools inspect different scopes. `pip-audit` checks the specified Python dependency requirements, while Trivy scans packages detected in the container image.

## Pipeline Configuration and Gate Behaviour

The Trivy command generates a vulnerability report in table format and saves it as `trivy-image-report.txt`.

The report is uploaded as a GitHub Actions artifact, including when earlier workflow steps fail.

The current Trivy command does not configure an explicit vulnerability-based exit code. Therefore, identified vulnerabilities are reported but do not, by themselves, fail the pipeline.

A successful workflow run should not be interpreted as an image with zero vulnerabilities.

## Recommended Remediation

- Review and update vulnerable Python packages to versions containing the available fixes, after checking compatibility.
- Review the Debian operating system findings and update the base image or affected system packages where appropriate.
- Rebuild the image after remediation.
- Run Trivy again and compare the new results with this baseline.
- Consider introducing a severity-based failure threshold once an appropriate remediation policy has been established.

