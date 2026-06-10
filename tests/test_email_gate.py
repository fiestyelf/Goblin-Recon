from goblin_recon.tools.email_gate import EmailDraft, EmailGate


def test_email_gate_passes_specific_value_email():
    result = EmailGate().evaluate(
        EmailDraft(
            subject="The metric you're not tracking",
            body=(
                "Most founders track open rates. Almost no one tracks this one number, "
                "and it predicts retention better than anything else. Reply if you want the checklist."
            ),
            campaign_type="value",
            brand_angle="b2b",
        )
    )

    assert result.verdict == "PASS"
    assert result.total >= 80


def test_email_gate_rejects_spam_and_filler():
    result = EmailGate().evaluate(
        EmailDraft(
            subject="Free limited time offer",
            body=(
                "I hope this email finds you well. Click here to buy now and double your revenue."
            ),
            campaign_type="launch",
            brand_angle="b2b",
        )
    )

    assert result.verdict == "REJECT"
    assert result.total < 60
    assert any("Spam trigger" in flag for flag in result.attention.flags)
    assert any("Filler opener" in flag for flag in result.attention.flags)


def test_email_gate_json_safe_feedback_has_no_emoji():
    result = EmailGate().evaluate(
        EmailDraft(
            subject="The metric you're not tracking",
            body=(
                "Most founders track open rates. Almost no one tracks this one number. "
                "Reply if you want the checklist."
            ),
        )
    )

    assert "[PASS]" in result.feedback or "[FAIL]" in result.feedback
    assert "\u2705" not in result.feedback
    assert "\u274c" not in result.feedback
