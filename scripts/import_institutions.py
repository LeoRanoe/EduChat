"""
Import institutions data from JSON to Supabase database.

This script reads the institutions.json file and imports the data into the
Supabase institutions and studies tables.

Usage:
    python scripts/import_institutions.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from educhat.services.supabase_client import get_service
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_json_data() -> Dict[str, Any]:
    """Load institutions data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "institutions.json"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def transform_institution(inst: Dict[str, Any]) -> Dict[str, Any]:
    """Transform JSON institution data to database format.
    
    Args:
        inst: Institution data from JSON
        
    Returns:
        Transformed data ready for database insertion
    """
    return {
        'short_name': inst.get('id'),  # Use JSON id as short_name
        'name': inst.get('name'),
        'description': inst.get('description'),
        'location': inst.get('location'),
        'website': inst.get('website'),
        'contact': inst.get('contact'),  # JSONB field
        'enrollment_process': f"Requirements: {inst.get('requirements', 'N/A')}\nAdmission Period: {inst.get('admission_period', 'N/A')}"
    }


def create_studies_from_programs(
    institution_id: str, 
    programs: List[str], 
    institution_type: str,
    admission: str
) -> List[Dict[str, Any]]:
    """Create study records from program list.
    
    Args:
        institution_id: UUID of the institution
        programs: List of program names
        institution_type: Type of institution
        admission: Admission requirements
        
    Returns:
        List of study dictionaries ready for insertion
    """
    studies = []
    
    # Determine study type based on institution type
    type_mapping = {
        'university': 'Bachelor/Master',
        'polytechnic': 'HBO',
        'technical': 'MBO',
        'business_school': 'HBO',
        'teacher_training': 'HBO',
        'art_academy': 'HBO',
        'specialized': 'HBO',
        'secondary_vocational': 'MBO',
        'agricultural': 'MBO',
        'nursing': 'HBO/MBO'
    }
    
    study_type = type_mapping.get(institution_type, 'Onbekend')
    
    for program in programs:
        studies.append({
            'institution_id': institution_id,
            'title': program,
            'type': study_type,
            'admission': admission,
            'source': 'institutions.json'
        })
    
    return studies


def import_data():
    """Main import function."""
    print("🚀 Starting data import...")
    
    # Load JSON data
    print("📖 Loading institutions.json...")
    data = load_json_data()
    institutions_data = data.get('institutions', [])
    print(f"   Found {len(institutions_data)} institutions in JSON")
    
    # Get database service
    print("🔌 Connecting to Supabase...")
    db = get_service()
    
    # Check if data already exists
    print("🔍 Checking existing data...")
    existing = db.get_all_institutions()
    
    if existing:
        print(f"⚠️  Warning: Found {len(existing)} existing institutions in database")
        response = input("   Delete existing data and reimport? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Import cancelled")
            return
        
        # Delete existing institutions (CASCADE will delete studies)
        print("🗑️  Deleting existing data...")
        for inst in existing:
            db.client.table('institutions').delete().eq('id', inst['id']).execute()
        print("   Existing data deleted")
    
    # Import institutions and studies
    imported_count = 0
    studies_count = 0
    
    for inst_data in institutions_data:
        try:
            # Transform and insert institution
            inst_db = transform_institution(inst_data)
            print(f"\n📝 Importing: {inst_db['name']}")
            
            response = db.client.table('institutions').insert(inst_db).execute()
            institution_id = response.data[0]['id']
            imported_count += 1
            
            # Create and insert studies from programs
            programs = inst_data.get('programs', [])
            if programs:
                studies = create_studies_from_programs(
                    institution_id,
                    programs,
                    inst_data.get('type', 'unknown'),
                    inst_data.get('requirements', 'Zie website voor toelatingseisen')
                )
                
                if studies:
                    db.client.table('studies').insert(studies).execute()
                    studies_count += len(studies)
                    print(f"   ✅ Imported {len(studies)} programs")
            
        except Exception as e:
            print(f"   ❌ Error importing {inst_data.get('name', 'unknown')}: {e}")
            continue
    
    print(f"\n✨ Import complete!")
    print(f"   📚 {imported_count} institutions imported")
    print(f"   🎓 {studies_count} programs imported")
    
    # Test search
    print("\n🧪 Testing search...")
    results = db.search_institutions("Universiteit")
    print(f"   Search for 'Universiteit': {len(results)} results")
    
    if results:
        print(f"   Sample: {results[0]['name']}")


if __name__ == '__main__':
    try:
        import_data()
    except KeyboardInterrupt:
        print("\n❌ Import cancelled by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
