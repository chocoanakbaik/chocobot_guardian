# Chocobot Guardian

**A lightweight, local-first intelligent guardian for Windows.**

Chocobot Guardian (CG) is a desktop system utility project designed to help users inspect, monitor, diagnose, protect, and manage their computer through a lightweight local application.

CG is built with a strong focus on:

* Local-first operation
* Offline capability
* Lightweight resource usage
* Windows compatibility
* Modular architecture
* Security and system awareness
* A futuristic and professional user experience

> **Chocobot Guardian is not designed to be a large general-purpose chatbot.**
>
> Its intelligence is intended to serve the computer itself: understanding system conditions, detecting problems, assisting with diagnostics, and helping the user manage their device.

---

## Project Status

**Current stage: Foundation / Active Development**

The repository currently contains the application foundation, user interface structure, configuration system, logging system, splash screen, and the planned modular engine architecture.

Some engine modules are still under development and may currently contain placeholder or empty implementations.

The project is intentionally being developed in stages rather than pretending that unfinished features are already functional.

---

## Core Direction

Chocobot Guardian is being developed around several major capabilities.

### System Monitoring

CG is intended to observe important system information such as:

* CPU usage
* Memory usage
* Running processes
* Basic operating-system information
* Resource conditions
* General system status

### Security

The security engine is intended to provide local analysis and protection features such as:

* File inspection
* Suspicious-file analysis
* Security scanning
* Quarantine management
* Local whitelist management
* Risk-oriented analysis

### File Intelligence

CG is designed to provide useful information about files and folders, including:

* File information
* Folder analysis
* Hash generation
* Local file inspection
* File-related utilities

### Link Inspection

The link-inspection engine is intended to help users analyze links locally through:

* URL parsing
* Suspicious-pattern detection
* Risk scoring
* Link inspection

CG does not depend on an online URL-scanning service.

### Network Utilities

The project includes a foundation for local network diagnostic utilities such as:

* DNS lookup
* IP information
* Ping
* Port checking

These tools are intended as diagnostic utilities rather than cloud-based services.

### File Conversion

The project also provides a modular foundation for file-conversion utilities, including planned support for:

* Image to PDF
* PDF to image
* PDF to Word
* Word to PDF

Individual conversion modules are being implemented progressively.

---

# Design Philosophy

## Local First

Chocobot Guardian is designed to operate locally on the user's computer.

The project does not depend on:

* Cloud AI
* Remote servers
* Mandatory online accounts
* External APIs
* Third-party online security services

The goal is to keep the core application useful even without an internet connection.

---

## Lightweight

CG is designed with older and lower-specification computers in mind.

The architecture prioritizes:

* Low memory usage
* Reasonable CPU usage
* Lightweight dependencies
* Efficient local processing
* Compatibility with older Windows environments

The project aims to remain practical on machines that cannot comfortably run large modern applications.

---

## Modular Architecture

CG is divided into separate layers so individual systems can be developed and tested independently.

```text
Chocobot Guardian
│
├── Application
│
├── UI
│   ├── Screens
│   ├── Widgets
│   └── Styles
│
├── Engine
│   ├── Converter
│   ├── File Tools
│   ├── Link Inspector
│   ├── Network
│   ├── Security
│   ├── System
│   └── Utilities
│
├── Data
│   ├── Configuration
│   ├── Language
│   └── Logs
│
├── Tests
│
└── Tools
```

This structure allows CG to grow without turning the entire application into one large monolithic script.

---

# Technology

The current project is built primarily with:

* Python
* Tkinter
* Pillow
* JSON
* Python standard library

The application is intentionally avoiding unnecessary frameworks and heavyweight dependencies.

---

# Repository Structure

