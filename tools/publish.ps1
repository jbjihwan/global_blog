param(
    [string]$Message = "feat: Update blog content and series"
)

$ErrorActionPreference = "Stop"
$BlogDir = "D:\ai\antigravity\global_blog"
Set-Location $BlogDir

Write-Host "==> [1/4] Git Stage All..." -ForegroundColor Cyan
git add -A

Write-Host "==> [2/4] Git Commit ($Message)..." -ForegroundColor Cyan
$status = git status --porcelain
if ($status) {
    git commit -m $Message
    Write-Host "==> [3/4] Git Push to origin main..." -ForegroundColor Cyan
    git push origin main
} else {
    Write-Host "No changes to commit." -ForegroundColor Yellow
}

Write-Host "==> [4/4] Deploying to GitHub Pages..." -ForegroundColor Cyan
$env:GIT_USER = "jbjihwan"
npm run deploy

Write-Host "All tasks finished! Live at https://globaldevlog.com/" -ForegroundColor Green
