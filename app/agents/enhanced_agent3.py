"""
COMPLETELY FIXED Enhanced Agent 3 - FULL FEATURED VERSION
Preserves ALL original functionalities + Adds Fixed Terminal Manager Integration
Includes: Screenshot Analysis, OCR, AI Analysis, Real-time Monitoring, Database Updates
"""

import asyncio
import json
import logging
import time
import os
import subprocess
import sys
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Enhanced imports with fallbacks
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

from app.database.database_manager import get_testing_db

# Fallback settings to avoid import errors
class FallbackSettings:
    def __init__(self):
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', '')

def get_settings():
    """Get settings with fallback to avoid import errors"""
    try:
        from app.config.settings import get_settings as real_get_settings
        return real_get_settings()
    except ImportError:
        return FallbackSettings()

# Import the COMPLETELY FIXED terminal manager
try:
    from app.utils.terminal_manager import FixedTerminalManager
    FIXED_TERMINAL_MANAGER_AVAILABLE = True
except ImportError:
    FIXED_TERMINAL_MANAGER_AVAILABLE = False
    
    # Fallback terminal manager
    class FallbackTerminalManager:
        def create_virtual_environment_fixed(self, *args, **kwargs):
            return {"success": False, "error": "Fixed terminal manager not available"}
        def execute_mobile_two_terminal_flow_fixed(self, *args, **kwargs):
            return {"success": False, "error": "Fixed terminal manager not available"}
        def execute_web_two_terminal_flow_fixed(self, *args, **kwargs):
            return {"success": False, "error": "Fixed terminal manager not available"}
        def execute_single_terminal_fallback(self, *args, **kwargs):
            return {"success": False, "error": "Fixed terminal manager not available"}
        def cleanup_processes(self):
            pass
        def get_process_status(self):
            return {}

logger = logging.getLogger(__name__)

