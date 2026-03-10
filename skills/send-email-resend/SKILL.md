---
name: send-email-resend
description: Send emails through Resend API. Use when the user asks to send an email, draft and send an email, or set up email-sending automation from OpenClaw using a Resend API key and verified sender address.
---

# Send Email via Resend

Use this skill to send transactional emails through Resend.

## Required inputs

Collect these fields before sending:

- `to` (recipient email)
- `from` (must be a sender allowed by Resend)
- `subject`
- `html` or `text`
- API key (`RESEND_API_KEY` env preferred)

## Safety and secrets

- Prefer using `RESEND_API_KEY` in environment variables, not hardcoded in files.
- If a key was posted in chat, treat it as sensitive and avoid re-posting it.

## Send flow

1. Confirm recipient, subject, and body.
2. Ensure API key is available (`RESEND_API_KEY`).
3. Run `scripts/send_resend_email.py`.
4. Report Resend response id/status back to the user.

## Command examples

Use env var:

```bash
export RESEND_API_KEY='re_xxx'
python3 skills/send-email-resend/scripts/send_resend_email.py \
  --from 'onboarding@resend.dev' \
  --to 'alice@example.com' \
  --subject 'Hello World' \
  --html '<p>Congrats on sending your <strong>first email</strong>!</p>'
```

Or explicit key flag (less secure):

```bash
python3 skills/send-email-resend/scripts/send_resend_email.py \
  --api-key 're_xxx' \
  --from 'onboarding@resend.dev' \
  --to 'alice@example.com' \
  --subject 'Hello World' \
  --html '<p>Test</p>'
```
