
import asyncio
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from spine.chapters.hitl.guardrails import validate_url, SafetyViolation
import logging

logger = logging.getLogger(__name__)

class SafeBrowserService:
    _browser: Optional[Browser] = None
    _playwright = None

    async def start(self):
        if not self._playwright:
            self._playwright = await async_playwright().start()
        
        if not self._browser:
            # Launch chromium in headless mode
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox'] # Standard for container environments
            )
            logger.info("SafeBrowserService started.")

    async def stop(self):
        if self._browser:
            await self._browser.close()
            self._browser = None
        
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
            logger.info("SafeBrowserService stopped.")

    async def fetch_page(self, url: str, timeout_ms: int = 15000) -> Dict[str, Any]:
        """
        Safely fetches a page and returns title, text content, and screenshot (if feasible).
        """
        try:
            # 1. Guardrail Check
            validate_url(url)
        except SafetyViolation as e:
            logger.warning(f"Blocked URL fetch attempt: {url} - {str(e)}")
            raise

        if not self._browser:
            await self.start()

        context: BrowserContext = await self._browser.new_context(
            user_agent="AssistantsCo/1.0 (SafeBrowser; +https://assistants.co)",
            viewport={"width": 1280, "height": 720}
        )
        
        page: Page = await context.new_page()
        
        try:
            # 2. Navigate with Timeout
            response = await page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            
            if not response:
                raise Exception("No response from page")

            # 3. Extract Data
            title = await page.title()
            content = await page.content() # Full HTML
            text = await page.inner_text("body") # Text only
            
            # Simple metadata extraction
            result = {
                "url": url,
                "status": response.status,
                "title": title,
                "text_preview": text[:1000], # Limit return size
                "html_length": len(content)
            }
            
            return result

        except Exception as e:
            logger.error(f"Browser fetch failed for {url}: {e}")
            raise
        finally:
            # 4. Cleanup Context (Essential for privacy/isolation)
            await context.close()
