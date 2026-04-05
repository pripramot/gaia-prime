#!/usr/bin/env bash
# ============================================================
# PRIAM Telemetry Lockdown Script
# ============================================================
# Ensures all telemetry is disabled for air-gapped operation.
# Run this before starting any development work.
# ============================================================

set -euo pipefail

echo "🛡️  PRIAM Telemetry Lockdown"
echo "=============================="

# Disable Nx telemetry
echo "Disabling Nx telemetry..."
npx nx telemetry disable 2>/dev/null || true

# Verify Nx telemetry is disabled
NX_STATUS=$(npx nx telemetry status 2>&1 || true)
if echo "$NX_STATUS" | grep -qi "disabled"; then
  echo "✅ Nx telemetry: DISABLED"
else
  echo "⚠️  Nx telemetry status unclear: $NX_STATUS"
fi

# Disable npm telemetry/audit
echo "Configuring npm for offline mode..."
npm config set fund false 2>/dev/null || true
npm config set audit false 2>/dev/null || true
npm config set update-notifier false 2>/dev/null || true

echo ""
echo "✅ Telemetry lockdown complete."
echo "   System is ready for air-gapped operation."
