# Branch Protection Setup

The `main` branch is protected to enforce best practices and maintain code quality.

## 🔒 Protection Rules

| Rule | Status | Description |
|------|--------|-------------|
| **Require Pull Request** | ✅ Enabled | All changes must go through PR |
| **Enforce for Admins** | ✅ Enabled | Even admins must use PRs |
| **Required Approvals** | 0 | PRs can be self-approved (solo developer) |
| **Dismiss Stale Reviews** | ❌ Disabled | Reviews stay valid after new commits |
| **Require Code Owners** | ❌ Disabled | No CODEOWNERS file required |
| **Force Pushes** | 🚫 Blocked | Cannot force push to main |
| **Branch Deletion** | 🚫 Blocked | Cannot delete main branch |
| **Linear History** | ❌ Disabled | Merge commits are allowed |

## 📋 What This Means

### ✅ You CAN:
- Create feature branches
- Commit to feature branches
- Push feature branches to GitHub
- Create pull requests
- Merge PRs (even your own)
- Delete feature branches after merging

### 🚫 You CANNOT:
- Commit directly to `main`
- Push directly to `main`
- Force push to `main`
- Delete the `main` branch
- Bypass PR workflow (even as admin)

## 🔄 Required Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add my feature"

# 3. Push branch
git push origin feature/my-feature

# 4. Create PR
gh pr create

# 5. Merge PR
gh pr merge --squash

# 6. Clean up
git checkout main
git pull origin main
git branch -d feature/my-feature
```

## 🛠️ Setup Details

Branch protection was configured using GitHub CLI:

```bash
gh api repos/silverbeer/qualityplaybook.dev/branches/main/protection \
  --method PUT \
  --input branch-protection.json
```

Configuration:
```json
{
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "enforce_admins": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

## 📝 Why These Settings?

**Solo Developer Optimized:**
- **0 Required Approvals**: You can merge your own PRs without waiting
- **Enforce for Admins**: Keeps you honest and maintains git history
- **Allow Merge Commits**: Flexibility in merge strategy

**Safety First:**
- **Block Force Push**: Prevents accidental history rewriting
- **Block Deletion**: Protects main branch from accidents
- **Require PRs**: Ensures all changes are reviewable

## 🎯 Benefits

1. **Better Git History**: Every change is documented in a PR
2. **Code Review Ready**: Easy to add collaborators later
3. **Rollback Friendly**: Easy to revert PRs if needed
4. **CI/CD Integration**: Can add status checks later
5. **Professional Practice**: Industry standard workflow

## 🔧 Modifying Protection Rules

To update branch protection:

```bash
# Edit the JSON
cat > /tmp/protection.json << 'EOF'
{
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  ...
}
EOF

# Apply changes
gh api repos/silverbeer/qualityplaybook.dev/branches/main/protection \
  --method PUT \
  --input /tmp/protection.json
```

Or use GitHub UI:
1. Go to repository Settings
2. Click "Branches" in left sidebar
3. Click "Edit" on main branch rule
4. Adjust settings
5. Save changes

## 🚨 Emergency Override

If you absolutely need to bypass protection (emergencies only):

1. Temporarily disable protection:
```bash
gh api repos/silverbeer/qualityplaybook.dev/branches/main/protection \
  --method DELETE
```

2. Make your changes and push

3. Re-enable protection:
```bash
gh api repos/silverbeer/qualityplaybook.dev/branches/main/protection \
  --method PUT \
  --input /tmp/branch-protection.json
```

**Note:** This defeats the purpose! Only use in true emergencies.

## 📚 Resources

- [GitHub Branch Protection Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub CLI Branch Protection](https://docs.github.com/en/rest/branches/branch-protection)
- [CONTRIBUTING.md](./.CONTRIBUTING.md) - PR workflow guide

---

Protection enabled: 2025-10-05
Last updated: 2025-10-05
