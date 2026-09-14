import { NextResponse } from 'next/server';

const catalog = [
  { id: 'series_001', title: 'Ishq Ke Raaz', language: 'hi-IN', genre: 'romance', format: 'vertical_9_16', episodeCount: 18, access: 'mixed' },
  { id: 'series_002', title: 'Gully Ke Dost', language: 'hi-IN', genre: 'comedy', format: 'vertical_9_16', episodeCount: 24, access: 'mixed' },
  { id: 'series_003', title: 'Dil Se Gujarat', language: 'gu-IN', genre: 'family', format: 'vertical_9_16', episodeCount: 16, access: 'mixed' },
];

export async function GET() {
  return NextResponse.json({ ok: true, version: 'v1', data: catalog }, { headers: { 'Cache-Control': 'public, max-age=60, stale-while-revalidate=300' } });
}
