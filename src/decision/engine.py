import yaml
import logging

logger = logging.getLogger(__name__)

class DecisionEngine:
    def __init__(self, rules_path: str):
        with open(rules_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        self.rules = data.get('rules', [])
        logger.info(f"Loaded {len(self.rules)} rules into DecisionEngine.")
        
    def evaluate(self, minerals: dict, predictions: dict, confidence: float) -> list:
        decisions = []
        for rule in self.rules:
            cond = rule['condition']
            target = cond.get('target')
            
            # Extract actual value to test
            val = None
            if target in predictions:
                val = predictions[target]['value']
            elif target in minerals:
                val = minerals[target]
            elif target == 'pyrite_fraction' and 'pyrite' in minerals:
                val = minerals['pyrite']
            
            if val is None:
                continue
                
            # Check operator
            op = cond.get('operator')
            cond_val = cond.get('value')
            trigger = False
            if op == '<' and val < cond_val: trigger = True
            elif op == '>' and val > cond_val: trigger = True
            elif op == '<=' and val <= cond_val: trigger = True
            elif op == '>=' and val >= cond_val: trigger = True
            elif op == '==' and val == cond_val: trigger = True
            
            if not trigger:
                continue
                
            # Check confidence condition if exists
            if 'confidence' in cond:
                c_op = cond['confidence']
                c_val = cond['confidence_value']
                c_trigger = False
                if c_op == '<' and confidence < c_val: c_trigger = True
                elif c_op == '>=' and confidence >= c_val: c_trigger = True
                
                if not c_trigger:
                    continue
                    
            decisions.append({
                "priority": rule['action']['priority'],
                "message": rule['action']['message'],
                "reason": rule['description'],
                "icon": rule['action']['icon']
            })
            
        return decisions
