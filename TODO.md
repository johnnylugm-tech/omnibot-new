# TODO — omnibot-new

## [TECH-DEBT] omnibot/ → app/ 套件遷移

**背景**：目前 `03-development/src/` 下有兩個套件共存：
- `omnibot/` — Phase 1 實作，測試仍依賴 `omnibot.*` imports（FR-04、FR-05、FR-06、FR-08、FR-09 等）
- `app/` — Phase 2/3 目標結構，目前只有 `models.py` 和 `infrastructure/config.py`

**現況**：SAD.md SAB block 已用真實相對路徑（`03-development/src/omnibot/security/` 等）登記所有 `omnibot/` 檔案，drift detector 不再誤報。

**待辦**：每個 FR 逐步在 `app/` 實作時，同步執行以下三步：
1. 將對應 `omnibot/` module 移至 `app/<layer>/<module>.py`
2. 更新 `tests/` 的 import（`from omnibot.x` → `from app.x`）
3. 更新 SAD.md SAB block 對應 layer 的 `modules[]`，移除 `omnibot/` 路徑、改為 `app/` 路徑，並執行 `python3 harness/scripts/generate_sab.py --project .` 重新生成 SAB.json

**參考遷移對照表**：

| SAD 邏輯名稱 | 現在位置 | 目標位置 |
|---|---|---|
| `security` layer | `omnibot/security/` | `app/security/` |
| `adapters` layer | `omnibot/adapters/`, `omnibot/models/` | `app/adapters/`, `app/models/` |
| `processing` layer | `omnibot/processing/` | `app/processing/` |
| `knowledge` layer | `omnibot/knowledge/`, `omnibot/escalation/` | `app/knowledge/` |
| `infrastructure` layer | `omnibot/logging/`, `omnibot/errors/`, `omnibot/config.py` | `app/infrastructure/` |
| `transport` layer | — | `app/api/webhooks.py`（尚未實作） |

**不緊急**：目前 SAB drift score 92%，gate 評估正常，不影響 FR 開發流程。
