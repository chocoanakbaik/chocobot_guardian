# Chocobot Guardian

**A lightweight, local-first intelligent guardian for Windows.**

Chocobot Guardian (CG) is a desktop system utility project designed to help users inspect, monitor, diagnose, protect, and manage their computer through a lightweight local application.

CG is built with a strong focus on:

* Local-first operation
* Offline capability
* Lightweight resource usage
* Adaptive device compatibility
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

# Adaptive Device Architecture

## Core Principle

> **CG adapts to the user's device. The user's device does not adapt to CG.**

Chocobot Guardian is intended to run on different computers with different hardware, operating-system versions, architectures, installed runtimes, permissions, and available system capabilities.

CG must therefore discover the actual environment it is running on and adapt its own behavior accordingly.

CG must **not** assume that the developer's machine represents every user's machine.

Compatibility is not determined by Windows version alone. Two computers running the same Windows version can have different CPUs, RAM amounts, graphics capabilities, storage conditions, Python/runtime environments, permissions, and other system characteristics.

The device environment is therefore treated as part of CG's runtime context.

## Startup Device Discovery

The long-term startup flow is designed to follow this order:

```text
CG starts
   │
   ▼
Splash / Loading
   │
   ▼
Device Discovery
   │
   ├── Operating system
   ├── OS version/build
   ├── Architecture
   ├── CPU
   ├── RAM
   ├── GPU / graphics capability
   ├── Storage information
   ├── Python/runtime environment
   ├── Required system components
   └── Relevant permissions/capabilities
   │
   ▼
Compatibility Profile
   │
   ▼
Capability & Component Selection
   │
   ▼
Activate compatible CG components
   │
   ├── Compatible → available
   ├── Alternative variant → selected
   └── Incompatible → disabled/locked safely
   │
   ▼
Start Chocobot Guardian
```

The discovery process should be lightweight, deterministic, and safe. It should not unnecessarily modify the user's system merely to determine compatibility.

## Compatibility Profile

CG should eventually build a local compatibility profile from the detected environment.

The profile may include:

* OS family and version
* Architecture
* CPU characteristics
* Available memory
* Graphics capability
* Storage conditions relevant to CG
* Python/runtime version
* Installed components required by CG
* Permission and capability information
* Feature-specific compatibility information

The profile exists so CG can make informed decisions about which implementation or component variant should be used.

## Component Strategy

CG should be distributed with **only the components, runtimes, libraries, or installer payloads that CG actually needs**.

The goal is not to bundle every possible installer or every possible version of every system component.

When multiple variants are genuinely required for supported environments, the CG distribution may contain multiple compatible variants. CG should select the appropriate variant after device discovery.

Conceptually:

```text
CG Distribution
│
├── CG Application
├── Core Engine
├── Compatibility Rules
├── Device Detection
└── Required Component Packages
    ├── Variant A
    ├── Variant B
    └── Variant C
```

The exact package contents must be based on actual CG requirements, supported environments, redistribution rights, security, and maintenance feasibility.

CG must not blindly bundle unrelated Microsoft/system installers, third-party software, or unnecessary runtimes simply because they might be useful someday.

## Component Selection Rules

Component selection should consider the complete detected environment, not only one variable.

For example:

```text
Detected Device
       │
       ├── Windows version
       ├── Architecture
       ├── CPU capability
       ├── RAM
       ├── Graphics capability
       ├── Runtime version
       └── Permissions
              │
              ▼
       Compatibility Rules
              │
       ┌──────┴──────┐
       ▼             ▼
 Compatible       Incompatible
       │                 │
       ▼                 ▼
 Activate         Disable / Lock
```

An incompatible component must never be activated merely to force CG to run.

If an alternative compatible component exists, CG should prefer that alternative.

If no compatible implementation exists, CG should degrade gracefully, clearly report the limitation, and keep the rest of the application usable where possible.

## Safety and Transparency

Automatic compatibility handling must not become uncontrolled system modification.

CG should:

* Detect before changing
* Validate before installing
* Prefer existing compatible components when possible
* Avoid unnecessary system changes
* Keep component selection explainable
* Record important compatibility decisions in local logs
* Fail safely when a required component cannot be provided
* Never pretend that an incompatible component is compatible

Any future installer system must also account for licensing, redistribution rights, package integrity, version maintenance, and security before a component is bundled with CG.

This architecture is a design requirement for future development, not a claim that the complete automatic installer system is already implemented.

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

The adaptive device architecture will eventually become an engine-level capability and should remain separated from the UI. The UI may present compatibility information, but it must not contain the core compatibility logic.

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
├── tools/
│   └── icon_converter.py
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

### 7. Adapt to the device

CG must adapt to the user's actual device environment instead of requiring the user's device to conform to CG.

### 8. Detect before modifying

CG should inspect the environment before installing, activating, disabling, repairing, or otherwise changing system components.

### 9. Never force incompatibility

An incompatible component must not be forced into operation. CG should select a compatible alternative, disable the incompatible component, or gracefully reduce functionality.

### 10. Planned is not implemented

Architecture, roadmap items, and documentation must never be presented as completed functionality until the corresponding code has actually been implemented and tested.

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

* [ ] Adaptive device discovery and compatibility profiling
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
* [ ] Adaptive component management
* [ ] Compatible component installation/activation

## Phase 5 — Polish

* [ ] UI refinement
* [ ] Animation optimization
* [ ] Performance optimization
* [ ] Accessibility improvements
* [ ] Expanded testing
* [ ] Packaging
* [ ] Windows deployment testing
* [ ] Multi-device compatibility testing

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

The long-term compatibility strategy is adaptive: CG should inspect the actual machine and choose compatible behavior instead of assuming that every supported Windows version has the same hardware or runtime environment.

---

# Testing

Tests are located in:

```text
tests/
```

The project uses separate test modules for major engine categories.

Before releasing a major feature, the relevant engine should be tested independently from the graphical interface where practical.

Adaptive compatibility features should be tested across different OS versions, architectures, hardware profiles, runtime versions, permissions, and missing-component scenarios where practical.

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
  ├── Adaptive Device Layer
  │     ├── Device Discovery
  │     ├── Compatibility Profile
  │     └── Component Selection
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

The long-term direction is for CG to be able to reason about the situation locally:

> "CPU usage is unusually high. These processes are responsible for most of the current load. The system has been under high load for several minutes. Consider closing or investigating the listed processes."

The same philosophy applies to security, storage, networking, diagnostics, and other system conditions.

The intelligence should serve the device.

The same principle applies to compatibility: CG should understand the device it is running on and adapt itself to that environment.

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
