import aiohttp
import asyncio


SOIL_API = "https://api.india.gov.in/soil-data?state={state}&district={district}"
RAINFALL_API = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum"
WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
SEASON_API = "https://api.season-data.com?state={state}&district={district}" 
GEOCODE_API = "https://nominatim.openstreetmap.org/search?district={district}&state={state}&format=json&limit=1"

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()

# 1. Get lat/lon from district + state
async def get_lat_lon(session, state, district):
    url = GEOCODE_API.format(state=state, district=district)
    data = await fetch_json(session, url)
    if data:
        return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    return {"lat": None, "lon": None}

# 2. Get soil data
async def get_soil_data(session, state, district):
    url = SOIL_API.format(state=state, district=district)
    data = await fetch_json(session, url)
    return {
        "soil_ph": data.get("ph"),
        "soil_type": data.get("type")
    }

# 3. Get rainfall
async def get_rainfall_data(session, lat, lon):
    url = RAINFALL_API.format(lat=lat, lon=lon)
    data = await fetch_json(session, url)
    return {"rainfall": data["daily"]["precipitation_sum"][0]}

# 4. Get weather
async def get_weather_data(session, lat, lon):
    url = WEATHER_API.format(lat=lat, lon=lon)
    data = await fetch_json(session, url)
    return {"temperature": data["current_weather"]["temperature"]}

# 5. Get season data
async def get_season_data(session, state, district):
    url = SEASON_API.format(state=state, district=district)
    data = await fetch_json(session, url)
    return {"season": data.get("season")}

# Main Orchestrator
async def fetch_state_info(state, district):
    async with aiohttp.ClientSession() as session:
        # Start tasks that don't need lat/lon
        soil_task = asyncio.create_task(get_soil_data(session, state, district))
        season_task = asyncio.create_task(get_season_data(session, state, district))
        
        # Start lat/lon lookup
        latlon_task = asyncio.create_task(get_lat_lon(session, state, district))
        
        # Wait for lat/lon first
        latlon = await latlon_task
        lat, lon = latlon["lat"], latlon["lon"]
        
        # Now fetch rainfall + weather in parallel
        rain_task = asyncio.create_task(get_rainfall_data(session, lat, lon))
        weather_task = asyncio.create_task(get_weather_data(session, lat, lon))
        
        # Gather everything
        results = await asyncio.gather(soil_task, season_task, rain_task, weather_task)
        
        state_info = {}
        for r in results:
            state_info.update(r)
        
        return state_info


# Example usage:
# asyncio.run(fetch_state_info("Haryana", "Gurugram"))
