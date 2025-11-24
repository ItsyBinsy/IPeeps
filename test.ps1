# Run tests before commit
python -m pytest -v
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Tests failed!" -ForegroundColor Red
    exit 1
}
