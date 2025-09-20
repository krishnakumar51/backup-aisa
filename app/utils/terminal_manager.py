"""
Terminal Management Utility
Handles opening separate terminals for Agent 3 testing and Appium server
"""

import subprocess
import platform
import logging
import time
import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class TerminalManager:
    """Manages terminal windows for isolated process execution"""
    
    def __init__(self):
        self.system = platform.system()
        self.processes = {}
        
    def get_terminal_command(self, command: str, title: str = "Agent3 Testing") -> list:
        """Get platform-specific terminal command"""
        if self.system == "Windows":
            # Use PowerShell with new window
            return [
                "powershell.exe", 
                "-Command", 
                f"Start-Process powershell -ArgumentList '-NoExit', '-Command', '{command}' -WindowStyle Normal"
            ]
            
        elif self.system == "Darwin":  # macOS
            # Use osascript to open Terminal
            return [
                "osascript", 
                "-e", 
                f'tell application "Terminal" to do script "{command}"'
            ]
            
        else:  # Linux
            # Try different terminal emulators
            terminal_commands = [
                ["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"],
                ["konsole", "-e", "bash", "-c", f"{command}; exec bash"],
                ["xterm", "-e", "bash", "-c", f"{command}; exec bash"],
                ["x-terminal-emulator", "-e", "bash", "-c", f"{command}; exec bash"]
            ]
            
            # Find available terminal
            for term_cmd in terminal_commands:
                try:
                    subprocess.run(["which", term_cmd[0]], capture_output=True, check=True)
                    return term_cmd
                except subprocess.CalledProcessError:
                    continue
                    
            # Fallback to system default
            return ["x-terminal-emulator", "-e", "bash", "-c", f"{command}; exec bash"]
    
    def launch_appium_server(self, port: int = 4723) -> Optional[subprocess.Popen]:
        """Launch Appium server in separate terminal"""
        try:
            appium_command = f"appium server --port {port} --allow-cors"
            terminal_cmd = self.get_terminal_command(appium_command, "Appium Server")
            
            logger.info(f"🚀 Starting Appium server on port {port}")
            
            if self.system == "Windows":
                # Windows specific approach
                process = subprocess.Popen(
                    terminal_cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                # Unix systems
                process = subprocess.Popen(
                    terminal_cmd,
                    preexec_fn=os.setsid
                )
            
            self.processes["appium_server"] = process
            
            # Wait a moment for server to start
            time.sleep(3)
            
            logger.info(f"✅ Appium server terminal launched (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to launch Appium server: {str(e)}")
            return None
    
    def launch_agent3_testing(self, script_path: Path, venv_python: Path) -> Optional[subprocess.Popen]:
        """Launch Agent 3 testing in separate terminal"""
        try:
            # Change to script directory and run
            script_dir = script_path.parent
            test_command = f"cd {script_dir} && {venv_python} {script_path.name}"
            
            terminal_cmd = self.get_terminal_command(test_command, "Agent 3 Testing")
            
            logger.info(f"🧪 Starting Agent 3 testing in separate terminal")
            logger.info(f"   Script: {script_path}")
            logger.info(f"   Python: {venv_python}")
            
            if self.system == "Windows":
                process = subprocess.Popen(
                    terminal_cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                    cwd=str(script_dir)
                )
            else:
                process = subprocess.Popen(
                    terminal_cmd,
                    preexec_fn=os.setsid,
                    cwd=str(script_dir)
                )
            
            self.processes["agent3_testing"] = process
            
            logger.info(f"✅ Agent 3 testing terminal launched (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to launch Agent 3 testing: {str(e)}")
            return None
    
    def launch_monitoring_terminal(self, log_path: Path) -> Optional[subprocess.Popen]:
        """Launch terminal to monitor logs in real-time"""
        try:
            if self.system == "Windows":
                monitor_command = f"Get-Content {log_path} -Wait -Tail 20"
            else:
                monitor_command = f"tail -f {log_path}"
                
            terminal_cmd = self.get_terminal_command(monitor_command, "Testing Monitor")
            
            logger.info(f"📊 Starting log monitoring terminal")
            
            if self.system == "Windows":
                process = subprocess.Popen(
                    terminal_cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                process = subprocess.Popen(
                    terminal_cmd,
                    preexec_fn=os.setsid
                )
            
            self.processes["monitoring"] = process
            
            logger.info(f"✅ Monitoring terminal launched (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to launch monitoring terminal: {str(e)}")
            return None
    
    def check_appium_running(self, port: int = 4723) -> bool:
        """Check if Appium server is running"""
        try:
            import requests
            response = requests.get(f"http://localhost:{port}/status", timeout=5)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def wait_for_appium_ready(self, port: int = 4723, timeout: int = 30) -> bool:
        """Wait for Appium server to be ready"""
        start_time = time.time()
        
        logger.info(f"⏳ Waiting for Appium server on port {port}...")
        
        while time.time() - start_time < timeout:
            if self.check_appium_running(port):
                logger.info(f"✅ Appium server is ready on port {port}")
                return True
                
            time.sleep(2)
            
        logger.error(f"❌ Appium server not ready after {timeout} seconds")
        return False
    
    def ensure_appium_server(self, port: int = 4723) -> bool:
        """Ensure Appium server is running, start if needed"""
        if self.check_appium_running(port):
            logger.info(f"✅ Appium server already running on port {port}")
            return True
            
        # Try to start Appium server
        process = self.launch_appium_server(port)
        if process:
            return self.wait_for_appium_ready(port)
            
        return False
    
    def cleanup_processes(self):
        """Clean up all managed processes"""
        for name, process in self.processes.items():
            try:
                if process and process.poll() is None:  # Still running
                    logger.info(f"🛑 Terminating {name} (PID: {process.pid})")
                    
                    if self.system == "Windows":
                        process.terminate()
                    else:
                        os.killpg(os.getpgid(process.pid), 15)  # SIGTERM
                        
                    # Wait briefly for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        # Force kill if needed
                        if self.system == "Windows":
                            process.kill()
                        else:
                            os.killpg(os.getpgid(process.pid), 9)  # SIGKILL
                            
            except Exception as e:
                logger.error(f"❌ Error cleaning up {name}: {str(e)}")
                
        self.processes.clear()
        logger.info("✅ Process cleanup completed")
    
    def get_process_status(self) -> Dict[str, Any]:
        """Get status of all managed processes"""
        status = {}
        
        for name, process in self.processes.items():
            if process:
                status[name] = {
                    "pid": process.pid,
                    "running": process.poll() is None,
                    "returncode": process.returncode
                }
            else:
                status[name] = {"running": False, "error": "Process not started"}
                
        return status


# Convenience functions for Agent 3
def ensure_testing_environment(port: int = 4723) -> TerminalManager:
    """Ensure complete testing environment is ready"""
    terminal_manager = TerminalManager()
    
    # Ensure Appium server is running
    if not terminal_manager.ensure_appium_server(port):
        logger.warning("⚠️ Appium server not available, some tests may fail")
        
    return terminal_manager


def launch_agent3_in_terminal(script_path: Path, venv_python: Path) -> Optional[subprocess.Popen]:
    """Quick function to launch Agent 3 in separate terminal"""
    terminal_manager = TerminalManager()
    return terminal_manager.launch_agent3_testing(script_path, venv_python)


if __name__ == "__main__":
    # Test terminal management
    logging.basicConfig(level=logging.INFO)
    
    terminal_manager = TerminalManager()
    
    print(f"🖥️  System: {terminal_manager.system}")
    print("🔍 Testing terminal capabilities...")
    
    # Test Appium server
    if terminal_manager.ensure_appium_server():
        print("✅ Appium server management: OK")
    else:
        print("❌ Appium server management: FAILED")
    
    # Show process status
    status = terminal_manager.get_process_status()
    if status:
        print("📊 Process Status:")
        for name, info in status.items():
            print(f"   • {name}: {'Running' if info['running'] else 'Stopped'}")
    
    # Cleanup
    terminal_manager.cleanup_processes()