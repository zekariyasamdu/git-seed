#!/usr/bin/env python3
"""
Firewall Log Analyzer - Provides detailed analysis and reports
"""
import sys
import os
from datetime import datetime, timedelta
import json
import csv
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.firewall import firewall

class FirewallAnalyzer:
    def __init__(self):
        self.log_dir = Path.home() / ".firewall_logs"
        
    def show_realtime_dashboard(self):
        """Real-time monitoring dashboard"""
        import time
        from collections import deque
        
        print("🔥 REAL-TIME FIREWALL MONITOR")
        print("🔥" + "="*50 + "🔥")
        print("Monitoring connections... Press Ctrl+C to stop\n")
        
        # Track recent activity
        recent_activity = deque(maxlen=10)
        
        try:
            while True:
                # Get recent logs
                logs = firewall.get_connection_log(20)
                new_logs = [log for log in logs if log not in recent_activity]
                
                if new_logs:
                    for log in new_logs:
                        recent_activity.append(log)
                        time_str = datetime.fromisoformat(log['timestamp']).strftime("%H:%M:%S")
                        status = "✅ ALLOWED" if log['allowed'] else "❌ BLOCKED"
                        print(f"{time_str} - {log['ip']:15} - {status} - {log['reason']}")
                    print()
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nStopping monitor...")

    def generate_detailed_report(self):
        """Generate comprehensive detailed report"""
        report = firewall.generate_report()
        print(report)
        
        # Save report
        firewall.save_report()
        
        # Show log location
        print(f"\n📁 Log files location: {self.log_dir}")

    def show_top_offenders(self, days: int = 7):
        """Show top blocked IPs with timestamps"""
        print(f"🔍 TOP OFFENDERS (last {days} days)")
        print("=" * 60)
        
        # Read from CSV for historical data
        csv_file = self.log_dir / "connections.csv"
        if not csv_file.exists():
            print("No historical data found")
            return
        
        offenders = {}
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['allowed'] == 'False':
                    ip = row['ip']
                    timestamp = datetime.fromisoformat(row['timestamp'])
                    
                    # Filter by days
                    if (datetime.now() - timestamp).days <= days:
                        if ip not in offenders:
                            offenders[ip] = []
                        offenders[ip].append(timestamp)
        
        print("Top Offending IPs:")
        for ip, timestamps in sorted(offenders.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
            last_attempt = max(timestamps)
            first_attempt = min(timestamps)
            print(f"  {ip:15} → {len(timestamps):3d} attempts")
            print(f"     First: {first_attempt.strftime('%Y-%m-%d %H:%M')}")
            print(f"     Last:  {last_attempt.strftime('%Y-%m-%d %H:%M')}")
            print()

    def show_hourly_stats(self, hours: int = 24):
        """Show hourly traffic statistics"""
        print(f"📈 HOURLY TRAFFIC STATISTICS (last {hours} hours)")
        print("=" * 60)
        
        analytics = firewall.get_analytics()
        hourly_stats = analytics.get('hourly_stats', {})
        
        # Get last 24 hours
        now = datetime.now()
        for i in range(hours):
            hour_key = (now - timedelta(hours=i)).strftime("%Y-%m-%d %H:00")
            if hour_key in hourly_stats:
                stats = hourly_stats[hour_key]
                block_percent = stats['blocked'] / max(stats['allowed'] + stats['blocked'], 1) * 100
                print(f"  {hour_key} → ✅ {stats['allowed']:3d} | ❌ {stats['blocked']:3d} | 🚫 {block_percent:5.1f}%")
            else:
                print(f"  {hour_key} → ✅    0 | ❌    0 | 🚫   0.0%")

    def export_logs(self, format: str = "csv"):
        """Export logs in different formats"""
        export_file = self.log_dir / f"firewall_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == "csv":
            # CSV is already maintained, just copy
            import shutil
            source = self.log_dir / "connections.csv"
            if source.exists():
                shutil.copy2(source, export_file)
                print(f"📊 Logs exported to: {export_file}")
        
        elif format == "json":
            logs = firewall.get_connection_log(1000)  # Last 1000 entries
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)
            print(f"📊 Logs exported to: {export_file}")

def main():
    analyzer = FirewallAnalyzer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "live":
            analyzer.show_realtime_dashboard()
        elif sys.argv[1] == "report":
            analyzer.generate_detailed_report()
        elif sys.argv[1] == "offenders":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            analyzer.show_top_offenders(days)
        elif sys.argv[1] == "hourly":
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            analyzer.show_hourly_stats(hours)
        elif sys.argv[1] == "export":
            format = sys.argv[2] if len(sys.argv) > 2 else "csv"
            analyzer.export_logs(format)
        else:
            show_help()
    else:
        show_help()

def show_help():
    print("🔥 FIREWALL ANALYZER - Usage:")
    print("  python firewall_analyzer.py live        - Real-time monitoring")
    print("  python firewall_analyzer.py report      - Generate detailed report")
    print("  python firewall_analyzer.py offenders   - Show top blocked IPs")
    print("  python firewall_analyzer.py offenders 30- Show offenders from last 30 days")
    print("  python firewall_analyzer.py hourly      - Hourly statistics")
    print("  python firewall_analyzer.py hourly 48   - Last 48 hours stats")
    print("  python firewall_analyzer.py export      - Export logs to CSV")
    print("  python firewall_analyzer.py export json - Export logs to JSON")

if __name__ == "__main__":
    # Load firewall config first
    config_path = os.path.join(os.path.dirname(__file__), 'firewall.conf')
    if os.path.exists(config_path):
        firewall.load_config_from_file(config_path)
    
    main()