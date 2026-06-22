# Carousel Output Vault

Generated carousel jobs are saved here.

Expected package shape:

```text
<date-topic-page>/
  manifest.json
  brief.md
  generation-log.md
  assets/
    bg-slide-01.png
    final-slide-01.png
  exports/
    instagram/
      slide-01.png
    facebook/
      slide-01.png
```

Rules:

- Keep one folder per carousel job.
- `manifest.json` is the source of truth for revisions.
- Text edits should update the manifest and re-render with Pillow.
- Background edits should regenerate only affected visual layers when possible.
- Replicate/MCP may create backgrounds, but final text is always local-rendered.
- Do not publish/export externally without human approval.
