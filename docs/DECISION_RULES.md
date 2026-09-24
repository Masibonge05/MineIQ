# Decision Rules
Rules are defined in `configs/rules.yaml`. The engine evaluates them in order.

Example structure:
```yaml
- id: "rule_id"
  description: "What this rule does"
  condition:
    target: "cu_recovery"
    operator: "<"
    value: 70
    confidence: ">="
    confidence_value: 0.80
  action:
    priority: "HIGH"
    message: "Alert message"
    icon: "alert-triangle"
```
