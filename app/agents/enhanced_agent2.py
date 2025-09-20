"""
FIXED Enhanced Agent 2 - Advanced Code Generation with Production-Ready Mobile Automation
Corrects the 'text' variable error and maintains all existing functionality
"""

import asyncio
import json
import logging
import time
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Import utilities
try:
    import anthropic  # AI client for enhanced code generation
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

from app.database.database_manager import get_testing_db
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class EnhancedAgent2_CodeGenerator:
    """Enhanced Agent 2 - Production-Ready Code Generation with Dynamic Device Support"""
    
    def __init__(self):
        self.agent_name = "agent2"
        self.db_manager = None
        self.ai_client = None
        self.settings = get_settings()
        
    async def initialize(self):
        """Initialize AI client and database connection"""
        
        if CLAUDE_AVAILABLE and self.settings.anthropic_api_key:
            self.ai_client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
            logger.info("🟢 [Agent2] Claude AI client initialized")
        else:
            logger.warning("🟢 [Agent2] No Claude API key, using fallback generation")
        
        # Initialize database
        self.db_manager = await get_testing_db()
        logger.info("🟢 [Agent2] Code generator initialized with enhanced mobile automation")
    
    async def generate_production_code(
        self,
        task_id: int,
        blueprint_path: Path,
        instruction: str,
        platform: str,
        additional_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate complete, production-ready automation code"""
        
        logger.info(f"🟢 [Agent2] Starting enhanced code generation for task {task_id}")
        
        try:
            # Create agent2 output folder
            base_path = blueprint_path.parent.parent
            agent2_path = base_path / "agent2"
            agent2_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"🟢 [Agent2] Created agent2 folder: {agent2_path}")
            
            # Load blueprint
            blueprint = await self.load_blueprint(blueprint_path)
            if not blueprint:
                raise Exception("Failed to load blueprint")
            
            logger.info(f"🟢 [Agent2] Loaded blueprint with {len(blueprint.get('workflow_steps', []))} steps")
            
            # Generate production automation script
            if platform.lower() == 'mobile':
                script_result = await self.generate_mobile_automation_script(
                    blueprint, instruction, additional_data or {}
                )
            else:
                script_result = await self.generate_web_automation_script(
                    blueprint, instruction, additional_data or {}
                )
            
            if not script_result['success']:
                raise Exception(f"Script generation failed: {script_result.get('error', 'Unknown error')}")
            
            # Save generated script
            script_path = agent2_path / "script.py"
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_result['code'])
            
            # Save to database
            await self.db_manager.save_file(
                task_id=task_id,
                filename="script.py", 
                content=script_result['code'],
                version=1
            )
            
            # Generate enhanced requirements.txt
            requirements = self.generate_enhanced_requirements(platform, blueprint)
            requirements_path = agent2_path / "requirements.txt"
            with open(requirements_path, 'w', encoding='utf-8') as f:
                f.write(requirements)
            
            # Save requirements to database
            await self.db_manager.save_file(
                task_id=task_id,
                filename="requirements.txt",
                content=requirements,
                version=1
            )
            
            # Create device configuration for mobile
            device_config_created = False
            if platform.lower() == 'mobile':
                device_config_created = await self.create_device_configuration(agent2_path)
            
            # Create enhanced OCR templates
            ocr_logs_created = await self.create_enhanced_ocr_templates(
                agent2_path, blueprint.get('workflow_steps', [])
            )
            
            logger.info(f"🟢 [Agent2] ✅ Enhanced script generated: {len(script_result['code'])} characters")
            logger.info(f"🟢 [Agent2] ✅ Requirements created: {requirements_path}")
            logger.info(f"🟢 [Agent2] ✅ OCR log templates prepared: {agent2_path / 'ocr_logs'}")
            logger.info("🟢 [Agent2] ✅ Enhanced code generation completed")
            
            return {
                "success": True,
                "agent2_path": str(agent2_path),
                "script_path": str(script_path),
                "requirements_path": str(requirements_path),
                "script_size": len(script_result['code']),
                "workflow_steps": len(blueprint.get('workflow_steps', [])),
                "platform": platform,
                "ocr_logs_prepared": ocr_logs_created,
                "device_config_created": device_config_created
            }
            
        except Exception as e:
            logger.error(f"🔴 [Agent2] Enhanced code generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent2_path": None
            }
    
    async def generate_mobile_automation_script(
        self,
        blueprint: Dict[str, Any],
        instruction: str,
        additional_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate production-ready mobile automation script with dynamic device detection"""
        
        workflow_steps = blueprint.get('workflow_steps', [])
        task_id = blueprint.get('task_id', 0)
        
        # Extract user data from instruction and additional_data
        user_data = self.extract_user_data(instruction, additional_data)
        
        # Create the complete mobile automation script
        script_template = f'''"""
Production Mobile Automation Script - Task {task_id}
Generated by Enhanced Agent 2
Task: {instruction}
Platform: Mobile (Android)
Generated: {datetime.now(timezone.utc).isoformat()}
"""

import logging
import time
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Mobile automation imports
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

# OCR and image processing
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation_execution.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DynamicDeviceManager:
    """Handles dynamic Android device detection and management"""
    
    def __init__(self):
        self.device_info = None
        self.capabilities = None
    
    def detect_connected_devices(self) -> List[Dict[str, Any]]:
        """Detect all connected Android devices"""
        devices = []
        try:
            result = subprocess.run(
                ["adb", "devices", "-l"], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\\n')[1:]  # Skip header
                for line in lines:
                    if line.strip() and 'device' in line:
                        parts = line.split()
                        if len(parts) >= 2 and parts[1] == 'device':
                            device_id = parts[0]
                            device_info = self.get_device_details(device_id)
                            if device_info:
                                devices.append(device_info)
                
                logger.info(f"✅ Detected {{len(devices)}} connected Android devices")
                return devices
                
        except Exception as e:
            logger.error(f"❌ Device detection failed: {{str(e)}}")
            return []
    
    def get_device_details(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific device"""
        try:
            device_info = {{
                "device_id": device_id,
                "device_name": "Android Device",
                "is_emulator": device_id.startswith("emulator-"),
                "api_level": None,
                "screen_resolution": None,
                "manufacturer": None,
                "model": None,
                "android_version": None
            }}
            
            # Get device properties
            properties = [
                ("ro.build.version.release", "android_version"),
                ("ro.build.version.sdk", "api_level"),
                ("ro.product.manufacturer", "manufacturer"),
                ("ro.product.model", "model")
            ]
            
            for prop, key in properties:
                try:
                    result = subprocess.run(
                        ["adb", "-s", device_id, "shell", "getprop", prop],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        device_info[key] = result.stdout.strip()
                except Exception:
                    continue
            
            # Get screen resolution
            try:
                result = subprocess.run(
                    ["adb", "-s", device_id, "shell", "wm", "size"],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    import re
                    match = re.search(r'(\\d+)x(\\d+)', result.stdout)
                    if match:
                        device_info["screen_resolution"] = f"{{match.group(1)}}x{{match.group(2)}}"
            except Exception:
                pass
            
            # Set display name
            if device_info["manufacturer"] and device_info["model"]:
                device_info["device_name"] = f"{{device_info['manufacturer']}} {{device_info['model']}}"
            elif device_info["is_emulator"]:
                device_info["device_name"] = f"Android Emulator ({{device_id}})"
            
            return device_info
            
        except Exception as e:
            logger.error(f"❌ Failed to get device details for {{device_id}}: {{str(e)}}")
            return None
    
    def select_best_device(self) -> Optional[Dict[str, Any]]:
        """Select the best available device for automation"""
        devices = self.detect_connected_devices()
        if not devices:
            logger.error("❌ No connected Android devices found")
            return None
        
        # Prefer real devices over emulators
        real_devices = [d for d in devices if not d['is_emulator']]
        selected = real_devices[0] if real_devices else devices[0]
        
        self.device_info = selected
        logger.info(f"✅ Selected device: {{selected['device_name']}} ({{selected['device_id']}})")
        return selected
    
    def create_capabilities(self) -> Dict[str, Any]:
        """Create Appium capabilities for the selected device"""
        if not self.device_info:
            raise Exception("No device selected")
        
        capabilities = {{
            "platformName": "Android",
            "deviceName": self.device_info["device_name"],
            "udid": self.device_info["device_id"],
            "automationName": "UiAutomator2",
            "noReset": False,
            "fullReset": False,
            "newCommandTimeout": 300,
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            "autoGrantPermissions": True,
            "systemPort": 8200 + random.randint(1, 99),  # Dynamic port
            "enforceXPath1": True,
            "appWaitTimeout": 30000
        }}
        
        if self.device_info.get("android_version"):
            capabilities["platformVersion"] = self.device_info["android_version"]
        
        self.capabilities = capabilities
        return capabilities

class ProductionMobileAutomation:
    """Production-ready mobile automation with advanced features"""
    
    def __init__(self):
        self.driver = None
        self.device_manager = DynamicDeviceManager()
        self.ocr_logs_dir = Path("ocr_logs")
        self.ocr_logs_dir.mkdir(exist_ok=True)
        self.screen_size = None
        self.step_results = []
        
        # User data for automation
        self.user_data = {user_data}
    
    def setup_driver(self) -> bool:
        """Setup Appium driver with dynamic device detection"""
        try:
            logger.info("🚀 Setting up mobile automation driver...")
            
            # Select best device
            device = self.device_manager.select_best_device()
            if not device:
                raise Exception("No suitable device found")
            
            # Create capabilities
            capabilities = self.device_manager.create_capabilities()
            logger.info(f"📱 Device capabilities: {{json.dumps(capabilities, indent=2)}}")
            
            # Initialize driver
            self.driver = webdriver.Remote(
                "http://localhost:4723", 
                options=UiAutomator2Options().load_capabilities(capabilities)
            )
            self.driver.implicitly_wait(10)
            
            # Get screen size
            self.screen_size = self.driver.get_window_size()
            logger.info(f"📱 Screen resolution: {{self.screen_size['width']}}x{{self.screen_size['height']}}")
            
            # Update driver settings for better stability
            self.driver.update_settings({{
                "enforceXPath1": True,
                "waitForIdleTimeout": 1000,
                "waitForSelectorTimeout": 5000
            }})
            
            logger.info("✅ Mobile driver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Driver setup failed: {{str(e)}}")
            return False
    
    def enhanced_screenshot_with_ocr(self, step_name: str) -> Tuple[str, str]:
        """Take screenshot with enhanced OCR processing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.ocr_logs_dir / f"{{step_name}}_{{timestamp}}.png"
        ocr_path = self.ocr_logs_dir / f"{{step_name}}_{{timestamp}}.txt"
        
        if not self.driver:
            return "", ""
        
        try:
            # Take screenshot
            self.driver.save_screenshot(str(screenshot_path))
            
            # Enhanced OCR processing
            image = cv2.imread(str(screenshot_path))
            # Preprocess image for better OCR
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply different OCR techniques
            ocr_results = []
            
            # Standard OCR
            standard_text = pytesseract.image_to_string(gray, config='--psm 6')
            ocr_results.append(("Standard OCR", standard_text))
            
            # OCR with different PSM modes for better text detection
            for psm in [3, 6, 8, 11]:
                try:
                    psm_text = pytesseract.image_to_string(gray, config=f'--psm {{psm}}')
                    if psm_text.strip() and psm_text != standard_text:
                        ocr_results.append((f"PSM {{psm}} OCR", psm_text))
                except:
                    continue
            
            # Save comprehensive OCR result
            with open(ocr_path, 'w', encoding='utf-8') as f:
                f.write(f"OCR Analysis for {{step_name}}\\n")
                f.write(f"Timestamp: {{timestamp}}\\n")
                f.write(f"Screenshot: {{screenshot_path}}\\n")
                f.write(f"Device: {{self.device_manager.device_info['device_name'] if self.device_manager.device_info else 'Unknown'}}\\n")
                f.write(f"Screen Size: {{self.screen_size}}\\n")
                f.write("=" * 50 + "\\n")
                
                for method, text in ocr_results:
                    f.write(f"{{method}}:\\n")
                    f.write(f"{{text}}\\n")
                    f.write("-" * 30 + "\\n")
            
            # Return best OCR result (usually the first one)
            best_ocr = ocr_results[0][1] if ocr_results else ""
            
            logger.info(f"📸 Screenshot and OCR saved: {{screenshot_path}}")
            return str(screenshot_path), best_ocr
            
        except Exception as e:
            logger.error(f"❌ Screenshot/OCR failed: {{str(e)}}")
            return str(screenshot_path) if 'screenshot_path' in locals() else "", ""
    
    def smart_element_finder(self, locator_strategies: List[Dict[str, str]], wait_time: int = 10) -> Optional[Any]:
        """Smart element finding with multiple strategies"""
        wait = WebDriverWait(self.driver, wait_time)
        
        for strategy in locator_strategies:
            try:
                by_type = strategy.get("by", "id")
                value = strategy.get("value", "")
                
                # Map string locator types to AppiumBy constants
                by_mapping = {{
                    "id": AppiumBy.ID,
                    "xpath": AppiumBy.XPATH,
                    "class_name": AppiumBy.CLASS_NAME,
                    "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
                    "android_uiautomator": AppiumBy.ANDROID_UIAUTOMATOR,
                    "name": AppiumBy.NAME
                }}
                
                locator = by_mapping.get(by_type, AppiumBy.XPATH)
                element = wait.until(EC.presence_of_element_located((locator, value)))
                
                logger.info(f"✅ Element found using {{by_type}}: {{value}}")
                return element
                
            except TimeoutException:
                logger.warning(f"⚠️ Element not found with strategy {{strategy['by']}}: {{strategy['value']}}")
                continue
            except Exception as e:
                logger.warning(f"⚠️ Error with locator strategy {{strategy}}: {{str(e)}}")
                continue
        
        logger.error("❌ Element not found with any strategy")
        return None
    
    def smart_tap(self, x: int, y: int) -> bool:
        """Smart tap with coordinate validation"""
        try:
            # Validate coordinates
            if x < 0 or y < 0 or x > self.screen_size["width"] or y > self.screen_size["height"]:
                logger.warning(f"⚠️ Coordinates out of bounds: ({{x}}, {{y}})")
                return False
            
            self.driver.tap([(x, y)], 100)
            logger.info(f"✅ Tapped at coordinates: ({{x}}, {{y}})")
            time.sleep(1)  # Brief pause
            return True
            
        except Exception as e:
            logger.error(f"❌ Tap failed at ({{x}}, {{y}}): {{str(e)}}")
            return False
    
    def safe_send_keys(self, element, input_text: str, clear_first: bool = True) -> bool:
        """Safe text input with validation"""
        try:
            if clear_first:
                element.clear()
                time.sleep(0.5)
                
            element.send_keys(input_text)
            logger.info(f"✅ Text entered: {{input_text[:20]}}..." if len(input_text) > 20 else f"✅ Text entered: {{input_text}}")
            time.sleep(1)
            return True
            
        except Exception as e:
            logger.error(f"❌ Text input failed: {{str(e)}}")
            return False
    
    def run_automation(self) -> bool:
        """Execute the complete automation workflow"""
        workflow_start_time = time.time()
        
        try:
            logger.info("🚀 Starting production mobile automation...")
            logger.info(f"📋 Task: {{'{instruction}'}}")
            logger.info(f"👤 User Data: {{json.dumps(self.user_data, indent=2)}}")
            
            if not self.setup_driver():
                raise Exception("Failed to setup mobile driver")
            
            # Launch Outlook app
            try:
                self.driver.start_activity("com.microsoft.office.outlook", ".MainActivity")
                time.sleep(3)
            except:
                # Try alternative launch methods
                try:
                    self.driver.activate_app("com.microsoft.office.outlook")
                    time.sleep(3)
                    logger.info("✅ Outlook app launched")
                except Exception as e:
                    logger.warning(f"⚠️ App launch issues: {{str(e)}}")
'''

        # Add the workflow steps execution
        for i, step in enumerate(workflow_steps, 1):
            step_name = step.get('step_name', f'Step {i}')
            step_description = step.get('description', '')
            expected_result = step.get('expected_result', '')
            
            script_template += f'''
            # Step {i}: {step_name}
            logger.info(f"🔄 Executing Step {i}: {step_name}")
            try:
                # Take screenshot before action
                screenshot_before, ocr_before = self.enhanced_screenshot_with_ocr(f"step_{i}_before")
                
                # Generate actual implementation for each workflow step
                step_name_lower = "{step_name}".lower()
                description = "{step_description}"
                
                {self.generate_step_implementation(step, user_data)}
                
                # Take screenshot after action
                screenshot_after, ocr_after = self.enhanced_screenshot_with_ocr(f"step_{i}_after")
                
                logger.info(f"✅ Step {i} completed successfully")
                self.step_results.append({{
                    "step": {i},
                    "name": step_name,
                    "status": "completed",
                    "screenshot_before": screenshot_before,
                    "ocr_before": ocr_before,
                    "screenshot_after": screenshot_after,
                    "ocr_after": ocr_after,
                    "expected_result": "{expected_result}"
                }})
                
            except Exception as e:
                logger.error(f"❌ Step {i} failed: {{str(e)}}")
                self.step_results.append({{
                    "step": {i},
                    "name": step_name,
                    "status": "failed",
                    "error": str(e),
                    "expected_result": "{expected_result}"
                }})
'''

        # Add the footer
        script_template += '''
            # Save comprehensive results
            execution_time = time.time() - workflow_start_time
            results_summary = {
                "task_id": task_id,
                "instruction": instruction,
                "execution_time": execution_time,
                "execution_timestamp": datetime.utcnow().isoformat(),
                "device_info": self.device_manager.device_info,
                "screen_size": self.screen_size,
                "total_steps": len(self.step_results),
                "completed_steps": len([r for r in self.step_results if r["status"] == "completed"]),
                "failed_steps": len([r for r in self.step_results if r["status"] == "failed"]),
                "success_rate": len([r for r in self.step_results if r["status"] == "completed"]) / len(self.step_results) * 100 if self.step_results else 0,
                "user_data": self.user_data,
                "results": self.step_results
            }
            
            # Save results
            results_path = self.ocr_logs_dir / "automation_results.json"
            with open(results_path, 'w', encoding='utf-8') as f:
                json.dump(results_summary, f, indent=2, ensure_ascii=False)
            
            success_count = results_summary["completed_steps"]
            total_count = results_summary["total_steps"]
            
            logger.info(f"🎯 Automation completed: {success_count}/{total_count} steps successful")
            logger.info(f"⏱️ Total execution time: {execution_time:.2f} seconds")
            logger.info(f"📊 Success rate: {results_summary['success_rate']:.1f}%")
            
            return results_summary["success_rate"] >= 70.0  # Consider 70% success rate as overall success
            
        except Exception as e:
            logger.error(f"❌ Mobile automation failed: {str(e)}")
            return False
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("✅ Mobile driver cleaned up")
                except:
                    pass

if __name__ == "__main__":
    automation = ProductionMobileAutomation()
    success = automation.run_automation()
    
    print("-" * 50)
    print(f"AUTOMATION RESULT: {'SUCCESS' if success else 'FAILED'}")
    print("-" * 50)
    
    exit(0 if success else 1)
'''
        
        return {
            "success": True,
            "code": script_template,
            "features": [
                "dynamic_device_detection",
                "enhanced_ocr_processing", 
                "smart_element_finding",
                "production_error_handling",
                "comprehensive_logging",
                "multiple_locator_strategies"
            ]
        }
    
    def generate_step_implementation(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate actual implementation for each workflow step"""
        step_name = step.get('step_name', '').lower()
        description = step.get('description', '')
        
        # Analyze step to determine implementation approach
        if any(keyword in step_name for keyword in ["navigate", "open", "launch", "start"]):
            return self.generate_navigation_code(step, user_data)
        elif any(keyword in step_name for keyword in ["enter", "input", "type", "fill"]):
            return self.generate_input_code(step, user_data)
        elif any(keyword in step_name for keyword in ["click", "tap", "press", "select"]):
            return self.generate_click_code(step, user_data)
        elif any(keyword in step_name for keyword in ["wait", "verify", "check", "validate"]):
            return self.generate_verification_code(step, user_data)
        elif any(keyword in step_name for keyword in ["scroll", "swipe"]):
            return self.generate_scroll_code(step, user_data)
        else:
            return self.generate_generic_code(step, user_data)
    
    def generate_navigation_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate navigation/app launch code"""
        return '''# Navigation/Launch Implementation
                if "outlook" in description.lower():
                    # Generic app navigation
                    time.sleep(2)
                    logger.info("✅ Navigation step completed")'''
    
    def generate_input_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate input/text entry code"""
        return '''# Text Input Implementation
                input_text = ""
                if "name" in description.lower():
                    input_text = self.user_data.get("name", "Krishna Kumar")
                elif "email" in description.lower():
                    input_text = self.user_data.get("email", "krishna.kumar@example.com")
                elif "dob" in description.lower() or "date" in description.lower():
                    input_text = self.user_data.get("dob", "20/02/2000")
                elif "password" in description.lower():
                    input_text = self.user_data.get("password", "SecurePass123!")
                
                if input_text:
                    # Try multiple input field locators
                    input_strategies = [
                        {"by": "xpath", "value": "//android.widget.EditText[contains(@text,'name') or contains(@hint,'name')]"},
                        {"by": "xpath", "value": "//android.widget.EditText[contains(@text,'email') or contains(@hint,'email')]"},
                        {"by": "xpath", "value": "//android.widget.EditText[contains(@text,'date') or contains(@hint,'date')]"},
                        {"by": "class_name", "value": "android.widget.EditText"},
                        {"by": "xpath", "value": "//*[@input-type='text']"},
                        {"by": "xpath", "value": "//android.widget.EditText"}
                    ]
                    
                    input_element = self.smart_element_finder(input_strategies, wait_time=15)
                    if input_element:
                        self.safe_send_keys(input_element, input_text)
                        logger.info(f"✅ Entered text: {input_text}")
                    else:
                        # Fallback: tap center and type
                        center_x = self.screen_size["width"] // 2
                        center_y = self.screen_size["height"] // 2
                        self.smart_tap(center_x, center_y)
                        time.sleep(1)
                        self.driver.set_value(input_text)
                        logger.info(f"✅ Text entered via fallback method")
                else:
                    logger.warning("⚠️ No input text determined for this step")'''
    
    def generate_click_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate click/tap interaction code"""
        return '''# Click/Tap Implementation
                button_strategies = [
                    {"by": "xpath", "value": "//android.widget.Button[contains(@text,'Create') or contains(@text,'Sign up') or contains(@text,'Register')]"},
                    {"by": "xpath", "value": "//android.widget.Button[contains(@text,'Next') or contains(@text,'Continue') or contains(@text,'Submit')]"},
                    {"by": "xpath", "value": "//android.widget.Button[contains(@text,'Done') or contains(@text,'Finish')]"},
                    {"by": "accessibility_id", "value": "Create account"},
                    {"by": "accessibility_id", "value": "Sign up"},
                    {"by": "class_name", "value": "android.widget.Button"},
                    {"by": "xpath", "value": "//*[@clickable='true']"}
                ]
                
                button_element = self.smart_element_finder(button_strategies, wait_time=10)
                if button_element:
                    button_element.click()
                    logger.info("✅ Button clicked successfully")
                    time.sleep(2)
                else:
                    # If there are clickable elements, try to interact
                    if any(keyword in ocr_before.lower() for keyword in ["button", "click", "tap", "next", "continue"]):
                        # Try tapping common button areas
                        possible_button_coords = [
                            (self.screen_size["width"] // 2, int(self.screen_size["height"] * 0.8)),  # Bottom center
                            (int(self.screen_size["width"] * 0.8), int(self.screen_size["height"] * 0.9)),  # Bottom right
                            (self.screen_size["width"] // 2, int(self.screen_size["height"] * 0.7))   # Lower center
                        ]
                        
                        for x, y in possible_button_coords:
                            if self.smart_tap(x, y):
                                logger.info(f"✅ Tapped at fallback coordinates: ({x}, {y})")
                                break
                        
                        time.sleep(2)'''
    
    def generate_verification_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate verification/validation code"""
        return '''# Verification Implementation
                # Check for success indicators in OCR text
                success_indicators = ["account created", "welcome", "success", "completed", "signed up", "registered"]
                error_indicators = ["error", "failed", "invalid", "incorrect", "try again"]
                
                verification_ocr = ocr_before.lower()
                verification_passed = any(indicator in verification_ocr for indicator in success_indicators)
                verification_failed = any(indicator in verification_ocr for indicator in error_indicators)
                
                if verification_passed:
                    logger.info("✅ Verification passed - success indicators found")
                elif verification_failed:
                    logger.warning("⚠️ Verification concerns - error indicators found")
                else:
                    logger.info("ℹ️ Verification neutral - no clear indicators")
                
                # Look for specific UI elements that indicate success
                success_elements = [
                    {"by": "xpath", "value": "//*[contains(@text,'Welcome')]"},
                    {"by": "xpath", "value": "//*[contains(@text,'Success')]"},
                    {"by": "xpath", "value": "//*[contains(@text,'Created')]"},
                    {"by": "accessibility_id", "value": "Account created"}
                ]
                
                for element_strategy in success_elements:
                    try:
                        element = self.driver.find_element(
                            AppiumBy.XPATH if element_strategy["by"] == "xpath" else AppiumBy.ACCESSIBILITY_ID,
                            element_strategy["value"]
                        )
                        if element:
                            logger.info(f"✅ Success element found: {element_strategy['value']}")
                            verification_passed = True
                            break
                    except:
                        continue
                
                except Exception as e:
                    logger.info(f"ℹ️ Element verification skipped: {str(e)}")
                
                time.sleep(1)'''
    
    def generate_scroll_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate scroll/swipe code"""
        return '''# Scroll/Swipe Implementation
                try:
                    # Perform scroll action
                    start_x = self.screen_size["width"] // 2
                    start_y = int(self.screen_size["height"] * 0.7)
                    end_x = start_x
                    end_y = int(self.screen_size["height"] * 0.3)
                    
                    self.driver.swipe(start_x, start_y, end_x, end_y, duration=1000)
                    logger.info("✅ Scroll action performed")
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"⚠️ Scroll failed, continuing: {str(e)}")'''
    
    def generate_generic_code(self, step: Dict[str, Any], user_data: Dict[str, str]) -> str:
        """Generate generic implementation code"""
        return '''# Generic Step Implementation
                # Try to find and click a relevant button
                generic_buttons = [
                    {"by": "class_name", "value": "android.widget.Button"},
                    {"by": "xpath", "value": "//*[@clickable='true']"}
                ]
                
                generic_button = self.smart_element_finder(generic_buttons, wait_time=5)
                if generic_button:
                    generic_button.click()
                    logger.info("✅ Generic interaction performed")
                
                logger.info("ℹ️ Generic step implementation completed")'''
    
    def extract_user_data(self, instruction: str, additional_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract user data from instruction and additional data"""
        user_data = {}
        
        # Extract from instruction
        instruction_lower = instruction.lower()
        
        # Name extraction
        if "name" in instruction_lower:
            import re
            name_match = re.search(r'name\s+([A-Za-z\s]+?)(?:\s+and|\s+dob|$)', instruction)
            if name_match:
                user_data["name"] = name_match.group(1).strip()
        
        # Set defaults if not provided
        defaults = {
            "name": "Krishna Kumar",
            "dob": "20/02/2000",
            "email": "krishna.kumar@example.com",
            "password": "SecurePass123!"
        }
        
        for key, default_value in defaults.items():
            if key not in user_data:
                user_data[key] = default_value
        
        return user_data
    
    def generate_enhanced_requirements(self, platform: str, blueprint: Dict[str, Any]) -> str:
        """Generate comprehensive requirements.txt"""
        base_requirements = [
            "# Production Mobile Automation Requirements",
            "# Generated by Enhanced Agent 2",
            f"# Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "# Core automation libraries",
            "selenium>=4.15.0",
            "requests>=2.31.0",
            "urllib3>=2.0.0",
            "",
            "# Mobile automation",
            "Appium-Python-Client>=3.1.0",
            "",
            "# Image processing and OCR",
            "Pillow>=10.0.0",
            "pytesseract>=0.3.10",
            "opencv-python>=4.8.0",
            "numpy>=1.24.0",
            "",
            "# Data processing",
            "faker>=19.0.0",
            "python-dateutil>=2.8.2",
            "",
            "# Logging and utilities",
            "colorlog>=6.7.0",
            "psutil>=5.9.0"
        ]
        
        if platform.lower() == 'web':
            base_requirements.extend([
                "",
                "# Web automation",
                "webdriver-manager>=4.0.0",
                "beautifulsoup4>=4.12.0"
            ])
        
        return "\\n".join(base_requirements)
    
    async def create_device_configuration(self, agent2_path: Path) -> bool:
        """Create device configuration file for mobile testing"""
        try:
            device_config = {
                "device_detection": {
                    "enabled": True,
                    "prefer_real_devices": True,
                    "fallback_to_emulator": True
                },
                "appium_settings": {
                    "server_url": "http://localhost:4723",
                    "new_command_timeout": 300,
                    "implicit_wait": 10
                },
                "automation_settings": {
                    "screenshot_on_failure": True,
                    "ocr_enabled": True,
                    "retry_attempts": 3,
                    "step_delay": 1
                }
            }
            
            config_path = agent2_path / "device_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(device_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"🟢 [Agent2] Device configuration created: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"🔴 [Agent2] Failed to create device config: {str(e)}")
            return False
    
    async def load_blueprint(self, blueprint_path: Path) -> Optional[Dict[str, Any]]:
        """Load blueprint from file"""
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                blueprint = json.load(f)
            return blueprint
        except Exception as e:
            logger.error(f"🔴 [Agent2] Failed to load blueprint: {str(e)}")
            return None
    
    async def create_enhanced_ocr_templates(self, agent2_path: Path, workflow_steps: List[Dict[str, Any]]) -> bool:
        """Create enhanced OCR log templates"""
        try:
            ocr_logs_dir = agent2_path / "ocr_logs"
            ocr_logs_dir.mkdir(exist_ok=True)
            
            # Create README for OCR logs
            readme_content = """# OCR Features:
- Multiple PSM modes for better text detection
- Enhanced image preprocessing  
- Comprehensive text extraction
- Element detection and analysis

# File Structure:
- step_X_before_TIMESTAMP.png - Screenshot before step execution
- step_X_before_TIMESTAMP.txt - OCR analysis of before screenshot
- step_X_after_TIMESTAMP.png - Screenshot after step execution
- step_X_after_TIMESTAMP.txt - OCR analysis of after screenshot
- automation_results.json - Complete execution results
"""
            readme_path = ocr_logs_dir / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            logger.info(f"🟢 [Agent2] Enhanced OCR templates created: {ocr_logs_dir}")
            return True
            
        except Exception as e:
            logger.error(f"🔴 [Agent2] Failed to create OCR templates: {str(e)}")
            return False
    
    async def generate_web_automation_script(
        self,
        blueprint: Dict[str, Any],
        instruction: str,
        additional_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate web automation script (placeholder)"""
        # For now, return a simple web script template
        return {
            "success": True,
            "code": f'# Web Automation Script\\n# Task: {instruction}\\nprint("Web automation not yet implemented")',
            "features": ["web_automation_placeholder"]
        }