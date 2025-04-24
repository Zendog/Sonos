from SiriusHelper_FIXED_v4_FINAL_CLEANED_FIXED import SiriusXM

# Replace these with your actual SiriusXM credentials
USERNAME = "DTrasente"
PASSWORD = "bAG84^mm*"

sxm = SiriusXM(USERNAME, PASSWORD)

if sxm.login():
    print("✅ Login successful")
    print("🎧 Available channels:")
    channels = sxm.get_channels()
    if channels:
        for ch in channels[:10]:  # Limit to first 10 channels for readability
            print(f"- {ch.get('name')} ({ch.get('channelId')})")
    else:
        print("⚠️ No channels returned")
else:
    print("❌ Login failed")
