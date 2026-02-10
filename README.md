# Cube Crafter Discord Bot

[![Servers](https://img.shields.io/badge/dynamic/json?label=Servers&query=%24.stats.guilds&url=https%3A%2F%2Fdiscordbotlist.com%2Fapi%2Fv1%2Fbots%2F1197268536918278236&color=blue&logo=discord)](https://discordbotlist.com/bots/cube-crafter)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cube Crafter** is a high-performance Discord bot designed for the cubing community. It provides official WCA scrambles, visual cube representations, and a robust personal timing system directly within your Discord server.

[**Visit Official Website**](https://cubecrafter.azurewebsites.net/) | [**Invite Bot**](https://discord.com/api/oauth2/authorize?client_id=1197268536918278236&permissions=2147483648&scope=bot%20applications.commands)

---

## Key Features

- **WCA Scrambles:** Generate high-quality scrambles for all official WCA puzzles (2x2 - 7x7, Megaminx, Pyraminx, etc.).
- **Visual Representations:** Every scramble comes with a 2D image of the scrambled state to help you verify your scramble.
- **Personal Stopwatch:** Time your solves with an interactive stopwatch view.
- **Solve History:** Track your progress with a database-backed history system.
- **WCA Averages:** Automatically calculates **Average of 5 (Ao5)** and **Average of 12 (Ao12)** according to WCA standards (removing best/worst solves).
- **Per-Puzzle Tracking:** Keeps your history organized by puzzle type with a 15-entry limit per puzzle to keep your data relevant.
- **Algorithm Library:** Access OLL and PLL algorithm guides with visual aids.

---

## 
Commands

| Command | Description |
| :--- | :--- |
| `/scramble [puzzle]` | Generates a scramble and visual for the specified puzzle. |
| `/stopwatch [puzzle]` | Launches an interactive timer to record a new solve. |
| `/time [puzzle]` | Displays your 15 most recent solves and current averages for a puzzle. |
| `/delete_time [id]` | Removes a specific solve from your history using its TimeID. |
| `/oll [group]` | View OLL algorithms with visual guides and pagination. |
| `/pll [group]` | View PLL algorithms with visual guides and pagination. |
| `/invite` | Generates invite link. |

---

##  Technical Stack

- **Language:** Python 3.12 (`discord.py`)
- **Database:** Azure SQL (managed via `pyodbc`)
- **Storage:** Azure Blob Storage (for algorithm images)
- **Infrastructure:** Dockerized and hosted on Azure.

---

## 📊 Bot Stats

[![](https://discordbotlist.com/api/v1/bots/1197268536918278236/widget)](https://discordbotlist.com/bots/cube-crafter)
![Discord Bots](https://top.gg/api/widget/1197268536918278236.svg)
---
© 2024 Cube Crafter. All rights reserved.