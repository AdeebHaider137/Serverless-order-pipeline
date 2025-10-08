🧩 Serverless Order Processing Pipeline (Alpha)


[![AWS](https://img.shields.io/badge/Cloud-AWS-orange?logo=amazonaws)](https://aws.amazon.com/)
[![Serverless Framework](https://img.shields.io/badge/Infra-Serverless_Framework-blueviolet?logo=serverless)](https://www.serverless.com/)
[![CI/CD](https://img.shields.io/badge/CI/CD-GitHub_Actions-blue?logo=githubactions)](https://github.com/features/actions)
[![Status](https://img.shields.io/badge/Stage-Alpha-yellow)]()


A serverless, event-driven order processing workflow built on **AWS Lambda**, **DynamoDB**, **SQS**, and **SNS** — designed for scalability, fault tolerance, and automated notifications.

 Overview

This project demonstrates a **cloud-native order pipeline** where orders flow through DynamoDB, get processed asynchronously via SQS and Lambda, and trigger SNS notifications upon updates or failures.

Tech Stack

* **AWS Lambda** – Core compute for order processing & notification
* **Amazon DynamoDB** – NoSQL order storage
* **Amazon SQS (DLQ)** – Reliable, decoupled message queue
* **Amazon SNS** – Real-time alerts & notifications
* **Serverless Framework** – Infrastructure as Code (IaC)
* **GitHub Actions** – CI/CD for automated deployments

---

Current Status

> **Alpha Phase** – Core components deployed and functional.
> Further improvements planned for enhanced observability, testing, and automation.

---

Deployment

```
npx serverless deploy --stage prod
```

