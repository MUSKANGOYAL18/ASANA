"""Validation utilities for checking data quality."""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

def validate_database(db_path: str):
    """Run validation checks on generated database."""
    
    print("=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    checks_passed = 0
    checks_failed = 0
    
    # Check 1: Temporal consistency - tasks
    print("\n1. Checking temporal consistency (tasks)...")
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE completed = 1 AND completed_at < created_at
    """)
    invalid_completions = cursor.fetchone()[0]
    
    if invalid_completions == 0:
        print("   ✓ PASS: All completed tasks have completed_at >= created_at")
        checks_passed += 1
    else:
        print(f"   ✗ FAIL: {invalid_completions} tasks have completed_at < created_at")
        checks_failed += 1
        
    # Check 2: Relational integrity - task assignments
    print("\n2. Checking relational integrity (task assignments)...")
    cursor.execute("""
        SELECT COUNT(*) FROM tasks t
        LEFT JOIN users u ON t.assignee_id = u.user_id
        WHERE t.assignee_id IS NOT NULL AND u.user_id IS NULL
    """)
    orphaned_assignments = cursor.fetchone()[0]
    
    if orphaned_assignments == 0:
        print("   ✓ PASS: All task assignees exist in users table")
        checks_passed += 1
    else:
        print(f"   ✗ FAIL: {orphaned_assignments} tasks assigned to non-existent users")
        checks_failed += 1
        
    # Check 3: Business logic - no "Task 1" patterns
    print("\n3. Checking for placeholder task names...")
    cursor.execute("""
        SELECT COUNT(*) FROM tasks 
        WHERE name LIKE 'Task %' AND name GLOB 'Task [0-9]*'
    """)
    placeholder_tasks = cursor.fetchone()[0]
    
    if placeholder_tasks == 0:
        print("   ✓ PASS: No placeholder task names found")
        checks_passed += 1
    else:
        print(f"   ✗ FAIL: {placeholder_tasks} tasks have placeholder names")
        checks_failed += 1
        
    # Check 4: Distribution check - task assignment rate
    print("\n4. Checking task assignment distribution...")
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE assignee_id IS NOT NULL")
    assigned = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    assignment_rate = assigned / total if total > 0 else 0
    
    if 0.80 <= assignment_rate <= 0.90:
        print(f"   ✓ PASS: Task assignment rate is {assignment_rate:.2%} (expected: 85%)")
        checks_passed += 1
    else:
        print(f"   ✗ FAIL: Task assignment rate is {assignment_rate:.2%} (expected: 85%)")
        checks_failed += 1
        
    # Check 5: Completion rate reasonableness
    print("\n5. Checking task completion distribution...")
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
    completed = cursor.fetchone()[0]
    
    completion_rate = completed / total if total > 0 else 0
    
    if 0.50 <= completion_rate <= 0.85:
        print(f"   ✓ PASS: Task completion rate is {completion_rate:.2%} (expected: 50-85%)")
        checks_passed += 1
    else:
        print(f"   ✗ FAIL: Task completion rate is {completion_rate:.2%} (expected: 50-85%)")
        checks_failed += 1
        
    # Summary
    print("\n" + "=" * 80)
    print(f"VALIDATION SUMMARY: {checks_passed} passed, {checks_failed} failed")
    print("=" * 80)
    
    conn.close()
    
    return checks_failed == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate.py <database_path>")
        sys.exit(1)
        
    db_path = sys.argv[1]
    
    if not Path(db_path).exists():
        print(f"Error: Database not found: {db_path}")
        sys.exit(1)
        
    success = validate_database(db_path)
    sys.exit(0 if success else 1)