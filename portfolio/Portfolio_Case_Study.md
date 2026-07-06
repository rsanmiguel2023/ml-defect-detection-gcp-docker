# Portfolio Case Study

# 1. Cover Page

**Project:** Enterprise Machine Learning Platform for Industrial Visual Inspection

**Repository:** Industrial Defect Detection Platform

**Author:** Roberto San Miguel

**Version:** 1.0

---

# 2. Document Control

| Item | Description |
|---|---|
| Document Type | Portfolio Case Study |
| Audience | Recruiters, Hiring Managers, Solution Architects, Engineering Managers |
| Purpose | Present the project as an end-to-end enterprise ML engineering engagement |

---

# 3. Revision History

| Version | Date | Description |
|---|---|---|
|1.0|2026|Initial portfolio draft|

---

# 4. Table of Contents

1. Executive Summary
2. Business Context
3. Manufacturing Industry Overview

---

# 5. Executive Summary

This portfolio presents an end-to-end machine learning engineering project designed to demonstrate how a computer vision solution can evolve from experimentation into a production-oriented cloud platform.

Rather than focusing solely on model accuracy, the project emphasizes the engineering practices required to deploy, operate, secure, monitor, and maintain machine learning workloads. The implementation combines TensorFlow and PyTorch model pipelines with FastAPI, Docker, Terraform, GitHub Actions, Google Cloud services, structured observability, automated testing, performance benchmarking, and operational documentation.

The solution was intentionally developed in incremental stages, mirroring the lifecycle of an enterprise software project. Each capability—from infrastructure provisioning to production operations—was introduced through a dedicated feature branch, peer-review workflow, and documented implementation. This approach demonstrates disciplined engineering practices alongside machine learning development.

The resulting repository represents more than an image classification application. It is a reference implementation of a cloud-native ML platform showing how software engineering, cloud engineering, DevOps, and MLOps converge to support reliable production services.

---

# 6. Business Context

Manufacturing organizations continuously seek improvements in quality, throughput, and operational efficiency. Product defects can increase warranty costs, reduce customer confidence, and disrupt production schedules. As manufacturing volumes increase, manual inspection becomes more difficult to scale while maintaining consistent quality.

Computer vision has emerged as a practical technology for supporting quality assurance. Deep learning models can identify patterns in images with consistency that complements human inspectors. However, successful adoption requires more than a trained model. Organizations need secure deployment, repeatable infrastructure, monitoring, testing, documentation, and operational processes before AI solutions can become dependable business assets.

This project addresses those engineering requirements by demonstrating the complete lifecycle of a machine learning application rather than limiting the scope to model development.

---

# 7. Manufacturing Industry Overview

Visual inspection is used throughout manufacturing sectors including automotive, electronics, food processing, pharmaceuticals, and consumer goods. Typical inspection workflows verify product dimensions, packaging quality, surface finish, contamination, and structural integrity.

Historically these inspections have relied heavily on manual review. While experienced inspectors provide valuable expertise, manual processes introduce variability due to fatigue, environmental conditions, and subjective judgement. Scaling inspection generally requires additional personnel, increasing operational costs.

Modern computer vision platforms augment these workflows by providing consistent image classification that can support inspectors, improve throughput, and provide digital traceability. Enterprise adoption, however, depends on much more than predictive performance. Reliability, security, deployment automation, observability, and maintainability become equally important.

The remainder of this case study explains how those engineering concerns shaped the design and implementation of the Industrial Defect Detection Platform.

---

# 8. Current-State Assessment

Most machine learning initiatives begin with experimentation in notebooks where success is measured primarily by model accuracy. While this approach is appropriate during research, it rarely addresses the operational requirements of enterprise environments. Models that perform well during development frequently lack standardized deployment mechanisms, repeatable infrastructure, monitoring, testing, version management, and operational governance.

For industrial inspection workloads, these gaps can become significant barriers to adoption. Manufacturing organizations require dependable systems that are maintainable, observable, and capable of supporting production operations over long periods.

The existing state can therefore be characterized by four common observations:

- Machine learning artifacts are often tightly coupled to development environments.
- Infrastructure is frequently created manually, making deployments difficult to reproduce.
- Operational visibility is limited without structured logs, health checks, or metrics.
- Documentation focuses on model development rather than long-term operational support.

