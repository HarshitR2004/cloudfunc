# CloudFunc - Serverless Function Platform

CloudFunc is a lightweight, serverless function platform that enables developers to deploy and execute functions in isolated Docker containers. It implements a microservices architecture with intelligent container lifecycle management, including warm container optimization to reduce cold start latency.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Features](#features)

## Overview

CloudFunc provides a complete serverless execution environment with the following capabilities:

- Deploy custom functions as Docker containers
- Execute functions on-demand via CLI or API
- Asynchronous invocation using message queues
- Warm container pooling for optimized performance
- Automatic container lifecycle management
- Function registry with PostgreSQL persistence

## Architecture

CloudFunc follows a distributed microservices architecture:

```
┌─────────────┐
│     CLI     │
└──────┬──────┘
       │
       v
┌─────────────────┐      ┌──────────────────┐
│   API Gateway   │─────>│ Function Registry│
│                 │                         │
└────────┬────────┘      └────────┬─────────┘
         │                        │
         v                        v
┌─────────────────┐         ┌──────────┐
│    Scheduler    │────────>│PostgreSQL│
│                 │         └──────────┘
└────────┬────────┘
         │
         v
    ┌─────────┐
    │RabbitMQ │
    └────┬────┘
         │
         v
┌──────────────────┐       ┌─────────────────┐
│Container Manager │──────>│Docker Containers│
│                  │       │  (Functions)    │
└──────────────────┘       └─────────────────┘
```

## Components

### 1. API Gateway
- Entry point for all client requests
- Handles function deployment requests
- Routes invocation requests to the scheduler

### 2. Function Registry
- Manages function metadata and state
- Stores function information in PostgreSQL
- Tracks warm container status

### 3. Scheduler
- Receives invocation requests from API Gateway
- Publishes function invocation messages to RabbitMQ
- Coordinates between API Gateway and Container Manager

### 4. Container Manager
- Consumes invocation messages from RabbitMQ
- Manages Docker container lifecycle (start, stop, cleanup)
- Implements warm container pooling with intelligent timeout management
- Executes functions in isolated containers
- Handles both cold starts and warm starts

### 5. PostgreSQL Database
- Persists function metadata
- Stores function registry information

### 6. RabbitMQ Message Queue
- Enables asynchronous function invocation
- Decouples scheduler from container execution

### 7. CLI Tool
- Command-line interface for function management
- Supports deployment and invocation operations

## Features

### Warm Container Management
CloudFunc implements an intelligent container lifecycle management system:
- Containers remain "warm" for 60 seconds after the last invocation
- Subsequent invocations within the warm period execute immediately (warm start)
- Timer resets on each invocation to keep frequently-used functions warm
- Automatic cleanup after idle timeout to free resources

### Cold Start Optimization
- First invocation creates and starts a new container (cold start)
- Container is added to the warm pool immediately
- Future invocations within 60 seconds use the existing container

### Asynchronous Execution
- All function invocations are processed asynchronously via RabbitMQ
- Non-blocking API responses
- Reliable message delivery with acknowledgments


