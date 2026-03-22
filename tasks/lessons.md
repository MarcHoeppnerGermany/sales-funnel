# Lessons Learned

## 2026-03-22: Initiales Setup
- **Keine externen API-Keys voraussetzen**: Wenn das Tool innerhalb von Claude Code läuft, sind WebSearch/WebFetch bereits verfügbar. Kein Anthropic SDK oder Brave API nötig.
- **Linter-Änderungen sofort committen**: Wenn der Linter Dateien ändert, diese nicht ignorieren sondern direkt mit-committen.
