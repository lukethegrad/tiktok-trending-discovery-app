import asyncio
from playwright.async_api import async_playwright

IPHONE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
)

async def scrape_spotify_label(song_title: str, artist_name: str):
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=True)
        context = await browser.new_context(
            user_agent=IPHONE_USER_AGENT,
            viewport={"width": 375, "height": 812},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
        )
        page = await context.new_page()

        query = f"{song_title} {artist_name}".replace(" ", "%20")
        search_url = f"https://open.spotify.com/search/{query}"
        await page.goto(search_url, timeout=60000)

        try:
            await page.wait_for_selector('a[href^="/track/"]', timeout=10000)
            track_link = await page.query_selector('a[href^="/track/"]')
            await track_link.click()
            await page.wait_for_timeout(3000)
        except Exception:
            await browser.close()
            return {"error": "Track not found on Spotify"}

        try:
            track_title = await page.text_content('h1[data-testid="nowplaying-track-link"]')
            artist = await page.text_content('span[data-testid="nowplaying-artist"] a')
        except Exception:
            track_title = song_title
            artist = artist_name

        try:
            album_button = await page.query_selector('a[href^="/album/"]')
            await album_button.click()
            await page.wait_for_timeout(3000)
        except Exception:
            await browser.close()
            return {"error": "Could not access album page"}

        try:
            album_title = await page.text_content('h1[data-testid="entityTitle"]')
            label_block = await page.text_content('span[class*="Type__TypeElement"] >> text=/℗/')
            label_text = label_block.strip() if label_block else "Unknown"
        except Exception:
            album_title = "Unknown"
            label_text = "Unknown"

        await browser.close()
        return {
            "track": track_title,
            "artist": artist,
            "album": album_title,
            "label": label_text,
        }