This project was intentionally designed to address these limitations by treating machine learning as an engineering product rather than an isolated analytical exercise.

---

# 9. Business Challenges

Several business challenges influenced the overall solution design.

## Maintaining Product Quality

Product quality directly affects customer satisfaction, warranty claims, regulatory compliance, and brand reputation. Organizations require reliable inspection processes capable of identifying manufacturing defects consistently.

## Scaling Inspection Capacity

As production volumes increase, scaling manual inspection generally requires additional personnel. This approach increases operational costs while introducing variability between inspectors.

## Operational Reliability

Business users require dependable services that remain available, provide predictable performance, and can be supported by operational teams.

## Technology Governance

Enterprise solutions must satisfy security, deployment, documentation, and infrastructure standards before they can be adopted within production environments.

---

# 10. Problem Statement

The primary question addressed by this portfolio is:

> **How can an industrial computer vision model be transformed into a production-ready cloud platform using modern software engineering, cloud engineering, DevOps, and MLOps practices?**

Answering this question required extending the scope beyond image classification into infrastructure automation, deployment, testing, monitoring, benchmarking, security, and operational documentation.

The solution therefore focuses equally on engineering quality attributes and predictive capability.

---

# 11. Opportunity Statement

The opportunity presented by this project extends beyond demonstrating computer vision. It illustrates how organizations can establish repeatable engineering practices for deploying machine learning services.

Key opportunities include:

- Standardized REST-based inference
- Repeatable infrastructure provisioning
- Automated validation and deployment
- Version-controlled model management
- Improved operational visibility
- Better support for future model evolution

These capabilities reduce operational risk while improving maintainability and scalability.

---

# 12. Business Drivers

The architecture was guided by several business drivers.

| Driver | Influence on Solution |
|---|---|
| Consistency | Automated inference provides repeatable predictions |
| Scalability | Cloud Run supports demand-based scaling |
| Maintainability | Modular project structure and Infrastructure as Code |
| Reliability | Health endpoints, readiness checks, and operational procedures |
| Security | Least-privilege configuration and dependency validation |
| Governance | Version control, CI/CD, documentation, and reproducible deployments |

Collectively, these drivers shaped the engineering decisions implemented throughout the repository. Rather than optimizing only for model performance, the platform emphasizes long-term sustainability, operational readiness, and reproducibility. These principles provide a stronger foundation for enterprise adoption than model accuracy alone.

---

The next section of the case study transitions from business analysis into solution architecture, explaining how these drivers influenced the technical design of the platform.


# 13. Project Vision

The vision of the Industrial Defect Detection Platform is to demonstrate how an enterprise machine learning solution can be engineered from concept through production readiness using modern cloud-native practices. The project was intentionally designed to balance data science, software engineering, cloud engineering, DevOps, and MLOps disciplines within a single implementation.

Rather than optimizing only for predictive performance, the platform emphasizes maintainability, scalability, reproducibility, security, and operational support. These qualities enable organizations to transition machine learning solutions from experimentation into dependable production services.

---

# 14. Business Objectives

The project objectives were divided into business, technical, and operational goals.

## Business Objectives

- Improve consistency of image-based inspection.
- Demonstrate a repeatable cloud deployment approach.
- Showcase enterprise engineering practices suitable for production systems.

## Technical Objectives

- Support TensorFlow and PyTorch inference.
- Expose predictions through a REST API.
- Implement Infrastructure as Code.
- Automate testing and CI/CD.
- Provide benchmark tooling and versioned model management.

## Operational Objectives

- Deliver structured logging.
- Provide health, readiness, and metrics endpoints.
- Document production support procedures.
- Establish operational monitoring guidance.

---

# 15. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Accept image uploads for inference |
| FR-02 | Support TensorFlow and PyTorch models |
| FR-03 | Provide single-image prediction |
| FR-04 | Provide batch prediction |
| FR-05 | Support model version selection |
| FR-06 | Return standardized prediction responses |
| FR-07 | Expose health and readiness endpoints |
| FR-08 | Record benchmark results |

---

# 16. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Responsive inference API and benchmark reporting |
| Reliability | Health monitoring and operational documentation |
| Maintainability | Modular architecture and clear project structure |
| Security | Secure configuration and dependency validation |
| Scalability | Stateless deployment suitable for Cloud Run |
| Portability | Docker-based runtime |

