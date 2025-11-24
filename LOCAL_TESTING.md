# Local Testing Scripts

Since GitHub Actions is not available due to billing restrictions, use these local alternatives:

## Run Tests Before Commit

### Option 1: Automatic Pre-commit Hook (Recommended)
The pre-commit hook automatically runs tests before every commit.

**Install:**
```powershell
# The hook is already in .git/hooks/pre-commit
# Just make sure you run this once to test it works:
python .git/hooks/pre-commit
```

### Option 2: Manual Testing
Run these commands manually before committing:

```powershell
# Run all tests
python -m pytest -v

# Run tests with coverage
python -m pip install pytest-cov
python -m pytest --cov=src --cov-report=term-missing

# Check code quality
python -m pip install flake8
python -m flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Quick Test Script
Create a quick test script:

```powershell
# test.ps1
python -m pytest -v
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Tests failed!" -ForegroundColor Red
}
```

Run with: `.\test.ps1`
