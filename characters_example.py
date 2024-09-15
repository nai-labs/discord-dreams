# characters_example.py

characters = {
    "example_character": {
        "system_prompt": """
You are Example Character, a [brief description of character's personality and background].

[Add more detailed character information here, including personality traits, likes, dislikes, and any specific instructions for how the character should behave or respond]

[Include any specific formatting or language patterns the character should use]
""",
        "image_prompt": "Describe the character's appearance for image generation, e.g., 'a [age] year-old [ethnicity] [gender] with [distinctive features]'",
        "tts_url": "https://api.elevenlabs.io/v1/text-to-speech/[YOUR-ELEVENLABS-VOICE-ID-HERE]",
        "source_faces_folder": "path/to/folder/with/face/to/swap/with",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.45,
            "style": 0.5
        }
    }
}