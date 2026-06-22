"""Email Quality Gate - 5-dimension validation engine.

Usage:
    from goblin_recon.tools.email_gate import EmailGate, EmailDraft

    gate = EmailGate("config/email-guardrails.yaml", "config/email-campaigns.yaml")
    draft = EmailDraft(
        subject="The metric you're not tracking",
        body="First line of the email...",
        campaign_type="value",
        brand_angle="b2b",
    )
    result = gate.evaluate(draft)
    print(result.verdict)  # PASS / FLAGGED / REJECT
"""

from __future__ import annotations

import re
import argparse
import json
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# Data types


@dataclass
class EmailDraft:
    """An email to be evaluated."""

    subject: str
    body: str
    campaign_type: str = "value"  # value | trust_building | launch | re_engagement
    brand_angle: str = "b2b"  # b2b | b2c | both
    audience_segment: str = "general"
    previous_email_subject: str | None = None  # for campaign alignment


@dataclass
class DimensionScore:
    score: int
    max_score: int
    flags: list[str] = field(default_factory=list)
    passed: bool = True


@dataclass
class EvaluationResult:
    attention: DimensionScore
    psychological_fit: DimensionScore
    brand_voice: DimensionScore
    professional_guardrails: DimensionScore
    campaign_alignment: DimensionScore

    @property
    def total(self) -> int:
        return (
            self.attention.score
            + self.psychological_fit.score
            + self.brand_voice.score
            + self.professional_guardrails.score
            + self.campaign_alignment.score
        )

    @property
    def max_total(self) -> int:
        return (
            self.attention.max_score
            + self.psychological_fit.max_score
            + self.brand_voice.max_score
            + self.professional_guardrails.max_score
            + self.campaign_alignment.max_score
        )

    @property
    def verdict(self) -> str:
        if self.total >= 80:
            return "PASS"
        elif self.total >= 60:
            return "FLAGGED"
        else:
            return "REJECT"

    @property
    def feedback(self) -> str:
        lines = [f"Email Gate - {self.verdict} ({self.total}/{self.max_total})"]
        for name, dim in [
            ("Attention", self.attention),
            ("Psychological Fit", self.psychological_fit),
            ("Brand Voice", self.brand_voice),
            ("Professional Guardrails", self.professional_guardrails),
            ("Campaign Alignment", self.campaign_alignment),
        ]:
            status = "PASS" if dim.passed else "FAIL"
            lines.append(f"  [{status}] {name}: {dim.score}/{dim.max_score}")
            for flag in dim.flags:
                lines.append(f"       - {flag}")
        return "\n".join(lines)


# The gate


