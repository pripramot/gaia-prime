# PRIAM: GAIA PRIME Master Orchestrator

> คือความพยายามเชิงยุทธศาสตร์ในการสร้างโครงสร้างพื้นฐานด้านความมั่นคงทางดิจิทัลที่ยั่งยืนและพึ่งพาตนเองได้

**PRIAM** คือสถาปัตยกรรม Nx Monorepo แบบ Local-first 100% ทำหน้าที่เป็นโครงสร้างพื้นฐานสำหรับ **GAIA PRIME** (Master Orchestrator) ในการควบคุมและจัดการ AI Agents เฉพาะทางด้านนิติวิทยาศาสตร์ ความมั่นคง และข่าวกรองยุทธวิธี

## 🪐 Core Architecture

- **Environment:** Air-gapped / No-Internet Dependency
- **Monorepo Manager:** Nx (Telemetry Disabled: Strict)
- **Local BaaS (Backend-as-a-Service):** Supabase (Self-Hosted)
- **Protocol:** Model Context Protocol (MCP) สำหรับการสื่อสารระหว่าง Agent
- **Data Bridge:** Rclone Volume Mapping สำหรับจัดการ Asset ขนาดใหญ่แบบ Standalone

## 🛡️ Tactical Sub-Systems (Agents)

| # | Agent | Description |
|---|-------|-------------|
| 1 | **ภูผาแดง (Phuphadang Alpha AI)** | Core AI สำหรับการวิเคราะห์ Digital Forensics |
| 2 | **C.H.R.O.N.O.S.** | Mobile Tracking, Geo-Intelligence และ Sovereign Map (Supabase PostGIS + MapLibre) |
| 3 | **UNICORN** | ชุดเครื่องมือ Cyber Security และ Hardening |
| 4 | **GtsAlpha Wallet** | Web3 Smart Contracts (React Native / Expo / Supabase) |
| 5 | **ms-mcp-flutter** | เชื่อมต่อข้อมูล Microsoft Build/Graph APIs ระดับ Local |

## 🛠️ Tech Stack

- **Database & BaaS:** Supabase Local (PostgreSQL, PostGIS, Realtime, Auth, Storage)
- **Backend / MCP Servers:** Python (FastAPI), Go
- **Frontend / Dashboard:** Node.js, Next.js 14 (App Router), React, MapLibre GL JS
- **Mobile Development:** Flutter (Strict `snake_case`), React Native
- **Local MCP State:** SQLite

## 📁 Monorepo Structure

```
gaia-prime/
├── apps/
│   ├── gaia-prime-dashboard/   # Main orchestrator dashboard (Next.js 14)
│   ├── chronos-tracker/        # C.H.R.O.N.O.S. Geo-Intelligence app
│   └── gtsalpha-wallet/        # GtsAlpha Web3 wallet app
├── libs/
│   ├── shared/
│   │   ├── types/              # Shared TypeScript type definitions
│   │   └── utils/              # Common utility functions
│   └── mcp/
│       └── core/               # MCP protocol core library
├── tools/
│   └── scripts/                # Automation and lockdown scripts
├── docs/                       # Project documentation
├── nx.json                     # Nx workspace configuration
├── tsconfig.base.json          # Base TypeScript configuration
└── package.json                # Root package manifest
```

## 🚀 Getting Started

### Prerequisites

- Node.js >= 20.0.0
- Python >= 3.10
- Docker Desktop (สำหรับรัน Supabase Local)
- Supabase CLI
- Nx CLI (Global)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd gaia-prime

# Install dependencies
npm install

# Run telemetry lockdown (REQUIRED for air-gapped operation)
bash tools/scripts/telemetry-lockdown.sh
```

### Security Notice (Telemetry Lockdown)

ระบบนี้ปฏิเสธการส่งข้อมูลกลับ Cloud ทุกกรณี ตรวจสอบให้แน่ใจว่า Nx Telemetry ถูกปิดก่อนเริ่มงาน:

```bash
npx nx telemetry status
# Expected output: Nx telemetry is currently disabled.
```

### Verify Workspace

```bash
# List all projects in the monorepo
npx nx show projects

# View project graph
npx nx graph
```

## 📜 License

UNLICENSED - Proprietary and Confidential
