# GitHub Actions Workflows

This directory contains automated workflows for continuous integration, code review, and quality assurance.

## Workflows Overview

### 1. Code Review (`code-review.yml`)

**Triggers:** Pull requests to `main` or `develop` branches

**Purpose:** Automated code quality checks on pull requests

**Jobs:**
- **Code Quality Checks**
  - Black formatter validation
  - isort import sorting check
  - Flake8 linting
  - Pylint analysis
  - Bandit security scanning

- **Test**
  - Python module compilation tests
  - Import validation
  - Module loading verification

- **Notebook Check**
  - Jupyter notebook validation
  - Notebook execution tests

- **Summary**
  - Aggregated review results
  - Status overview

**Usage:** Automatically runs on PR creation/updates. Review the summary in the PR comments and GitHub Actions tab.

---

### 2. CI Pipeline (`ci.yml`)

**Triggers:** Push to `main`/`develop` or pull requests

**Purpose:** Continuous integration across multiple Python versions

**Jobs:**
- **Build and Test**
  - Tests on Python 3.9, 3.10, 3.11
  - Dependency installation
  - Module import verification
  - Data loading tests

- **Dashboard Validation**
  - Streamlit installation check
  - Dashboard module validation

- **Documentation Check**
  - Verifies all documentation files exist
  - Checks required Python files
  - Validates requirements.txt

**Usage:** Automatically runs on every push and PR. Ensures compatibility across Python versions.

---

### 3. Claude Code Review (`claude-code-review.yml`)

**Triggers:** Pull requests

**Purpose:** Automated intelligent code review with detailed analysis

**Jobs:**
- **Claude Review**
  - Changed files detection
  - Large file warnings
  - TODO/FIXME comment detection
  - Print statement detection (suggests logging)
  - Hardcoded credential detection
  - Code complexity analysis (using radon)
  - Style compliance checking
  - Automated PR comment with findings

**Features:**
- 🔍 Analyzes changed files only
- 📊 Calculates cyclomatic complexity
- 🔐 Security pattern detection
- 💬 Posts comprehensive review comment
- 📦 Uploads analysis artifacts

**Usage:** Automatically posts detailed review comments on PRs. Review the bot comments for insights.

---

### 4. Dependency Review (`dependency-review.yml`)

**Triggers:**
- Pull requests to `main`
- Weekly schedule (Sundays)
- Manual trigger

**Purpose:** Security and dependency management

**Jobs:**
- **Dependency Check**
  - pip-audit vulnerability scanning
  - Safety security checks
  - JSON report generation

- **Dependency Graph**
  - Generates visual dependency tree
  - Shows package relationships

- **Outdated Check**
  - Lists outdated packages
  - Recommends updates

**Artifacts:**
- `safety-report.json`: Security vulnerabilities
- `dependency-tree.md`: Package dependency visualization
- `outdated-packages.md`: Update recommendations

**Usage:**
- Runs automatically weekly
- Run manually: Actions tab → Dependency Review → Run workflow
- Review artifacts for security and update info

---

## How to Use

### For Contributors

1. **Before Creating PR:**
   - Run `black *.py` to format code
   - Run `flake8 *.py` to check linting
   - Test your changes locally

2. **After Creating PR:**
   - Wait for all checks to complete
   - Review automated comments
   - Address any issues found
   - Push fixes to update PR

3. **Reviewing Artifacts:**
   - Go to Actions tab
   - Click on the workflow run
   - Download artifacts at bottom of page

### For Maintainers

1. **Reviewing PRs:**
   - Check workflow status badges
   - Review automated comments
   - Check for security warnings
   - Review complexity reports

2. **Manual Workflow Runs:**
   - Go to Actions tab
   - Select workflow
   - Click "Run workflow"
   - Choose branch and parameters

3. **Weekly Dependency Reviews:**
   - Check Sunday runs for updates
   - Review security vulnerabilities
   - Create issues for critical updates

---

## Workflow Status Badges

Add these to your README.md:

```markdown
![Code Review](https://github.com/gwho/ecommerce-analytics-dashboard/actions/workflows/code-review.yml/badge.svg)
![CI Pipeline](https://github.com/gwho/ecommerce-analytics-dashboard/actions/workflows/ci.yml/badge.svg)
![Claude Code Review](https://github.com/gwho/ecommerce-analytics-dashboard/actions/workflows/claude-code-review.yml/badge.svg)
![Dependency Review](https://github.com/gwho/ecommerce-analytics-dashboard/actions/workflows/dependency-review.yml/badge.svg)
```

---

## Customization

### Modifying Python Versions

Edit `ci.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']  # Add/remove versions
```

### Adjusting Code Quality Rules

Edit `code-review.yml`:
```yaml
- name: Run Flake8 (Linting)
  run: |
    flake8 *.py --max-line-length=120 --extend-ignore=E203,W503,E501
```

### Changing Schedule

Edit `dependency-review.yml`:
```yaml
schedule:
  - cron: '0 0 * * 1'  # Change to Monday
```

---

## Troubleshooting

### Workflow Fails

1. Check the logs in Actions tab
2. Look for red X marks
3. Click "Details" to see error messages
4. Common fixes:
   - Update requirements.txt
   - Fix import errors
   - Address linting issues

### Security Alerts

1. Review safety-report.json artifact
2. Update vulnerable packages
3. If false positive, document in PR

### Performance Issues

1. Workflows taking too long?
2. Consider:
   - Reducing test matrix
   - Caching dependencies
   - Splitting into separate workflows

---

## Support

For issues with workflows:
1. Check GitHub Actions documentation
2. Review workflow logs
3. Open an issue with error details
4. Tag with `ci/cd` label