class EmailGate:
    """Validates email drafts against a 5-dimension quality gate."""

    def __init__(
        self,
        guardrails_path: str | Path = "config/email-guardrails.yaml",
        campaigns_path: str | Path = "config/email-campaigns.yaml",
        brand_voice_path: str | Path = "config/brand-voice.yaml",
    ):
        self.guardrails = _load_yaml(guardrails_path)
        self.campaigns = _load_yaml(campaigns_path)
        self.brand_voice = _load_yaml(brand_voice_path)

    def evaluate(self, draft: EmailDraft) -> EvaluationResult:
        specificity_points = _specificity_points(draft.subject, draft.body)
        return EvaluationResult(
            attention=self._score_attention(draft, specificity_points),
            psychological_fit=self._score_psychological_fit(draft, specificity_points),
            brand_voice=self._score_brand_voice(draft),
            professional_guardrails=self._score_professional_guardrails(draft),
            campaign_alignment=self._score_campaign_alignment(draft),
        )

    # Dimension 1: attention score (0-25)

    def _score_attention(self, draft: EmailDraft, specificity_points: int) -> DimensionScore:
        score = 0
        flags = []
        subject = draft.subject.strip()
        body = draft.body.strip()
        first_two = " ".join(body.split()[:30])  # ~2 sentences

        # Subject: curiosity gap
        # Looks for known pattern: "The [X] you [verb]" or "[X] vs [Y]" or "[number] [things]"
        if _has_pattern(subject, r"\b(the|your|this)\b.*\b(you|your|you\'re|they|don\'t|should|need|missing|not|cost)\b"):
            score += 5
        elif _has_pattern(subject, r"\d+\s+\w+"):
            score += 4  # numbered list hook
        elif _has_pattern(subject, r"vs?\."):
            score += 4  # comparison hook
        elif _has_pattern(subject, r"\?"):
            score += 3  # question hook

        # Subject: specificity (specific numbers, names, metrics)
        if _has_pattern(subject, r"\d{1,3}(%|x|hrs?|days?|weeks?|months?|people|founders|teams?|signals?|metrics?)"):
            score += 5
        elif _has_pattern(subject, r"\b(metric|retention|founders?|teams?|operators?|manual|pipeline|revenue|calendar|handoff|churn)\b"):
            score += 3
        elif _has_pattern(subject, r"[A-Z][a-z]+ [A-Z][a-z]+"):  # Proper name
            score += 3

        # Subject: under 9 words
        word_count = len(subject.split())
        if word_count <= 9:
            score += 3
        elif word_count <= 12:
            score += 1

        # Subject: no spam triggers
        spam = _load_list(self.guardrails, "spam_triggers")
        for word in spam:
            if word.lower() in subject.lower():
                score -= 5
                flags.append(f"Spam trigger in subject: '{word}'")
                break

        # Opener: matches subject promise
        subject_keywords = _normalized_keywords(subject)
        body_keywords = _normalized_keywords(first_two)
        overlap = subject_keywords & body_keywords
        if len(overlap) >= 2:
            score += 4
        elif len(overlap) == 1:
            score += 2
        else:
            flags.append("Opener does not echo subject keywords")

        # Opener: speaks to known pain
        pain_words = _load_list(self.guardrails, "pain_signal_words")
        if any(w in first_two.lower() for w in pain_words):
            score += 3

        if specificity_points >= 4:
            score += 3

        # Opener: no filler phrases
        filler = _load_list(self.guardrails, "filler_openers")
        for phrase in filler:
            if phrase.lower() in first_two.lower():
                score -= 5
                flags.append(f"Filler opener: '{phrase}'")
                break

        return DimensionScore(
            score=max(0, score),
            max_score=25,
            flags=flags,
            passed=score >= 16,
        )

    # Dimension 2: psychological fit (0-20)

    def _score_psychological_fit(self, draft: EmailDraft, specificity_points: int) -> DimensionScore:
        score = 0
        flags = []
        campaign_config = self.campaigns.get("campaigns", {}).get(draft.campaign_type, {})
        expected_trigger = campaign_config.get("primary_trigger", "curiosity_gap")
        secondary_trigger = campaign_config.get("secondary_trigger")

        trigger_keywords = _load_nested(self.guardrails, f"triggers.{expected_trigger}.keywords", [])
        subject_lower = draft.subject.lower()
        body_lower = draft.body.lower()

        matches = sum(1 for kw in trigger_keywords if kw in subject_lower or kw in body_lower)
        score += min(matches * 5, 15)

        if secondary_trigger == "specificity":
            score += min(specificity_points, 5)
        elif secondary_trigger:
            secondary_keywords = _load_nested(self.guardrails, f"triggers.{secondary_trigger}.keywords", [])
            secondary_matches = sum(1 for kw in secondary_keywords if kw in subject_lower or kw in body_lower)
            score += min(secondary_matches * 3, 5)

        if matches == 0:
            flags.append(
                f"Expected trigger '{expected_trigger}' not detected in subject or body"
            )

        # Identity match (for trust campaigns)
        identity_words = _load_list(campaign_config, "identity_words")
        if identity_words:
            identity_hits = sum(1 for w in identity_words if w in body_lower)
            score += min(identity_hits * 3, 5)

        return DimensionScore(
            score=min(score, 20),
            max_score=20,
            flags=flags,
            passed=score >= 12,
        )

    # Dimension 3: brand voice (0-25)

    def _score_brand_voice(self, draft: EmailDraft) -> DimensionScore:
        score = 25
        flags = []
        full_text = f"{draft.subject} {draft.body}".lower()

        blacklist = self.brand_voice.get("blacklist", {})
        for category, terms in blacklist.items():
            for term in terms:
                if term.lower() in full_text:
                    score -= 10
                    flags.append(f"Blacklist [{category}]: '{term}'")
                    break  # one penalty per category

        # Tone match check
        tone_config = _load_nested(
            self.brand_voice, f"caption_tones.tones.{_tone_for_angle(draft.brand_angle)}", {}
        )
        no_go_words = _load_list(tone_config, "guardrails")
        for guard in no_go_words:
            if guard.replace("_", " ") in full_text:
                score -= 5
                flags.append(f"Tone guardrail violation: {guard}")

        return DimensionScore(
            score=max(0, score),
            max_score=25,
            flags=flags,
            passed=score >= 15,
        )

    # Dimension 4: professional guardrails (0-15)

    def _score_professional_guardrails(self, draft: EmailDraft) -> DimensionScore:
        score = 15
        flags = []
        subject = draft.subject.strip()
        body = draft.body.strip()

        # Length checks
        if len(subject.split()) > 9:
            score -= 3
            flags.append(f"Subject too long ({len(subject.split())} words, max 9)")

        body_word_count = len(body.split())
        if body_word_count > 200 and "\n" not in body:
            score -= 4
            flags.append(f"Body >200 words with no paragraph breaks")
        elif body_word_count > 150:
            score -= 1

        # No CTA
        cta_patterns = _load_list(self.guardrails, "cta_patterns")
        if not any(p in body.lower() for p in cta_patterns):
            score -= 4
            flags.append("No call-to-action detected")

        # Wall of text
        paragraphs = body.split("\n\n")
        longest = max(len(p.split()) for p in paragraphs) if paragraphs else body_word_count
        if longest > 80:
            score -= 2
            flags.append(f"Longest paragraph is {longest} words (max 80)")

        # Spam triggers in body
        spam = _load_list(self.guardrails, "spam_triggers")
        for word in spam:
            if word in body.lower():
                score -= 2
                flags.append(f"Spam trigger in body: '{word}'")
                break

        return DimensionScore(
            score=max(0, score),
            max_score=15,
            flags=flags,
            passed=score >= 9,
        )

    # Dimension 5: campaign alignment (0-15)

    def _score_campaign_alignment(self, draft: EmailDraft) -> DimensionScore:
        score = 10  # base: we have a campaign type
        flags = []
        campaign_config = self.campaigns.get("campaigns", {}).get(draft.campaign_type, {})
        stage = campaign_config.get("stage", "awareness")

        if stage != "awareness" and draft.previous_email_subject:
            prior_keywords = set(re.findall(r"[a-zA-Z]{4,}", draft.previous_email_subject.lower()))
            current_keywords = set(re.findall(r"[a-zA-Z]{4,}", draft.subject.lower()))
            if prior_keywords & current_keywords:
                score += 2

        # Campaign-specific checks
        expected_cta = _load_list(campaign_config, "expected_cta")
        if expected_cta:
            if any(c in draft.body.lower() for c in expected_cta):
                score += 3
            else:
                score -= 3
                flags.append(f"CTA type mismatch: expected one of {expected_cta}")

        return DimensionScore(
            score=max(0, score),
            max_score=15,
            flags=flags,
            passed=score >= 8,
        )


