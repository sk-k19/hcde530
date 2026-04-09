def count_words(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    return len(text.split())


# 50 made-up app reviews (each string is one review)
reviews = [
    "Clean design and easy to use. I finished my setup in two minutes.",
    "Good idea, but it crashes when I try to upload a photo.",
    "Notifications are way too aggressive even after I turned them off.",
    "Search is fast and the filters actually make sense.",
    "The onboarding is confusing and I had to guess what the buttons do.",
    "Love the dark mode and the font options. Great accessibility touches.",
    "Sync between my phone and laptop is unreliable and sometimes duplicates items.",
    "The latest update fixed the lag. Scrolling feels smooth now.",
    "Please add an option to export my data as a CSV.",
    "Too many ads for a paid subscription. Feels misleading.",
    "The app is helpful, but the tutorial covers the wrong features first.",
    "I like the reminders, but I wish I could snooze them longer.",
    "Customer support replied quickly and solved my billing issue.",
    "It keeps logging me out randomly, which is frustrating.",
    "Great for tracking habits. The streak view motivates me.",
    "The calendar view is cluttered and hard to read on small screens.",
    "I can’t find where to change my email address in settings.",
    "Audio playback stops when the screen locks. Please fix.",
    "The widgets are useful, but they don’t update consistently.",
    "I appreciate the simple layout. No extra clutter.",
    "Wish there were more templates for planning weekly tasks.",
    "The app drains my battery faster than any other app I use.",
    "Signing in with Google worked instantly. Nice.",
    "The text is too small and there’s no size slider.",
    "Offline mode is a lifesaver when I’m traveling.",
    "The app froze during checkout and I got charged twice.",
    "Great concept, average execution. Needs polishing.",
    "I love the animations, but they slow down older devices.",
    "The stats page is misleading and doesn’t match my activity.",
    "Auto-save works well and I never lose my notes.",
    "I don’t like the new icon. It looks generic now.",
    "The app is fast, but the color contrast is low in light mode.",
    "Please let me reorder items with drag and drop.",
    "Voice input is surprisingly accurate and saves time.",
    "The privacy options are clear and easy to understand.",
    "It took forever to load the first time and almost made me uninstall.",
    "Sharing links with friends works, but the preview looks broken.",
    "The keyboard covers the input field on my phone.",
    "I keep getting error messages with no explanation.",
    "The app is okay, but it needs better organization tools.",
    "I like the idea of goals, but the labels are confusing.",
    "The map feature is inaccurate and sends me to the wrong address.",
    "This is the first app that actually helped me stick to a routine.",
    "The free version is basically unusable because of paywalls.",
    "I wish the app remembered my filters between sessions.",
    "The update changed the layout and now I can’t find anything.",
    "Loading times improved a lot. Nice work by the team.",
    "I reported a bug and it was fixed in the next release. Thanks!",
    "The app doesn’t support landscape mode on tablets.",
    "Simple, reliable, and does exactly what I need every day.",
]


word_counts = [count_words(review) for review in reviews]

print(f"{'Review #':<8} {'Words':<6} {'Preview'}")
print("-" * 70)
for i, (review, wc) in enumerate(zip(reviews, word_counts), start=1):
    preview = review if len(review) <= 55 else review[:55] + "..."
    print(f"{i:<8} {wc:<6} {preview}")

print()
print("── Summary ─────────────────────────────────")
print(f"  Total reviews   : {len(word_counts)}")
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")

