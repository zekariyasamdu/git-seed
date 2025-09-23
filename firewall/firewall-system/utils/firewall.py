# utils/firewall.py
import ipaddress
from typing import Set, List, Optional, Callable, Dict, Any
import socket
import logging
from datetime import datetime, timedelta
import json
import csv
from pathlib import Path
import threading

class Firewall:
    def __init__(self):
        self.allowed_ips: Set[str] = set()
        self.blocked_ips: Set[str] = set()
        self.rate_limits: dict = {}
        self.rate_limit_window = timedelta(seconds=60)
        self.max_requests_per_minute = 100
        self.custom_rules: List[Callable[[str], bool]] = []
        
        # Enhanced logging and analytics
        self.connection_log: List[Dict[str, Any]] = []
        self.analytics_data: Dict[str, Any] = {
            'total_connections': 0,
            'allowed_connections': 0,
            'blocked_connections': 0,
            'blocked_by_reason': {},
            'top_blocked_ips': {},
            'top_allowed_ips': {},
            'hourly_stats': {},
            'daily_stats': {}
        }
        
        # Logging setup with file rotation
        self.log_dir = Path.home() / ".firewall_logs"
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
        # Setup logging
        self.logger = logging.getLogger("Firewall")
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = self.log_dir / "firewall.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Thread lock for thread safety
        self.lock = threading.Lock()
        
        self.logger.info("🔥 Firewall initialized with enhanced logging and analytics")

    def allow_ip(self, ip: str) -> None:
        try:
            validated_ip = str(ipaddress.ip_address(ip))
            self.allowed_ips.add(validated_ip)
            self.logger.info(f"✅ Allowed IP: {validated_ip}")
        except ValueError:
            self.logger.warning(f"❌ Invalid IP address: {ip}")

    def block_ip(self, ip: str) -> None:
        try:
            validated_ip = str(ipaddress.ip_address(ip))
            self.blocked_ips.add(validated_ip)
            self.logger.info(f"❌ Blocked IP: {validated_ip}")
        except ValueError:
            self.logger.warning(f"❌ Invalid IP address: {ip}")

    def add_cidr_range(self, cidr: str, allow: bool = True) -> None:
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            if allow:
                self.allowed_ips.update(str(ip) for ip in network.hosts())
            else:
                self.blocked_ips.update(str(ip) for ip in network.hosts())
            action = "Allowed" if allow else "Blocked"
            self.logger.info(f"📋 {action} CIDR range: {cidr}")
        except ValueError:
            self.logger.warning(f"❌ Invalid CIDR range: {cidr}")

    def add_custom_rule(self, rule_func: Callable[[str], bool]) -> None:
        self.custom_rules.append(rule_func)
        self.logger.info(f"📝 Added custom rule: {rule_func.__name__}")

    def check_rate_limit(self, ip: str) -> bool:
        now = datetime.now()
        if ip in self.rate_limits:
            count, last_time = self.rate_limits[ip]
            if now - last_time < self.rate_limit_window:
                if count >= self.max_requests_per_minute:
                    return False
                self.rate_limits[ip] = (count + 1, last_time)
            else:
                self.rate_limits[ip] = (1, now)
        else:
            self.rate_limits[ip] = (1, now)
        return True

    def _log_connection(self, ip: str, allowed: bool, reason: str = ""):
        """Log connection attempt with detailed analytics"""
        timestamp = datetime.now()
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'ip': ip,
            'allowed': allowed,
            'reason': reason,
            'time_str': timestamp.strftime("%H:%M:%S"),
            'date_str': timestamp.strftime("%Y-%m-%d"),
            'hour': timestamp.hour
        }
        
        with self.lock:
            # Add to connection log (keep last 10,000 entries)
            self.connection_log.append(log_entry)
            if len(self.connection_log) > 10000:
                self.connection_log.pop(0)
            
            # Update analytics
            self.analytics_data['total_connections'] += 1
            
            if allowed:
                self.analytics_data['allowed_connections'] += 1
                self.analytics_data['top_allowed_ips'][ip] = self.analytics_data['top_allowed_ips'].get(ip, 0) + 1
            else:
                self.analytics_data['blocked_connections'] += 1
                self.analytics_data['top_blocked_ips'][ip] = self.analytics_data['top_blocked_ips'].get(ip, 0) + 1
                self.analytics_data['blocked_by_reason'][reason] = self.analytics_data['blocked_by_reason'].get(reason, 0) + 1
            
            # Update hourly stats
            hour_key = timestamp.strftime("%Y-%m-%d %H:00")
            if hour_key not in self.analytics_data['hourly_stats']:
                self.analytics_data['hourly_stats'][hour_key] = {'allowed': 0, 'blocked': 0}
            if allowed:
                self.analytics_data['hourly_stats'][hour_key]['allowed'] += 1
            else:
                self.analytics_data['hourly_stats'][hour_key]['blocked'] += 1
            
            # Update daily stats
            date_key = timestamp.strftime("%Y-%m-%d")
            if date_key not in self.analytics_data['daily_stats']:
                self.analytics_data['daily_stats'][date_key] = {'allowed': 0, 'blocked': 0}
            if allowed:
                self.analytics_data['daily_stats'][date_key]['allowed'] += 1
            else:
                self.analytics_data['daily_stats'][date_key]['blocked'] += 1
            
            # Write to log files
            self._write_to_log_files(log_entry)
            
            # Console output
            status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
            time_display = timestamp.strftime("%H:%M:%S")
            self.logger.info(f"{time_display} - {ip} - {status} - {reason}")

    def _write_to_log_files(self, log_entry: Dict[str, Any]):
        """Write log entry to multiple log files"""
        # Text log
        text_log = self.log_dir / "connections.log"
        with open(text_log, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry['time_str']} - {log_entry['ip']} - {'ALLOWED' if log_entry['allowed'] else 'BLOCKED'} - {log_entry['reason']}\n")
        
        # CSV log (create header if first entry)
        csv_log = self.log_dir / "connections.csv"
        if not csv_log.exists():
            with open(csv_log, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'ip', 'allowed', 'reason', 'time', 'date'])
        
        with open(csv_log, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                log_entry['timestamp'],
                log_entry['ip'],
                log_entry['allowed'],
                log_entry['reason'],
                log_entry['time_str'],
                log_entry['date_str']
            ])
        
        # JSON log for easy parsing
        json_log = self.log_dir / "connections.json"
        logs = []
        if json_log.exists():
            with open(json_log, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        
        logs.append(log_entry)
        # Keep only last 1000 entries in JSON file
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        with open(json_log, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)

    def is_allowed(self, ip: str) -> bool:
        try:
            validated_ip = str(ipaddress.ip_address(ip))
        except ValueError:
            self._log_connection(ip, False, "Invalid IP format")
            return False

        if validated_ip in self.blocked_ips:
            self._log_connection(validated_ip, False, "IP in blocked list")
            return False

        if self.allowed_ips and validated_ip not in self.allowed_ips:
            self._log_connection(validated_ip, False, "IP not in allowed list")
            return False

        if not self.check_rate_limit(validated_ip):
            self._log_connection(validated_ip, False, "Rate limit exceeded")
            return False

        for rule in self.custom_rules:
            if not rule(validated_ip):
                self._log_connection(validated_ip, False, "Failed custom rule")
                return False

        self._log_connection(validated_ip, True, "All checks passed")
        return True

    def generate_report(self) -> str:
        """Generate comprehensive firewall report"""
        report = [
            "🔥 FIREWALL SECURITY REPORT",
            "=" * 60,
            f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"📊 Total Connections: {self.analytics_data['total_connections']:,}",
            f"✅ Allowed: {self.analytics_data['allowed_connections']:,}",
            f"❌ Blocked: {self.analytics_data['blocked_connections']:,}",
            f"🚫 Block Rate: {self.analytics_data['blocked_connections']/max(self.analytics_data['total_connections'], 1)*100:.1f}%",
            "",
            "🛑 TOP BLOCKED IPs:"
        ]
        
        # Top blocked IPs
        for ip, count in sorted(self.analytics_data['top_blocked_ips'].items(), 
                               key=lambda x: x[1], reverse=True)[:10]:
            report.append(f"  {ip:15} → {count:4d} blocks")
        
        report.extend(["", "✅ TOP ALLOWED IPs:"])
        
        # Top allowed IPs
        for ip, count in sorted(self.analytics_data['top_allowed_ips'].items(), 
                               key=lambda x: x[1], reverse=True)[:5]:
            report.append(f"  {ip:15} → {count:4d} allows")
        
        report.extend(["", "📋 BLOCK REASONS:"])
        
        # Block reasons
        for reason, count in sorted(self.analytics_data['blocked_by_reason'].items(), 
                                   key=lambda x: x[1], reverse=True):
            report.append(f"  {reason:20} → {count:4d} blocks")
        
        report.extend(["", "⏰ RECENT ACTIVITY (last 10):"])
        
        # Recent activity
        for log in self.get_connection_log(10):
            time_str = datetime.fromisoformat(log['timestamp']).strftime("%H:%M:%S")
            status = "✅ ALLOWED" if log['allowed'] else "❌ BLOCKED"
            report.append(f"  {time_str} - {log['ip']:15} - {status} - {log['reason']}")
        
        report.extend(["", "📈 HOURLY TRAFFIC (last 6 hours):"])
        
        # Hourly stats
        now = datetime.now()
        for i in range(6):
            hour = (now - timedelta(hours=i)).strftime("%Y-%m-%d %H:00")
            if hour in self.analytics_data['hourly_stats']:
                stats = self.analytics_data['hourly_stats'][hour]
                report.append(f"  {hour} → ✅ {stats['allowed']:3d} | ❌ {stats['blocked']:3d}")
        
        return "\n".join(report)

    def get_connection_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent connection log entries"""
        with self.lock:
            return self.connection_log[-limit:]

    def save_report(self, filename: str = None):
        """Save report to file"""
        if filename is None:
            filename = self.log_dir / f"firewall_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"📄 Report saved to: {filename}")

    def load_config_from_file(self, config_path: str) -> None:
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    
                    action, target = parts[0], parts[1]
                    
                    if action == 'allow':
                        if '/' in target:
                            self.add_cidr_range(target, allow=True)
                        else:
                            self.allow_ip(target)
                    elif action == 'block':
                        if '/' in target:
                            self.add_cidr_range(target, allow=False)
                        else:
                            self.block_ip(target)
        
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}")
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")

# Global firewall instance
firewall = Firewall()