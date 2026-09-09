# AFTERCARE

AFTERCARE retroactively funds the people who kept important things from breaking.

This repository contains the Next.js App Router frontend and the `contracts/aftercare.py` Intelligent Contract. The frontend is currently configured for StudioNet through `NEXT_PUBLIC_GENLAYER_CHAIN`; set `NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS` after deployment.

## Status

The interface and contract source are implemented. Production build passes. A live StudioNet deployment, contract integration tests, and GitHub push require network access and credentials available to the operator. No deployment or transaction success is claimed by this repository until those steps are run.

## Run locally

```bash
npm install
npm run dev
npm run build
```

The app demonstrates the full user journey and clearly labels the consensus lifecycle. The contract keeps the funding pool and claim state on-chain, independently retrieves frozen evidence during assessment, bounds verdicts, abstains on insufficient evidence, and prevents duplicate payouts.
