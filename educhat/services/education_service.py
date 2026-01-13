"""Education data service for EduChat.

This service loads and queries Surinamese education data from the local JSON file
and optionally from Supabase database. It provides relevant context to the AI 
for answering education questions.
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path


class EducationDataService:
    """Service for loading and querying education data."""
    
    def __init__(self, use_supabase: bool = True):
        """Initialize the education data service.
        
        Args:
            use_supabase: Whether to also query Supabase for data.
        """
        self._data: Dict = {}
        self._loaded = False
        self._use_supabase = use_supabase
        self._supabase_institutions: List[Dict] = []
        self._supabase_loaded = False
    
    def _get_data_path(self) -> Path:
        """Get the path to the institutions.json file."""
        # Get the path relative to this file's location
        current_dir = Path(__file__).parent.parent.parent  # educhat/services -> educhat -> EduChat
        return current_dir / "data" / "institutions.json"
    
    def _load_supabase_data(self) -> bool:
        """Load institutions and studies from Supabase.
        
        Returns:
            True if data loaded successfully, False otherwise.
        """
        if self._supabase_loaded or not self._use_supabase:
            return self._supabase_loaded
        
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            
            # Load institutions with studies
            self._supabase_institutions = db.get_all_institutions(include_studies=True)
            self._supabase_loaded = True
            print(f"Loaded {len(self._supabase_institutions)} institutions from Supabase")
            return True
        
        except Exception as e:
            print(f"Error loading from Supabase: {e}")
            self._supabase_loaded = False
            return False
    
    def load_data(self) -> bool:
        """Load education data from JSON file.
        
        Returns:
            True if data loaded successfully, False otherwise.
        """
        if self._loaded:
            return True
        
        try:
            data_path = self._get_data_path()
            if not data_path.exists():
                print(f"Education data file not found: {data_path}")
                return False
            
            with open(data_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            
            self._loaded = True
            print(f"Loaded education data: {len(self._data.get('institutions', []))} institutions")
            return True
        
        except Exception as e:
            print(f"Error loading education data: {e}")
            return False
    
    def get_all_institutions(self) -> List[Dict]:
        """Get all institutions from both local JSON and Supabase.
        
        Returns:
            List of all institution dictionaries.
        """
        self.load_data()
        
        # Combine local and Supabase data
        local_institutions = self._data.get('institutions', [])
        
        # Try to load from Supabase
        self._load_supabase_data()
        
        # Merge, avoiding duplicates by id
        all_institutions = list(local_institutions)
        local_ids = {inst.get('id') for inst in local_institutions}
        
        for inst in self._supabase_institutions:
            if inst.get('id') not in local_ids:
                all_institutions.append(inst)
        
        return all_institutions
    
    def search_institutions_supabase(self, query: str) -> List[Dict]:
        """Search institutions in Supabase database.
        
        Args:
            query: Search query string.
            
        Returns:
            List of matching institutions from Supabase.
        """
        if not self._use_supabase:
            return []
        
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            return db.search_institutions(query)
        except Exception as e:
            print(f"Error searching Supabase: {e}")
            return []
    
    def search_institutions(self, query: str) -> List[Dict]:
        """Search institutions by name, type, or programs.
        
        Args:
            query: Search query string.
            
        Returns:
            List of matching institutions.
        """
        self.load_data()
        
        if not query:
            return []
        
        query_lower = query.lower()
        results = []
        
        for inst in self._data.get('institutions', []):
            # Check name
            if query_lower in inst.get('name', '').lower():
                results.append(inst)
                continue
            
            # Check type
            if query_lower in inst.get('type', '').lower():
                results.append(inst)
                continue
            
            # Check programs
            programs = inst.get('programs', [])
            for program in programs:
                if query_lower in program.lower():
                    results.append(inst)
                    break
            
            # Check description
            if query_lower in inst.get('description', '').lower():
                results.append(inst)
                continue
        
        # Also search Supabase if enabled
        if self._use_supabase and len(results) < 5:
            supabase_results = self.search_institutions_supabase(query)
            # Avoid duplicates
            result_ids = {r.get('id') for r in results}
            for r in supabase_results:
                if r.get('id') not in result_ids:
                    results.append(r)
        
        return results
    
    def get_institution_by_id(self, institution_id: str) -> Optional[Dict]:
        """Get a specific institution by ID.
        
        Args:
            institution_id: Institution ID (e.g., 'adekus').
            
        Returns:
            Institution dictionary or None if not found.
        """
        self.load_data()
        
        for inst in self._data.get('institutions', []):
            if inst.get('id') == institution_id:
                return inst
        
        return None
    
    def get_programs_for_institution(self, institution_id: str) -> List[str]:
        """Get list of programs for an institution.
        
        Args:
            institution_id: Institution ID.
            
        Returns:
            List of program names.
        """
        inst = self.get_institution_by_id(institution_id)
        if inst:
            return inst.get('programs', [])
        return []
    
    def get_education_system_info(self) -> Dict:
        """Get information about the Surinamese education system.
        
        Returns:
            Dictionary with education system structure.
        """
        self.load_data()
        return self._data.get('education_system', {})
    
    def get_important_dates(self) -> Dict:
        """Get important dates for education.
        
        Returns:
            Dictionary with important dates.
        """
        self.load_data()
        return self._data.get('important_dates', {})
    
    def get_ministry_info(self) -> Dict:
        """Get MINOV ministry information.
        
        Returns:
            Dictionary with ministry info.
        """
        self.load_data()
        return self._data.get('ministry', {})
    
    def get_context_for_query(self, user_query: str) -> str:
        """Generate relevant context for an AI query.
        
        This method analyzes the user's query and returns relevant
        education data to inject into the AI prompt.
        
        Args:
            user_query: The user's question.
            
        Returns:
            Formatted context string for AI prompt.
        """
        self.load_data()
        
        context_parts = []
        query_lower = user_query.lower()
        
        # Check for institution-specific queries
        institutions = self.search_institutions(user_query)
        if institutions:
            context_parts.append("=== RELEVANTE INSTELLINGEN ===")
            for inst in institutions[:3]:  # Limit to top 3
                context_parts.append(f"\n📚 {inst['name']}")
                context_parts.append(f"   Type: {inst.get('type', 'N/A')}")
                context_parts.append(f"   Locatie: {inst.get('location', 'N/A')}")
                context_parts.append(f"   {inst.get('description', '')}")
                if inst.get('programs'):
                    context_parts.append(f"   Opleidingen: {', '.join(inst['programs'][:5])}")
                if inst.get('requirements'):
                    context_parts.append(f"   Toelatingseisen: {inst['requirements']}")
                if inst.get('admission_period'):
                    context_parts.append(f"   Inschrijvingsperiode: {inst['admission_period']}")
        
        # Check for education system queries
        edu_keywords = ['onderwijs', 'systeem', 'school', 'niveau', 'mulo', 'vwo', 'havo', 'hbo', 'wo']
        if any(kw in query_lower for kw in edu_keywords):
            edu_system = self.get_education_system_info()
            if edu_system:
                context_parts.append("\n=== ONDERWIJSSYSTEEM SURINAME ===")
                
                # Primary
                primary = edu_system.get('primary', {})
                if primary:
                    context_parts.append(f"\n🎒 Basisonderwijs: {primary.get('name', 'GLO')}")
                    context_parts.append(f"   Duur: {primary.get('duration', '6 jaar')}")
                    context_parts.append(f"   Leeftijd: {primary.get('age_range', '6-12 jaar')}")
                
                # Secondary Junior
                sec_junior = edu_system.get('secondary_junior', {})
                if sec_junior:
                    context_parts.append(f"\n📖 {sec_junior.get('name', 'VOJ')}:")
                    for t in sec_junior.get('types', []):
                        context_parts.append(f"   - {t['name']}: {t.get('description', '')}")
                
                # Secondary Senior
                sec_senior = edu_system.get('secondary_senior', {})
                if sec_senior:
                    context_parts.append(f"\n📚 {sec_senior.get('name', 'VOS')}:")
                    for t in sec_senior.get('types', []):
                        context_parts.append(f"   - {t['name']}: {t.get('description', '')}")
        
        # Check for MINOV queries
        minov_keywords = ['minov', 'ministerie', 'onderwijs']
        if any(kw in query_lower for kw in minov_keywords):
            ministry = self.get_ministry_info()
            if ministry:
                context_parts.append("\n=== MINISTERIE VAN ONDERWIJS (MINOV) ===")
                context_parts.append(f"📍 {ministry.get('name', '')}")
                context_parts.append(f"   {ministry.get('description', '')}")
                if ministry.get('responsibilities'):
                    context_parts.append(f"   Verantwoordelijkheden: {', '.join(ministry['responsibilities'][:4])}")
        
        # Check for date-related queries
        date_keywords = ['deadline', 'datum', 'wanneer', 'inschrijv', 'examen', 'aanmeld']
        if any(kw in query_lower for kw in date_keywords):
            dates = self.get_important_dates()
            if dates:
                context_parts.append("\n=== BELANGRIJKE DATA ===")
                
                app_periods = dates.get('application_periods', {})
                if app_periods:
                    context_parts.append("📅 Inschrijvingsperiodes:")
                    for level, period in app_periods.items():
                        context_parts.append(f"   - {level.upper()}: {period}")
                
                exam_periods = dates.get('exam_periods', {})
                if exam_periods:
                    context_parts.append("📝 Examenperiodes:")
                    for exam, period in exam_periods.items():
                        context_parts.append(f"   - {exam.replace('_', ' ').title()}: {period}")
        
        if context_parts:
            return "\n".join(context_parts)
        
        return ""


# Singleton instance
_education_service = None


def get_education_service() -> EducationDataService:
    """Get the singleton education data service instance.
    
    Returns:
        EducationDataService instance.
    """
    global _education_service
    if _education_service is None:
        _education_service = EducationDataService()
    return _education_service
