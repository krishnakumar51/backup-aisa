"""
Enhanced Agent 3: Terminal-Isolated Testing Environment with Appium Management  
Runs testing in completely separate terminals with automatic Appium server management
"""

import asyncio
import json
import logging
import time
import os
import subprocess
import sys
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Import enhanced utilities
from app.utils.device_manager import DeviceManager, detect_android_devices
from app.utils.terminal_manager import TerminalManager, ensure_testing_environment
from app.database.database_manager import get_testing_db
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class EnhancedAgent3_IsolatedTesting:
    """Enhanced Agent 3: Terminal-Isolated Testing with Appium Management"""
    
    def __init__(self):
        self.agent_name = "agent3"
        self.db_manager = None
        self.terminal_manager = None
        self.device_manager = None
        self.settings = get_settings()
        self.max_test_attempts = 3
        self.testing_processes = {}
        
    async def initialize(self):
        """Initialize testing environment managers"""
        self.db_manager = await get_testing_db()
        self.terminal_manager = TerminalManager()
        self.device_manager = DeviceManager()
        
        logger.info("🟡 Agent 3: Enhanced isolated testing environment initialized")
        logger.info(f"🟡 Agent 3: Platform: {self.terminal_manager.system}")
        
    async def execute_isolated_testing(
        self,
        task_id: int,
        base_path: Path,
        agent2_results: Dict[str, Any],
        platform: str,
        additional_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute testing in completely isolated environment with separate terminals"""
        
        logger.info(f"🟡 [Agent3] Starting isolated testing environment for task {task_id}")
        
        try:
            # Create agent3 folder structure
            agent3_path = base_path / "agent3"
            testing_path = agent3_path / "testing"
            venv_path = testing_path / "venv"
            logs_path = testing_path / "logs"
            
            # Create directories
            for path in [agent3_path, testing_path, logs_path]:
                path.mkdir(parents=True, exist_ok=True)
                
            logger.info(f"🟡 [Agent3] Created isolated testing structure: {testing_path}")
            
            # Step 1: Setup isolated virtual environment
            venv_setup_success = await self.setup_isolated_virtual_environment(
                venv_path, 
                Path(agent2_results["requirements_path"])
            )
            
            if not venv_setup_success:
                raise Exception("Failed to setup isolated virtual environment")
            
            # Step 2: Prepare testing environment for mobile
            if platform.lower() == 'mobile':
                mobile_setup_success = await self.prepare_mobile_testing_environment(
                    testing_path, task_id
                )
                if not mobile_setup_success:
                    logger.warning("⚠️ Mobile environment setup had issues, continuing...")
            
            # Step 3: Execute testing in separate terminal
            testing_success = await self.execute_testing_in_terminal(
                script_path=Path(agent2_results["script_path"]),
                venv_path=venv_path,
                testing_path=testing_path,
                task_id=task_id
            )
            
            # Step 4: Collect and analyze results
            results = await self.collect_testing_results(testing_path, task_id)
            
            logger.info("🟡 [Agent3] ✅ Isolated testing environment completed")
            
            return {
                "success": testing_success,
                "agent3_path": str(agent3_path),
                "testing_path": str(testing_path),
                "virtual_environment": "✅ Created",
                "dependencies_installed": venv_setup_success,
                "mobile_environment": platform.lower() == 'mobile',
                "terminal_execution": testing_success,
                "test_results": results,
                "processes_launched": len(self.testing_processes),
                "logs_directory": str(logs_path)
            }
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Isolated testing failed: {str(e)}")
            
            # Cleanup processes on failure
            await self.cleanup_testing_processes()
            
            return {
                "success": False,
                "error": str(e),
                "agent3_path": str(agent3_path) if 'agent3_path' in locals() else None,
                "cleanup_performed": True
            }
    
    async def setup_isolated_virtual_environment(self, venv_path: Path, requirements_path: Path) -> bool:
        """Setup virtual environment in completely isolated subprocess"""
        try:
            logger.info(f"🟡 [Agent3] Creating isolated virtual environment: {venv_path}")
            
            # Use subprocess with isolated working directory
            isolation_dir = venv_path.parent
            
            # Step 1: Create venv in isolated subprocess  
            create_cmd = [
                sys.executable, "-m", "venv", 
                str(venv_path), "--clear", "--copies"
            ]
            
            logger.info(f"🟡 [Agent3] Running: {' '.join(create_cmd)}")
            
            result = subprocess.run(
                create_cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(isolation_dir),
                env={**os.environ, "PYTHONPATH": ""}  # Clean environment
            )
            
            if result.returncode != 0:
                logger.error(f"🔴 [Agent3] Venv creation failed: {result.stderr}")
                return False
                
            logger.info(f"🟡 [Agent3] ✅ Virtual environment created successfully")
            
            # Step 2: Install dependencies in isolated subprocess
            if platform.system() == "Windows":
                pip_exe = venv_path / "Scripts" / "pip.exe"
                python_exe = venv_path / "Scripts" / "python.exe"
            else:
                pip_exe = venv_path / "bin" / "pip"
                python_exe = venv_path / "bin" / "python"
            
            # Upgrade pip first
            upgrade_cmd = [str(python_exe), "-m", "pip", "install", "--upgrade", "pip"]
            
            upgrade_result = subprocess.run(
                upgrade_cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(isolation_dir),
                env={**os.environ, "PYTHONPATH": ""}
            )
            
            if upgrade_result.returncode != 0:
                logger.warning(f"⚠️ [Agent3] Pip upgrade warning: {upgrade_result.stderr}")
            
            # Install requirements
            install_cmd = [
                str(python_exe), "-m", "pip", "install", 
                "-r", str(requirements_path), 
                "--no-cache-dir", "--isolated"
            ]
            
            logger.info(f"🟡 [Agent3] Installing dependencies...")
            
            install_result = subprocess.run(
                install_cmd,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minutes for installation
                cwd=str(isolation_dir),
                env={**os.environ, "PYTHONPATH": ""}
            )
            
            if install_result.returncode != 0:
                logger.error(f"🔴 [Agent3] Dependencies installation failed:")
                logger.error(f"STDOUT: {install_result.stdout}")
                logger.error(f"STDERR: {install_result.stderr}")
                return False
                
            logger.info(f"🟡 [Agent3] ✅ Dependencies installed successfully")
            
            # Verify installation
            verify_cmd = [str(python_exe), "-m", "pip", "list"]
            verify_result = subprocess.run(
                verify_cmd,
                capture_output=True, 
                text=True,
                timeout=30,
                cwd=str(isolation_dir)
            )
            
            if verify_result.returncode == 0:
                installed_packages = len(verify_result.stdout.strip().split('\n')) - 2  # Exclude header
                logger.info(f"🟡 [Agent3] ✅ Verified {installed_packages} packages installed")
            
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("🔴 [Agent3] Virtual environment setup timeout")
            return False
        except Exception as e:
            logger.error(f"🔴 [Agent3] Virtual environment setup failed: {str(e)}")
            return False
    
    async def prepare_mobile_testing_environment(self, testing_path: Path, task_id: int) -> bool:
        """Prepare mobile testing environment with Appium and device detection"""
        try:
            logger.info("🟡 [Agent3] Preparing mobile testing environment...")
            
            # Step 1: Check and setup Appium server
            appium_ready = await self.ensure_appium_server()
            
            # Step 2: Detect connected devices
            device_info = None
            if self.device_manager.check_adb_available():
                device_info = self.device_manager.select_best_device()
                
                if device_info:
                    # Save device configuration
                    device_config_path = testing_path / "device_config.json"
                    self.device_manager.save_device_config(device_config_path)
                    
                    # Update database with device info
                    await self.db_manager.update_task_metadata(
                        task_id,
                        {"selected_device": device_info}
                    )
                    
                    logger.info(f"🟡 [Agent3] ✅ Device ready: {device_info['device_name']}")
                else:
                    logger.warning("⚠️ [Agent3] No suitable devices found")
            else:
                logger.warning("⚠️ [Agent3] ADB not available")
            
            # Step 3: Create mobile testing configuration
            mobile_config = {
                "appium_server": {
                    "url": "http://localhost:4723",
                    "status": "ready" if appium_ready else "not_ready"
                },
                "device_info": device_info,
                "adb_available": self.device_manager.check_adb_available(),
                "testing_features": {
                    "screenshots": True,
                    "ocr_analysis": True,
                    "device_logs": True,
                    "performance_monitoring": False
                }
            }
            
            config_path = testing_path / "mobile_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(mobile_config, f, indent=2, ensure_ascii=False)
                
            logger.info(f"🟡 [Agent3] ✅ Mobile config saved: {config_path}")
            
            return appium_ready and (device_info is not None)
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Mobile environment preparation failed: {str(e)}")
            return False
    
    async def ensure_appium_server(self) -> bool:
        """Ensure Appium server is running, launch in separate terminal if needed"""
        try:
            # Check if Appium is already running
            if self.terminal_manager.check_appium_running():
                logger.info("✅ [Agent3] Appium server already running")
                return True
                
            logger.info("🟡 [Agent3] Starting Appium server in separate terminal...")
            
            # Launch Appium server in dedicated terminal
            appium_process = self.terminal_manager.launch_appium_server()
            
            if appium_process:
                self.testing_processes["appium_server"] = appium_process
                
                # Wait for server to be ready
                server_ready = self.terminal_manager.wait_for_appium_ready()
                
                if server_ready:
                    logger.info("✅ [Agent3] Appium server ready in separate terminal")
                    return True
                else:
                    logger.error("❌ [Agent3] Appium server failed to start properly")
                    return False
            else:
                logger.error("❌ [Agent3] Failed to launch Appium server terminal")
                return False
                
        except Exception as e:
            logger.error(f"❌ [Agent3] Appium server setup failed: {str(e)}")
            return False
    
    async def execute_testing_in_terminal(
        self, 
        script_path: Path, 
        venv_path: Path,
        testing_path: Path,
        task_id: int
    ) -> bool:
        """Execute testing script in completely separate terminal"""
        try:
            logger.info("🟡 [Agent3] Launching testing in separate terminal...")
            
            # Determine Python executable path
            if platform.system() == "Windows":
                venv_python = venv_path / "Scripts" / "python.exe"
            else:
                venv_python = venv_path / "bin" / "python"
            
            # Copy script to testing directory for isolated execution
            testing_script = testing_path / "automation_script.py"
            
            # Read original script and modify for testing environment
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
                
            # Add testing environment setup to script
            enhanced_script = f'''# Enhanced Testing Environment Setup
import sys
import os
from pathlib import Path

# Add testing directory to path
testing_dir = Path(__file__).parent
sys.path.insert(0, str(testing_dir))

# Configure logging for terminal execution
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(testing_dir / "testing_execution.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Original script content
{script_content}
'''
            
            with open(testing_script, 'w', encoding='utf-8') as f:
                f.write(enhanced_script)
                
            # Launch testing in separate terminal
            testing_process = self.terminal_manager.launch_agent3_testing(
                testing_script, venv_python
            )
            
            if testing_process:
                self.testing_processes["agent3_testing"] = testing_process
                
                # Launch monitoring terminal for logs
                log_file = testing_path / "testing_execution.log"
                monitoring_process = self.terminal_manager.launch_monitoring_terminal(log_file)
                
                if monitoring_process:
                    self.testing_processes["log_monitoring"] = monitoring_process
                
                logger.info("✅ [Agent3] Testing launched in separate terminal")
                logger.info(f"📊 [Agent3] Monitoring logs: {log_file}")
                
                # Update database with process info
                await self.db_manager.update_task_metadata(
                    task_id,
                    {
                        "testing_process_pid": testing_process.pid,
                        "testing_script_path": str(testing_script),
                        "testing_log_path": str(log_file)
                    }
                )
                
                return True
            else:
                logger.error("❌ [Agent3] Failed to launch testing terminal")
                return False
                
        except Exception as e:
            logger.error(f"❌ [Agent3] Terminal testing execution failed: {str(e)}")
            return False
    
    async def collect_testing_results(self, testing_path: Path, task_id: int) -> Dict[str, Any]:
        """Collect and analyze testing results from isolated execution"""
        try:
            results = {
                "execution_completed": False,
                "results_found": False,
                "ocr_logs_count": 0,
                "screenshots_count": 0,
                "automation_success": False,
                "test_summary": {},
                "process_status": {}
            }
            
            # Check process status
            process_status = self.terminal_manager.get_process_status()
            results["process_status"] = process_status
            
            # Look for automation results
            results_file = testing_path / "ocr_logs" / "automation_results.json"
            
            if results_file.exists():
                try:
                    with open(results_file, 'r', encoding='utf-8') as f:
                        automation_results = json.load(f)
                        
                    results["results_found"] = True
                    results["test_summary"] = automation_results
                    results["automation_success"] = automation_results.get("success_rate", 0) >= 70.0
                    
                    logger.info(f"✅ [Agent3] Automation results collected")
                    logger.info(f"📊 [Agent3] Success rate: {automation_results.get('success_rate', 0):.1f}%")
                    
                except Exception as e:
                    logger.warning(f"⚠️ [Agent3] Failed to parse results: {str(e)}")
            else:
                logger.warning("⚠️ [Agent3] No automation results file found")
            
            # Count OCR logs and screenshots
            ocr_logs_dir = testing_path / "ocr_logs"
            if ocr_logs_dir.exists():
                ocr_files = list(ocr_logs_dir.glob("*.txt"))
                screenshot_files = list(ocr_logs_dir.glob("*.png"))
                
                results["ocr_logs_count"] = len(ocr_files)
                results["screenshots_count"] = len(screenshot_files)
                
                logger.info(f"📁 [Agent3] Found {len(ocr_files)} OCR logs, {len(screenshot_files)} screenshots")
            
            # Check execution log
            execution_log = testing_path / "testing_execution.log"
            if execution_log.exists():
                results["execution_completed"] = True
                
                # Read last few lines to check completion
                try:
                    with open(execution_log, 'r', encoding='utf-8') as f:
                        log_lines = f.readlines()
                        
                    if log_lines and any("completed" in line.lower() for line in log_lines[-10:]):
                        results["execution_completed"] = True
                        
                except Exception:
                    pass
            
            # Update database with results
            await self.db_manager.update_task_metadata(
                task_id,
                {"testing_results": results}
            )
            
            return results
            
        except Exception as e:
            logger.error(f"❌ [Agent3] Results collection failed: {str(e)}")
            return {"error": str(e)}
    
    async def cleanup_testing_processes(self):
        """Clean up all testing-related processes"""
        try:
            logger.info("🟡 [Agent3] Cleaning up testing processes...")
            
            if self.terminal_manager:
                self.terminal_manager.cleanup_processes()
                
            self.testing_processes.clear()
            logger.info("✅ [Agent3] Process cleanup completed")
            
        except Exception as e:
            logger.error(f"❌ [Agent3] Cleanup failed: {str(e)}")
    
    async def get_testing_status(self, task_id: int) -> Dict[str, Any]:
        """Get current status of testing processes"""
        try:
            status = {
                "task_id": task_id,
                "agent3_active": True,
                "processes": self.terminal_manager.get_process_status() if self.terminal_manager else {},
                "appium_server": self.terminal_manager.check_appium_running() if self.terminal_manager else False,
                "device_manager": self.device_manager is not None
            }
            
            return status
            
        except Exception as e:
            return {"error": str(e), "task_id": task_id}
    
    # Compatibility methods for main orchestrator
    async def execute_testing_with_agent2_collaboration(
        self, 
        task_id: int,
        base_path: Path,
        agent2_results: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Main entry point for orchestrator compatibility"""
        return await self.execute_isolated_testing(
            task_id, base_path, agent2_results, platform
        )


# Convenience functions for orchestrator integration
async def create_isolated_testing_environment(
    task_id: int,
    base_path: Path, 
    agent2_results: Dict[str, Any],
    platform: str
) -> Dict[str, Any]:
    """Quick function to create isolated testing environment"""
    
    agent3 = EnhancedAgent3_IsolatedTesting()
    await agent3.initialize()
    
    try:
        results = await agent3.execute_isolated_testing(
            task_id, base_path, agent2_results, platform
        )
        return results
        
    finally:
        # Cleanup is handled internally
        pass


if __name__ == "__main__":
    # Test isolated testing setup
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_agent3():
        agent3 = EnhancedAgent3_IsolatedTesting()
        await agent3.initialize()
        
        print("🧪 Testing Agent 3 isolated environment...")
        
        # Test device detection
        if agent3.device_manager.check_adb_available():
            devices = agent3.device_manager.get_connected_devices()
            print(f"📱 Found {len(devices)} connected device(s)")
            
        # Test terminal management
        print(f"🖥️  Platform: {agent3.terminal_manager.system}")
        
        # Test Appium server
        server_status = agent3.terminal_manager.get_appium_server_status()
        print(f"🔧 Appium server: {server_status['status']}")
        
        await agent3.cleanup_testing_processes()
        print("✅ Agent 3 test completed")
    
    asyncio.run(test_agent3())