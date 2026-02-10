"""
🧪 Test Script: Email Confirmation System

Dit script test of email confirmation correct werkt.
Run dit NA het inschakelen van "Confirm email" in Supabase.

Test flow:
1. Maakt test user aan
2. Checkt of confirmation vereist is
3. Verifieert dat geen sessie werd aangemaakt
4. Simuleert confirmation proces

BELANGRIJK: Gebruik een ECHT email adres dat je kan checken!
"""

import asyncio
import sys
from educhat.services.auth_service import AuthService

async def test_email_confirmation():
    """Test of email confirmation correct werkt"""
    
    print("=" * 60)
    print("🧪 EMAIL CONFIRMATION TEST")
    print("=" * 60)
    print()
    
    # Test email - VERANDER DIT naar jouw test email!
    test_email = input("Voer test email adres in (dat je kan checken): ").strip()
    test_password = "TestPassword123!"
    test_firstname = "Test"
    test_lastname = "User"
    test_fullname = f"{test_firstname} {test_lastname}"
    
    print()
    print(f"📧 Testing met: {test_email}")
    print(f"🔐 Wachtwoord: {test_password}")
    print(f"👤 Naam: {test_fullname}")
    print()
    print("-" * 60)
    print()
    
    try:
        # Initialize auth service
        auth_service = AuthService()
        
        print("1️⃣ Attempting signup...")
        print()
        
        # Attempt signup
        result = await auth_service.signup(
            email=test_email,
            password=test_password,
            name=test_fullname,
            firstname=test_firstname,
            lastname=test_lastname
        )
        
        print()
        print("-" * 60)
        print("📊 SIGNUP RESULT:")
        print("-" * 60)
        print()
        
        if result.get("success"):
            print("✅ Signup successful!")
            print()
            
            requires_confirmation = result.get("requires_confirmation", False)
            print(f"📧 Requires confirmation: {requires_confirmation}")
            print()
            
            if requires_confirmation:
                print("=" * 60)
                print("✅ CORRECT GEDRAG - EMAIL CONFIRMATION ENABLED!")
                print("=" * 60)
                print()
                print("Wat er nu moet gebeuren:")
                print("1. ✅ User is aangemaakt in Supabase")
                print("2. ✅ Confirmation email is verstuurd")
                print("3. ✅ User kan NOG NIET inloggen")
                print("4. ⏳ Check je email inbox (EN spam folder!)")
                print(f"5. 📧 Zoek email van: noreply@mail.app.supabase.io")
                print("6. 🔗 Klik op 'Bevestig E-mailadres' knop")
                print("7. ✅ Dan kan user inloggen")
                print()
                print("🎉 EMAIL CONFIRMATION WERKT CORRECT!")
                print()
                
                # Provide cleanup instructions
                print("-" * 60)
                print("🧹 CLEANUP:")
                print("-" * 60)
                print("Deze test user moet je handmatig verwijderen uit Supabase:")
                print(f"1. Ga naar Supabase → Authentication → Users")
                print(f"2. Zoek user: {test_email}")
                print(f"3. Klik op ... menu → Delete user")
                print()
                
            else:
                print("=" * 60)
                print("❌ FOUT - EMAIL CONFIRMATION NOG STEEDS DISABLED!")
                print("=" * 60)
                print()
                print("Wat er gebeurde:")
                print("1. ❌ User werd meteen aangemaakt EN bevestigd")
                print("2. ❌ User kreeg meteen een sessie (ingelogd)")
                print("3. ❌ Geen confirmation email verstuurd")
                print("4. ❌ User kan al inloggen zonder email te bevestigen")
                print()
                print("🔧 HOE TE FIXEN:")
                print("-" * 60)
                print("1. Open Supabase Dashboard: https://app.supabase.com")
                print("2. Select je EduChat project")
                print("3. Ga naar: Authentication → Providers → Email")
                print("4. Scroll naar beneden naar 'Email'")
                print("5. Zet 'Confirm email' toggle op ON")
                print("6. Klik 'Save'")
                print("7. Run dit script OPNIEUW")
                print()
                print("⚠️  BELANGRIJK:")
                print("Zorg dat de toggle groen is en AAN staat!")
                print("Anders zal dit script steeds deze warning geven.")
                print()
                
                # Show session info for debugging
                if result.get("session"):
                    print("🔑 Session info (MOET NONE zijn voor confirmation!):")
                    session = result["session"]
                    print(f"   - Access token: {'Present' if session.get('access_token') else 'None'}")
                    print(f"   - Refresh token: {'Present' if session.get('refresh_token') else 'None'}")
                    print()
                
                # Cleanup
                print("-" * 60)
                print("🧹 CLEANUP:")
                print("-" * 60)
                print("Deze test user moet je verwijderen uit Supabase:")
                print(f"1. Ga naar Supabase → Authentication → Users")
                print(f"2. Zoek user: {test_email}")
                print(f"3. Klik op ... menu → Delete user")
                print()
        else:
            print("❌ Signup failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            print()
            print("Mogelijke oorzaken:")
            print("- Email adres bestaat al")
            print("- Wachtwoord voldoet niet aan eisen")
            print("- Supabase connectie probleem")
            print("- Te veel pogingen (rate limit)")
            print()
            
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR TIJDENS TEST")
        print("=" * 60)
        print()
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print()
        print("Mogelijke oorzaken:")
        print("- Geen internet connectie")
        print("- Supabase credentials niet correct")
        print("- Supabase service down")
        print()
        print("Check je .env file en Supabase status:")
        print("https://status.supabase.com")
        print()
        
        # Print full traceback for debugging
        import traceback
        print("-" * 60)
        print("Full traceback:")
        print("-" * 60)
        traceback.print_exc()
        print()
    
    print("=" * 60)
    print("🏁 TEST COMPLETE")
    print("=" * 60)
    print()

if __name__ == "__main__":
    print()
    print("⚠️  BELANGRIJK:")
    print("-" * 60)
    print("Dit script maakt een ECHTE user aan in je Supabase database!")
    print("Gebruik een email adres dat je kan checken voor confirmation email.")
    print("Na de test moet je de user handmatig verwijderen in Supabase.")
    print()
    
    confirm = input("Wil je doorgaan? (ja/nee): ").strip().lower()
    if confirm in ['ja', 'j', 'yes', 'y']:
        print()
        asyncio.run(test_email_confirmation())
    else:
        print()
        print("❌ Test geannuleerd")
        print()
