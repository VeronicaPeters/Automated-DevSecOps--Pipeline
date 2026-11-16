# Gitleaks Secret Detection Findings

## 1. Assessment Overview

| Attribute | Details |
|---|---|
| Tool | Gitleaks |
| Assessment type | Secret detection |
| Integration | GitHub Actions |
| CI action version | v3.0.0 |
| Historical scan scope | Git repository history |
| Historical scan date | 11 November 2026 |
| Latest documented CI result | No leaks detected in one scanned commit |

Gitleaks was integrated into the DevSecOps pipeline to identify potential secrets and sensitive credential material committed to the repository.

Two forms of assessment were performed:

- Automated secret detection through the GitHub Actions workflow.
- A separate full-history scan to investigate historical detections across repository commits.

## 2. CI Pipeline Configuration

The GitHub Actions workflow uses the Gitleaks GitHub Action:

```yaml
- name: Gitleaks Secret Scan
  uses: gitleaks/gitleaks-action@e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The action is pinned to a specific commit corresponding to version v3.0.0.

GitHub's built-in `GITHUB_TOKEN` is supplied to the action.

### Latest documented CI result

- Commits scanned: 1
- Leaks detected: 0

This result indicates that the documented CI execution did not identify leaks in the commit it scanned. It should not be interpreted as proof that the entire historical repository is free of exposed secrets.

## 3. Historical Scan Results

A separate full-history scan was performed using:

```bash
gitleaks git . \
  --log-opts="--all" \
  --redact \
  --report-format=json \
  --report-path=gitleaks-full-history-report.json \
  --exit-code=0
```

The `--redact` option was used to avoid displaying detected secret values in the report output.
The --exit-code=0 option allows the historical scan to complete and generate its report without returning a failure status solely because detections were found. The results were then reviewed separately

### Detection summary

| Attribute | Result |
|---|---:|
| Commits scanned | 17 |
| Total detections | 242 |
| Detection rule | private-key |
| Confirmed rule categories | 1 |

All 242 detections were classified under Gitleaks' `private-key` rule.

### Findings by file

| File | Detections |
|---|---:|
| `fake.pem` | 1 |
| `gitleaks-report.json` | 160 |
| `trivy-report.txt` | 81 |
| **Total** | **242** |

### Historical commit context

The detections originated from two historical commits:

| Commit | Date | Commit message | Associated files |
|---|---|---|---|
| `fd52898` | 20 June 2026 | `test secrets` | `fake.pem`, `trivy-report.txt` |
| `7463021` | 23 June 2026 | `Add DevSecOps pipeline` | `gitleaks-report.json` |

The first commit introduced test-related files, including a PEM file and a generated Trivy report.

The second commit introduced the DevSecOps pipeline and a larger Gitleaks report.

The concentration of detections in generated security reports indicates that report content contributed substantially to the historical matches. However, the rule matches should not automatically be classified as false positives without individual validation.

## 4. Investigation and Validation

The historical detections were investigated using the report metadata, affected filenames and associated Git commits.

The investigation established that:

- All 242 detections were associated with the `private-key` rule.
- 241 detections originated from two generated security report files.
- One detection originated from `fake.pem`.
- The affected files were introduced in commits associated with testing and pipeline development.
- The dummy credentials identified during the exercise were confirmed not to be live credentials.

The investigation did not establish that all 242 private-key-pattern matches represented valid, usable private keys.

Individual validation remains important when determining whether a detection represents an actual credential exposure, test material, generated content or a false positive.

## 5. Remediation and Improvements

The following changes were made during the remediation exercise.

### 5.1 Environment-based JWT secret management

The previous hardcoded JWT secret was replaced with environment-variable retrieval.

Current implementation in `config.py`:

```python
import os

JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable is not set")
```

This prevents the application from silently using a hardcoded fallback secret when the required environment variable is missing.

### 5.2 Generated report exclusions

The repository's `.gitignore` file now excludes:

- `gitleaks-report.json`
- `gitleaks-full-history-report.json`
- `trivy-report.txt`

These exclusions help prevent generated security reports from being accidentally committed again.

### 5.3 Current repository status

The following files are no longer tracked in the current Git index:

- `fake.pem`
- `gitleaks-report.json`
- `trivy-report.txt`
- `gitleaks-full-history-report.json`

The `fake.pem` file is also absent from the current working directory.

**Important:** Removing files from the current working tree or excluding them through `.gitignore` does not remove their contents from historical Git commits.

## 6. Residual Risks and Limitations

The assessment identified the following considerations:

- Historical private-key detections remain in the repository's Git history.
- Not every historical detection has been independently established as a valid or invalid private key.
- The latest documented CI scan covered one commit and does not establish that every historical commit is clean.
- No actual credential revocation has been established as part of this exercise.
- `.gitignore` prevents future accidental tracking but does not rewrite existing repository history.

If any historical detection is subsequently validated as a real exposed private key or credential, the appropriate owner should be notified and the credential revoked or rotated. Historical cleanup should also be considered where necessary.

## 7. Recommendations

1. Continue running Gitleaks as part of the CI/CD workflow.
2. Investigate new detections before classifying them as false positives.
3. Avoid committing generated scanner reports unless they are intentionally sanitized and required for documentation.
4. Use environment variables or an appropriate secrets manager for application secrets.
5. Review historical detections and determine whether any require credential rotation or repository-history remediation.
6. Consider extending secret scanning to pull requests and relevant repository history where appropriate.

## 8. Conclusion

The Gitleaks assessment demonstrated the importance of secret detection throughout the software development lifecycle.

The historical scan identified 242 private-key-pattern detections, primarily within generated security reports. The investigation provided context for these findings, while the remediation exercise improved secret handling and reduced the likelihood of generated reports being committed again.

The latest documented CI execution reported no leaks in the scanned commit.

The remaining priority is to maintain continuous secret detection and appropriately validate any historical matches that could represent genuine credential exposure.
