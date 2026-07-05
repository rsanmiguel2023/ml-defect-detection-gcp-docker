# Security

## Overview

This project includes baseline security controls for the Industrial Defect Detection platform across API responses, dependency management, cloud deployment, and infrastructure configuration.

## Security Controls

The current implementation includes:

- FastAPI security headers
- Dependency vulnerability scanning with `pip-audit`
- Cloud Run service account separation
- Workload Identity Federation for GitHub Actions
- No long-lived GCP service account keys
- Terraform-managed IAM resources
- Public access prevention on Cloud Storage
- Uniform bucket-level access
- `.env` and local secrets excluded from Git

## API Security Headers

The FastAPI service adds the following response headers:

```text
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: no-referrer
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

These reduce common browser and client-side risks.

## Dependency Security Scanning

GitHub Actions runs dependency scanning using:

```bash
pip-audit -r requirements.txt
```

This checks Python dependencies for known vulnerabilities.

## Cloud Security

### Workload Identity Federation

GitHub Actions authenticates to Google Cloud using Workload Identity Federation instead of static JSON keys.

Benefits:

- No long-lived credentials in GitHub
- Short-lived identity tokens
- Reduced secret exposure risk
- Better alignment with cloud security best practices

### Cloud Run Identity

Cloud Run runs using a dedicated service account instead of the default compute service account.

This supports least-privilege access control.

## Storage Security

The Cloud Storage bucket is configured with:

- Uniform bucket-level access
- Public access prevention
- Versioning
- Lifecycle rules

## Secrets Handling

The following files must not be committed:

```text
.env
terraform.tfvars
service-account-key.json
github-actions-key.json
```

## Future Enhancements

Planned security improvements:

- Google Secret Manager integration
- Container image vulnerability scanning
- Rate limiting
- API authentication
- Signed upload URLs
- Security event logging
- Terraform IAM least-privilege review
- Cloud Armor protection
- SAST scanning
- SBOM generation