#!/usr/bin/env python3
"""
Free LLM Auto-Installer for Windows
Automatically downloads and installs all major free open-source LLMs
"""

import os
import sys
import subprocess
import json
import shutil
import platform
from pathlib import Path
from typing import List, Dict, Tuple
import urllib.request
import time

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LLMInstaller:
    def __init__(self, model_path: str = None):
        """Initialize the LLM installer"""
        self.system = platform.system()
        
        if model_path is None:
            if self.system == "Windows":
                self.model_path = Path(os.path.expanduser("~/.ollama/models"))
            else:
                self.model_path = Path(os.path.expanduser("~/.ollama/models"))
        else:
            self.model_path = Path(model_path)
        
        # Ensure model directory exists
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        # Models to install (name, display_name, size_gb)
        self.models = [
            {"name": "llama2", "display": "Llama 2 (7B)", "size": "3.8GB"},
            {"name": "mistral", "display": "Mistral (7B)", "size": "4.1GB"},
            {"name": "phi", "display": "Phi-3 Mini (3.8B)", "size": "2.3GB"},
            {"name": "gemma:7b", "display": "Gemma (7B)", "size": "5.0GB"},
            {"name": "neural-chat", "display": "Neural Chat (7B)", "size": "4.0GB"},
            {"name": "dolphin-mixtral", "display": "Dolphin Mixtral (47B)", "size": "27GB"},
        ]
        
    def print_header(self):
        """Print installation header"""
        print(f"\n{Colors.HEADER}{'╔' + '═' * 40 + '╗'}{Colors.ENDC}")
        print(f"{Colors.HEADER}║{Colors.BOLD} Free LLM Auto-Installer for Windows {Colors.ENDC}{Colors.HEADER}║{Colors.ENDC}")
        print(f"{Colors.HEADER}{'╚' + '═' * 40 + '╝'}{Colors.ENDC}\n")
    
    def check_ollama(self) -> bool:
        """Check if Ollama is installed"""
        try:
            subprocess.run(["ollama", "--version"], 
                         capture_output=True, 
                         check=True,
                         timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def install_ollama(self) -> bool:
        """Install Ollama on Windows"""
        print(f"{Colors.OKCYAN}Step 1: Installing Ollama...{Colors.ENDC}")
        
        if self.check_ollama():
            print(f"{Colors.OKGREEN}✓ Ollama is already installed{Colors.ENDC}\n")
            return True
        
        if self.system != "Windows":
            print(f"{Colors.FAIL}✗ This installer is for Windows only{Colors.ENDC}")
            print(f"{Colors.WARNING}Please install Ollama manually from: https://ollama.ai/download{Colors.ENDC}\n")
            return False
        
        print(f"{Colors.WARNING}Ollama not found. Attempting automatic installation...{Colors.ENDC}")
        
        try:
            installer_url = "https://ollama.ai/download/windows"
            installer_path = Path.cwd() / "OllamaSetup.exe"
            
            print(f"{Colors.OKCYAN}Downloading Ollama installer...{Colors.ENDC}")
            urllib.request.urlretrieve(installer_url, installer_path)
            
            print(f"{Colors.OKCYAN}Running Ollama installer (this may take several minutes)...{Colors.ENDC}")
            subprocess.run([str(installer_path)], check=False)
            
            # Clean up
            installer_path.unlink(missing_ok=True)
            
            # Verify installation
            time.sleep(3)
            if self.check_ollama():
                print(f"{Colors.OKGREEN}✓ Ollama installed successfully{Colors.ENDC}\n")
                return True
            else:
                print(f"{Colors.WARNING}⚠ Ollama may not be in PATH yet. Please restart your terminal.{Colors.ENDC}\n")
                return True
                
        except Exception as e:
            print(f"{Colors.FAIL}✗ Error installing Ollama: {e}{Colors.ENDC}")
            print(f"{Colors.WARNING}Please install manually from: https://ollama.ai/download{Colors.ENDC}\n")
            return False
    
    def download_models(self) -> Tuple[int, int]:
        """Download all LLM models"""
        print(f"\n{Colors.OKCYAN}Step 2: Downloading LLM Models...{Colors.ENDC}")
        print(f"{Colors.WARNING}This may take 30+ minutes depending on your internet connection{Colors.ENDC}\n")
        
        success_count = 0
        failure_count = 0
        
        for i, model in enumerate(self.models, 1):
            print(f"{Colors.OKCYAN}[{i}/{len(self.models)}] Downloading: {model['display']} ({model['size']})...{Colors.ENDC}")
            
            try:
                result = subprocess.run(
                    ["ollama", "pull", model["name"]],
                    capture_output=True,
                    text=True,
                    timeout=3600  # 1 hour timeout per model
                )
                
                if result.returncode == 0:
                    print(f"{Colors.OKGREEN}✓ Successfully installed {model['display']}{Colors.ENDC}\n")
                    success_count += 1
                else:
                    print(f"{Colors.FAIL}✗ Failed to install {model['display']}{Colors.ENDC}")
                    print(f"  Error: {result.stderr}\n")
                    failure_count += 1
                    
            except subprocess.TimeoutExpired:
                print(f"{Colors.FAIL}✗ Timeout downloading {model['display']}. Skipping...{Colors.ENDC}\n")
                failure_count += 1
            except Exception as e:
                print(f"{Colors.FAIL}✗ Error downloading {model['display']}: {e}{Colors.ENDC}\n")
                failure_count += 1
        
        return success_count, failure_count
    
    def list_downloaded_models(self):
        """List all downloaded models"""
        print(f"\n{Colors.OKCYAN}Step 3: Verifying Downloaded Models...{Colors.ENDC}\n")
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"{Colors.OKGREEN}Downloaded Models:{Colors.ENDC}")
                print(result.stdout)
            else:
                print(f"{Colors.WARNING}Could not list models{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.WARNING}Could not verify models: {e}{Colors.ENDC}")
    
    def print_completion_summary(self, success: int, failure: int):
        """Print completion summary"""
        print(f"\n{Colors.HEADER}{'═' * 40}{Colors.ENDC}")
        print(f"{Colors.BOLD}Installation Summary:{Colors.ENDC}")
        print(f"  {Colors.OKGREEN}✓ Successful: {success}{Colors.ENDC}")
        print(f"  {Colors.FAIL}✗ Failed: {failure}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'═' * 40}{Colors.ENDC}\n")
        
        print(f"{Colors.OKGREEN}{Colors.BOLD}✅ Installation Complete!{Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}🚀 Next Steps:{Colors.ENDC}")
        print(f"  1. Open Command Prompt or PowerShell")
        print(f"  2. Run a model with: {Colors.BOLD}ollama run llama2{Colors.ENDC}")
        print(f"  3. Or start the API server: {Colors.BOLD}ollama serve{Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}📚 Resources:{Colors.ENDC}")
        print(f"  • Ollama Docs: https://ollama.ai")
        print(f"  • Model Library: https://ollama.ai/library")
        print(f"  • API Reference: https://github.com/ollama/ollama/blob/main/docs/api.md\n")
        print(f"{Colors.OKBLUE}💾 Models stored in: {self.model_path}{Colors.ENDC}\n")
    
    def run(self):
        """Run the complete installation process"""
        self.print_header()
        
        # Check system
        if self.system != "Windows":
            print(f"{Colors.WARNING}⚠ This installer is optimized for Windows{Colors.ENDC}\n")
        
        # Step 1: Install Ollama
        if not self.install_ollama():
            sys.exit(1)
        
        # Step 2: Download models
        success, failure = self.download_models()
        
        # Step 3: Verify
        self.list_downloaded_models()
        
        # Summary
        self.print_completion_summary(success, failure)
        
        # Option to run a model
        try:
            response = input(f"{Colors.OKCYAN}Would you like to run a model now? (y/n): {Colors.ENDC}").strip().lower()
            if response == 'y':
                print(f"\n{Colors.OKBLUE}Available models:{Colors.ENDC}")
                for i, model in enumerate(self.models[:5], 1):
                    print(f"  {i}. {model['name']}")
                
                choice = input(f"\n{Colors.OKCYAN}Enter model name or number (or press Enter to skip): {Colors.ENDC}").strip()
                
                if choice.isdigit() and 1 <= int(choice) <= len(self.models):
                    model_name = self.models[int(choice)-1]['name']
                elif choice:
                    model_name = choice
                else:
                    return
                
                print(f"\n{Colors.OKCYAN}Starting: {model_name}{Colors.ENDC}\n")
                subprocess.run(["ollama", "run", model_name])
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Installation complete!{Colors.ENDC}\n")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automatically install free LLMs on Windows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install_llms.py
  python install_llms.py --model-path "D:/LLM_Models"
  python install_llms.py --skip-models
        """
    )
    
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Custom path to store downloaded models"
    )
    
    parser.add_argument(
        "--skip-models",
        action="store_true",
        help="Skip model downloads (only install Ollama)"
    )
    
    args = parser.parse_args()
    
    installer = LLMInstaller(model_path=args.model_path)
    installer.run()

if __name__ == "__main__":
    main()
