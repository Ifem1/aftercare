# AFTERCARE

AFTERCARE retroactively funds the people who kept important things from breaking.

This repository contains the Next.js App Router frontend and the `contracts/aftercare.py` Intelligent Contract. The frontend is currently configured for StudioNet through `NEXT_PUBLIC_GENLAYER_CHAIN`; set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` after deployment.

## Status

The interface and contract source are implemented. The verified StudioNet contract is `0x5FF044EF2a3f7aca1B69A16B5428FF777C6AD433`. Its schema exposes round creation/funding, claim submission, independent evidence assessment, deterministic payout accounting, and claimant-only GEN payout.

## Run locally

```bash
npm install
npm run dev
npm run build
```

The app wires claim submission and transaction receipt lifecycle to GenLayer JS. The contract keeps funding and claim state on-chain, independently retrieves frozen evidence during comparative assessment, bounds verdicts, abstains on insufficient evidence, and prevents duplicate or unauthorized payouts. StudioNet schema verification and a fresh round-creation smoke transaction completed successfully. Set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` to the deployed address before Vercel deployment.
