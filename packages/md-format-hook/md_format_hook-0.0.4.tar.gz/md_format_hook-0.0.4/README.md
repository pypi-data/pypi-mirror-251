# md-format
A pre-commit hook that formats .md files. It automatically adds reasonable spaces between Chinese and English and corrects the case of special nouns.

For pre-commit: see https://github.com/pre-commit/pre-commit

## Using md-format with pre-commit
Add this to your `.pre-commit-config.yaml` :

```yaml
- repo: https://github.com/PKUcoldkeyboard/md-format
  rev: 0.0.4
  hooks:
  - id: md-format
```
