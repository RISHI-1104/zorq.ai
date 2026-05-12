# Contributing to ZORQ AI

Thank you for your interest in contributing to ZORQ AI! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- **Report Bugs** – Found an issue? [Open a GitHub Issue](https://github.com/YOUR_USERNAME/zorq/issues)
- **Suggest Features** – Have an idea? [Start a Discussion](https://github.com/YOUR_USERNAME/zorq/discussions)
- **Submit Code** – Fix bugs or add features with a Pull Request
- **Improve Docs** – Better documentation helps everyone
- **Share Your Deployment** – Tell us how you deployed ZORQ

## 🐛 Reporting Bugs

Before reporting, please check if the issue already exists.

### Bug Report Template
```
**Describe the bug:**
[Clear description of what's wrong]

**Steps to reproduce:**
1. Go to...
2. Click on...
3. See error...

**Expected behavior:**
[What should happen]

**Actual behavior:**
[What actually happens]

**Environment:**
- OS: [Windows/Mac/Linux]
- Python Version: [3.8+]
- Browser: [Chrome/Firefox/Safari]

**Error message/logs:**
[Paste any error messages or terminal output]
```

## 💡 Suggesting Features

### Feature Request Template
```
**Description:**
[Clear description of the feature]

**Why is this useful?**
[Explain the benefit]

**Example usage:**
[Show how it would be used]
```

## 🔧 Setting Up Development Environment

1. **Fork the repository:**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/zorq.git
   cd zorq
   ```

3. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run locally:**
   ```bash
   python server.py
   ```

## 📝 Development Guidelines

### Code Style

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **JavaScript**: Use clear variable names, comments for complex logic
- **HTML/CSS**: Use semantic HTML, organize CSS logically

### Commit Messages

```
[TYPE] Short description (50 chars max)

Longer explanation if needed (72 chars wrap).
- Bullet point 1
- Bullet point 2

Fixes #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructure
- `perf:` Performance improvement
- `test:` Tests

### Testing Before Submission

- [ ] Code runs without errors
- [ ] No console errors (F12)
- [ ] Tested on mobile (320px)
- [ ] Tested on tablet (768px)
- [ ] Tested on desktop (1024px+)
- [ ] All links work
- [ ] Responsive design intact

## 🔐 Security Guidelines

**Never:**
- Commit API keys or credentials
- Store sensitive data in code
- Use hardcoded passwords
- Push .env files

**Always:**
- Use .env files for secrets
- Validate user input
- Sanitize output
- Keep dependencies updated

## 📤 Submitting Changes

1. **Ensure your code follows guidelines** (above)

2. **Make meaningful commits:**
   ```bash
   git add .
   git commit -m "feat: Add voice input support"
   git push origin feature/amazing-feature
   ```

3. **Open a Pull Request:**
   - Clear title: "Add voice input support"
   - Description: What does it do?
   - Closes: Reference any issues (#123)
   - Screenshots: For UI changes

### PR Template
```markdown
## Description
[What does this PR do?]

## Type of Change
- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change
- [ ] Documentation update

## How to Test
1. Step 1
2. Step 2
3. Expected result

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for clarity
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No new warnings generated
```

## ✅ PR Review Process

1. **Automated checks:**
   - Code linting
   - Build verification
   - Tests passing

2. **Maintainer review:**
   - Code quality
   - Design consistency
   - Performance impact
   - Security implications

3. **Feedback & Revisions:**
   - Address reviewer comments
   - Push additional commits
   - Mark as ready for re-review

4. **Merge:**
   - Squash commits (if needed)
   - Merge to main branch

## 📚 Documentation

### Updating README
- Keep installation instructions up-to-date
- Document new features clearly
- Include examples for complex features

### Adding Code Comments
```python
def complex_function(param1, param2):
    """
    Brief description of what this does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this is raised
    """
    # Complex logic explanation
    result = param1 + param2
    return result
```

## 🚀 Performance Considerations

- Minimize network requests
- Optimize CSS/JavaScript
- Cache where appropriate
- Lazy load heavy components
- Test on slow connections (throttle in DevTools)

## 🌍 Community Standards

- Be respectful and inclusive
- No harassment or discrimination
- Constructive feedback only
- Help others when possible
- Give credit to contributors

## 📖 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [HTML Best Practices](https://www.w3.org/community/webed/wiki/Best_practices_for_authoring_HTML_in_2020)

## ❓ Questions?

- 📧 Email: [your-email@example.com]
- 💬 GitHub Issues: [Ask a question](https://github.com/YOUR_USERNAME/zorq/issues)
- 🗨️ Discussions: [Start a discussion](https://github.com/YOUR_USERNAME/zorq/discussions)

---

## 🎉 Thank You!

Your contributions make ZORQ better for everyone. We appreciate your effort!

**Happy coding!** 🚀