# Helpers


def _load_yaml(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _load_list(config: dict, key: str) -> list[str]:
    val = config
    for part in key.split("."):
        if isinstance(val, dict):
            val = val.get(part, {})
        else:
            return []
    return val if isinstance(val, list) else []


def _load_nested(config: dict, key: str, default: Any = None) -> Any:
    val = config
    for part in key.split("."):
        if isinstance(val, dict):
            val = val.get(part)
        else:
            return default
    return val if val is not None else default


def _has_pattern(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE))


def _normalized_keywords(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z]{4,}", text.lower()))


def _specificity_points(subject: str, body: str) -> int:
    text = f"{subject} {body}".lower()
    score = 0
    if re.search(r"\d{1,3}(%|x|hrs?|days?|weeks?|months?|people|founders|teams?|signals?|metrics?)", text):
        score += 3
    if re.search(r"\b(metric|retention|pipeline|handoff|calendar|revenue|churn|open rates?|ctr|manual|founders?|operators?|teams?)\b", text):
        score += 2
    if re.search(r"\b(almost no one|no one tracks|predicts?|benchmarks?|checklist|template)\b", text):
        score += 2
    return score


def _tone_for_angle(brand_angle: str) -> str:
    mapping = {"b2b": "professional_genx", "b2c": "warm", "both": "professional_genx"}
    return mapping.get(brand_angle, "professional_genx")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate an email draft against the GenX email gate.")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", required=True, help="Email body or opener")
    parser.add_argument("--campaign-type", default="value", choices=["value", "trust_building", "launch", "re_engagement"])
    parser.add_argument("--brand-angle", default="b2b", choices=["b2b", "b2c", "both"])
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = EmailGate().evaluate(
        EmailDraft(
            subject=args.subject,
            body=args.body,
            campaign_type=args.campaign_type,
            brand_angle=args.brand_angle,
        )
    )
    if args.json:
        print(
            json.dumps(
                {
                    "verdict": result.verdict,
                    "total": result.total,
                    "max_total": result.max_total,
                    "dimensions": {
                        "attention": result.attention.score,
                        "psychological_fit": result.psychological_fit.score,
                        "brand_voice": result.brand_voice.score,
                        "professional_guardrails": result.professional_guardrails.score,
                        "campaign_alignment": result.campaign_alignment.score,
                    },
                },
                indent=2,
            )
        )
    else:
        print(result.feedback)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
