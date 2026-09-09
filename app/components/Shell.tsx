'use client';
import Link from 'next/link';
export default function Shell({children}:{children:React.ReactNode}){return <><header className="appbar"><Link href="/" className="logo"><span>✦</span> AFTERCARE</Link><nav><Link href="/rounds">Funding rounds</Link><Link href="/studio">Submit a claim</Link><Link href="/claims">My claims</Link></nav><button className="connect">Connect wallet</button></header><div className="networkbar"><span className="dot green"/> StudioNet <span className="muted">·</span> contract connected <span className="contract">0xff5a…8044</span></div>{children}</>}
