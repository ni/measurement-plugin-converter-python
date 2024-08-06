# NI Measurement Plug In Converter

- [NI Measurement Plug In Converter](#ni-measurement-plug-in-converter)
  - [Who](#who)
  - [Related links](#related-links)
  - [Problem statement](#problem-statement)
  - [Workflow](#workflow)
  - [Design \& Implementation](#design--implementation)
  - [Alternative implementations / Designs](#alternative-implementations--designs)
  - [Open items](#open-items)

## Who

Author: National Instruments \
Team: ModernLab Success

## Related links

[Feature - Python Code Migration Utility](https://dev.azure.com/ni/DevCentral/_backlogs/backlog/ModernLab%20Reference%20Architecture/Epics/?workitem=2809380)

## Problem statement

- For a test engineer who develops Python measurements needs to convert those Python measurements to measurement plugins. `NI Measurement Plug In Converter` solves the problem of manual conversion and helps in automating the conversion process.
<!--
    Provide a brief overview of the issue this tool addresses and the tool's objective.
-->

## Workflow
<!--
    Attach the workflow diagram
-->

## Design & Implementation

<!--
    Explain how the design addresses the user problem and workflow.

    Possible sections to add:
    * Notable high-level changes to existing design
    * Subdivisions of the problem addressed in this implementation
    * Examples
    * Performance considerations
    * UX considerations
-->

## Alternative implementations / Designs

- No alternate implementations.

## Open items

- It supports integer, float, string, boolean and their array counter part data types only.
- It supports NI-DCPower, NI-DMM, NI-Digital, NI-FGEN, NI-Switch, NI-Scope and NI-DAQmx instrument drivers only.
- The user measurements should contain a measurement function with properly type hinted return value.
- Initialization of session should be done inside the measurement function.
- The measurement plug-in created by this tool doesn't include a measurement UI file.
