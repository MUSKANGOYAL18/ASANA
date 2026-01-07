"""Quick test to verify setup is correct."""
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.config import Config
        print("  ✓ Config imported")
        
        from src.models.schema import Organization, User, Task
        print("  ✓ Models imported")
        
        from src.utils.database import Database
        print("  ✓ Database utils imported")
        
        from src.utils.temporal import TemporalGenerator
        print("  ✓ Temporal utils imported")
        
        from src.scrapers.company_scraper import CompanyScraper
        print("  ✓ Company scraper imported")
        
        from src.scrapers.name_generator import NameGenerator
        print("  ✓ Name generator imported")
        
        from src.generators.organization import OrganizationGenerator
        print("  ✓ Organization generator imported")
        
        from src.generators.users import UserGenerator
        print("  ✓ User generator imported")
        
        return True
        
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        'README.md',
        'requirements.txt',
        'schema.sql',
        '.env.example',
        'src/main.py',
        'src/config.py',
        'src/models/schema.py',
        'src/utils/database.py',
        'src/utils/temporal.py',
        'src/utils/llm.py',
        'src/scrapers/company_scraper.py',
        'src/scrapers/name_generator.py',
        'src/generators/organization.py',
        'src/generators/users.py',
        'src/generators/tasks.py',
        'docs/METHODOLOGY.md',
        'docs/SCHEMA_DOCUMENTATION.md',
        'prompts/task_engineering.txt',
        'prompts/task_marketing.txt',
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} NOT FOUND")
            all_exist = False
            
    return all_exist

def test_basic_generation():
    """Test basic data generation."""
    print("\nTesting basic generation...")
    
    try:
        from src.scrapers.company_scraper import CompanyScraper
        from src.scrapers.name_generator import NameGenerator
        
        # Test company scraper
        scraper = CompanyScraper(seed=42)
        company = scraper.get_company_name()
        print(f"  ✓ Generated company: {company}")
        
        # Test name generator
        name_gen = NameGenerator(seed=42)
        first, last = name_gen.generate_name()
        print(f"  ✓ Generated name: {first} {last}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Generation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("ASANA SIMULATION - SETUP TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Imports", test_imports()))
    results.append(("Basic Generation", test_basic_generation()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:.<40} {status}")
        if not passed:
            all_passed = False
            
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Setup is correct.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OPENAI_API_KEY to .env")
        print("3. Run: python src/main.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())