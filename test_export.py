"""Test script to understand Reflex export structure"""
import os
import subprocess

print("Testing reflex export...")
result = subprocess.run(["reflex", "export", "--help"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
