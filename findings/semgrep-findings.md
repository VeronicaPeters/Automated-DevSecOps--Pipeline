# Semgrep Static Application Security Testing (SAST) Findings

## 1. Assessment Overview

| Attribute | Details |
|---|---|
| Tool | Semgrep OSS |
| Assessment type | Static Application Security Testing (SAST) |
| Integration | GitHub Actions |
| Scan configuration | Automatic ruleset selection |
| Scan command | `semgrep scan --config=auto --error .` |
| Latest local scan date | 16 November 2026 |
| Targets scanned | 23 files |
| Rules executed | 329 |
| Findings | 0 |
| Blocking findings | 0 |

Semgrep was integrated into the DevSecOps pipeline to perform static analysis of the application's source code and identify potential security weaknesses.

The scan examines source code without requiring the application to be running. This allows potential issues to be identified during development and before deployment.

## 2. CI Pipeline Configuration

The GitHub Actions workflow runs Semgrep using:

```bash
semgrep scan --config=auto --error .
```

The command uses the following options:

- `--config=auto`: Automatically selects an appropriate set of Semgrep rules for the project.
- `--error`: Returns a failure status when Semgrep reports findings that meet its error criteria.
- `.`: Specifies the current project directory as the scan target.

This configuration makes Semgrep part of the pipeline's security quality checks.

## 3. Latest Scan Results

The latest scan completed successfully.

### Scan summary

| Metric | Result |
|---|---:|
| Targets scanned | 23 |
| Rules executed | 329 |
| Total findings | 0 |
| Blocking findings | 0 |
| Parsed lines | Approximately 100% |
| Scan completion | Successful |

Semgrep reported:

```text
Scan completed successfully.
Findings: 0 (0 blocking)
Rules run: 329
Targets scanned: 23
Parsed lines: ~100.0%
```

No findings were reported across the 23 Git-tracked files included in this scan.

## 4. Investigation and Interpretation

The scan completed without identifying any security findings under the rules executed.

This means that Semgrep did not detect code patterns matching its active security rules in the scanned files.

However, a zero-finding result should not be interpreted as proof that the application contains no vulnerabilities.

Static analysis is dependent on the rules available, the code being scanned and the ability of the tool to recognise particular vulnerability patterns.

## 5. Scan Scope and Limitations

The following limitations were identified from the scan output:

### 5.1 Git-tracked files only

Semgrep reported that the scan was limited to files tracked by Git.

Consequently, untracked files were not included in the assessment.

### 5.2 Semgrep OSS coverage

The scan was performed using Semgrep OSS without logging in to the Semgrep platform.

The output indicated that additional Semgrep Code and Supply Chain capabilities were unavailable, including 1,881 additional Pro rules.

Therefore, the results represent the coverage provided by the rules available to the OSS scan, not the full coverage of Semgrep's commercial products.

### 5.3 Static analysis limitations

Semgrep analyses code patterns and cannot independently establish the security of the complete running application.

Some issues may require additional testing techniques, including:

- Dynamic Application Security Testing (DAST).
- Manual secure code review.
- Authentication and authorization testing.
- Runtime validation and security testing.

## 6. Remediation and Improvements

No Semgrep findings were reported in the latest scan. Therefore, no code remediation was required based on this particular scan result.

The following improvements were retained as part of the assessment:

1. Semgrep was integrated into the automated GitHub Actions workflow.
2. The `--error` option was configured to make qualifying findings fail the pipeline.
3. Automatic ruleset selection was used to provide security analysis without manually maintaining individual rules.
4. Semgrep was used alongside other security tools to provide complementary assessment coverage.

## 7. Recommendations

1. Continue running Semgrep on pushes and pull requests.
2. Review new findings and validate their relevance before deciding on remediation or suppression.
3. Ensure important source files are tracked by Git so they are included in the scan.
4. Periodically review the ruleset and update Semgrep where appropriate.
5. Complement static analysis with dependency scanning, container scanning, DAST and manual code review.
6. Consider additional rules and analysis capabilities where broader coverage is required.

## 8. Conclusion

Semgrep was successfully integrated into the DevSecOps pipeline as a static application security testing tool.

The latest local scan executed 329 rules against 23 Git-tracked files and reported zero findings.

The `--error` configuration also ensures that qualifying findings can affect the pipeline's execution rather than being treated as informational output only.

Although the scan produced no findings, its coverage limitations reinforce the importance of using multiple security testing techniques throughout the application development lifecycle.
