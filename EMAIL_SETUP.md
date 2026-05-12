# Email Automation Setup Guide for ZORQ

## 📧 Welcome Email Feature

When a new user registers in ZORQ, they automatically receive a beautiful welcome email with:
- Personalized greeting with their name
- Account confirmation with User ID
- Join date
- Features they can use in ZORQ
- Call-to-action button

## 🔧 Configuration Steps

### Option 1: Gmail SMTP (Recommended)

1. **Create Gmail App Password:**
   - Go to https://myaccount.google.com/
   - Click "Security" in the left menu
   - Enable "2-Step Verification" (if not already enabled)
   - Go back to Security and select "App passwords"
   - Choose "Mail" and "Windows Computer"
   - Copy the generated 16-character password

2. **Set Environment Variables (Windows PowerShell):**
   ```powershell
   $env:ZORQ_SENDER_EMAIL="your-gmail@gmail.com"
   $env:ZORQ_SENDER_PASSWORD="your-16-char-app-password"
   ```

3. **Or Set in Command Prompt:**
   ```cmd
   set ZORQ_SENDER_EMAIL=your-gmail@gmail.com
   set ZORQ_SENDER_PASSWORD=your-16-char-app-password
   ```

4. **Restart Flask Server:**
   ```powershell
   python server.py
   ```

### Option 2: Other Email Providers

Modify the SMTP settings in `server.py`:

```python
# For Outlook/Microsoft
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587

# For Yahoo
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 587

# For custom servers
SMTP_SERVER = 'your-server.com'
SMTP_PORT = 587
```

## 📋 Email Template

The welcome email includes:
- **Header:** ZORQ logo and branding
- **Greeting:** Personalized with user's name
- **Account Details:**
  - Name
  - Email
  - User ID
  - Join Date
- **Features List:**
  - Chat in multiple languages (Tamil, English, etc.)
  - Save conversations
  - Edit profile
  - Get AI responses
- **CTA Button:** Link to dashboard
- **Footer:** Security notice

## 🧪 Testing

1. **Register a new user** at `http://localhost:5000/auth.html`
2. **Check your email** for the welcome message
3. **If email fails gracefully:**
   - Account is still created successfully
   - Error is logged in server console
   - User can still sign in and use ZORQ

## 🔒 Security Notes

⚠️ **Important:**
- **Never** commit passwords to git
- **Always** use environment variables
- For Gmail: Use App Passwords, not your actual password
- Consider using a dedicated "noreply" email account

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "SMTP authentication failed" | Check email/password in environment variables |
| "Connection refused" | Verify SMTP server address and port |
| Email not received | Check spam folder, verify recipient email |
| No error but email not sent | Check server console logs |

## 📝 Server Logs

View email sending logs in the Flask server console:
```
[DEBUG] Sending welcome email to user@example.com
[SUCCESS] Welcome email sent to user@example.com
[ERROR] SMTP authentication failed - check email credentials
```

## 💡 Features Included

✅ HTML formatted email with dark theme
✅ Graceful failure - won't break signup if email fails
✅ Supports multiple languages
✅ Beautiful, professional design
✅ Mobile-responsive layout
✅ Auto-retry on transient failures

---

**Questions?** Check the console output for detailed error messages!
