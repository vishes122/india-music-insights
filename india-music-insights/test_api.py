#!/usr/bin/env python3
"""
Test script for India Music Insights API
"""

import asyncio
import httpx
import json
from datetime import datetime


class APITester:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.admin_key = "india_music_insights_admin_2025"
    
    async def test_health(self):
        """Test health endpoint"""
        print("🔍 Testing health endpoint...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/v1/health")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ API Status: {data.get('status')}")
                    print(f"   ✅ Database: {data.get('database')}")
                    print(f"   ✅ Spotify API: {data.get('spotify_api')}")
                    print(f"   ✅ Cache: {data.get('cache_status')}")
                    return True
                else:
                    print(f"   ❌ Health check failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Health check error: {e}")
                return False
    
    async def test_root(self):
        """Test root endpoint"""
        print("\n🏠 Testing root endpoint...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ App Name: {data.get('name')}")
                    print(f"   ✅ Version: {data.get('version')}")
                    print(f"   ✅ Markets: {data.get('markets')}")
                    return True
                else:
                    print(f"   ❌ Root endpoint failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Root endpoint error: {e}")
                return False
    
    async def test_ingest(self, market: str = "IN"):
        """Test manual ingestion"""
        print(f"\n📥 Testing ingestion for market {market}...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                headers = {"X-Admin-Key": self.admin_key}
                response = await client.post(
                    f"{self.base_url}/v1/admin/ingest/run?market={market}",
                    headers=headers
                )
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Success: {data.get('success')}")
                    print(f"   ✅ Tracks processed: {data.get('tracks_processed')}")
                    print(f"   ✅ Artists processed: {data.get('artists_processed')}")
                    print(f"   ✅ Duration: {data.get('duration_seconds'):.2f}s")
                    print(f"   ✅ Message: {data.get('message')}")
                    return True
                else:
                    print(f"   ❌ Ingestion failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Ingestion error: {e}")
                return False
    
    async def test_today_chart(self, market: str = "IN"):
        """Test today's chart endpoint"""
        print(f"\n📊 Testing today's chart for market {market}...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/v1/charts/top-today?market={market}&limit=5")
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Market: {data.get('market')}")
                    print(f"   ✅ Snapshot Date: {data.get('snapshot_date')}")
                    print(f"   ✅ Total Tracks: {data.get('total_tracks')}")
                    
                    tracks = data.get('tracks', [])
                    if tracks:
                        print("   ✅ Top 3 tracks:")
                        for i, track in enumerate(tracks[:3], 1):
                            print(f"      {i}. {track['track_name']} - {', '.join(track['artists'])}")
                    
                    return True
                else:
                    print(f"   ❌ Today chart failed: {response.text}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Today chart error: {e}")
                return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting India Music Insights API Tests")
        print("=" * 50)
        
        results = []
        
        # Test basic endpoints
        results.append(await self.test_health())
        results.append(await self.test_root())
        
        # Test ingestion (this will populate the database)
        ingest_success = await self.test_ingest()
        results.append(ingest_success)
        
        # Only test today's chart if ingestion was successful
        if ingest_success:
            results.append(await self.test_today_chart())
        else:
            print("\n⚠️  Skipping today's chart test due to failed ingestion")
        
        print("\n" + "=" * 50)
        print("🎯 Test Results Summary:")
        print(f"   Total tests: {len(results)}")
        print(f"   Passed: {sum(results)}")
        print(f"   Failed: {len(results) - sum(results)}")
        
        if all(results):
            print("   🎉 All tests passed!")
        else:
            print("   ⚠️  Some tests failed")
        
        return all(results)


async def main():
    tester = APITester()
    success = await tester.run_all_tests()
    return success


if __name__ == "__main__":
    asyncio.run(main())