These requirements influenced technology selection and architectural decisions throughout the project.

---

# 17. Project Scope

## Included

- Machine learning pipelines
- FastAPI service
- Docker
- Cloud Run
- Terraform
- GitHub Actions
- Testing
- Observability
- Benchmarking
- Production documentation

## Excluded

- Kubernetes orchestration
- Multi-region deployment
- GPU inference
- Automatic retraining
- Model drift detection
- Enterprise ERP/MES integration

The exclusions intentionally limit project complexity while preserving a realistic production architecture.

---

# 18. Stakeholders

| Stakeholder | Role | Primary Interest |
|---|---|---|
| Engineering Manager | Project oversight | Delivery quality |
| Solution Architect | Architecture governance | Technical design |
| ML Engineer | Model development | Prediction quality |
| Cloud Engineer | Infrastructure | Deployment and scalability |
| DevOps Engineer | Automation | CI/CD and reliability |
| Operations Team | Production support | Monitoring and incident response |

---

# 19. Solution Architecture

The Industrial Defect Detection Platform was designed using a layered architecture that separates presentation, application, inference, infrastructure, and operations. This separation allows each layer to evolve independently while maintaining a stable interface for consumers.

```text
Client / Streamlit / Swagger
            │
            ▼
      FastAPI REST API
            │
     Request Validation
            │
     Image Preprocessing
            │
       Model Registry
      ┌──────────────┐
      │              │
TensorFlow      PyTorch
      │              │
      └──────┬───────┘
             ▼
      Prediction Engine
             │
 Structured Logging & Metrics
             │
        JSON Response
```

The API layer isolates clients from implementation details. Consumers interact with a consistent REST interface regardless of the underlying framework or model version.

---

# 20. Architecture Principles

The solution was guided by several architectural principles:

| Principle | Implementation |
|---|---|
| Separation of Concerns | Independent modules for API, models, infrastructure, tests, and documentation |
| Stateless Services | Cloud Run compatible API with no session affinity |
| Infrastructure as Code | Terraform manages cloud resources |
| Automation First | GitHub Actions validates code and deployment workflows |
| Security by Default | Dependency scanning, secure configuration, least privilege |
| Observability | Health endpoints, readiness checks, structured logs, benchmark reporting |

These principles improve maintainability and simplify future enhancements.

---

# 21. Cloud Architecture

```text
Developer
    │
GitHub Repository
    │
GitHub Actions
    │
Docker Build
    │
Artifact Registry
    │
Cloud Run
    │
FastAPI Service
    │
Cloud Storage
```

Infrastructure resources are defined through Terraform, allowing environments to be recreated consistently while reducing configuration drift.

---

# 22. Request and Model Lifecycle

## Request Lifecycle

1. Client uploads an image.
2. FastAPI validates the request.
3. Image preprocessing prepares the input.
4. The requested framework and model version are resolved.
5. The model is loaded from cache or registry.
6. Inference is executed.
7. Prediction results are returned.
8. Structured logs and timing metrics are recorded.

## Model Lifecycle

```text
Training
   │
Validation
   │
Version Registration
   │
Deployment
   │
Inference
   │
Monitoring
   │
Future Retraining
```

Versioned models enable controlled upgrades and future rollback strategies without changing the API contract.

---

# 23. Technology Selection

| Technology | Selected Because | Alternatives Considered |
|---|---|---|
| FastAPI | High performance, OpenAPI support, validation | Flask |
| TensorFlow | Mature transfer learning ecosystem | PyTorch only |
| PyTorch | Flexible experimentation | TensorFlow only |
| Docker | Consistent runtime | Native deployment |
| Cloud Run | Serverless scalability | Virtual Machines, GKE |
| Terraform | Reproducible infrastructure | Manual provisioning |
| GitHub Actions | Native repository automation | Jenkins |

The chosen technologies balance implementation complexity with operational simplicity and align well with modern cloud-native engineering practices.

---

# 24. Engineering Decisions

Several architectural decisions significantly influenced the final implementation.

* FastAPI was selected to provide a modern REST interface with automatic API documentation and request validation.

* Cloud Run was selected to reduce infrastructure management while supporting automatic scaling and container-based deployment.

* Terraform ensures cloud resources remain version-controlled and reproducible.

