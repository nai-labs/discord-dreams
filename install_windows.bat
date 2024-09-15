@echo off
echo Discord Dreams Installer for Windows
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

REM Prompt for API keys
set /p discord_token=Discord Bot Token: 
set /p discord_user_id=Discord User ID: 
set /p openrouter_key=OpenRouter API Key: 
set /p openrouter_referer=OpenRouter HTTP Referer (https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID^&permissions=YOUR_PERMISSIONS^&scope=bot): 
set /p anthropic_key=Anthropic API Key: 
set /p elevenlabs_key=ElevenLabs API Key: 
set /p replicate_token=Replicate API Token: 

REM Create .env file
(
echo DISCORD_BOT_TOKEN=%discord_token%
echo DISCORD_USER_ID=%discord_user_id%
echo OPENROUTER_KEY=%openrouter_key%
echo OPENROUTER_HTTP_REFERER=%openrouter_referer%
echo ANTHROPIC_API_KEY=%anthropic_key%
echo ELEVENLABS_API_KEY=%elevenlabs_key%
echo REPLICATE_API_TOKEN=%replicate_token%
echo DEFAULT_LLM=anthropic
) > .env

echo.
echo Installation complete! To run Discord Dreams, follow these steps:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the bot: python main.py
echo.
echo Open Discord, and enjoy using Discord Dreams!

pause