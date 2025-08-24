# Multilingual Data Directory

This directory will contain translated Q&A pairs in various Indian languages.

To generate multilingual data:
```python
from train_college_ai_agent import CollegeAIAgent
agent = CollegeAIAgent(enable_multilingual=True)
agent.generate_multilingual_data()  # Takes 10-15 minutes
```

Supported languages: Hindi, Bengali, Telugu, Tamil, Marathi, Gujarati, Urdu, Kannada, Malayalam, Odia, Punjabi, Assamese, and more.
