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
        """Search institutions by name, type, or programs with strict relevance filtering.
        
        Args:
            query: Search query string.
            
        Returns:
            List of matching institutions, sorted by relevance.
        """
        self.load_data()
        
        if not query:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Remove common stop words for better matching
        stop_words = {'de', 'het', 'een', 'van', 'in', 'op', 'met', 'voor', 'is', 'en', 'te', 'naar', 'om', 'wat', 'hoe', 'welke', 'waar', 'ik', 'je', 'wil', 'kan', 'graag', 'over', 'mij', 'meer'}
        query_words = query_words - stop_words
        
        results = []
        
        for inst in self._data.get('institutions', []):
            relevance_score = 0
            match_type = None
            
            inst_name_lower = inst.get('name', '').lower()
            inst_type_lower = inst.get('type', '').lower()
            inst_desc_lower = inst.get('description', '').lower()
            
            # Exact name match (highest priority)
            if query_lower in inst_name_lower or inst_name_lower in query_lower:
                relevance_score = 10
                match_type = 'name_exact'
            # ID match
            elif query_lower == inst.get('id', '').lower():
                relevance_score = 10
                match_type = 'id_exact'
            # Partial name match
            elif any(word in inst_name_lower for word in query_words if len(word) > 2):
                matching_words = sum(1 for word in query_words if word in inst_name_lower and len(word) > 2)
                relevance_score = min(8, 4 + matching_words)
                match_type = 'name_partial'
            # Type match
            elif any(word in inst_type_lower for word in query_words if len(word) > 2):
                relevance_score = 5
                match_type = 'type'
            # Program match
            else:
                programs = inst.get('programs', [])
                program_text = ' '.join(programs).lower()
                matching_programs = sum(1 for word in query_words if word in program_text and len(word) > 3)
                if matching_programs > 0:
                    relevance_score = min(6, 3 + matching_programs)
                    match_type = 'program'
                # Description match (lowest priority)
                elif any(word in inst_desc_lower for word in query_words if len(word) > 3):
                    matching_words = sum(1 for word in query_words if word in inst_desc_lower and len(word) > 3)
                    if matching_words >= 2:  # Require at least 2 matching words for description
                        relevance_score = min(4, 2 + matching_words)
                        match_type = 'description'
            
            if relevance_score > 0:
                results.append({
                    **inst,
                    '_relevance_score': relevance_score,
                    '_match_type': match_type
                })
        
        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
        
        # Filter out low relevance matches if we have high relevance ones
        if results and results[0].get('_relevance_score', 0) >= 8:
            # Keep only high relevance matches
            results = [r for r in results if r.get('_relevance_score', 0) >= 5]
        
        # Clean up internal fields before returning
        for r in results:
            r.pop('_relevance_score', None)
            r.pop('_match_type', None)
        
        # Also search Supabase if enabled and local results are insufficient
        if self._use_supabase and len(results) < 2:
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
    
    def _calculate_relevance_score(self, query: str, text: str) -> int:
        """Calculate relevance score between query and text.
        
        Args:
            query: User query
            text: Text to check relevance against
            
        Returns:
            Relevance score from 0-10
        """
        if not query or not text:
            return 0
        
        query_words = set(query.lower().split())
        text_lower = text.lower()
        
        # Remove common stop words
        stop_words = {'de', 'het', 'een', 'van', 'in', 'op', 'met', 'voor', 'is', 'en', 'te', 'naar', 'om', 'wat', 'hoe', 'welke', 'waar', 'ik', 'je', 'wil', 'kan', 'graag'}
        query_words = query_words - stop_words
        
        if not query_words:
            return 0
        
        # Count matching words
        matches = sum(1 for word in query_words if word in text_lower)
        
        # Calculate score
        score = min(10, int((matches / len(query_words)) * 10))
        
        return score
    
    def _extract_query_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract named entities and key concepts from query.
        
        Args:
            query: User query
            
        Returns:
            Dictionary with entity types and their values
        """
        query_lower = query.lower()
        entities = {
            'institutions': [],
            'programs': [],
            'topics': []
        }
        
        # Institution name patterns
        institution_patterns = {
            'adekus': ['adekus', 'anton de kom', 'universiteit', 'uvs'],
            'iob': ['iob', 'opleiding van leraren', 'lerarenopleiding', 'kweekschool'],
            'natin': ['natin', 'natuurtechnisch'],
            'ptc': ['ptc', 'polytechnic', 'hbo'],
            'ahkco': ['ahkco', 'kunstacademie', 'kunst en cultuur'],
            'fhi': ['fhi', 'business school']
        }
        
        for inst_id, patterns in institution_patterns.items():
            if any(p in query_lower for p in patterns):
                entities['institutions'].append(inst_id)
        
        # Topic detection
        topic_patterns = {
            'admission': ['toelating', 'inschrijv', 'aanmeld', 'requirements', 'vereisten', 'hoe schrijf'],
            'programs': ['opleiding', 'studie', 'programma', 'richting', 'faculteit'],
            'dates': ['deadline', 'datum', 'wanneer', 'periode'],
            'costs': ['kosten', 'geld', 'betalen', 'financier', 'beurs'],
            'contact': ['contact', 'adres', 'telefoon', 'email', 'website'],
            'education_system': ['onderwijs', 'systeem', 'niveau', 'mulo', 'vwo', 'havo']
        }
        
        for topic, patterns in topic_patterns.items():
            if any(p in query_lower for p in patterns):
                entities['topics'].append(topic)
        
        return entities
    
    def get_context_for_query(self, user_query: str) -> tuple:
        """Generate strictly relevant context for an AI query.
        
        This method analyzes the user's query and returns ONLY relevant
        education data to inject into the AI prompt. It maintains context
        integrity and prevents mixing of unrelated data.
        
        Args:
            user_query: The user's question.
            
        Returns:
            Tuple of (context_string, relevance_score, matched_entities)
        """
        self.load_data()
        
        context_parts = []
        matched_entities = []
        total_relevance = 0
        query_lower = user_query.lower()
        
        # Extract entities from query for focused retrieval
        entities = self._extract_query_entities(user_query)
        
        # Determine if query is about general system vs specific institutions
        is_system_query = 'education_system' in entities['topics']
        is_institution_query = bool(entities['institutions'])
        
        # =====================================================================
        # INSTITUTION-SPECIFIC QUERIES (highest priority - most precise)
        # =====================================================================
        if is_institution_query:
            # User asked about specific institution(s) - ONLY return those
            for inst_id in entities['institutions']:
                inst = self.get_institution_by_id(inst_id)
                if inst:
                    matched_entities.append(inst['name'])
                    relevance = self._calculate_relevance_score(user_query, inst.get('description', '') + ' ' + inst.get('name', ''))
                    total_relevance = max(total_relevance, relevance)
                    
                    context_parts.append(f"\n=== {inst['name'].upper()} (EXACTE MATCH) ===")
                    context_parts.append(f"Type: {inst.get('type', 'N/A')}")
                    context_parts.append(f"Locatie: {inst.get('location', 'N/A')}")
                    context_parts.append(f"Beschrijving: {inst.get('description', 'N/A')}")
                    
                    # Only include relevant sections based on query topics
                    if 'programs' in entities['topics'] or not entities['topics']:
                        if inst.get('programs'):
                            context_parts.append(f"Opleidingen: {', '.join(inst['programs'])}")
                    
                    if 'admission' in entities['topics'] or not entities['topics']:
                        if inst.get('requirements'):
                            context_parts.append(f"Toelatingseisen: {inst['requirements']}")
                        if inst.get('admission_period'):
                            context_parts.append(f"Inschrijvingsperiode: {inst['admission_period']}")
                    
                    if 'contact' in entities['topics'] or not entities['topics']:
                        contact = inst.get('contact', {})
                        if contact:
                            context_parts.append("Contactgegevens:")
                            if contact.get('phone'):
                                context_parts.append(f"  Telefoon: {contact['phone']}")
                            if contact.get('email'):
                                context_parts.append(f"  Email: {contact['email']}")
                            if contact.get('address'):
                                context_parts.append(f"  Adres: {contact['address']}")
                    
                    if inst.get('website'):
                        context_parts.append(f"Website: {inst['website']}")
        
        # If no specific institution matched and NOT a system-level query, try broader search
        elif not is_institution_query and not is_system_query:
            # Search institutions but require high relevance
            institutions = self.search_institutions(user_query)
            
            # Filter by relevance score
            relevant_institutions = []
            for inst in institutions:
                score = self._calculate_relevance_score(
                    user_query, 
                    f"{inst.get('name', '')} {inst.get('description', '')} {' '.join(inst.get('programs', []))}"
                )
                if score >= 3:  # Minimum relevance threshold
                    relevant_institutions.append((inst, score))
            
            # Sort by relevance and take only top match to avoid mixing
            relevant_institutions.sort(key=lambda x: x[1], reverse=True)
            
            if relevant_institutions:
                # Only return the MOST relevant institution to prevent mixing
                inst, score = relevant_institutions[0]
                total_relevance = max(total_relevance, score)
                matched_entities.append(inst['name'])
                
                context_parts.append(f"\n=== {inst['name'].upper()} (BESTE MATCH - relevantie {score}/10) ===")
                context_parts.append(f"Type: {inst.get('type', 'N/A')}")
                context_parts.append(f"Locatie: {inst.get('location', 'N/A')}")
                context_parts.append(f"Beschrijving: {inst.get('description', 'N/A')}")
                
                if inst.get('programs'):
                    context_parts.append(f"Opleidingen: {', '.join(inst['programs'])}")
                if inst.get('requirements'):
                    context_parts.append(f"Toelatingseisen: {inst['requirements']}")
                if inst.get('admission_period'):
                    context_parts.append(f"Inschrijvingsperiode: {inst['admission_period']}")
        
        # =====================================================================
        # EDUCATION SYSTEM QUERIES (only if specifically asked)
        # =====================================================================
        if 'education_system' in entities['topics']:
            edu_system = self.get_education_system_info()
            if edu_system:
                matched_entities.append("Onderwijssysteem Suriname")
                total_relevance = max(total_relevance, 7)
                
                context_parts.append("\n=== ONDERWIJSSYSTEEM SURINAME ===")
                
                # Primary
                primary = edu_system.get('primary', {})
                if primary:
                    context_parts.append(f"Basisonderwijs ({primary.get('name', 'GLO')}): Duur {primary.get('duration', '6 jaar')}, Leeftijd {primary.get('age_range', '6-12 jaar')}")
                
                # Secondary Junior
                sec_junior = edu_system.get('secondary_junior', {})
                if sec_junior:
                    context_parts.append(f"{sec_junior.get('name', 'VOJ')}:")
                    for t in sec_junior.get('types', []):
                        context_parts.append(f"  - {t['name']}: {t.get('description', '')}")
                
                # Secondary Senior
                sec_senior = edu_system.get('secondary_senior', {})
                if sec_senior:
                    context_parts.append(f"{sec_senior.get('name', 'VOS')}:")
                    for t in sec_senior.get('types', []):
                        context_parts.append(f"  - {t['name']}: {t.get('description', '')}")
        
        # =====================================================================
        # DATE QUERIES (only if specifically asked about dates/deadlines)
        # =====================================================================
        if 'dates' in entities['topics']:
            dates = self.get_important_dates()
            if dates:
                matched_entities.append("Belangrijke Data")
                total_relevance = max(total_relevance, 6)
                
                context_parts.append("\n=== BELANGRIJKE DATA (controleer actualiteit!) ===")
                
                app_periods = dates.get('application_periods', {})
                if app_periods:
                    context_parts.append("Inschrijvingsperiodes:")
                    for level, period in app_periods.items():
                        context_parts.append(f"  - {level.upper()}: {period}")
                
                exam_periods = dates.get('exam_periods', {})
                if exam_periods:
                    context_parts.append("Examenperiodes:")
                    for exam, period in exam_periods.items():
                        context_parts.append(f"  - {exam.replace('_', ' ').title()}: {period}")
        
        # =====================================================================
        # MINISTRY QUERIES (only if specifically about MINOV)
        # =====================================================================
        minov_specific = any(kw in query_lower for kw in ['minov', 'ministerie van onderwijs'])
        if minov_specific:
            ministry = self.get_ministry_info()
            if ministry:
                matched_entities.append("MINOV")
                total_relevance = max(total_relevance, 8)
                
                context_parts.append("\n=== MINISTERIE VAN ONDERWIJS (MINOV) ===")
                context_parts.append(f"Naam: {ministry.get('name', '')}")
                context_parts.append(f"Beschrijving: {ministry.get('description', '')}")
                if ministry.get('responsibilities'):
                    context_parts.append(f"Verantwoordelijkheden: {', '.join(ministry['responsibilities'])}")
        
        # Return context with metadata
        if context_parts:
            context_string = "\n".join(context_parts)
            return (context_string, total_relevance, matched_entities)
        
        return ("", 0, [])


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
