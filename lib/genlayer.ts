import { createAccount, createClient, generatePrivateKey } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import type { Address } from 'viem';
export const contractAddress = process.env.NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS as Address | undefined;
export function getStoredAccount() { if (typeof window === 'undefined') return null; let key = window.localStorage.getItem('aftercare.privateKey'); if (!key) { key = generatePrivateKey(); window.localStorage.setItem('aftercare.privateKey', key); } return createAccount(key as `0x${string}`); }
export function getClient() { return createClient({ chain: studionet, account: getStoredAccount() ?? undefined }); }
function requireAddress() { if (!contractAddress) throw new Error('Set NEXT_PUBLIC_AFTERCARE_CONTRACT_ADDRESS before using the app.'); return contractAddress; }
export async function waitFor(hash: string) { return getClient().waitForTransactionReceipt({ hash: hash as never }); }
export async function readContract<T>(functionName: string, args: any[] = []) { return getClient().readContract({ address: requireAddress(), functionName, args }) as Promise<T>; }
export async function writeContract(functionName: string, args: any[] = [], value = BigInt(0)) { const account = getStoredAccount(); if (!account) throw new Error('Wallet unavailable.'); const hash = await getClient().writeContract({ address: requireAddress(), functionName, args, value, account }); return { hash, receipt: await waitFor(String(hash)) }; }
export async function submitClaim(roundId: string, title: string, description: string, period: string, evidence: string[]) { return writeContract('submit_claim', [roundId, title, description, period, evidence.join(',')]); }
export async function getRound(roundId: string) { return readContract<string>('get_round', [roundId]); }
export async function getClaim(claimId: string) { return readContract<string>('get_claim', [claimId]); }
export async function getCounts() { const [rounds, claims] = await Promise.all([readContract<bigint>('get_round_count'), readContract<bigint>('get_claim_count')]); return { rounds: Number(rounds), claims: Number(claims) }; }
export function parseRecord(raw: string) { return JSON.parse(raw) as Record<string, any>; }
export function explorerUrl(hash: string) { return `https://genlayer-explorer.vercel.app/tx/${hash}`; }
export function activeAddress() { return getStoredAccount()?.address?.toLowerCase() ?? ''; }
export function exportPrivateKey() { if(typeof window==='undefined') return ''; return window.localStorage.getItem('aftercare.privateKey')||''; }
export function importPrivateKey(key:string) { if(!/^0x[0-9a-fA-F]{64}$/.test(key)) throw new Error('Private key must be 32-byte hex.'); if(typeof window!=='undefined'&&window.localStorage.getItem('aftercare.privateKey')) throw new Error('A browser wallet already exists; export or clear it explicitly first.'); if(typeof window!=='undefined') window.localStorage.setItem('aftercare.privateKey',key); return createAccount(key as `0x${string}`).address; }
export async function createRound(title:string, description:string, closesAt:string) { return writeContract('create_round',[title,description,closesAt]); }
export async function fundRound(roundId:string, amount:string) { const value=BigInt(Math.round(Number(amount)*1e18)); if(value<=0n) throw new Error('Enter a positive GEN amount.'); return writeContract('fund_round',[roundId],value); }
export async function assessClaim(claimId:string) { return writeContract('assess_claim',[claimId]); }
export async function claimPayout(claimId:string) { return writeContract('claim_payout',[claimId]); }
export async function connectInjectedWallet() { const provider = (window as Window & { ethereum?: { request: (args: { method: string }) => Promise<string[]> } }).ethereum; if (!provider) return null; const accounts = await provider.request({ method: 'eth_requestAccounts' }); if (!accounts[0]) return null; const client = createClient({ chain: studionet, account: accounts[0] as Address, provider }); await client.connect('studionet'); return accounts[0]; }
