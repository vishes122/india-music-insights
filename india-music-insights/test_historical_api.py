#!/usr/bin/env python3
"""
Test script for Historical Music Search API endpoints

Tests the new year-based search functionality to demonstrate
what years can be fetched from Spotify API.
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, Any

API_BASE = "http://localhost:8001/v1"


class HistoricalAPITester:
    def __init__(self):
        self.session: aiohttp.ClientSession = None
        self.results = []

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_endpoint(self, endpoint: str, description: str) -> Dict[str, Any]:
        """Test an API endpoint and return results"""
        print(f"\n🧪 Testing: {description}")
        print(f"📡 Endpoint: {endpoint}")
        
        try:
            async with self.session.get(f"{API_BASE}{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Extract key info
                    total_tracks = len(data.get("tracks", []))
                    total_available = data.get("total", 0)
                    
                    print(f"✅ SUCCESS: Found {total_tracks} tracks (Total available: {total_available})")
                    
                    # Show sample tracks
                    if data.get("tracks"):
                        print(f"📚 Sample tracks from results:")
                        for i, track in enumerate(data["tracks"][:3], 1):
                            release_date = track.get("album", {}).get("release_date", "Unknown")
                            artists = ", ".join([a["name"] for a in track.get("artists", [])])
                            print(f"  {i}. {track['name']} - {artists} ({release_date}) [Popularity: {track.get('popularity', 0)}]")
                    
                    result = {
                        "endpoint": endpoint,
                        "description": description,
                        "status": "success",
                        "tracks_found": total_tracks,
                        "total_available": total_available,
                        "data": data
                    }
                    
                else:
                    error_text = await response.text()
                    print(f"❌ FAILED: Status {response.status}")
                    print(f"Error: {error_text}")
                    
                    result = {
                        "endpoint": endpoint,
                        "description": description,
                        "status": "failed",
                        "error": error_text,
                        "status_code": response.status
                    }
                    
        except Exception as e:
            print(f"💥 ERROR: {str(e)}")
            result = {
                "endpoint": endpoint,
                "description": description,
                "status": "error",
                "error": str(e)
            }
        
        self.results.append(result)
        return result

    async def run_comprehensive_tests(self):
        """Run comprehensive historical search tests"""
        print("🚀 Starting Historical Music Search API Tests")
        print(f"🕐 Test started at: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # Test 1: Health check
        await self.test_endpoint("/health", "API Health Check")
        
        # Test 2: Search tracks from 2020 (recent year)
        await self.test_endpoint(
            "/search/tracks/year/2020?query=bollywood&limit=10",
            "Top Bollywood tracks from 2020"
        )
        
        # Test 3: Search tracks from 2015
        await self.test_endpoint(
            "/search/tracks/year/2015?query=hindi&limit=10",
            "Hindi tracks from 2015"
        )
        
        # Test 4: Search tracks from 2010
        await self.test_endpoint(
            "/search/tracks/year/2010?query=india&limit=10",
            "Indian tracks from 2010"
        )
        
        # Test 5: Search tracks from 2005
        await self.test_endpoint(
            "/search/tracks/year/2005?query=bollywood&limit=10",
            "Bollywood tracks from 2005"
        )
        
        # Test 6: Search tracks from 2000
        await self.test_endpoint(
            "/search/tracks/year/2000?query=hindi&limit=10",
            "Hindi tracks from year 2000"
        )
        
        # Test 7: Search tracks from 1995
        await self.test_endpoint(
            "/search/tracks/year/1995?query=bollywood&limit=10",
            "Bollywood tracks from 1995"
        )
        
        # Test 8: Search tracks from 1990
        await self.test_endpoint(
            "/search/tracks/year/1990?query=india&limit=10",
            "Indian tracks from 1990"
        )
        
        # Test 9: Search tracks from 1980
        await self.test_endpoint(
            "/search/tracks/year/1980?query=hindi&limit=10",
            "Hindi tracks from 1980"
        )
        
        # Test 10: Year range search (2018-2022)
        await self.test_endpoint(
            "/search/tracks/year-range/2018-2022?query=bollywood&limit=15",
            "Bollywood tracks from 2018-2022"
        )
        
        # Test 11: Year range search (2010-2015) 
        await self.test_endpoint(
            "/search/tracks/year-range/2010-2015?query=hindi&limit=15",
            "Hindi tracks from 2010-2015"
        )
        
        # Test 12: Top tracks of specific year
        await self.test_endpoint(
            "/search/top-of-year/2020?limit=10",
            "Top tracks of 2020"
        )
        
        # Test 13: Top tracks with genre filter
        await self.test_endpoint(
            "/search/top-of-year/2019?genre=bollywood&limit=10",
            "Top Bollywood tracks of 2019"
        )

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 80)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 80)
        
        successful_tests = [r for r in self.results if r["status"] == "success"]
        failed_tests = [r for r in self.results if r["status"] == "failed"]
        error_tests = [r for r in self.results if r["status"] == "error"]
        
        print(f"✅ Successful tests: {len(successful_tests)}")
        print(f"❌ Failed tests: {len(failed_tests)}")
        print(f"💥 Error tests: {len(error_tests)}")
        print(f"📊 Total tests: {len(self.results)}")
        
        # Show year coverage analysis
        print("\n📅 YEAR COVERAGE ANALYSIS:")
        print("-" * 50)
        
        year_results = {}
        for result in successful_tests:
            endpoint = result["endpoint"]
            if "/year/" in endpoint and result["tracks_found"] > 0:
                # Extract year from endpoint
                year_part = endpoint.split("/year/")[1].split("?")[0]
                if year_part.isdigit():
                    year = int(year_part)
                    year_results[year] = result["tracks_found"]
        
        if year_results:
            print("Years with available data:")
            for year in sorted(year_results.keys(), reverse=True):
                print(f"  📅 {year}: {year_results[year]} tracks found")
                
            oldest_year = min(year_results.keys())
            newest_year = max(year_results.keys())
            print(f"\n🕐 Historical range: {oldest_year} - {newest_year} ({newest_year - oldest_year} years)")
        
        # Show failed tests details
        if failed_tests:
            print(f"\n❌ Failed Tests Details:")
            for test in failed_tests:
                print(f"  • {test['description']}: {test.get('error', 'Unknown error')}")
        
        print(f"\n🕐 Tests completed at: {datetime.now().isoformat()}")

    async def save_detailed_results(self, filename: str = "historical_test_results.json"):
        """Save detailed test results to JSON file"""
        with open(filename, "w") as f:
            json.dump({
                "test_run_time": datetime.now().isoformat(),
                "total_tests": len(self.results),
                "successful_tests": len([r for r in self.results if r["status"] == "success"]),
                "results": self.results
            }, f, indent=2)
        print(f"💾 Detailed results saved to: {filename}")


async def main():
    """Main test function"""
    print("🎵 Historical Music Search API Test Suite")
    print("🔍 Testing year-based search capabilities\n")
    
    try:
        async with HistoricalAPITester() as tester:
            await tester.run_comprehensive_tests()
            tester.print_summary()
            await tester.save_detailed_results()
            
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test suite error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
