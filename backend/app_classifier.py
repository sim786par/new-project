# backend/app_classifier.py

def classify_app(app_name):
    """Classify app into category based on window title"""
    
    # Handle None or empty value
    if app_name is None or app_name == "":
        return 'Other'
    
    # Convert to lowercase for matching
    name = app_name.lower()
    
    # Define app categories
    streaming = ['netflix', 'youtube', 'spotify', 'prime', 'hotstar', 
                 'disney', 'hulu', 'video', 'vlc']
    
    social = ['facebook', 'instagram', 'twitter', 'whatsapp', 'telegram', 
              'snapchat', 'linkedin', 'messenger', 'discord']
    
    coding = ['vs code', 'visual studio', 'pycharm', 'notepad', 'sublime', 
              'terminal', 'cmd', 'powershell', 'anaconda', 'jupyter']
    
    gaming = ['game', 'steam', 'epic', 'minecraft', 'valorant', 'fortnite',
              'roblox', 'league of legends']
    
    browsing = ['chrome', 'firefox', 'edge', 'browser', 'safari', 'opera', 'brave']
    
    work = ['word', 'excel', 'powerpoint', 'pdf', 'slack', 'zoom', 
            'teams', 'outlook', 'notion']
    
    # Check matches
    for app in streaming:
        if app in name:
            return 'Streaming'
    
    for app in social:
        if app in name:
            return 'Social Media'
    
    for app in coding:
        if app in name:
            return 'Coding'
    
    for app in gaming:
        if app in name:
            return 'Gaming'
    
    for app in browsing:
        if app in name:
            return 'Browsing'
    
    for app in work:
        if app in name:
            return 'Work'
    
    return 'Other'


# ====== ALTERNATIVE: SAB EK FILE MEIN ======
# Agar abhi bhi error aaye, toh sirf ye 3 files hi honi chahiye:
# 1. main.py (sab kuch usmein)
# 2. requirements.txt
# 3. carbon_tracker.db (auto banega)
