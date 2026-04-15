import sys
sys.path.insert(0, '.')
from app.bot_flow import process_message, clear_session

def test_flow(phone, steps, label):
    clear_session(phone)
    print(f"\n{'='*50}")
    print(f"TEST: {label}")
    print('='*50)
    for msg in steps:
        reply = process_message(phone, msg)
        print(f"You: {msg}")
        print(f"Bot: {reply[:100]}...")
        print()

# Test 1: English with licence - Bangalore
test_flow("911111111111", 
    ["hi", "2", "1", "Rahul", "Bangalore", "2"],
    "English + Licence + Bangalore + Budget 2")

# Test 2: Hindi without licence - Mumbai  
test_flow("912222222222",
    ["hi", "1", "2", "Rahul", "Mumbai", "1"],
    "Hindi + No Licence + Mumbai + Budget 1")

# Test 3: Invalid city
test_flow("913333333333",
    ["hi", "2", "1", "Test", "XYZCity", "2"],
    "Invalid city test")

print("\n✅ All tests completed!")
