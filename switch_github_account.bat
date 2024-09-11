@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    echo Please provide an account name (nai or gh)
    exit /b 1
)

if "%1"=="nai" (
    git config user.name "nai-research"
    git config user.email "nikola.nai2003@gmail.com"
    echo Switched to GitHub Account: nai-research
) else if "%1"=="gh" (
    git config user.name "fizt656"
    git config user.email "gushalwani@alum.mit.edu"
    echo Switched to GitHub Account: fizt656
) else (
    echo Invalid account name. Please use 'nai' or 'gh'
    exit /b 1
)

echo Current Git configuration:
git config user.name
git config user.email