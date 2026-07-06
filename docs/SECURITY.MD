# Security

## Overview

This document summarizes the security controls implemented across the platform.

## Security Principles

- Least privilege
- Defense in depth
- Secure by default
- No embedded secrets
- Infrastructure as Code
- Immutable container deployment

## Implemented Controls

- FastAPI security headers
- Dependency scanning with pip-audit
- Workload Identity Federation
- Dedicated Cloud Run service account
- Terraform-managed IAM
- Public Access Prevention
- Uniform Bucket-Level Access
- Secrets excluded from Git

## Future Enhancements

- Google Secret Manager
- Cloud Armor
- SBOM generation
- Container vulnerability scanning
- API authentication
- Rate limiting
- Security event logging
