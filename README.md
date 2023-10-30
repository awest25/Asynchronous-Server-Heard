# Application Server Herd using `asyncio`

**Language**: Python <br/>
**Date**: Mar 2023 <br/>
**Repository**: [github.com/awest25/Asynchronous-Server-Heard](https://github.com/awest25/Asynchronous-Server-Heard)

## Overview
A modern and scalable approach to server communication, this project evaluates the strengths of Python's `asyncio` for building a decentralized server architecture, called "Application Server Herd". Aimed at potentially replacing Wikimedia's centralized server platform, this architecture intends to meet the rising demand for faster updates, versatile protocol support, and optimized mobile client experiences.

## Objectives

1. **Research**: Dive deep into `asyncio` (Python 3.11.2), understanding its intricacies and performance metrics.
2. **Server Prototyping**: Develop five distinct servers with designated IDs: 'Bailey', 'Bona', 'Campbell', 'Clark', 'Jaquez'. Communication protocol:
    - Clark <-> Jaquez, Bona
    - Campbell <-> Bailey, Bona, Jaquez
    - Bona <-> Bailey
3. **Mobile Integration**: Servers to be primed to accept TCP connections from mobile devices. Adopted message format: `IAMAT kiwi.cs.ucla.edu +34.068930-118.445127 1621464827.959498503`.
4. **Server Response**: `AT Clark +0.263873386 kiwi.cs.ucla.edu +34.068930-118.445127 1621464827.959498503`.
5. **Location-based Queries**: Clients can inquire about nearby places with: `WHATSAT kiwi.cs.ucla.edu 10 5`.
6. **Inter-Server Communication**: While AT messages ensure location updates propagation between servers, Google Places will directly provide the place data.
7. **Logging**: Maintain comprehensive logs for each server detailing operations and connections.
8. **Integration with Google Places API**: Utilize `aiohttp` for HTTP requests to the Google Places API.
9. **Server Initialization**: The main file, `server.py`, when executed, will require a server name argument (e.g., `python3 server.py Clark`).

## Technical Report

Detailed in `Server_Heard_Feasibility.pdf` is the feasibility report for using `asyncio` for a server-heard-style application. It includes answers to the following questions:

1. **Evaluation**: Is `asyncio` the right tool for this project?
2. **Python's Technicalities**: Discuss Python's type checking mechanism, its memory management system, and its stand on multithreading, especially in comparison with Java.
3. **Comparative Analysis**: Position `asyncio` against the likes of Node.js. Understand where each shines and falters.
4. **Programming Language Insights**: Dive into language-level intricacies, examining the composition and performance of asyncio-based programs.

## Technology Stack

- **Main Framework**: `asyncio` (Python 3.11.2)
- **HTTP Requests**: `aiohttp`
- **Location Data Source**: Google Places API
- **Server Communication**: Custom TCP-based protocol

## Quick Start

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the directory: `cd <repository-directory>`
3. Start a server: `python3 server.py <server_name>`
