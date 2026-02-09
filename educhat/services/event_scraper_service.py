"""Event Scraper Service for EduChat.

This service uses AI to scrape and extract educational events from various sources:
- Institution websites
- Social media posts
- News articles
- Official announcements
- Email notifications

Features:
- Response caching (12-hour TTL by default)
- Rate limiting (max 3 requests per second)
- Retry logic with exponential backoff
- Expanded Surinamese education sources

The scraped events are then added to Google Calendar automatically.
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
import re
import json
import hashlib
from functools import lru_cache
import time


# Simple in-memory cache for scraped content
_scrape_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_HOURS = 12


class RateLimiter:
    """Simple rate limiter for scraping requests."""
    
    def __init__(self, max_requests_per_second: float = 3.0):
        self.min_interval = 1.0 / max_requests_per_second
        self.last_request_time = 0.0
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Wait if necessary to respect rate limit."""
        async with self._lock:
            now = time.time()
            time_since_last = now - self.last_request_time
            if time_since_last < self.min_interval:
                await asyncio.sleep(self.min_interval - time_since_last)
            self.last_request_time = time.time()


class EventScraperService:
    """Service for scraping educational events using AI."""
    
    # Expanded sources for Surinamese educational events
    DEFAULT_SOURCES = [
        # Universities
        {
            'name': 'AdeKUS Website',
            'url': 'https://www.adekus.sr',
            'type': 'university',
            'institution': 'Anton de Kom Universiteit',
        },
        # Ministry
        {
            'name': 'MINOV Website',
            'url': 'https://www.minovsr.org',
            'type': 'ministry',
            'institution': 'Ministerie van Onderwijs',
        },
        # Higher education institutions
        {
            'name': 'COVAB Website',
            'url': 'https://www.covab.sr',
            'type': 'vocational',
            'institution': 'COVAB',
        },
        {
            'name': 'IMEAO Website',
            'url': 'https://www.imeao.sr',
            'type': 'vocational',
            'institution': 'IMEAO',
        },
        # Secondary schools (add major schools)
        {
            'name': 'NATIN Website',
            'url': 'https://www.natin.sr',
            'type': 'secondary',
            'institution': 'NATIN',
        },
        # Government education portals
        {
            'name': 'Studielink Suriname',
            'url': 'https://www.studielink.sr',
            'type': 'portal',
            'institution': 'Studielink',
        },
        # Scholarship organizations
        {
            'name': 'SOB Website',
            'url': 'https://www.sob.sr',
            'type': 'scholarship',
            'institution': 'Stichting Onderwijs Beurs',
        },
        # Professional education
        {
            'name': 'IOL Website',
            'url': 'https://www.iol.sr',
            'type': 'professional',
            'institution': 'IOL',
        },
    ]
    
    def __init__(self, ai_service=None, cache_ttl_hours: int = 12, rate_limit: float = 3.0):
        """Initialize the event scraper service.
        
        Args:
            ai_service: AI service instance for extracting event data from text
            cache_ttl_hours: Cache time-to-live in hours
            rate_limit: Maximum requests per second
        """
        self.ai_service = ai_service
        self.session = None
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.rate_limiter = RateLimiter(rate_limit)
        self.max_retries = 3
        self.base_delay = 1.0  # seconds
        self.max_content_length = 15000  # Increased from 8000
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            headers = {
                'User-Agent': 'EduChat/1.0 (Educational Event Scraper)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'nl,en;q=0.5',
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self.session
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def _get_cache_key(self, url: str) -> str:
        """Generate cache key for a URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_entry: Dict) -> bool:
        """Check if a cache entry is still valid."""
        if not cache_entry:
            return False
        cached_at = cache_entry.get('cached_at')
        if not cached_at:
            return False
        return datetime.now() - cached_at < self.cache_ttl
    
    def _get_from_cache(self, url: str) -> Optional[str]:
        """Get content from cache if valid."""
        cache_key = self._get_cache_key(url)
        cache_entry = _scrape_cache.get(cache_key)
        if self._is_cache_valid(cache_entry):
            print(f"Cache hit for {url}")
            return cache_entry.get('content')
        return None
    
    def _store_in_cache(self, url: str, content: str):
        """Store content in cache."""
        cache_key = self._get_cache_key(url)
        _scrape_cache[cache_key] = {
            'content': content,
            'cached_at': datetime.now(),
        }
    
    def clear_cache(self):
        """Clear the scrape cache."""
        global _scrape_cache
        _scrape_cache = {}
        print("Scrape cache cleared")
    
    async def scrape_url(self, url: str) -> Optional[str]:
        """Scrape content from a URL with caching and rate limiting.
        
        Args:
            url: URL to scrape
        
        Returns:
            Page content as text or None if error
        """
        # Check cache first
        cached = self._get_from_cache(url)
        if cached:
            return cached
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(self.max_retries):
            try:
                session = await self._get_session()
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Parse with BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Remove script, style, nav, footer, and other non-content elements
                        for element in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript"]):
                            element.decompose()
                        
                        # Try to find main content area
                        main_content = soup.find('main') or soup.find('article') or soup.find('div', {'class': re.compile(r'content|main|body', re.I)})
                        if main_content:
                            text = main_content.get_text()
                        else:
                            text = soup.get_text()
                        
                        # Clean up text
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        # Store in cache
                        self._store_in_cache(url, text)
                        
                        return text
                    elif response.status == 429:
                        # Rate limited by server
                        retry_after = int(response.headers.get('Retry-After', 5))
                        print(f"Rate limited by {url}, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    elif response.status in [500, 502, 503, 504]:
                        # Server error, retry
                        delay = self.base_delay * (2 ** attempt)
                        print(f"Server error {response.status} from {url}, retrying in {delay}s")
                        await asyncio.sleep(delay)
                        continue
                    else:
                        print(f"Error scraping {url}: HTTP {response.status}")
                        return None
                        
            except asyncio.TimeoutError:
                last_error = "Timeout"
                delay = self.base_delay * (2 ** attempt)
                print(f"Timeout scraping {url}, retrying in {delay}s (attempt {attempt + 1}/{self.max_retries})")
                await asyncio.sleep(delay)
            except aiohttp.ClientError as e:
                last_error = str(e)
                delay = self.base_delay * (2 ** attempt)
                print(f"Client error scraping {url}: {e}, retrying in {delay}s")
                await asyncio.sleep(delay)
            except Exception as e:
                last_error = str(e)
                print(f"Unexpected error scraping {url}: {e}")
                break
        
        print(f"Failed to scrape {url} after {self.max_retries} attempts: {last_error}")
        return None
    
    async def extract_events_with_ai(
        self, 
        content: str, 
        source_name: str,
        institution_name: str = ""
    ) -> List[Dict]:
        """Use AI to extract events from scraped content.
        
        Args:
            content: Scraped text content
            source_name: Name of the source
            institution_name: Name of the institution (if known)
        
        Returns:
            List of extracted event dictionaries
        """
        if not self.ai_service:
            print("AI service not available for event extraction")
            return []
        
        # Truncate content to avoid token limits (increased limit)
        if len(content) > self.max_content_length:
            content = content[:self.max_content_length]
        
        # Get current date for reference
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_year = datetime.now().year
        
        prompt = f"""Je bent een AI-assistent die belangrijke educatieve evenementen extraheert uit tekst.

Huidige datum: {current_date}

Analyseer de volgende tekst van {source_name} en extraheer ALLE belangrijke educatieve evenementen zoals:
- Toelating deadlines
- Inschrijvingsdata
- Tentamen periodes
- Open dagen
- Informatiesessies
- Academische kalender evenementen
- Feestdagen en vakanties
- Graduatieceremonies
- Workshops en trainingen

Geef voor elk evenement een JSON object terug met de volgende structuur:
{{
    "title": "Titel van het evenement",
    "description": "Korte beschrijving",
    "date": "YYYY-MM-DD" (beste schatting als exacte datum niet gegeven is),
    "time": "HH:MM" (indien beschikbaar, anders "00:00"),
    "location": "Locatie" (indien beschikbaar),
    "type": "deadline|exam|open_day|info_session|holiday|graduation|workshop|other",
    "institution": "{institution_name if institution_name else 'Onbekend'}",
    "importance": "high|medium|low"
}}

BELANGRIJK:
- Retourneer ALLEEN een JSON array met evenementen, geen andere tekst
- Als je geen specifieke datum vindt, schat dan gebaseerd op context
- Bij maandaanduidingen zonder jaar, gebruik {current_year} of {current_year + 1} afhankelijk van of het in de toekomst ligt
- Negeer evenementen die al voorbij zijn (voor {current_date})
- Focus op academisch belangrijke evenementen
- Als er geen evenementen zijn, retourneer een lege array: []

TEKST:
{content}

JSON ARRAY:"""

        try:
            # Get response from AI with retry logic
            for attempt in range(self.max_retries):
                try:
                    messages = [{"role": "user", "content": prompt}]
                    response = await self.ai_service.get_chat_completion_async(
                        messages=messages,
                        temperature=0.2,  # Lower temperature for more accurate extraction
                        max_tokens=3000,
                    )
                    break
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        delay = self.base_delay * (2 ** attempt)
                        print(f"AI extraction error, retrying in {delay}s: {e}")
                        await asyncio.sleep(delay)
                    else:
                        raise
            
            if not response:
                return []
            
            # Extract JSON from response
            response_text = response.strip()
            
            # Try to find JSON array in response
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                events = json.loads(json_str)
                
                # Validate and normalize events
                normalized_events = []
                for event in events:
                    if isinstance(event, dict) and 'title' in event and 'date' in event:
                        # Validate date is in the future
                        try:
                            event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                            if event_date < datetime.now() - timedelta(days=1):
                                continue  # Skip past events
                        except ValueError:
                            continue  # Skip invalid dates
                        
                        # Add source information
                        event['source'] = source_name
                        event['scraped_at'] = datetime.now().isoformat()
                        
                        # Ensure required fields exist
                        event.setdefault('description', '')
                        event.setdefault('time', '00:00')
                        event.setdefault('location', '')
                        event.setdefault('type', 'other')
                        event.setdefault('institution', institution_name or 'Onbekend')
                        event.setdefault('importance', 'medium')
                        
                        normalized_events.append(event)
                
                return normalized_events
            else:
                print(f"No JSON array found in AI response from {source_name}")
                return []
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from AI response: {e}")
            return []
        except Exception as e:
            print(f"Error extracting events with AI: {e}")
            return []
    
    async def categorize_and_enrich_events(
        self,
        events: List[Dict],
        use_gemini: bool = True
    ) -> List[Dict]:
        """Use AI to categorize and enrich scraped events with confidence scores.
        
        Args:
            events: List of event dictionaries to categorize
            use_gemini: Whether to use Google Gemini (faster) or OpenAI
        
        Returns:
            List of enriched event dictionaries with AI categorization
        """
        if not self.ai_service or not events:
            return events
        
        # Prepare events for categorization
        events_json = json.dumps(events, indent=2, ensure_ascii=False)
        
        prompt = f"""Je bent een AI-assistent die educatieve evenementen categoriseert en verrijkt.

Analyseer de volgende evenementen en voeg voor elk evenement deze extra velden toe:
- "ai_category": De beste categorie (deadline|exam|open_day|info_session|holiday|graduation|workshop|lecture|other)
- "ai_importance": Belang niveau (high|medium|low) gebaseerd op impact op studenten
- "ai_confidence": Betrouwbaarheidsscore (0.0-1.0) van de categorisatie
- "ai_required_action": Of studenten actie moeten ondernemen (true|false)
- "ai_tags": Array van relevante tags (bijv. ["inschrijving", "deadline", "bachelor"])
- "ai_summary": Zeer korte samenvatting (max 100 karakters)

CATEGORISATIE RICHTLIJNEN:
- "deadline" = Inschrijvings-, aanmeldings- of inzenddeadlines (hoge prioriteit!)
- "exam" = Tentamens, toetsen, assessments (hoge prioriteit voor studenten)
- "open_day" = Open dagen, informatiedagen, rondleidingen
- "info_session" = Voorlichtingssessies, webinars, Q&A sessies
- "holiday" = Vakanties, feestdagen, vrije dagen
- "graduation" = Graduaties, diploma-uitreikingen, ceremonies
- "workshop" = Workshops, trainingen, skillsessies
- "lecture" = Gastcolleges, lezingen, seminars
- "other" = Alles wat niet past in bovenstaande categorieën

IMPORTANCE RICHTLIJNEN:
- "high" = Deadlines, examens, verplichte events, grote impact op studie
- "medium" = Informatiesessies, optionele maar nuttige events
- "low" = Sociale events, algemene aankondigingen

CONFIDENCE RICHTLIJNEN:
- 1.0 = Zeer duidelijke categorie en datum
- 0.8-0.9 = Duidelijke categorie, datum redelijk zeker
- 0.5-0.7 = Categorie waarschijnlijk, datum geschat
- <0.5 = Onzeker over categorie of datum

Retourneer ALLEEN een JSON array met de verrijkte evenementen, geen andere tekst.

EVENEMENTEN:
{events_json}

VERRIJKTE JSON ARRAY:"""

        try:
            # Use Gemini for faster categorization if available
            if use_gemini and hasattr(self.ai_service, 'use_gemini'):
                # Temporarily switch to Gemini
                original_provider = getattr(self.ai_service, 'provider', None)
                self.ai_service.provider = 'gemini'
            
            messages = [{"role": "user", "content": prompt}]
            response = await self.ai_service.get_chat_completion_async(
                messages=messages,
                temperature=0.1,  # Very low for consistent categorization
                max_tokens=4000,
            )
            
            # Restore original provider
            if use_gemini and hasattr(self.ai_service, 'use_gemini'):
                if original_provider:
                    self.ai_service.provider = original_provider
            
            if not response:
                return events
            
            # Extract JSON from response
            response_text = response.strip()
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                enriched_events = json.loads(json_str)
                
                # Merge with original events (in case AI missed some fields)
                result = []
                for i, enriched in enumerate(enriched_events):
                    if i < len(events):
                        original = events[i].copy()
                        original.update(enriched)
                        
                        # Ensure all AI fields exist
                        original.setdefault('ai_category', original.get('type', 'other'))
                        original.setdefault('ai_importance', original.get('importance', 'medium'))
                        original.setdefault('ai_confidence', 0.7)
                        original.setdefault('ai_required_action', original.get('type') in ['deadline', 'exam'])
                        original.setdefault('ai_tags', [])
                        original.setdefault('ai_summary', original.get('title', '')[:100])
                        
                        result.append(original)
                
                print(f"AI categorized {len(result)} events with average confidence: {sum(e.get('ai_confidence', 0.7) for e in result) / len(result):.2f}")
                return result
            else:
                print("No JSON array found in AI categorization response")
                return events
                
        except Exception as e:
            print(f"Error categorizing events with AI: {e}")
            return events
    
    async def scrape_source(self, source: Dict) -> List[Dict]:
        """Scrape events from a single source.
        
        Args:
            source: Source dictionary with 'name', 'url', and optional 'institution'
        
        Returns:
            List of extracted events
        """
        url = source.get('url')
        name = source.get('name', url)
        institution = source.get('institution', '')
        
        print(f"Scraping events from {name}...")
        
        # Scrape content
        content = await self.scrape_url(url)
        
        if not content:
            print(f"No content retrieved from {name}")
            return []
        
        # Extract events using AI
        events = await self.extract_events_with_ai(content, name, institution)
        
        print(f"Extracted {len(events)} events from {name}")
        
        return events
    
    async def scrape_all_sources(
        self, 
        sources: Optional[List[Dict]] = None,
        user_institutions: Optional[List[str]] = None,
        max_concurrent: int = 3
    ) -> List[Dict]:
        """Scrape events from all configured sources.
        
        Args:
            sources: List of source dictionaries. If None, uses DEFAULT_SOURCES
            user_institutions: List of institution names the user is interested in
            max_concurrent: Maximum concurrent scraping tasks
        
        Returns:
            Combined list of all extracted events
        """
        if sources is None:
            sources = self.DEFAULT_SOURCES.copy()
        
        # Add user's institutions to sources if available
        if user_institutions:
            # This would normally query institution URLs from database
            # For now, we'll use the default sources
            pass
        
        # Scrape sources with limited concurrency
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_semaphore(source):
            async with semaphore:
                return await self.scrape_source(source)
        
        tasks = [scrape_with_semaphore(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine all events
        all_events = []
        successful_sources = 0
        failed_sources = 0
        
        for i, result in enumerate(results):
            if isinstance(result, list):
                all_events.extend(result)
                successful_sources += 1
            elif isinstance(result, Exception):
                print(f"Error scraping {sources[i].get('name', 'unknown')}: {result}")
                failed_sources += 1
        
        # Remove duplicates using fuzzy matching on title
        unique_events = self._deduplicate_events(all_events)
        
        print(f"Scraping complete: {successful_sources} sources successful, {failed_sources} failed")
        print(f"Total unique events: {len(unique_events)}")
        
        return unique_events
    
    def _deduplicate_events(self, events: List[Dict]) -> List[Dict]:
        """Remove duplicate events using fuzzy matching.
        
        Args:
            events: List of events
            
        Returns:
            Deduplicated list
        """
        unique_events = []
        seen_keys = set()
        
        for event in events:
            # Normalize title for comparison
            title = event.get('title', '').lower().strip()
            title_normalized = re.sub(r'[^\w\s]', '', title)  # Remove punctuation
            title_words = set(title_normalized.split())
            
            date = event.get('date', '')
            institution = event.get('institution', '').lower().strip()
            
            # Create a unique key
            key = (frozenset(title_words), date, institution)
            
            # Check for similar existing events
            is_duplicate = False
            for seen_key in seen_keys:
                seen_words, seen_date, seen_institution = seen_key
                # Check if dates match and there's significant word overlap
                if seen_date == date:
                    overlap = len(title_words & seen_words)
                    total_words = max(len(title_words), len(seen_words), 1)
                    if overlap / total_words > 0.6:  # 60% word overlap threshold
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                seen_keys.add(key)
                unique_events.append(event)
        
        return unique_events
    
    def parse_datetime(self, date_str: str, time_str: str = "00:00") -> datetime:
        """Parse date and time strings into datetime object.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            time_str: Time string in HH:MM format
        
        Returns:
            Parsed datetime object
        """
        try:
            # Combine date and time
            datetime_str = f"{date_str} {time_str}"
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            # Fallback: use date only
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                # Last resort: use current date
                return datetime.now()
    
    def prepare_events_for_calendar(self, events: List[Dict]) -> List[Dict]:
        """Prepare scraped events for Google Calendar.
        
        Args:
            events: List of scraped event dictionaries
        
        Returns:
            List of events formatted for Google Calendar service
        """
        calendar_events = []
        
        for event in events:
            # Parse datetime
            start_time = self.parse_datetime(
                event.get('date', ''),
                event.get('time', '00:00')
            )
            
            # Determine duration based on event type
            event_type = event.get('type', 'other')
            if event_type == 'deadline':
                # Deadlines are all-day events
                end_time = start_time + timedelta(hours=1)
            elif event_type in ['exam', 'open_day', 'graduation']:
                # Longer events
                end_time = start_time + timedelta(hours=3)
            elif event_type == 'workshop':
                end_time = start_time + timedelta(hours=2)
            else:
                # Default 1-hour events
                end_time = start_time + timedelta(hours=1)
            
            # Build description
            description_parts = []
            if event.get('description'):
                description_parts.append(event['description'])
            description_parts.append(f"\n📍 Bron: {event.get('source', 'Onbekend')}")
            description_parts.append(f"🏫 Instelling: {event.get('institution', 'Onbekend')}")
            description_parts.append(f"📋 Type: {event_type}")
            if event.get('importance'):
                description_parts.append(f"⚡ Prioriteit: {event['importance']}")
            
            calendar_event = {
                'summary': event.get('title', 'Educatief Evenement'),
                'description': '\n'.join(description_parts),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Amsterdam',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Amsterdam',
                },
                'location': event.get('location', ''),
                'source': {
                    'title': event.get('institution', 'EduChat'),
                    'url': event.get('link', '')
                }
            }
            calendar_events.append(calendar_event)
        
        return calendar_events


async def scrape_and_sync_events(
    ai_service,
    calendar_service,
    sources: Optional[List[Dict]] = None,
    user_institutions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Scrape events and sync them to Google Calendar.
    
    Args:
        ai_service: AI service instance
        calendar_service: Google Calendar service instance
        sources: List of sources to scrape
        user_institutions: User's institutions of interest
    
    Returns:
        Dictionary with sync results
    """
    scraper = EventScraperService(ai_service=ai_service)
    
    try:
        # Scrape events
        events = await scraper.scrape_all_sources(
            sources=sources,
            user_institutions=user_institutions
        )
        
        # Prepare for calendar
        calendar_events = scraper.prepare_events_for_calendar(events)
        
        # Sync to calendar
        if calendar_events:
            results = calendar_service.batch_create_events(calendar_events)
            return {
                'success': True,
                'scraped': len(events),
                'synced': results['success'],
                'failed': len(results['failed']),
                'events': events,
            }
        else:
            return {
                'success': True,
                'scraped': 0,
                'synced': 0,
                'failed': 0,
                'events': [],
            }
    
    finally:
        await scraper.close()


def get_event_scraper(ai_service=None) -> EventScraperService:
    """Get an event scraper service instance.
    
    Args:
        ai_service: AI service instance
    
    Returns:
        EventScraperService instance
    """
    return EventScraperService(ai_service=ai_service)
