# Hybrid Classical and Post-Quantum TLS Proxy for Secure Legacy Applications

## Project Overview

This project implements a TLS proxy that enables legacy applications to communicate securely with modern backend services using hybrid classical and post-quantum cryptography.

The proxy acts as an intermediate layer between a legacy client and a backend server. It terminates the TLS connection from the legacy application and establishes a new TLS connection with the backend using either classical or hybrid post-quantum cryptography.

## Architecture

Legacy Application
        |
        | TLS
        v
   TLS Proxy
        |
        | TLS 1.3
        | Classical / Hybrid
        v
Backend Application

## Security Modes

### Classical TLS

- TLS 1.3
- RSA-2048 certificate for authentication
- X25519 for key establishment

### Hybrid Post-Quantum TLS

- TLS 1.3
- RSA-2048 certificate for authentication
- X25519 + ML-KEM-768 hybrid key establishment
- X25519MLKEM768 hybrid group

## Main Components

- TLS Proxy
- Legacy Client Simulator
- Backend Server
- Classical TLS configuration
- Hybrid Post-Quantum TLS configuration
- Performance benchmarking
- Security monitoring dashboard

## Technologies

- OpenSSL
- Python
- TLS 1.3
- RSA
- X25519
- ML-KEM-768
- Streamlit
- Git

