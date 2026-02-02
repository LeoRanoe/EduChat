# Quick Test Guide - Chatbot Improvements

## 🧪 Test the Implementation

### Prerequisites
```powershell
# Activate virtual environment
& D:/EduChat/.venv/Scripts/Activate.ps1

# Start the application
reflex run
```

---

## Test Cases

### ✅ Test 1: User Context (No Onboarding)
**Action**: Start chat as guest without completing onboarding

**Expected**:
- Context should have defaults: "Algemeen", "Volwassene", "Suriname"
- AI should still personalize responses
- No errors in console

**Test Query**: "Hoe werkt het onderwijssysteem in Suriname?"

**Check Console For**:
```
[ONBOARDING] Context set: {'education_level': 'Algemeen (nog niet gespecificeerd)', ...}
```

---

### ✅ Test 2: Dynamic Scraping (Event Query)
**Action**: Ask about an event or deadline

**Test Queries**:
- "Wanneer is de volgende open dag bij AdeKUS?"
- "Wat zijn de inschrijvingsdeadlines voor NATIN?"
- "Welke evenementen zijn er binnenkort bij IOL?"

**Expected**:
- Console shows: `[SCRAPING] Query analysis: {'should_scrape': True, 'scrape_type': 'events'...}`
- If first query: `[SCRAPING] No cache found, scraping fresh data...`
- If subsequent: `[SCRAPING] Using X cached events from database`
- Response includes specific dates/events from websites

**Check Console For**:
```
[SCRAPING] Triggering events scraping...
[SCRAPING] Added 8 events to context
```

---

### ✅ Test 3: Cache Performance
**Action**: Ask the same event query twice within 5 minutes

**First Query**: "Open dagen AdeKUS"
**Expected**: Takes 5-10 seconds (scraping)

**Second Query**: Same or similar
**Expected**: Takes <1 second (cache hit)

**Check Console For**:
```
First: [SCRAPING] No cache found, scraping fresh data...
Second: [SCRAPING] Using 8 cached events from database
```

---

### ✅ Test 4: Confident Responses (No "Don't Know")
**Action**: Ask questions about programs without exact data

**Test Queries**:
- "Hoe bereid ik me voor op een universitaire opleiding?"
- "Wat zijn algemene toelatingseisen voor technische studies?"
- "Welke vakken moet ik kiezen voor een economische richting?"

**Expected**:
- NO "Ik heb onvoldoende informatie" responses
- Instead: General guidance with transparency
- Examples: "Op basis van algemene studierichtlijnen..."

---

### ✅ Test 5: Personalization with Onboarding
**Action**: Complete onboarding with specific preferences

**Setup**:
1. Go to `/onboarding`
2. Select: HAVO, 16-18 jaar, Techniek interest
3. Complete all steps
4. Return to chat

**Test Query**: "Welke studies kan ik volgen?"

**Expected**:
- Response tailored to HAVO level
- Mentions technical programs
- Age-appropriate language
- Console shows full context with preferences

---

### ✅ Test 6: Institution Detection
**Action**: Mention specific institutions

**Test Queries**:
- "Vertel me over AdeKUS"
- "Wat biedt NATIN aan?"
- "IOL vs PTC vergelijking"

**Expected**:
- Console shows detected institutions
- May trigger institution-specific scraping
- Response includes institution-specific data

**Check Console For**:
```
[SCRAPING] Query analysis: {..., 'institutions': ['adekus', 'natin'], ...}
```

---

### ✅ Test 7: Error Handling
**Action**: Test with network issues

**Setup**: Disconnect internet briefly

**Test Query**: "Open dagen deze maand"

**Expected**:
- Console shows scraping error
- NO application crash
- Fallback to static database
- Response still helpful (from cached/static data)

**Check Console For**:
```
[SCRAPING] Error during scraping: ...
(continues without crashing)
```

---

## 🔍 Debugging Tips

### Check Context Loading
```python
# In browser console or Python terminal
# Access app state and print context
print(app_state.user_context)
```

### Check Cache Contents
```python
from educhat.services.supabase_client import get_service
db = get_service()
events = db.get_cached_scraped_events(hours=24)
print(f"Cached events: {len(events)}")
```

### Test Query Analysis
```python
from educhat.services.ai_service import get_ai_service
ai = get_ai_service()
analysis = ai.analyze_query_for_scraping("open dag adekus")
print(analysis)
```

### Clear Cache (If Needed)
```python
from educhat.services.supabase_client import get_service
db = get_service()
deleted = db.clear_old_scraped_events(days=0)  # Clear all
print(f"Deleted {deleted} events")
```

---

## 📊 Performance Benchmarks

| Query Type | Expected Response Time | Notes |
|------------|----------------------|-------|
| Static data | <500ms | From database only |
| Cached scrape | <1s | 24hr cache hit |
| Fresh scrape | 5-10s | First query or expired cache |
| General advice | <1s | No scraping needed |

---

## ✅ Success Indicators

**Onboarding Context**:
- [ ] Guest users have default context
- [ ] Authenticated users have full context
- [ ] No "None" values in context dict

**Scraping**:
- [ ] Event queries trigger scraping
- [ ] Cache is used for repeat queries
- [ ] Fresh data appears in responses
- [ ] No crashes on scraping errors

**Responses**:
- [ ] No more "Ik heb onvoldoende informatie"
- [ ] Provides general guidance when specific data missing
- [ ] Clearly distinguishes between exact data and advice
- [ ] Uses user preferences in answers

**Performance**:
- [ ] First query with scraping: 5-10s (acceptable)
- [ ] Cached queries: <1s (fast)
- [ ] No UI freezing during scraping
- [ ] Smooth typing animation maintained

---

## 🐛 Common Issues & Solutions

### Issue: "No cache found" every query
**Solution**: Check if `can_save_conversations()` returns True. Guest users won't cache to DB.

### Issue: Scraping takes too long
**Solution**: Expected for first query. Check network speed. Consider reducing scraped sources.

### Issue: Context is empty dict
**Solution**: Verify `load_onboarding_preferences()` is called in `initialize_chat()`.

### Issue: Scraping never triggers
**Solution**: Test query analysis manually. Check keyword detection in `analyze_query_for_scraping()`.

---

## 📝 Test Checklist

Copy this checklist for tracking:

```
□ Test 1: User Context (No Onboarding)
□ Test 2: Dynamic Scraping (Event Query)
□ Test 3: Cache Performance
□ Test 4: Confident Responses (No "Don't Know")
□ Test 5: Personalization with Onboarding
□ Test 6: Institution Detection
□ Test 7: Error Handling

Performance Checks:
□ Response time < 500ms (cached)
□ Response time < 10s (scraped)
□ No UI freezing
□ No console errors

Quality Checks:
□ No "onvoldoende informatie" responses
□ General advice when appropriate
□ Source transparency maintained
□ User context applied correctly
```

---

## 🎯 Expected Outcomes

After implementation, the chatbot should:
1. ✅ **Always have user context** - even for guests
2. ✅ **Scrape when needed** - fresh data for events/deadlines
3. ✅ **Use cache efficiently** - fast responses for common queries
4. ✅ **Provide helpful answers** - guidance instead of "don't know"
5. ✅ **Personalize responses** - based on user's education level/interests
6. ✅ **Handle errors gracefully** - fallback to available data

---

**Last Updated**: February 2, 2026
**Quick Start**: `reflex run` → Test queries above → Check console logs
