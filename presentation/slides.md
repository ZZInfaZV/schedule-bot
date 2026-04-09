---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    padding: 40px;
  }
  h1 {
    font-size: 2.2em;
    margin-bottom: 0.3em;
  }
  h2 {
    font-size: 1.6em;
    color: #4338ca;
    margin-bottom: 0.6em;
  }
  .title-info {
    font-size: 1.1em;
    color: #555;
    line-height: 1.8;
  }
  .feature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    font-size: 0.9em;
  }
  .links-table {
    width: 100%;
    font-size: 1em;
  }
  .link-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-bottom: 1px solid #e5e7eb;
  }
  .emoji {
    font-size: 2em;
  }
---

<!-- _class: lead -->

# 📅 Schedule Bot

### Zakhar Zaitcev
z.zaitcev@innopolis.university
CSE-05

---

## Context

| | |
|---|---|
| **End Users** | Students and faculty of Sirius University |
| **Problem** | Schedule in Google Sheets — inconvenient on phone, no quick search, hard to find a room or instructor |
| **Idea** | Schedule in one tap + AI bot that answers questions in natural language |

---

## Implementation

**How it was built:**
FastAPI web UI + Nanobot AI agent + MCP server + sync from Google Sheets → cache in SQLite

| Version 1 | Version 2 |
|---|---|
| LLM bot with natural language queries | "Whole week" button — bug fix (DAYS iteration) |
| Basic web chat | Fixed Google Sheets URL (typo in ID) |
| MCP server with 6 tools | Standalone web UI without LLM |
| Auto-sync from Sheets | README + MIT License |

**Feedback addressed:**
- "Whole week" showed "No classes" → **fixed**
- "What now?" showed incorrect information → **fixed**

---

## Demonstration

<div style="display:flex;justify-content:center;align-items:center;min-height:300px;">

### 🎬 Video Demonstration of Version 2

*[Insert recorded video (up to 2 min with voice)]*

</div>

---

<!-- _class: lead -->

## Links

<div style="display:flex; justify-content:space-around; margin-top:30px;">

<div style="text-align:center; flex:1;">

**📂 GitHub Repository**

`https://github.com/ZZInfaZV/schedule-bot`

![QR: GitHub](https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://github.com/ZZInfaZV/se-toolkit-hackathon)

</div>

<div style="text-align:center; flex:1;">

**🚀 Deployed Product**

`http://10.93.25.141:8080`

![QR: Live](https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=http://10.93.25.141:8080)

</div>

</div>
