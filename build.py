#!/usr/bin/env python3
"""
Build script for the OpenAI Cost Tracker package.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"   Removed {path}")
            else:
                path.unlink()
                print(f"   Removed {path}")

def build_package():
    """Build the package."""
    print("📦 Building package...")
    
    # Clean previous builds
    clean_build()
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return False
    
    print("✅ Package built successfully!")
    return True

def install_package():
    """Install the package in development mode."""
    print("🔧 Installing package in development mode...")
    
    if not run_command("pip install -e .", "Installing package"):
        return False
    
    print("✅ Package installed successfully!")
    return True

def test_package():
    """Test the installed package."""
    print("🧪 Testing package...")
    
    if not run_command("python test_package.py", "Running package tests"):
        return False
    
    print("✅ Package tests completed successfully!")
    return True

def main():
    """Main build process."""
    print("🚀 Starting OpenAI Cost Tracker package build process...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("setup.py").exists():
        print("❌ Error: setup.py not found. Please run this script from the package directory.")
        sys.exit(1)
    
    # Build the package
    if not build_package():
        print("❌ Build failed!")
        sys.exit(1)
    
    # Install the package
    if not install_package():
        print("❌ Installation failed!")
        sys.exit(1)
    
    # Test the package
    if not test_package():
        print("❌ Package test failed!")
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 Package build process completed successfully!")
    print("\nYou can now use the package:")
    print("  from openai_cost_tracker import CostEstimator, AsyncCostEstimator")
    print("\nTo uninstall:")
    print("  pip uninstall openai-cost-tracker")

if __name__ == "__main__":
    main()
