---
description: Auto git commit all changes in Voice_app repo with a meaningful message
---

// turbo-all

## Auto Git Commit — Voice_app

Use this workflow whenever you make changes to any file in the Voice_app project. It stages all modified/new files and commits with a descriptive message.

### Steps

1. Check current git status to understand what changed:
```powershell
git -C "c:\Users\vamsi\Documents\Voice_app" status --short
```

2. Stage all changes (new files, modifications, deletions):
```powershell
git -C "c:\Users\vamsi\Documents\Voice_app" add -A
```

3. Commit with a meaningful message describing the change. Use conventional commit format (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`):
```powershell
git -C "c:\Users\vamsi\Documents\Voice_app" commit -m "<type>: <short description of what changed and why>"
```

Replace `<type>: <short description>` with an appropriate message based on what was actually changed. Examples:
- `feat: add weather forecast to llm_summary in news_api`
- `fix: handle empty RSS feed gracefully in news_scrapper_api`
- `refactor: simplify scoring logic in news_api`
- `docs: update README with v2 endpoint examples`
- `test: add Tamil Nadu cotton test case to test_news_api`

4. Confirm the commit was created:
```powershell
git -C "c:\Users\vamsi\Documents\Voice_app" log --oneline -3
```