* TensorFlow and PyTorch were both implemented to demonstrate framework flexibility and enable comparative benchmarking.

* Benchmarking, testing, observability, and operational documentation were treated as first-class deliverables rather than optional enhancements.

---

# 25. Production Readiness

A successful machine learning model is only one component of an enterprise solution. Before deployment into production, organizations require confidence that the application can be operated, monitored, maintained, and supported over time.

The Industrial Defect Detection Platform incorporates several production-oriented capabilities:

| Capability | Implementation |
|---|---|
| Infrastructure as Code | Terraform |
| Containerization | Docker |
| Cloud Deployment | Google Cloud Run |
| CI/CD | GitHub Actions |
| Health Monitoring | `/health` and `/ready` endpoints |
| Observability | Structured logging and runtime metrics |
| Operational Documentation | Runbooks, SLOs, incident response, operations guide |

These capabilities provide a foundation for reliable deployment and future operational maturity.

---

# 26. Testing Strategy

Testing was integrated throughout the project lifecycle to improve confidence in application behavior and reduce regression risk.

Testing activities included:

- Unit testing of application components
- API endpoint validation
- Configuration verification
- Model registry validation
- Benchmark verification
- Dependency validation
- Continuous Integration checks

The objective was not simply to confirm functionality but to establish repeatable validation processes that support ongoing development.

---

# 27. Performance Benchmarking

Performance benchmarking established an initial baseline for evaluating the platform.

Benchmark categories included:

- API latency
- Batch prediction throughput
- TensorFlow inference
- PyTorch inference
- Cold-start versus warm inference

These measurements help identify performance characteristics and provide a reference point for future optimization efforts.

Benchmark reports are generated automatically and stored as part of the repository documentation, supporting reproducibility and engineering analysis.

---

# 28. Security and Observability

Security and operational visibility were treated as essential architectural concerns rather than post-development enhancements.

Security considerations include:

- Secure dependency management
- Least-privilege cloud configuration
- Externalized configuration
- Infrastructure managed through code
- Version-controlled deployments

Observability capabilities include:

- Structured JSON logging
- Request tracing identifiers
- Health endpoints
- Readiness endpoints
- Runtime metrics
- Benchmark reporting

Together, these capabilities improve operational awareness and simplify troubleshooting.

---

# 29. Project Outcomes

The project successfully demonstrates an end-to-end machine learning engineering workflow extending from model development to production readiness.

Key outcomes include:

- Functional TensorFlow and PyTorch inference pipelines
- REST-based prediction service
- Cloud-native deployment architecture
- Infrastructure as Code implementation
- Automated CI/CD validation
- Comprehensive testing framework
- Benchmarking utilities
- Production operations documentation

More importantly, the repository demonstrates how software engineering, cloud engineering, DevOps, and MLOps practices complement machine learning development within a unified solution.

---

# 30. Lessons Learned

Several themes emerged during implementation.

Machine learning systems require significantly more engineering effort than model development alone. Operational success depends on reproducible infrastructure, deployment automation, monitoring, documentation, and testing.

Incremental delivery through feature branches simplified development while reducing integration risk. Infrastructure as Code improved consistency across environments, while benchmarking and observability provided valuable operational insight.

The project also reinforced the importance of documentation. Well-structured technical documentation supports maintainability, onboarding, and long-term project evolution.

---

# 31. Future Roadmap

Future enhancements may include:

- Kubernetes deployment
- GPU-backed inference
- OpenTelemetry distributed tracing
- Prometheus and Grafana monitoring
- Model drift detection
- Automated retraining pipelines
- Canary deployments
- Multi-region disaster recovery
- Cost optimization dashboards

These enhancements build upon the existing architecture without requiring significant redesign.

---

# 32. Conclusion

The Industrial Defect Detection Platform demonstrates that delivering value from machine learning requires more than accurate predictive models. Sustainable enterprise solutions depend on thoughtful architecture, disciplined engineering, cloud-native deployment, operational visibility, automation, and comprehensive documentation.

By integrating machine learning, software engineering, cloud engineering, DevOps, and MLOps into a single implementation, the project provides a realistic example of how production-oriented AI systems can be designed and operated. The resulting repository serves not only as a technical demonstration but also as a portfolio showcasing the engineering practices necessary to support enterprise machine learning initiatives.
