# AFTERCARE

AFTERCARE retroactively funds the people who kept important things from breaking.

This repository contains the Next.js App Router frontend and the `contracts/aftercare.py` Intelligent Contract. The frontend is currently configured for StudioNet through `NEXT_PUBLIC_GENLAYER_CHAIN`; set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` after deployment.

## Status

The interface and contract source are implemented. The verified StudioNet contract is `0xfAcC18877B3618BBE2DAE905da28de5F98362b4c`. Its schema exposes round creation/funding, claim submission, independent evidence assessment, deterministic payout accounting, and claimant-only GEN payout.

## Run locally

```bash
npm install
npm run dev
npm run build
```

The app wires claim submission, live reads, wallet connection, and transaction receipt lifecycle to GenLayer JS. The contract keeps funding and claim state on-chain, independently retrieves frozen evidence during comparative assessment, bounds verdicts, abstains on insufficient evidence, and prevents duplicate or unauthorized payouts. Set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` to the deployed address before Vercel deployment.

## Verified StudioNet evidence

Final contract: `0xfAcC18877B3618BBE2DAE905da28de5F98362b4c` ([explorer](https://genlayer-explorer.vercel.app)). The reproducible integration runner is `npm run test:integration` and requires `AFTERCARE_INTEGRATION_PRIVATE_KEY` locally. The latest run created `round_3`, funded it with 1 GEN (`0xb1902edf974a00b641cfce90f9b6b4410e761bfb788064a155fe7f65a5d77133`), submitted `claim_2` (`0x5ab0984a4cf656e5a31cea98fa9a06860e2926b1b788228aac2a76dd051de716`), and finalized assessment (`0x7c6622663d866d0b2ff47fcad67e6ce8d2f7f3e74827b81bed9dde39fc5fa016`). Validators returned `insufficient_evidence` and the deterministic payout was `0`; no payout transaction was attempted. This is an honest abstention result, not a positive payout proof.

Live frontend: https://aftercare-wheat.vercel.app/