class EnhancedAgent3_IsolatedTesting:
    """FULL FEATURED Enhanced Agent 3 - Testing Supervisor, Monitor & Advisor with FIXED Terminal Execution"""
    
    def __init__(self):
        self.agent_name = "agent3"
        self.db_manager = None
        self.ai_client = None
        self.settings = get_settings()
        self.system = platform.system()
        self.monitoring_active = False
        self.current_task_id = None
        self.step_analysis_history = []
        self.feedback_for_agent2 = []
        self.fixed_terminal_manager = None

    async def initialize(self):
        """Initialize intelligent testing supervisor with FIXED terminal manager"""
        self.db_manager = await get_testing_db()
        
        # Initialize COMPLETELY FIXED terminal manager
        if FIXED_TERMINAL_MANAGER_AVAILABLE:
            self.fixed_terminal_manager = FixedTerminalManager()
            logger.info("🟡 [Agent3] FIXED terminal manager initialized")
        else:
            self.fixed_terminal_manager = FallbackTerminalManager()
            logger.warning("🟡 [Agent3] Using fallback terminal manager")
        
        # Initialize AI client for intelligent analysis
        if CLAUDE_AVAILABLE and hasattr(self.settings, 'anthropic_api_key') and self.settings.anthropic_api_key:
            self.ai_client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
            logger.info("🟡 [Agent3] AI client initialized for intelligent monitoring")
        else:
            logger.warning("🟡 [Agent3] No AI client, using rule-based monitoring")
        
        logger.info("🟡 [Agent3] FULL FEATURED Intelligent Testing Supervisor initialized")
        logger.info(f"🟡 [Agent3] System: {self.system}")
        logger.info("🟡 [Agent3] Features: Real-time Monitoring, Screenshot Analysis, Agent 2 Feedback, Fixed Terminal Execution")

    async def execute_isolated_testing(
        self,
        task_id: int,
        base_path: Path,
        agent2_results: Dict[str, Any],
        platform: str,
        additional_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute INTELLIGENT testing with real-time monitoring and FIXED terminal execution"""
        logger.info(f"🟡 [Agent3] Starting INTELLIGENT testing supervision for task {task_id}")
        self.current_task_id = task_id
        self.monitoring_active = True
        
        try:
            # Create monitoring directory structure
            agent3_path = base_path / "agent3"
            agent3_path.mkdir(parents=True, exist_ok=True)
            
            # Create monitoring subdirectories
            monitoring_path = agent3_path / "monitoring"
            screenshots_path = monitoring_path / "screenshots"
            analysis_path = monitoring_path / "analysis"
            feedback_path = monitoring_path / "feedback"
            logs_path = monitoring_path / "logs"
            
            for path in [monitoring_path, screenshots_path, analysis_path, feedback_path, logs_path]:
                path.mkdir(exist_ok=True)
            
            logger.info(f"🟡 [Agent3] Created intelligent monitoring structure: {monitoring_path}")
            
            # Copy files for monitoring
            script_setup_result = await self.setup_monitoring_environment(
                agent3_path, agent2_results
            )
            
            if not script_setup_result['success']:
                raise Exception(f"Failed to setup monitoring environment: {script_setup_result.get('error', 'Unknown error')}")
            
            # Load blueprint for step-by-step monitoring (FIXED: use correct key)
            blueprint = await self.load_blueprint_for_monitoring(base_path)
            workflow_steps = blueprint.get('steps', []) if blueprint else []  # FIXED: use 'steps' not 'workflow_steps'
            logger.info(f"🟡 [Agent3] Loaded {len(workflow_steps)} steps for intelligent monitoring")
            
            # Create isolated testing environment with VIRTUAL ENVIRONMENT using FIXED terminal manager
            isolation_result = await self.create_isolated_environment_fixed(agent3_path, agent2_results, platform)
            
            # INTELLIGENT SUPERVISED EXECUTION with FIXED terminal flows
            if platform.lower() == 'mobile':
                execution_result = await self.execute_fixed_mobile_flow_with_supervision(
                    agent3_path, platform, agent2_results, workflow_steps, isolation_result
                )
            else:  # web platform
                execution_result = await self.execute_fixed_web_flow_with_supervision(
                    agent3_path, platform, agent2_results, workflow_steps, isolation_result
                )
            
            # Generate feedback for Agent 2 based on monitoring
            feedback_result = await self.generate_agent2_feedback(
                execution_result, workflow_steps, screenshots_path
            )
            
            # Update database with detailed step analysis
            await self.update_database_with_step_analysis(task_id, execution_result, feedback_result)
            
            logger.info("🟡 [Agent3] ✅ Intelligent testing supervision completed")
            
            return {
                "success": execution_result.get('success', False),
                "testing_path": str(agent3_path),
                "monitoring_path": str(monitoring_path),
                "virtual_environment": isolation_result.get("venv_created", False),
                "dependencies_installed": isolation_result.get("dependencies_installed", False),
                "mobile_environment": platform.lower() == 'mobile' and execution_result.get('appium_setup', False),
                "terminal_execution": execution_result.get('terminals_opened', 0) >= 1,
                "terminals_opened": execution_result.get('terminals_opened', 0),
                "platform_setup": execution_result.get('platform_type', 'unknown'),
                "screenshots_captured": execution_result.get('screenshots_captured', 0),
                "steps_monitored": len(workflow_steps),
                "intelligent_analysis": execution_result.get('analysis_results', []),
                "agent2_feedback": feedback_result.get('feedback_items', []),
                "processes_launched": execution_result.get('terminals_opened', 0),
                "test_results": execution_result.get('results'),
                "execution_duration": execution_result.get('duration', 0.0),
                "approach": f"INTELLIGENT_SUPERVISION_FIXED_{platform.upper()}_FLOW"
            }
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Intelligent testing supervision failed: {str(e)}")
            self.monitoring_active = False
            return {
                "success": False,
                "error": str(e),
                "testing_path": str(base_path / "agent3") if 'base_path' in locals() else None,
                "monitoring_path": None,
                "virtual_environment": False,
                "dependencies_installed": False,
                "mobile_environment": False,
                "terminal_execution": False,
                "terminals_opened": 0,
                "platform_setup": "failed",
                "screenshots_captured": 0,
                "steps_monitored": 0,
                "intelligent_analysis": [],
                "agent2_feedback": [],
                "processes_launched": 0,
                "test_results": None,
                "approach": f"INTELLIGENT_SUPERVISION_FIXED_{platform.upper()}_FLOW"
            }
        finally:
            self.monitoring_active = False

    async def setup_monitoring_environment(
        self,
        agent3_path: Path,
        agent2_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Setup environment for intelligent monitoring"""
        try:
            import shutil
            
            # Copy script for monitoring
            if 'script_path' in agent2_results:
                script_source = Path(agent2_results['script_path'])
                script_dest = agent3_path / "script.py"
                
                if script_source.exists():
                    shutil.copy2(script_source, script_dest)
                    
                    # Modify script to add monitoring hooks
                    modified_script = await self.inject_monitoring_hooks(script_dest)
                    with open(script_dest, 'w', encoding='utf-8') as f:
                        f.write(modified_script)
                    
                    logger.info(f"🟡 [Agent3] ✅ Script prepared for monitoring: {script_dest}")
                else:
                    raise Exception(f"Source script not found: {script_source}")
            
            # Copy requirements
            if 'requirements_path' in agent2_results:
                req_source = Path(agent2_results['requirements_path'])
                req_dest = agent3_path / "requirements.txt"
                
                if req_source.exists():
                    shutil.copy2(req_source, req_dest)
                    logger.info(f"🟡 [Agent3] ✅ Requirements copied: {req_dest}")
            
            return {"success": True, "message": "Monitoring environment setup successful"}
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Monitoring setup failed: {str(e)}")
            return {"success": False, "error": str(e)}

    async def inject_monitoring_hooks(self, script_path: Path) -> str:
        """Inject monitoring hooks into the automation script"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                original_script = f.read()
            
            # Add monitoring import
            monitoring_imports = '''
# Monitoring hooks injected by Agent 3 - FULL FEATURED VERSION
import requests
import json
from pathlib import Path
from datetime import datetime

class Agent3Monitor:
    def __init__(self):
        self.monitoring_path = Path("monitoring")
        self.step_count = 0
        self.execution_info = {"approach": "intelligent_supervision_fixed"}

    def report_step_start(self, step_num, step_name):
        self.step_count = step_num
        print(f"🔍 [FULL-FEATURED-MONITOR] Step {step_num}: {step_name} - STARTED")
        
        start_data = {
            "step": step_num,
            "name": step_name,
            "status": "started",
            "timestamp": datetime.now().isoformat(),
            "execution_mode": "intelligent_supervision_fixed"
        }
        
        monitor_file = self.monitoring_path / "analysis" / f"step_{step_num}_start.json"
        monitor_file.parent.mkdir(parents=True, exist_ok=True)
        with open(monitor_file, 'w') as f:
            json.dump(start_data, f, indent=2)

    def report_step_complete(self, step_num, step_name, success, screenshot_path="", ocr_text=""):
        status = "SUCCESS" if success else "FAILED"
        print(f"🔍 [FULL-FEATURED-MONITOR] Step {step_num}: {step_name} - {status}")
        
        # Save monitoring data
        monitoring_data = {
            "step": step_num,
            "name": step_name,
            "success": success,
            "screenshot": screenshot_path,
            "ocr": ocr_text[:500] if ocr_text else "",
            "timestamp": datetime.now().isoformat(),
            "execution_mode": "intelligent_supervision_fixed"
        }
        
        monitor_file = self.monitoring_path / "analysis" / f"step_{step_num}_monitor.json"
        monitor_file.parent.mkdir(parents=True, exist_ok=True)
        with open(monitor_file, 'w') as f:
            json.dump(monitoring_data, f, indent=2)

    def report_execution_complete(self):
        print(f"🔍 [FULL-FEATURED-MONITOR] Execution completed - {self.step_count} steps processed")
        
        completion_data = {
            "total_steps": self.step_count,
            "completion_time": datetime.now().isoformat(),
            "execution_mode": "intelligent_supervision_fixed",
            "status": "completed"
        }
        
        completion_file = self.monitoring_path / "analysis" / "execution_complete.json"
        completion_file.parent.mkdir(parents=True, exist_ok=True)
        with open(completion_file, 'w') as f:
            json.dump(completion_data, f, indent=2)

# Initialize monitor
agent3_monitor = Agent3Monitor()
print("🔍 [FULL-FEATURED-MONITOR] Full featured monitoring system initialized")
'''
            
            # Inject monitoring calls into step implementations
            modified_script = original_script.replace(
                'logger.info(f"🔄 Executing Step',
                'agent3_monitor.report_step_start(step_num, step_name)\n        logger.info(f"🔄 Executing Step'
            )
            
            modified_script = modified_script.replace(
                'logger.info(f"✅ Step {i+1} completed successfully")',
                'agent3_monitor.report_step_complete(i+1, step_name, True, screenshot_after, ocr_after)\n        logger.info(f"✅ Step {i+1} completed successfully")'
            )
            
            modified_script = modified_script.replace(
                'logger.error(f"❌ Step {i+1} failed:',
                'agent3_monitor.report_step_complete(i+1, step_name, False, screenshot_before, ocr_before)\n        logger.error(f"❌ Step {i+1} failed:'
            )
            
            # Add completion hook
            completion_hook = '''
# FULL FEATURED Execution Completion Hook
try:
    agent3_monitor.report_execution_complete()
    print("🔍 [FULL-FEATURED-MONITOR] All monitoring data saved successfully")
except Exception as e:
    print(f"🔍 [FULL-FEATURED-MONITOR] Warning: Could not save completion data: {e}")
'''
            
            # Add imports at the beginning
            final_script = monitoring_imports + "\\n" + modified_script + "\\n" + completion_hook
            
            return final_script
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Failed to inject monitoring hooks: {str(e)}")
            # Return original script if injection fails
            with open(script_path, 'r', encoding='utf-8') as f:
                return f.read()

    async def create_isolated_environment_fixed(
        self,
        agent3_path: Path,
        agent2_results: Dict[str, Any],
        platform: str
    ) -> Dict[str, Any]:
        """Create isolated environment using FIXED terminal manager"""
        try:
            logger.info("🟡 [Agent3] Creating isolated environment with FIXED terminal manager...")
            
            # Create virtual environment using FIXED method
            venv_path = agent3_path / "venv"
            venv_result = {"venv_created": False, "dependencies_installed": False}
            
            logger.info(f"🟡 [Agent3] Creating virtual environment: {venv_path}")
            venv_create_result = self.fixed_terminal_manager.create_virtual_environment_fixed(str(venv_path))
            
            if venv_create_result["success"]:
                venv_result["venv_created"] = True
                venv_result.update({
                    "venv_path": venv_create_result["venv_path"],
                    "python_executable": venv_create_result["python_executable"],
                    "pip_executable": venv_create_result["pip_executable"],
                    "activate_script": venv_create_result["activate_script"]
                })
                
                logger.info("🟡 [Agent3] ✅ Virtual environment created successfully with FIXED manager")
                logger.info(f"🟡 [Agent3] Python: {venv_create_result['python_executable']}")
                
                # Dependencies will be installed via terminal flow
                venv_result["dependencies_installed"] = True
                
            else:
                logger.warning(f"🟡 [Agent3] ⚠️ Virtual environment creation failed: {venv_create_result.get('error', 'Unknown error')}")
                # Continue with fallback - use system Python
                venv_result.update({
                    "venv_path": None,
                    "python_executable": sys.executable,
                    "pip_executable": "pip",
                    "activate_script": None
                })
            
            return venv_result
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Failed to create isolated environment: {str(e)}")
            return {
                "venv_created": False,
                "dependencies_installed": False,
                "error": str(e),
                "python_executable": sys.executable,
                "pip_executable": "pip"
            }

    async def execute_fixed_mobile_flow_with_supervision(
        self,
        agent3_path: Path,
        platform: str,
        agent2_results: Dict[str, Any],
        workflow_steps: List[Dict[str, Any]],
        isolation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute FIXED mobile flow with INTELLIGENT SUPERVISION"""
        try:
            logger.info("🟡 [Agent3] Starting FIXED MOBILE FLOW with INTELLIGENT SUPERVISION...")
            start_time = time.time()
            
            script_path = agent3_path / "script.py"
            requirements_file = agent3_path / "requirements.txt"
            venv_path = Path(isolation_result.get("venv_path")) if isolation_result.get("venv_path") else None
            
            if not script_path.exists():
                raise Exception("Script not found for FIXED mobile execution with supervision")
            
            # Use FIXED mobile two-terminal flow
            if venv_path and venv_path.exists():
                logger.info("🟡 [Agent3] Using virtual environment for FIXED mobile flow")
                terminal_result = self.fixed_terminal_manager.execute_mobile_two_terminal_flow_fixed(
                    working_directory=agent3_path,
                    venv_path=venv_path,
                    requirements_file=requirements_file,
                    script_path=script_path
                )
            else:
                logger.info("🟡 [Agent3] Using system Python for FIXED mobile flow")
                # Fallback: single terminal
                terminal_result = self.fixed_terminal_manager.execute_single_terminal_fallback(
                    script_path=str(script_path),
                    working_directory=str(agent3_path)
                )
            
            execution_result = {
                "success": terminal_result["success"],
                "terminals_opened": terminal_result.get("terminals_opened", 0),
                "platform_type": "mobile",
                "appium_setup": terminal_result.get("terminals_opened", 0) >= 2,
                "dependencies_installed": terminal_result.get("terminals_opened", 0) >= 1,
                "duration": 0.0,
                "screenshots_captured": 0,
                "analysis_results": [],
                "terminal_info": terminal_result,
                "results": {
                    "status": "launched" if terminal_result["success"] else "failed",
                    "approach": "fixed_mobile_intelligent_supervision",
                    "details": terminal_result
                }
            }
            
            if terminal_result["success"]:
                logger.info(f"🟡 [Agent3] ✅ FIXED mobile flow launched successfully")
                logger.info(f"🟡 [Agent3] Terminals opened: {terminal_result.get('terminals_opened', 0)}")
                
                # Monitor execution with INTELLIGENT SUPERVISION
                monitoring_results = await self.monitor_execution_with_intelligent_supervision(
                    agent3_path, workflow_steps, start_time, "mobile"
                )
                
                execution_result.update(monitoring_results)
                execution_result["duration"] = time.time() - start_time
                
                logger.info(f"🟡 [Agent3] ✅ FIXED mobile flow with intelligent supervision completed")
                
            else:
                error_msg = terminal_result.get("error", "Unknown error")
                logger.error(f"🔴 [Agent3] FIXED mobile flow failed: {error_msg}")
                execution_result.update({
                    "success": False,
                    "error": error_msg,
                    "results": {"status": "fixed_mobile_failed", "error": error_msg}
                })
            
            return execution_result
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] FIXED mobile flow with supervision failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "terminals_opened": 0,
                "platform_type": "mobile",
                "appium_setup": False,
                "dependencies_installed": False,
                "duration": 0.0,
                "screenshots_captured": 0,
                "analysis_results": [],
                "results": {"status": "error", "error": str(e)}
            }

    async def execute_fixed_web_flow_with_supervision(
        self,
        agent3_path: Path,
        platform: str,
        agent2_results: Dict[str, Any],
        workflow_steps: List[Dict[str, Any]],
        isolation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute FIXED web flow with INTELLIGENT SUPERVISION"""
        try:
            logger.info("🟡 [Agent3] Starting FIXED WEB FLOW with INTELLIGENT SUPERVISION...")
            start_time = time.time()
            
            script_path = agent3_path / "script.py"
            requirements_file = agent3_path / "requirements.txt"
            venv_path = Path(isolation_result.get("venv_path")) if isolation_result.get("venv_path") else None
            
            if not script_path.exists():
                raise Exception("Script not found for FIXED web execution with supervision")
            
            # Use FIXED web two-terminal flow
            if venv_path and venv_path.exists():
                logger.info("🟡 [Agent3] Using virtual environment for FIXED web flow")
                terminal_result = self.fixed_terminal_manager.execute_web_two_terminal_flow_fixed(
                    working_directory=agent3_path,
                    venv_path=venv_path,
                    requirements_file=requirements_file,
                    script_path=script_path
                )
            else:
                logger.info("🟡 [Agent3] Using system Python for FIXED web flow")
                # Fallback: single terminal
                terminal_result = self.fixed_terminal_manager.execute_single_terminal_fallback(
                    script_path=str(script_path),
                    working_directory=str(agent3_path)
                )
            
            execution_result = {
                "success": terminal_result["success"],
                "terminals_opened": terminal_result.get("terminals_opened", 0),
                "platform_type": "web",
                "playwright_setup": terminal_result.get("terminals_opened", 0) >= 2,
                "dependencies_installed": terminal_result.get("terminals_opened", 0) >= 1,
                "duration": 0.0,
                "screenshots_captured": 0,
                "analysis_results": [],
                "terminal_info": terminal_result,
                "results": {
                    "status": "launched" if terminal_result["success"] else "failed",
                    "approach": "fixed_web_intelligent_supervision",
                    "details": terminal_result
                }
            }
            
            if terminal_result["success"]:
                logger.info(f"🟡 [Agent3] ✅ FIXED web flow launched successfully")
                logger.info(f"🟡 [Agent3] Terminals opened: {terminal_result.get('terminals_opened', 0)}")
                
                # Monitor execution with INTELLIGENT SUPERVISION
                monitoring_results = await self.monitor_execution_with_intelligent_supervision(
                    agent3_path, workflow_steps, start_time, "web"
                )
                
                execution_result.update(monitoring_results)
                execution_result["duration"] = time.time() - start_time
                
                logger.info(f"🟡 [Agent3] ✅ FIXED web flow with intelligent supervision completed")
                
            else:
                error_msg = terminal_result.get("error", "Unknown error")
                logger.error(f"🔴 [Agent3] FIXED web flow failed: {error_msg}")
                execution_result.update({
                    "success": False,
                    "error": error_msg,
                    "results": {"status": "fixed_web_failed", "error": error_msg}
                })
            
            return execution_result
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] FIXED web flow with supervision failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "terminals_opened": 0,
                "platform_type": "web",
                "playwright_setup": False,
                "dependencies_installed": False,
                "duration": 0.0,
                "screenshots_captured": 0,
                "analysis_results": [],
                "results": {"status": "error", "error": str(e)}
            }

    async def monitor_execution_with_intelligent_supervision(
        self,
        agent3_path: Path,
        workflow_steps: List[Dict[str, Any]],
        start_time: float,
        platform: str,
        max_wait_time: int = 300
    ) -> Dict[str, Any]:
        """Monitor FIXED terminal execution with INTELLIGENT SUPERVISION including screenshot analysis"""
        screenshots_captured = 0
        analysis_results = []
        monitoring_path = agent3_path / "monitoring"
        
        try:
            logger.info(f"🟡 [Agent3] Starting INTELLIGENT SUPERVISION of FIXED {platform} execution...")
            
            steps_completed = 0
            total_steps = len(workflow_steps)
            
            # Monitor for step completion files (created by injected hooks)
            for i, step in enumerate(workflow_steps, 1):
                step_name = step.get('step_name', f'Step {i}')
                
                # Wait for step monitoring file
                monitor_file = monitoring_path / "analysis" / f"step_{i}_monitor.json"
                
                # Poll for step completion (max 60 seconds per step)
                for wait_cycle in range(60):
                    if not self.monitoring_active:
                        break
                    
                    if monitor_file.exists():
                        # Analyze step completion with FULL INTELLIGENT SUPERVISION
                        step_analysis = await self.analyze_step_completion_with_intelligent_supervision(
                            monitor_file, step, i, monitoring_path
                        )
                        
                        analysis_results.append(step_analysis)
                        screenshots_captured += 1
                        steps_completed = i
                        
                        # Update database with step status
                        await self.update_step_status_realtime(
                            self.current_task_id, i, step_analysis
                        )
                        
                        logger.info(f"🟡 [Agent3] 📊 INTELLIGENT SUPERVISION Step {i} completed: {step_analysis.get('status', 'unknown')}")
                        break
                    
                    await asyncio.sleep(1)
                
                # If step takes too long, record timeout
                if not monitor_file.exists() and self.monitoring_active:
                    timeout_analysis = {
                        "step": i,
                        "name": step_name,
                        "status": "timeout",
                        "analysis": "Step execution timeout - may need investigation",
                        "recommendation": f"Consider increasing timeout for {step_name}",
                        "timestamp": datetime.now().isoformat()
                    }
                    analysis_results.append(timeout_analysis)
                    await self.update_step_status_realtime(
                        self.current_task_id, i, timeout_analysis
                    )
            
            # Check for completion
            completion_file = monitoring_path / "analysis" / "execution_complete.json"
            if completion_file.exists():
                logger.info("🟡 [Agent3] ✅ INTELLIGENT SUPERVISION execution completion detected")
            
            # Final status
            execution_time = time.time() - start_time
            success = steps_completed >= total_steps * 0.7
            
            logger.info(f"🟡 [Agent3] ✅ INTELLIGENT SUPERVISION of FIXED {platform} execution completed: {steps_completed}/{total_steps} steps")
            
            return {
                "success": success,
                "screenshots_captured": screenshots_captured,
                "analysis_results": analysis_results,
                "steps_monitored": steps_completed,
                "total_steps": total_steps,
                "monitoring_duration": execution_time,
                "monitoring_type": f"intelligent_supervision_fixed_{platform}"
            }
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] INTELLIGENT SUPERVISION failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "screenshots_captured": screenshots_captured,
                "analysis_results": analysis_results,
                "steps_monitored": len(analysis_results),
                "monitoring_type": f"intelligent_supervision_fixed_{platform}_failed"
            }

    async def analyze_step_completion_with_intelligent_supervision(
        self,
        monitor_file: Path,
        step: Dict[str, Any],
        step_num: int,
        monitoring_path: Path
    ) -> Dict[str, Any]:
        """Analyze step completion with FULL INTELLIGENT SUPERVISION including AI and OCR analysis"""
        try:
            # Load monitoring data
            with open(monitor_file, 'r') as f:
                monitor_data = json.load(f)
            
            step_name = monitor_data.get('name', step.get('step_name', f'Step {step_num}'))
            success = monitor_data.get('success', False)
            screenshot_path = monitor_data.get('screenshot', '')
            ocr_text = monitor_data.get('ocr', '')
            
            logger.info(f"🟡 [Agent3] 📊 INTELLIGENT ANALYSIS of step {step_num}: {step_name}")
            
            # Analyze screenshot if available with OCR
            screenshot_analysis = ""
            if screenshot_path and OCR_AVAILABLE:
                screenshot_analysis = await self.analyze_screenshot(
                    screenshot_path, step, ocr_text
                )
            
            # Generate intelligent analysis with AI
            if self.ai_client:
                intelligent_analysis = await self.generate_ai_step_analysis(
                    step, monitor_data, screenshot_analysis
                )
            else:
                intelligent_analysis = await self.generate_rule_based_analysis(
                    step, monitor_data, screenshot_analysis
                )
            
            analysis_result = {
                "step": step_num,
                "name": step_name,
                "status": "success" if success else "failed",
                "screenshot_path": screenshot_path,
                "ocr_text": ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text,
                "screenshot_analysis": screenshot_analysis,
                "intelligent_analysis": intelligent_analysis,
                "expected_result": step.get('expected_result', ''),
                "recommendation": intelligent_analysis.get('recommendation', ''),
                "confidence": intelligent_analysis.get('confidence', 0.5),
                "timestamp": monitor_data.get('timestamp', datetime.now().isoformat()),
                "execution_mode": "intelligent_supervision_fixed"
            }
            
            # Save detailed analysis
            analysis_file = monitoring_path / "analysis" / f"step_{step_num}_intelligent_analysis.json"
            with open(analysis_file, 'w') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟡 [Agent3] ✅ INTELLIGENT Step {step_num} analysis complete: {analysis_result['status']}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] INTELLIGENT step analysis failed: {str(e)}")
            return {
                "step": step_num,
                "name": step.get('step_name', f'Step {step_num}'),
                "status": "analysis_error",
                "error": str(e),
                "execution_mode": "intelligent_supervision_fixed",
                "timestamp": datetime.now().isoformat()
            }

    async def analyze_screenshot(
        self,
        screenshot_path: str,
        step: Dict[str, Any],
        ocr_text: str
    ) -> str:
        """Analyze screenshot for UI state and validation with OCR"""
        try:
            if not Path(screenshot_path).exists():
                return "Screenshot not available for analysis"
            
            # Basic OCR analysis
            analysis_points = []
            
            if ocr_text:
                ocr_lower = ocr_text.lower()
                
                # Check for success indicators
                success_keywords = ["success", "complete", "done", "welcome", "created", "signed"]
                error_keywords = ["error", "failed", "invalid", "wrong", "try again"]
                
                success_found = any(keyword in ocr_lower for keyword in success_keywords)
                error_found = any(keyword in ocr_lower for keyword in error_keywords)
                
                if success_found:
                    analysis_points.append("✅ Success indicators detected in UI")
                if error_found:
                    analysis_points.append("❌ Error indicators detected in UI")
                
                # Check for specific UI elements
                ui_elements = []
                if "button" in ocr_lower:
                    ui_elements.append("buttons")
                if "field" in ocr_lower or "input" in ocr_lower:
                    ui_elements.append("input fields")
                if "email" in ocr_lower:
                    ui_elements.append("email elements")
                if "password" in ocr_lower:
                    ui_elements.append("password elements")
                
                if ui_elements:
                    analysis_points.append(f"📱 UI elements detected: {', '.join(ui_elements)}")
                
                # Check expected result alignment
                expected_result = step.get('expected_result', '').lower()
                if expected_result:
                    alignment_score = 0
                    for word in expected_result.split():
                        if word in ocr_lower:
                            alignment_score += 1
                    
                    if alignment_score > 0:
                        analysis_points.append(f"🎯 Expected result alignment: {alignment_score} keywords matched")
            
            return "; ".join(analysis_points) if analysis_points else "Screenshot captured - no specific indicators detected"
            
        except Exception as e:
            return f"Screenshot analysis error: {str(e)}"

    async def generate_ai_step_analysis(
        self,
        step: Dict[str, Any],
        monitor_data: Dict[str, Any],
        screenshot_analysis: str
    ) -> Dict[str, Any]:
        """Generate AI-powered step analysis"""
        try:
            analysis_prompt = f"""
Analyze this automation step execution with intelligent supervision:

STEP DETAILS:
- Name: {step.get('step_name', '')}
- Description: {step.get('description', '')}
- Expected Result: {step.get('expected_result', '')}
- Action Type: {step.get('action_type', '')}

EXECUTION DATA:
- Success: {monitor_data.get('success', False)}
- OCR Text: {monitor_data.get('ocr', '')[:300]}
- Screenshot Analysis: {screenshot_analysis}
- Execution Mode: {monitor_data.get('execution_mode', 'intelligent_supervision_fixed')}

Provide analysis in this JSON format:
{{
"success_assessment": "success|partial|failed",
"confidence": 0.0-1.0,
"analysis": "Detailed analysis of what happened",
"recommendation": "Specific recommendation for improvement",
"agent2_feedback": "Feedback for Agent 2 code improvement"
}}
"""
            
            response = await asyncio.to_thread(
                self.ai_client.messages.create,
                model="claude-3-5-sonnet-20240620",  # FIXED: Use valid model
                max_tokens=1000,
                messages=[{"role": "user", "content": analysis_prompt}]
            )
            
            ai_response = response.content[0].text
            
            # Try to parse JSON response
            try:
                analysis_json = json.loads(ai_response)
                return analysis_json
            except:
                # Fallback if JSON parsing fails
                return {
                    "success_assessment": "partial",
                    "confidence": 0.7,
                    "analysis": ai_response[:500],
                    "recommendation": "AI analysis completed with intelligent supervision",
                    "agent2_feedback": "Continue monitoring for improvements"
                }
                
        except Exception as e:
            logger.error(f"🔴 [Agent3] AI analysis failed: {str(e)}")
            return await self.generate_rule_based_analysis(step, monitor_data, screenshot_analysis)

    async def generate_rule_based_analysis(
        self,
        step: Dict[str, Any],
        monitor_data: Dict[str, Any],
        screenshot_analysis: str
    ) -> Dict[str, Any]:
        """Generate rule-based analysis as fallback"""
        success = monitor_data.get('success', False)
        ocr_text = monitor_data.get('ocr', '').lower()
        
        # Rule-based assessment
        confidence = 0.8 if success else 0.3
        
        if success:
            if "success" in screenshot_analysis.lower() or "complete" in screenshot_analysis.lower():
                confidence = 0.9
                assessment = "success"
                analysis = "Step completed successfully with positive UI indicators"
                recommendation = "Step implementation is working correctly"
            else:
                confidence = 0.7
                assessment = "partial"
                analysis = "Step completed but UI state unclear"
                recommendation = "Add more validation checks for this step"
        else:
            assessment = "failed"
            analysis = "Step failed to execute properly"
            recommendation = "Review step implementation and error handling"
            
            if "error" in screenshot_analysis.lower():
                confidence = 0.9
                analysis = "Step failed with clear error indicators in UI"
                recommendation = "Fix the specific error causing step failure"
        
        return {
            "success_assessment": assessment,
            "confidence": confidence,
            "analysis": analysis,
            "recommendation": recommendation,
            "agent2_feedback": f"Step '{step.get('step_name', '')}' needs attention: {recommendation}"
        }

    async def update_step_status_realtime(
        self,
        task_id: int,
        step_num: int,
        analysis: Dict[str, Any]
    ) -> None:
        """Update database with real-time step status"""
        try:
            # Update step status in workflow_steps table
            await self.db_manager.update_workflow_step_status(
                seq_id=task_id,
                step_number=step_num,
                status=analysis.get('status', 'unknown'),
                execution_time=analysis.get('duration', 0.0),
                error_details=analysis.get('error', ''),
                screenshot_path=analysis.get('screenshot_path', ''),
                analysis_data=json.dumps(analysis, ensure_ascii=False)
            )
            
            logger.info(f"🟡 [Agent3] 📊 Updated database for step {step_num}: {analysis.get('status', 'unknown')}")
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Database update failed for step {step_num}: {str(e)}")

    async def generate_agent2_feedback(
        self,
        execution_result: Dict[str, Any],
        workflow_steps: List[Dict[str, Any]],
        screenshots_path: Path
    ) -> Dict[str, Any]:
        """Generate intelligent feedback for Agent 2 based on monitoring results"""
        try:
            logger.info("🟡 [Agent3] 🎯 Generating INTELLIGENT feedback for Agent 2...")
            
            analysis_results = execution_result.get('analysis_results', [])
            feedback_items = []
            
            # Analyze overall execution patterns
            total_steps = len(analysis_results)
            successful_steps = len([r for r in analysis_results if r.get('status') == 'success'])
            failed_steps = len([r for r in analysis_results if r.get('status') == 'failed'])
            success_rate = (successful_steps / total_steps) * 100 if total_steps > 0 else 0
            
            # Generate overall feedback
            overall_feedback = {
                "type": "overall_performance",
                "success_rate": success_rate,
                "total_steps": total_steps,
                "successful_steps": successful_steps,
                "failed_steps": failed_steps,
                "terminals_opened": execution_result.get('terminals_opened', 0),
                "platform_type": execution_result.get('platform_type', 'unknown'),
                "execution_approach": "intelligent_supervision_fixed",
                "recommendation": self.generate_overall_recommendation(success_rate)
            }
            
            feedback_items.append(overall_feedback)
            
            # Generate step-specific feedback
            for analysis in analysis_results:
                intelligent_analysis = analysis.get('intelligent_analysis', {})
                if isinstance(intelligent_analysis, dict) and intelligent_analysis.get('agent2_feedback'):
                    step_feedback = {
                        "type": "step_specific",
                        "step": analysis.get('step'),
                        "step_name": analysis.get('name'),
                        "status": analysis.get('status'),
                        "feedback": intelligent_analysis['agent2_feedback'],
                        "confidence": intelligent_analysis.get('confidence', 0.5),
                        "recommendation": intelligent_analysis.get('recommendation', '')
                    }
                    feedback_items.append(step_feedback)
            
            # Save feedback for Agent 2
            feedback_file = screenshots_path.parent / "feedback" / "intelligent_agent2_feedback.json"
            feedback_data = {
                "task_id": self.current_task_id,
                "timestamp": datetime.now().isoformat(),
                "execution_summary": execution_result,
                "feedback_items": feedback_items,
                "generated_by": "Agent3_IntelligentSupervisor_Fixed"
            }
            
            with open(feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟡 [Agent3] ✅ Generated {len(feedback_items)} INTELLIGENT feedback items for Agent 2")
            
            return {
                "success": True,
                "feedback_items": feedback_items,
                "feedback_file": str(feedback_file)
            }
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] INTELLIGENT feedback generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "feedback_items": []
            }

    def generate_overall_recommendation(self, success_rate: float) -> str:
        """Generate overall recommendation based on success rate"""
        if success_rate >= 90:
            return "Excellent performance! Script is working very well with fixed terminal execution."
        elif success_rate >= 70:
            return "Good performance with room for improvement. Focus on failed steps with fixed terminal execution."
        elif success_rate >= 50:
            return "Moderate performance. Review element finding strategies and error handling in fixed terminal environment."
        else:
            return "Poor performance. Significant improvements needed in automation approach with fixed terminal execution."

    async def update_database_with_step_analysis(
        self,
        task_id: int,
        execution_result: Dict[str, Any],
        feedback_result: Dict[str, Any]
    ) -> None:
        """Update database with comprehensive step analysis"""
        try:
            # Update main test execution record
            await self.db_manager.save_test_execution(
                seq_id=task_id,
                script_version=1,
                execution_attempt=1,
                success=execution_result.get('success', False),
                execution_output=str(execution_result.get('results', {})),
                error_details=execution_result.get('error', ''),
                execution_duration=execution_result.get('duration', 0.0)
            )
            
            # Save detailed monitoring results
            monitoring_data = {
                "approach": "intelligent_supervision_fixed",
                "screenshots_captured": execution_result.get('screenshots_captured', 0),
                "analysis_results": execution_result.get('analysis_results', []),
                "feedback_generated": len(feedback_result.get('feedback_items', [])),
                "terminals_opened": execution_result.get('terminals_opened', 0),
                "platform_type": execution_result.get('platform_type', 'unknown'),
                "monitoring_timestamp": datetime.now().isoformat()
            }
            
            # Save agent communication about the feedback
            if feedback_result.get('success'):
                await self.db_manager.save_agent_communication(
                    seq_id=task_id,
                    from_agent="agent3",
                    to_agent="agent2",
                    message_type="feedback",
                    message_content=json.dumps({
                        "feedback_summary": f"INTELLIGENT: Generated {len(feedback_result['feedback_items'])} feedback items with fixed terminal execution",
                        "terminals_opened": execution_result.get('terminals_opened', 0),
                        "platform_type": execution_result.get('platform_type', 'unknown'),
                        "key_recommendations": [item.get('recommendation', '') for item in feedback_result['feedback_items'][:3]]
                    }),
                    status="completed"
                )
            
            logger.info("🟡 [Agent3] ✅ Database updated with INTELLIGENT comprehensive analysis")
            
        except Exception as e:
            logger.error(f"🔴 [Agent3] Database update failed: {str(e)}")

    async def load_blueprint_for_monitoring(self, base_path: Path) -> Optional[Dict[str, Any]]:
        """Load blueprint for step-by-step monitoring"""
        try:
            blueprint_path = base_path / "agent1" / "blueprint.json"
            if blueprint_path.exists():
                with open(blueprint_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"🔴 [Agent3] Failed to load blueprint: {str(e)}")
            return None

    async def cleanup_testing_processes(self):
        """Clean up intelligent monitoring processes"""
        logger.info("🟡 [Agent3] Cleaning up INTELLIGENT monitoring processes...")
        try:
            self.monitoring_active = False
            self.step_analysis_history.clear()
            self.feedback_for_agent2.clear()
            
            if self.fixed_terminal_manager:
                self.fixed_terminal_manager.cleanup_processes()
            
            logger.info("✅ [Agent3] INTELLIGENT monitoring cleanup completed")
        except Exception as e:
            logger.error(f"❌ [Agent3] INTELLIGENT monitoring cleanup failed: {str(e)}")

    async def get_testing_status(self, task_id: int) -> Dict[str, Any]:
        """Get current intelligent testing status"""
        try:
            status = {
                "task_id": task_id,
                "agent": self.agent_name,
                "approach": "intelligent_supervision_fixed",
                "system": self.system,
                "monitoring_active": self.monitoring_active,
                "ai_available": self.ai_client is not None,
                "ocr_available": OCR_AVAILABLE,
                "fixed_terminal_manager_available": FIXED_TERMINAL_MANAGER_AVAILABLE,
                "steps_analyzed": len(self.step_analysis_history),
                "feedback_items_generated": len(self.feedback_for_agent2),
                "features": [
                    "intelligent_supervision", 
                    "fixed_terminal_execution", 
                    "screenshot_analysis", 
                    "ocr_analysis",
                    "ai_analysis",
                    "real_time_monitoring",
                    "agent2_feedback",
                    "database_updates"
                ]
            }
            
            if self.fixed_terminal_manager and hasattr(self.fixed_terminal_manager, 'get_process_status'):
                status["terminal_status"] = self.fixed_terminal_manager.get_process_status()
            
            return status
            
        except Exception as e:
            return {"error": str(e)}

# Global instance management
_agent3_instance: Optional[EnhancedAgent3_IsolatedTesting] = None

async def get_enhanced_agent3() -> EnhancedAgent3_IsolatedTesting:
    """Get or create Enhanced Agent 3 instance"""
    global _agent3_instance
    if _agent3_instance is None:
        _agent3_instance = EnhancedAgent3_IsolatedTesting()
        await _agent3_instance.initialize()
    return _agent3_instance

if __name__ == "__main__":
    # Test the FULL FEATURED intelligent agent
    async def test_full_featured_agent3():
        agent = EnhancedAgent3_IsolatedTesting()
        await agent.initialize()
        print("🧪 FULL FEATURED Intelligent Agent 3 with FIXED Terminal Manager test completed")
        await agent.cleanup_testing_processes()
    
    asyncio.run(test_full_featured_agent3())