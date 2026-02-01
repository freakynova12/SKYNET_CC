"""
Payment Data Simulator
Generates realistic payment transaction data for testing the agent
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
from core.agent import PaymentSignal, PaymentStatus


class PaymentSimulator:
    """Simulates realistic payment transaction streams"""
    
    def __init__(self):
        self.payment_methods = ['visa', 'mastercard', 'amex', 'discover', 'paypal']
        self.issuer_banks = ['chase', 'bofa', 'wells_fargo', 'citi', 'capital_one']
        self.processors = ['stripe', 'adyen', 'braintree', 'square']
        self.error_codes = ['E001_INSUFFICIENT_FUNDS', 'E002_CARD_DECLINED', 'E003_NETWORK_ERROR', 
                           'E004_TIMEOUT', 'E005_FRAUD_SUSPECTED', 'E006_INVALID_CARD']
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD']
        self.merchant_categories = ['retail', 'travel', 'food', 'entertainment', 'services']
        
        # Simulate degradation scenarios
        self.degradation_scenarios = []
        self.transaction_counter = 0
        
    def add_degradation_scenario(self, scenario_type: str, affected_dimension: str, 
                                 start_after: int, duration: int, severity: float):
        """Add a degradation scenario to simulate"""
        self.degradation_scenarios.append({
            'type': scenario_type,
            'affected': affected_dimension,
            'start': start_after,
            'end': start_after + duration,
            'severity': severity  # 0.0 to 1.0
        })
        
    def generate_payment(self) -> PaymentSignal:
        """Generate a single payment transaction"""
        self.transaction_counter += 1
        
        # Base transaction
        payment_method = random.choice(self.payment_methods)
        issuer = random.choice(self.issuer_banks)
        processor = random.choice(self.processors)
        
        # Default success probability
        success_prob = 0.85
        base_latency = random.randint(200, 800)
        retry_count = 0
        error_code = None
        
        # Apply degradation scenarios
        for scenario in self.degradation_scenarios:
            if scenario['start'] <= self.transaction_counter <= scenario['end']:
                if scenario['type'] == 'issuer_degradation':
                    if scenario['affected'] == issuer:
                        success_prob *= (1 - scenario['severity'])
                        base_latency += int(300 * scenario['severity'])
                        
                elif scenario['type'] == 'method_fatigue':
                    if scenario['affected'] == payment_method:
                        success_prob *= (1 - scenario['severity'])
                        
                elif scenario['type'] == 'retry_storm':
                    if random.random() < scenario['severity']:
                        retry_count = random.randint(1, 4)
                        success_prob *= 0.7
                        
                elif scenario['type'] == 'latency_spike':
                    base_latency += int(1000 * scenario['severity'])
                    
                elif scenario['type'] == 'error_clustering':
                    if random.random() < scenario['severity']:
                        error_code = scenario['affected']
                        success_prob = 0.1
        
        # Determine outcome
        if random.random() < success_prob:
            status = PaymentStatus.SUCCESS
            error_code = None
        else:
            status = PaymentStatus.FAILED
            if not error_code:
                error_code = random.choice(self.error_codes)
        
        # Add some variance
        latency = base_latency + random.randint(-100, 100)
        amount = round(random.uniform(10, 1000), 2)
        
        return PaymentSignal(
            transaction_id=f"txn_{self.transaction_counter:06d}",
            timestamp=datetime.now(),
            status=status,
            payment_method=payment_method,
            issuer_bank=issuer,
            processor=processor,
            amount=amount,
            currency=random.choice(self.currencies),
            latency_ms=max(latency, 100),
            error_code=error_code,
            retry_count=retry_count,
            merchant_category=random.choice(self.merchant_categories),
            risk_score=random.random()
        )
        
    def generate_batch(self, count: int) -> List[PaymentSignal]:
        """Generate a batch of payment transactions"""
        return [self.generate_payment() for _ in range(count)]
        
    def setup_realistic_scenarios(self):
        """Setup realistic degradation scenarios for demonstration"""
        
        # Scenario 1: Chase bank starts having issues after 50 transactions
        self.add_degradation_scenario(
            scenario_type='issuer_degradation',
            affected_dimension='chase',
            start_after=50,
            duration=100,
            severity=0.6  # 60% degradation
        )
        
        # Scenario 2: Retry storm kicks in after 100 transactions
        self.add_degradation_scenario(
            scenario_type='retry_storm',
            affected_dimension='global',
            start_after=100,
            duration=50,
            severity=0.5  # 50% of transactions will retry
        )
        
        # Scenario 3: Visa starts showing fatigue
        self.add_degradation_scenario(
            scenario_type='method_fatigue',
            affected_dimension='visa',
            start_after=80,
            duration=80,
            severity=0.4  # 40% degradation
        )
        
        # Scenario 4: Latency spike
        self.add_degradation_scenario(
            scenario_type='latency_spike',
            affected_dimension='global',
            start_after=150,
            duration=30,
            severity=0.7  # 70% latency increase
        )
        
        # Scenario 5: Error code clustering (fraud suspected errors)
        self.add_degradation_scenario(
            scenario_type='error_clustering',
            affected_dimension='E005_FRAUD_SUSPECTED',
            start_after=180,
            duration=40,
            severity=0.25  # 25% of transactions get this error
        )


class ScenarioDescriptor:
    """Describes what scenarios are configured"""
    
    @staticmethod
    def describe_scenarios(simulator: PaymentSimulator):
        """Print description of active scenarios"""
        print("\n" + "="*80)
        print("📋 CONFIGURED DEGRADATION SCENARIOS")
        print("="*80)
        
        for i, scenario in enumerate(simulator.degradation_scenarios, 1):
            print(f"\nScenario {i}: {scenario['type'].upper()}")
            print(f"  Affected: {scenario['affected']}")
            print(f"  Start: Transaction #{scenario['start']}")
            print(f"  Duration: {scenario['end'] - scenario['start']} transactions")
            print(f"  Severity: {scenario['severity']:.0%}")
            
            # Explain expected agent response
            if scenario['type'] == 'issuer_degradation':
                print(f"  📊 Expected Agent Response:")
                print(f"     - Detect issuer degradation pattern")
                print(f"     - Suppress failing path or optimize routing")
                print(f"     - Should improve success rate by routing around {scenario['affected']}")
                
            elif scenario['type'] == 'retry_storm':
                print(f"  📊 Expected Agent Response:")
                print(f"     - Detect retry storm pattern")
                print(f"     - Adjust retry delays and limits")
                print(f"     - Should reduce retry rate and system load")
                
            elif scenario['type'] == 'method_fatigue':
                print(f"  📊 Expected Agent Response:")
                print(f"     - Detect method fatigue pattern")
                print(f"     - Alert ops team or suppress if severe")
                print(f"     - Monitor {scenario['affected']} closely")
                
            elif scenario['type'] == 'latency_spike':
                print(f"  📊 Expected Agent Response:")
                print(f"     - Detect latency spike")
                print(f"     - Alert ops team for investigation")
                print(f"     - May optimize routing to faster processors")
                
            elif scenario['type'] == 'error_clustering':
                print(f"  📊 Expected Agent Response:")
                print(f"     - Detect error code clustering")
                print(f"     - Alert ops team with error details")
                print(f"     - Investigate {scenario['affected']}")
        
        print("\n" + "="*80 + "\n")
