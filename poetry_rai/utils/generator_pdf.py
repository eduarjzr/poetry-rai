import base64
import json
import time
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class PdfGenerator:
    """
     Simple use case:
        pdf_generator = PdfGenerator()
        pdf_generator.save_from_url('https://google.com')
    """
    driver = None

    def __init__(self, print_options: dict = None, time_sleep: int = 1) -> None:
        self.time_sleep = time_sleep
        
        # https://chromedevtools.github.io/devtools-protocol/tot/Page#method-printToPDF
        if not print_options:
            self.print_options = {
                'landscape': True,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'paperWidth': 11,
                'paperHeight': 17,
            }
        else:
            self.print_options = print_options

    def _get_pdf_from_url(self, url: str, *args, **kwargs) -> bytes:
        self.driver.get(url)

        time.sleep(self.time_sleep)  # allow the page to load, increase if needed

        # Readjust the size of the paper based on the size of the data
        result = self._send_devtools(self.driver, "Page.printToPDF")
        self.print_options['paperWidth'] = round( len(result['data']) % 11 ) * 10

        result = self._send_devtools(self.driver, "Page.printToPDF", self.print_options)
    
        return base64.b64decode(result['data'])

    @staticmethod
    def _send_devtools(driver: webdriver.Chrome, cmd: str, params: dict = {}) -> dict[str, str]:
        """
        Works only with chromedriver.
        Method uses cromedriver's api to pass various commands to it.
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)

        return response.get('value')

    def _generate_pdf(self, url: str) -> BytesIO:
        result = self._get_pdf_from_url(url)
        file = BytesIO()
        file.write(result)

        return file

    def save_from_url(self, url: str, output_file_name: str = "new_pdf.pdf") -> None:
        assert url, "You must provide a valid URL"

        webdriver_options = ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('--disable-gpu')

        pdf_file: BytesIO

        try:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=webdriver_options
            )
            pdf_file = self._generate_pdf(url=url)
        finally:
            self.driver.close()

        with open(output_file_name, "wb") as outfile:
            outfile.write(pdf_file.getbuffer())
        
        print(f"The file '{output_file_name}' has been successfully generated")