```text
chocobot_guardian/
│
├── assets/
│   ├── icons/
│   └── images/
│
├── chocobot/
│   ├── data/
│   │   ├── language/
│   │   ├── logs/
│   │   └── config.json
│   │
│   ├── docs/
│   │   ├── changelog.md
│   │   ├── developer_notes.md
│   │   ├── license.md
│   │   └── user_guide.md
│   │
│   ├── engine/
│   │   ├── converter/
│   │   ├── file_tools/
│   │   ├── link/
│   │   ├── network/
│   │   ├── security/
│   │   ├── system/
│   │   └── utils/
│   │
│   ├── ui/
│   │   ├── screens/
│   │   ├── styles.py
│   │   └── widgets.py
│   │
│   ├── app.py
│   ├── config.py
│   ├── constants.py
│   └── __init__.py
│
├── tests/
│
├── tools/
│   └── icon_converter.py
│
├── main.py
├── splash_screen.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# User Interface

The interface is being developed around a futuristic technology-oriented visual identity.

The design direction focuses on:

* Dark interface
* Neon-inspired visual accents
* Clear information hierarchy
* Smooth interaction
* Professional presentation
* Lightweight rendering

The visual design should feel like a real desktop product rather than a basic Python prototype.

At the same time, visual effects are expected to remain reasonable for low-spec hardware.

---

# Supported Languages

The project currently provides a language-data foundation for:

* English
* Indonesian
* Spanish
* French
* Russian
* Chinese
* Arabic

Language files are stored under:

```text
chocobot/data/language/
```

The language system is designed so additional translations can be added without rebuilding the entire application architecture.

---

# Configuration

Application configuration is stored locally.

```text
chocobot/data/config.json
```

The configuration system is designed to keep application preferences persistent between sessions without requiring a remote database.

---

# Logging

Application logs are stored locally.

```text
chocobot/data/logs/chocobot.log
```

Logging is used to help diagnose application errors and development issues.

---

# Security Philosophy

Chocobot Guardian is intended to assist with system security, but it should not make unrealistic claims.

The project does not currently claim to be a replacement for:

* Professional antivirus software
* Enterprise endpoint security
* Security researchers
* Operating-system security mechanisms

Security features will be implemented progressively and tested carefully before being considered production-ready.

---

# Development Principles

CG follows several development principles.

### 1. Do not fake functionality

A feature is not considered complete simply because a button or menu exists.

The underlying engine must actually perform the intended operation.

### 2. Local-first by design

Core functionality should remain usable without cloud infrastructure.

### 3. Avoid unnecessary dependencies

Every dependency should have a real reason to exist.

### 4. Keep modules independent

System monitoring should not unnecessarily depend on the security engine, and file utilities should not become tightly coupled to the UI.

### 5. Test before calling a feature complete

Important engine functionality should receive appropriate tests before being considered stable.

### 6. Performance matters

A feature that works but consumes excessive resources is not considered ideal for the CG target hardware.

---

# Development Roadmap

## Phase 1 — Foundation

* [x] Project structure
* [x] Application entry point
* [x] Splash screen foundation
* [x] Configuration system
* [x] Logging system
* [x] UI architecture
* [x] Language-data structure
* [x] Engine module structure
* [x] Test structure

## Phase 2 — Core Engines

* [ ] System information engine
* [ ] Resource monitoring
* [ ] Process monitoring
* [ ] File information engine
* [ ] Folder analysis
* [ ] Hashing
* [ ] Network diagnostics
* [ ] Link inspection
* [ ] Security scanner
* [ ] File analyzer
* [ ] Quarantine system
* [ ] File conversion utilities

## Phase 3 — Guardian Intelligence

* [ ] System condition analysis
* [ ] Local diagnostic reasoning
* [ ] Problem classification
* [ ] Risk prioritization
* [ ] Recommended actions
* [ ] Local persistent intelligence
* [ ] Historical system observations

## Phase 4 — Guardian Automation

* [ ] Automated diagnostics
* [ ] Safe repair operations
* [ ] Recovery mechanisms
* [ ] System health reports
* [ ] Advanced security workflows

## Phase 5 — Polish

* [ ] UI refinement
* [ ] Animation optimization
* [ ] Performance optimization
* [ ] Accessibility improvements
* [ ] Expanded testing
* [ ] Packaging
* [ ] Windows deployment testing

---

# Running the Project

Install the required dependency:

```text
py -m pip install -r requirements.txt
```

Then run:

```text
py main.py
```

The project is currently intended to be developed and tested from source.

---

# Development Environment

The project is designed with older Windows systems in mind, with particular attention to:

* Windows 7
* Windows 8.1
* Windows 10
* Windows 11

Actual compatibility may vary depending on the Python version, installed system components, and individual engine requirements.

---

# Testing

Tests are located in:

```text
tests/
```

The project uses separate test modules for major engine categories.

Before releasing a major feature, the relevant engine should be tested independently from the graphical interface where practical.

---

# Offline Architecture

The intended architecture is:

```text
User
  │
  ▼
Chocobot Guardian
  │
  ├── UI
  │
  ├── Local Engine
  │
  ├── Local Configuration
  │
  ├── Local Logs
  │
  └── Local Data
```

There is intentionally no required:

```text
Cloud API
Remote AI
External Server
Online Database
```

This keeps the core architecture independent from external service availability.

---

# Project Vision

Chocobot Guardian is being built as more than a collection of small utilities.

The long-term goal is to create a lightweight local guardian capable of understanding the state of a computer and helping the user respond to problems.

Instead of simply displaying:

> "CPU usage: 95%"

the long-term direction is for CG to be able to reason about the situation locally:

> "CPU usage is unusually high. These processes are responsible for most of the current load. The system has been under high load for several minutes. Consider closing or investigating the listed processes."

The same philosophy applies to security, storage, networking, diagnostics, and other system conditions.

The intelligence should serve the device.

---

# Project Status

Chocobot Guardian is an actively developed solo-development project.

Features marked as planned or under development should not be considered production-ready.

Architecture and implementation may change as development progresses.

---

# License

See:

```text
LICENSE
```

for the complete license terms.

---

## Chocobot Guardian

**Local intelligence.
System awareness.
Device protection.**

Built as an independent solo-development project.
