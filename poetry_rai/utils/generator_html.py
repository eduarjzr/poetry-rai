from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

class HtmlGenerator:
    def __init__(self, time_sleep: int = 1) -> None:
        self.time_sleep = time_sleep

    def save_from_url(self, url: str, output_file_name: str = "new_html.html"):
        assert url, "You must provide a valid URL"

        # Set browser options to disable the display of the header and footer bar during printing
        chrome_options = Options()
        chrome_options.add_argument('--kiosk-printing')

        # Abrir el navegador
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Load page
            driver.get(url=url)

            # Wait a few seconds to make sure the page loads completely
            time.sleep(self.time_sleep)

            # Get the source code of the web page
            html_source = driver.page_source

            # Save the source code to an HTML file
            with open(output_file_name, "w", encoding="utf-8") as html_file:
                html_file.write(html_source)

            print(f"The file '{output_file_name}' has been successfully generated")

        finally:
            # Close the browser
            driver.quit()