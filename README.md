# CloudFunc - Serverless Function Platform

CloudFunc is a lightweight, serverless function platform that enables developers to deploy and execute functions in isolated Docker containers. It implements a microservices architecture with intelligent container lifecycle management, including warm container optimization to reduce cold start latency.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
- [Features](#features)
- [Quick Start Example](#quick-start-example)

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

## Quick Start Example

This example demonstrates how to deploy and invoke the `hello_fn` function using the CloudFunc CLI.

### Prerequisites

1. Ensure all services are running:
```bash
docker compose up --build
```

2. Install CLI dependencies:
```bash
cd cli
pip install click requests
```

### Deploy the Function

The `hello_fn` function is a simple greeter that takes a name and returns a personalized greeting.

**Function Code** (`hello_fn/function.py`):
```python
def handler(event):
    return f"Hello {event.get('name', 'World')}!"
```

Deploy the function:
```bash
python cli/cloudfunc.py deploy hello_fn
```

This will:
- Build the Docker image using the Python runtime
- Register the function with the function registry
- Make it available for invocation

### Invoke the Function

**Example 1: Basic invocation**
```bash
python cli/cloudfunc.py invoke hello_fn --data '{"name":"Alice"}'
```

**Example 2: Without a name (uses default)**
```bash
python cli/cloudfunc.py invoke hello_fn --data '{}'
```

**Example 3: Multiple invocations (demonstrating warm start)**
```bash
python cli/cloudfunc.py invoke hello_fn --data '{"name":"Bob"}'
python cli/cloudfunc.py invoke hello_fn --data '{"name":"Charlie"}'
python cli/cloudfunc.py invoke hello_fn --data '{"name":"Diana"}'
```

The first invocation will experience a cold start (container creation), while subsequent invocations within 60 seconds will use the warm container for faster execution.

### View Function Output

To see the function execution results and logs:
```bash
docker logs cloudfunc-container-manager -f
```

You should see output similar to:
```
Cold start for hello_fn
Container started: a1b2c3d4e5f6
Executing hello_fn with payload {'name': 'Alice'}
Function output:
CloudFunc Python runtime started
Hello Alice!
Successfully invoked hello_fn
ContainerManager created for hello_fn. Cleanup in 60s.
```

### Understanding the Workflow

1. **CLI** sends deploy/invoke request to **API Gateway** (port 8000)
2. **API Gateway** registers the function in **Function Registry** (port 7000)
3. **Scheduler** (port 9000) receives invocation and publishes to **RabbitMQ**
4. **Container Manager** consumes the message and executes the function in a Docker container
5. Function output is printed to container-manager logs
6. Container remains warm for 60 seconds for subsequent invocations


