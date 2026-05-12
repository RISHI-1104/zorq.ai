# Security Policy

This document outlines the security practices and policies for the ZORQ AI project.

## 🔐 Security Commitment

We take security seriously and are committed to maintaining the highest standards of data protection and code security.

## 🛡️ Best Practices

### API Key Security

**NEVER:**
- Commit API keys to GitHub
- Share API keys in emails or messages
- Expose API keys in browser console
- Hardcode API keys in production code
- Log API keys in error messages

**ALWAYS:**
- Use `.env` files for local development
- Set environment variables on production servers
- Rotate keys periodically
- Revoke compromised keys immediately
- Use minimal-permission API keys
- Monitor API key usage

### Code Security

**NEVER:**
- Use `eval()` or `exec()` with user input
- Store passwords in plain text
- Trust user input without validation
- Expose server errors to users
- Use outdated dependencies

**ALWAYS:**
- Validate and sanitize all input
- Use parameterized queries
- Keep dependencies updated
- Use HTTPS in production
- Implement proper error handling
- Use security headers

### Deployment Security

**NEVER:**
- Deploy with `DEBUG = True`
- Use default credentials
- Expose admin interfaces
- Run with unnecessary permissions
- Disable HTTPS

**ALWAYS:**
- Set `FLASK_ENV = production`
- Use strong authentication
- Implement rate limiting
- Use environment variables for secrets
- Enable HTTPS
- Monitor logs regularly
- Keep server software updated

## 🔑 Environment Variables

### Required Variables (Production)

```
GROQ_API_KEY          # Your Groq API key (from console.groq.com/keys)
FLASK_ENV             # Set to "production"
SECRET_KEY            # Generate with: python -c "import secrets; print(secrets.token_hex(16))"
```

### Optional Variables

```
DEBUG                 # Set to false in production
PORT                  # Server port (default 5000)
GROQ_MODEL           # AI model name
```

### Generating Secure Values

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(16))"

# Example output: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, **DO NOT** open a public GitHub issue.

### How to Report

1. **Email:** Send details to [security@yoursite.com] with:
   - Type of vulnerability
   - Location in code
   - Steps to reproduce
   - Potential impact
   - Your contact information

2. **Include:**
   - Affected version(s)
   - Proof of concept (if possible)
   - Suggested fix (if you have one)

3. **Do NOT:**
   - Share vulnerability details publicly
   - Demonstrate exploit against live systems
   - Access data without permission
   - Violate laws in testing

### Response Timeline

- **24 hours**: Acknowledge receipt
- **7 days**: Provide initial assessment
- **30 days**: Deploy security patch
- **30+ days**: Public disclosure (after patch release)

## 🔍 Security Scanning

This project includes automated security scanning:

### GitHub Actions (CI/CD)

Every push triggers:
- Syntax checking
- Dependency vulnerability scanning
- Hardcoded credential detection
- Python security analysis (Bandit)
- Code quality checks (Flake8, Pylint)

### Manual Scanning

```bash
# Install security tools
pip install bandit safety

# Run Bandit (Python security)
bandit -r . -ll

# Check for vulnerable dependencies
safety check
```

## 🔐 Dependency Security

### Keep Dependencies Updated

```bash
# Check for updates
pip list --outdated

# Update all packages
pip install --upgrade -r requirements.txt

# Pin versions in requirements.txt
flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
```

### Vulnerable Dependencies

Monitor for security issues in dependencies:

- Receive GitHub security alerts
- Use `safety` package: `safety check`
- Check [CVE database](https://nvd.nist.gov) for known issues
- Update immediately if critical vulnerability found

## 🔒 Data Protection

### What We Collect

- **Chat messages** – Stored in browser localStorage only
- **User data** – Email/password stored in localStorage for demo
- **API usage** – Logged by Groq (check their privacy policy)

### What We DON'T Collect

- ✓ No persistent server-side storage
- ✓ No user analytics
- ✓ No third-party tracking
- ✓ No cookies (beyond session)
- ✓ No personal data collection

### Privacy

- Chat messages are client-side only
- API calls go through Groq
- No data is stored long-term
- Clear browser data to delete everything
- No GDPR compliance needed for local usage

## 🛡️ Headers & Protections

The application sets security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Content-Security-Policy: (configured)
```

## 🚀 Production Deployment

### Pre-Deployment Checklist

- [ ] `.env` contains all secrets
- [ ] `.env` is in `.gitignore`
- [ ] No hardcoded API keys in code
- [ ] FLASK_DEBUG = false
- [ ] FLASK_ENV = production
- [ ] All dependencies installed
- [ ] Error handling implemented
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Incident response plan ready

### Server Hardening

1. **Update system packages:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. **Use firewall:**
   ```bash
   sudo ufw enable
   sudo ufw allow 22/tcp
   sudo ufw allow 443/tcp
   sudo ufw allow 80/tcp
   ```

3. **SSL/TLS certificates:**
   - Use Let's Encrypt (free)
   - Auto-renew certificates
   - Force HTTPS redirect

4. **Reverse proxy:**
   - Use Nginx or Apache
   - Load balancer for HA
   - Rate limiting at proxy level

## 📊 Security Monitoring

### Logs to Monitor

```bash
# Check application logs
tail -f /var/log/zorq/app.log

# Check API calls
grep "API Error" /var/log/zorq/app.log

# Check unauthorized access
grep "401\|403\|404" /var/log/zorq/access.log
```

### Alerting

Set up alerts for:
- API errors (500+)
- Authentication failures (401)
- High request rates (potential DDoS)
- Unusual traffic patterns
- Server resource usage

## 🔄 Update Policy

### Security Updates

- Applied immediately
- May include breaking changes
- Released as patch versions (3.0.1 → 3.0.2)

### Feature Updates

- Released monthly
- Tested thoroughly
- Backward compatible when possible

### Dependency Updates

- Monitored continuously
- Applied within 30 days for minor
- Applied within 7 days for critical

## 📚 Security Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [Python Security](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Flask Security](https://flask.palletsprojects.com/security/)
- [Groq Security](https://www.groq.com/security)

## 🤝 Community Security

### Responsible Disclosure

- Test in staging environment
- Report privately before public disclosure
- Allow reasonable time for patch
- Provide proof of concept if possible
- Help verify fix if requested

### Code Review

All pull requests are reviewed for:
- Security vulnerabilities
- Code quality
- Testing coverage
- Documentation
- Dependency changes

## 📋 Compliance

### Standards

- OWASP guidelines
- PEP 8 (Python style)
- Common security practices
- Industry best practices

### Limitations

- Not HIPAA compliant (medical data)
- Not GDPR compliant (uses localStorage)
- Not PCI-DSS certified (payment processing)
- Not SOC 2 certified

## 🔗 Security Contacts

- **Report Vulnerability:** [security@yoursite.com]
- **Security Team:** [list your team]
- **Contact:** [your contact info]

## 📝 Security Changelog

### Version 1.0.0 (Initial Release)

- ✅ API key environment variable support
- ✅ HTTPS ready
- ✅ Security headers configured
- ✅ Input validation implemented
- ✅ Automated security scanning
- ✅ Dependency scanning enabled

---

**Last Updated:** 2024
**Version:** 1.0.0

For questions or concerns, please contact [security@yoursite.com]
