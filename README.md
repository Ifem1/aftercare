# AFTERCARE

AFTERCARE retroactively funds the people who kept important things from breaking.

This repository contains the Next.js App Router frontend and the `contracts/aftercare.py` Intelligent Contract. The frontend is currently configured for StudioNet through `NEXT_PUBLIC_GENLAYER_CHAIN`; set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` after deployment.

## Status

The interface and contract source are implemented. The verified StudioNet contract is `0x833668ebd3D48331d3B8118a16F6bC22AB449303`. Its schema exposes round creation/funding, claim submission, evidence assessment, and payout methods.

## Run locally

```bash
npm install
npm run dev
npm run build
```

The app demonstrates the full user journey and clearly labels the consensus lifecycle. The contract keeps the funding pool and claim state on-chain, independently retrieves frozen evidence during assessment, bounds verdicts, abstains on insufficient evidence, and prevents duplicate payouts. StudioNet smoke testing completed round creation, round read, 1 GEN funding, claim submission, claim read, and finalized consensus assessment.
