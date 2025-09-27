#!/usr/bin/env python3

# Test script to verify the security fix works correctly

from sandbox import check_code_safety

def test_security_fix():
    # Test case 1: Code with "evaluation" should pass
    code_with_evaluation = """
import numpy as np
import matplotlib.pyplot as plt

# Human Evaluation Scores
criteria = ['Factual Correctness', 'Evidence Alignment', 'Clinical Utility']
human_evaluation = [9.2, 9.0, 9.1]
plt.bar(criteria, human_evaluation)
plt.title('Human Evaluation Results')
plt.show()
"""
    
    print("Testing code with 'evaluation' keyword...")
    is_safe, error = check_code_safety(code_with_evaluation)
    print(f"Result: {'SAFE' if is_safe else 'UNSAFE'}")
    if not is_safe:
        print(f"Error: {error}")
    print()
    
    # Test case 2: Code with actual "eval" function should fail
    code_with_eval = """
import numpy as np
result = eval("2 + 2")
print(result)
"""
    
    print("Testing code with actual 'eval()' function...")
    is_safe, error = check_code_safety(code_with_eval)
    print(f"Result: {'SAFE' if is_safe else 'UNSAFE'}")
    if not is_safe:
        print(f"Error: {error}")
    print()
    
    # Test case 3: Code with "medieval" should pass (another word containing "eval")
    code_with_medieval = """
import matplotlib.pyplot as plt
title = "Medieval Population Data"
plt.title(title)
plt.show()
"""
    
    print("Testing code with 'medieval' keyword...")
    is_safe, error = check_code_safety(code_with_medieval)
    print(f"Result: {'SAFE' if is_safe else 'UNSAFE'}")
    if not is_safe:
        print(f"Error: {error}")
    print()

if __name__ == "__main__":
    test_security_fix()
