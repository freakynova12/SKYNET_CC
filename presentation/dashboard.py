"""
Interactive Dashboard for Payment Operations Agent
Provides real-time visualization of agent behavior and metrics
"""

import json
from datetime import datetime
from typing import Dict, List
from agent import PaymentOpsAgent, PaymentStatus
from collections import defaultdict


class AgentDashboard:
    """Real-time dashboard for monitoring agent behavior"""
    
    def __init__(self, agent: PaymentOpsAgent):
        self.agent = agent
        
    def generate_dashboard_html(self) -> str:
        """Generate HTML dashboard with live metrics"""
        status = self.agent.get_status()
        metrics = self.agent.observer.calculate_metrics()
        
        # Prepare data for visualization
        patterns_data = self._prepare_patterns_data()
        decisions_data = self._prepare_decisions_data()
        outcomes_data = self._prepare_outcomes_data()
        timeline_data = self._prepare_timeline_data()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Operations Agent Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 16px;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #22c55e;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .metric-card {{
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-label {{
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .metric-value {{
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 4px;
        }}
        
        .metric-change {{
            font-size: 14px;
            color: #22c55e;
        }}
        
        .metric-change.negative {{
            color: #ef4444;
        }}
        
        .section {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .pattern-item {{
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .pattern-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .pattern-type {{
            font-weight: 600;
            color: #333;
        }}
        
        .severity-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .severity-high {{
            background: #fee2e2;
            color: #dc2626;
        }}
        
        .severity-medium {{
            background: #fef3c7;
            color: #d97706;
        }}
        
        .severity-low {{
            background: #dbeafe;
            color: #2563eb;
        }}
        
        .decision-item {{
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid #22c55e;
        }}
        
        .approval-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            background: #dcfce7;
            color: #16a34a;
        }}
        
        .approval-badge.supervised {{
            background: #fef3c7;
            color: #d97706;
        }}
        
        .timeline {{
            position: relative;
            padding-left: 40px;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 10px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: #e5e7eb;
        }}
        
        .timeline-item {{
            position: relative;
            margin-bottom: 24px;
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -34px;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #667eea;
            border: 3px solid white;
            box-shadow: 0 0 0 2px #667eea;
        }}
        
        .timeline-time {{
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }}
        
        .timeline-content {{
            background: #f8fafc;
            padding: 12px;
            border-radius: 8px;
        }}
        
        .effectiveness-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }}
        
        .effectiveness-card {{
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
        }}
        
        .effectiveness-title {{
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }}
        
        .effectiveness-stat {{
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        .empty-state-icon {{
            font-size: 48px;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <span class="status-indicator"></span>
                Payment Operations Agent
            </h1>
            <p class="subtitle">Real-time autonomous payment optimization • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">{metrics['success_rate']:.1%}</div>
                <div class="metric-change">Live metric</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Avg Latency</div>
                <div class="metric-value">{metrics['avg_latency']:.0f}ms</div>
                <div class="metric-change">Current performance</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Transactions</div>
                <div class="metric-value">{status['total_signals_observed']}</div>
                <div class="metric-change">Total observed</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Patterns Detected</div>
                <div class="metric-value">{status['active_patterns']}</div>
                <div class="metric-change">{status['total_decisions']} decisions made</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span>🔍</span> Active Patterns
            </div>
            {patterns_data}
        </div>
        
        <div class="section">
            <div class="section-title">
                <span>🧠</span> Recent Decisions
            </div>
            {decisions_data}
        </div>
        
        <div class="section">
            <div class="section-title">
                <span>⚡</span> Action Outcomes
            </div>
            {outcomes_data}
        </div>
        
        <div class="section">
            <div class="section-title">
                <span>📚</span> Learning Effectiveness
            </div>
            {self._prepare_effectiveness_data()}
        </div>
        
        <div class="section">
            <div class="section-title">
                <span>📅</span> Event Timeline
            </div>
            <div class="timeline">
                {timeline_data}
            </div>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _prepare_patterns_data(self) -> str:
        """Prepare patterns HTML"""
        patterns = list(self.agent.memory.active_patterns.values())
        
        if not patterns:
            return '<div class="empty-state"><div class="empty-state-icon">🎯</div><div>No active patterns detected</div></div>'
        
        # Sort by severity
        patterns.sort(key=lambda p: p.severity, reverse=True)
        
        html_parts = []
        for pattern in patterns[:10]:  # Show top 10
            severity_class = 'severity-high' if pattern.severity > 0.7 else 'severity-medium' if pattern.severity > 0.4 else 'severity-low'
            severity_label = 'HIGH' if pattern.severity > 0.7 else 'MEDIUM' if pattern.severity > 0.4 else 'LOW'
            
            html_parts.append(f"""
            <div class="pattern-item">
                <div class="pattern-header">
                    <div class="pattern-type">{pattern.pattern_type.replace('_', ' ').title()}</div>
                    <span class="severity-badge {severity_class}">{severity_label}</span>
                </div>
                <div style="color: #666; margin-bottom: 8px;">{pattern.description}</div>
                <div style="font-size: 12px; color: #999;">
                    Affected: {pattern.affected_dimension} • Confidence: {pattern.confidence:.0%}
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def _prepare_decisions_data(self) -> str:
        """Prepare decisions HTML"""
        decisions = list(self.agent.memory.decisions.values())
        
        if not decisions:
            return '<div class="empty-state"><div class="empty-state-icon">🤔</div><div>No decisions made yet</div></div>'
        
        # Get most recent
        decisions.sort(key=lambda d: d.timestamp, reverse=True)
        
        html_parts = []
        for decision in decisions[:10]:
            approval_class = 'supervised' if decision.requires_approval else ''
            approval_label = '⏳ REQUIRES APPROVAL' if decision.requires_approval else '✓ AUTONOMOUS'
            status = '✓ Executed' if decision.executed else '⏳ Pending'
            
            html_parts.append(f"""
            <div class="decision-item">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-weight: 600; color: #333;">
                        {decision.action_type.value.replace('_', ' ').title()}
                    </div>
                    <span class="approval-badge {approval_class}">{approval_label}</span>
                </div>
                <div style="color: #666; margin-bottom: 8px;">{decision.rationale}</div>
                <div style="font-size: 12px; color: #999;">
                    {status} • {decision.timestamp.strftime('%H:%M:%S')} • Expected Impact: {decision.expected_impact.get('success_rate_delta', 0):+.1%}
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def _prepare_outcomes_data(self) -> str:
        """Prepare outcomes HTML"""
        outcomes = list(self.agent.memory.outcomes.values())
        
        if not outcomes:
            return '<div class="empty-state"><div class="empty-state-icon">📊</div><div>No outcomes recorded yet</div></div>'
        
        outcomes.sort(key=lambda o: o.executed_at, reverse=True)
        
        html_parts = []
        for outcome in outcomes[:10]:
            impact = outcome.actual_impact.get('success_rate_delta', 0)
            impact_class = '' if impact >= 0 else 'negative'
            
            html_parts.append(f"""
            <div class="timeline-item">
                <div class="timeline-time">{outcome.executed_at.strftime('%H:%M:%S')}</div>
                <div class="timeline-content">
                    <div style="font-weight: 600; margin-bottom: 4px;">
                        {outcome.action_type.value.replace('_', ' ').title()}
                    </div>
                    <div style="color: #666; font-size: 14px; margin-bottom: 8px;">
                        {outcome.learning_insights}
                    </div>
                    <div style="font-size: 12px;">
                        <span class="metric-change {impact_class}">
                            Impact: {impact:+.2%} success rate
                        </span>
                    </div>
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def _prepare_effectiveness_data(self) -> str:
        """Prepare effectiveness metrics HTML"""
        effectiveness = self.agent.memory.action_effectiveness
        
        if not effectiveness or not any(stats['count'] > 0 for stats in effectiveness.values()):
            return '<div class="empty-state"><div class="empty-state-icon">📈</div><div>Learning data will appear here</div></div>'
        
        html_parts = []
        for action_type, stats in effectiveness.items():
            if stats['count'] > 0:
                html_parts.append(f"""
                <div class="effectiveness-card">
                    <div class="effectiveness-title">{action_type.value.replace('_', ' ').title()}</div>
                    <div class="effectiveness-stat">{stats['success_rate']:.0%}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">
                        {stats['count']} executions • Avg impact: {stats['avg_impact']:+.1%}
                    </div>
                </div>
                """)
        
        return f'<div class="effectiveness-grid">{"".join(html_parts)}</div>'
    
    def _prepare_timeline_data(self) -> str:
        """Prepare timeline HTML"""
        # Combine decisions and outcomes into timeline
        events = []
        
        for decision in self.agent.memory.decisions.values():
            events.append({
                'time': decision.timestamp,
                'type': 'decision',
                'content': f"Decision: {decision.action_type.value.replace('_', ' ').title()}",
                'detail': decision.rationale
            })
        
        for outcome in self.agent.memory.outcomes.values():
            events.append({
                'time': outcome.executed_at,
                'type': 'outcome',
                'content': f"Executed: {outcome.action_type.value.replace('_', ' ').title()}",
                'detail': outcome.learning_insights
            })
        
        if not events:
            return '<div class="empty-state"><div class="empty-state-icon">⏱️</div><div>Timeline will appear here</div></div>'
        
        events.sort(key=lambda e: e['time'], reverse=True)
        
        html_parts = []
        for event in events[:15]:
            html_parts.append(f"""
            <div class="timeline-item">
                <div class="timeline-time">{event['time'].strftime('%H:%M:%S')}</div>
                <div class="timeline-content">
                    <div style="font-weight: 600; margin-bottom: 4px;">{event['content']}</div>
                    <div style="color: #666; font-size: 14px;">{event['detail']}</div>
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def save_dashboard(self, filename: str = "dashboard.html"):
        """Save dashboard to HTML file"""
        html = self.generate_dashboard_html()
        with open(filename, 'w') as f:
            f.write(html)
        return filename
