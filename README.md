# Cloud Security Operations & Detection Engineering Lab

A hands-on lab environment focused on building and validating security detection engineering workflows, simulating multi-vector attacks, triaging incidents using Microsoft Sentinel and Microsoft Defender, and automating response procedures.

## Repository Structure
* `scripts/`: Contains attack simulation scripts (such as PowerShell brute-force loops and custom payload generators).
* `detections/KQL/`: Stores custom KQL analytics rules, hunting queries, and detection logic used across the workspace.
* `playbooks/`: Houses automated response scripts, workbooks, and SOAR orchestration logic.
* `docs/`: Architecture diagrams, incident write-ups, and investigation screenshots.

## Lab Roadmap & Objectives
1. **Attack Simulation:** Execute controlled simulations (brute-force, credential access, lateral movement) against lab infrastructure.
2. **Detection Engineering:** Write, test, and tune custom KQL detection rules inside Microsoft Sentinel to catch simulated tactics.
3. **Triage & Investigation:** Investigate alerts using Microsoft Defender XDR and Sentinel's investigation graph to map out threat scopes.
4. **Automated Response:** Build automation and playbooks to accelerate incident triage and contain threats efficiently.
