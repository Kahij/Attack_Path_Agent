## 1. `risk_score.py` – Risk Scoring Engine

### Purpose

This script reads a raw **ZAP JSON report**, processes each vulnerability, and computes a **custom risk score** based on:

- CVSS-like severity estimation
    
- Confidence level
    
- Reachability
    
- Vulnerability type (e.g. SQLi, XSS)
    
- EPSS-like exploitability factor
    
- Optional chaining factor
    

### Input Format

Expects the **original ZAP JSON output**, typically structured like this:

```json
{
  "site": [
    {
      "@name": "https://example.com",
      "@host": "example.com",
      "@port": "443",
      "@ssl": "true",
      "alerts": [ ... ]
    },
    ...
  ]
}
```

Each alert contains:

- A vulnerability type (e.g. SQL Injection)
    
- A `riskdesc` field (e.g. `"High (Medium)"`)
    
- One or more `instances` describing the vulnerable requests
    

### Output Format

A JSON file containing **simplified vulnerability entries**:

```json
[
  {
    "id": "40018",
    "vuln_type": "SQL Injection",
    "risk_score": 14.4,
    "severity": "High",
    "confidence": "Medium",
    "cweid": 89,
    "target_uri": "https://example.com/login.php",
    "method": "POST",
    "param": "username",
    "instance_count": 2,
    "site_host": "example.com",
    "site_ssl": true
  },
  ...
]
```

Each finding is scored and filtered to include only **actionable vulnerabilities** (`risk_score >= 1.0` and not informational).

### Usage

```bash
python3 risk_score.py zap_output.json scored_findings.json
```

---

## 2. `attack_chains.py` – Attack Chain Builder

### Purpose

This script takes the output from `risk_score.py` and attempts to **logically chain vulnerabilities** into plausible multi-step attacks. It identifies:

- **Initial access** (e.g. injection, weak auth)
    
- **Lateral movement** (e.g. CSRF, LFI)
    
- **Impact** (e.g. RCE, data leak)
    

It computes **exploitability scores**, links vulnerabilities that occur on the same host or are reasonably chainable, and outputs detailed attack paths.

### Input Format

Requires the **output from `risk_score.py`** (JSON list of scored findings, as shown above).

### Output Format

A JSON object with:

- Metadata about chains and stats
    
- A list of chains (each containing 2–3 steps)
    

Example:

```json
{
  "metadata": {
    "total_findings": 10,
    "filtered_findings": 8,
    "total_chains_generated": 4,
    "avg_chain_risk": 15.3,
    "max_chain_risk": 21.4,
    ...
  },
  "attack_chains": [
    {
      "steps": [
        {
          "step": 1,
          "id": "40018",
          "type": "SQL Injection",
          "role": "initial_access",
          ...
        },
        {
          "step": 2,
          "id": "10202",
          "type": "Absence of Anti-CSRF Tokens",
          "role": "lateral_move",
          ...
        },
        {
          "step": 3,
          "id": "10038",
          "type": "CSP Header Not Set",
          "role": "impact",
          ...
        }
      ],
      "total_risk_score": 19.7,
      "adjusted_risk_score": 23.6,
      "summary": "3-step attack chain: SQL Injection -> Absence of Anti-CSRF Tokens -> CSP Header Not Set",
      ...
    },
    ...
  ]
}
```

### Usage

```bash
python3 attack_chains.py scored_findings.json attack_chains.json
```

Optional flags:

- `--min-risk 2.0` – Only include vulnerabilities with this risk or higher
    
- `--max-chains 50` – Limit the number of output chains
