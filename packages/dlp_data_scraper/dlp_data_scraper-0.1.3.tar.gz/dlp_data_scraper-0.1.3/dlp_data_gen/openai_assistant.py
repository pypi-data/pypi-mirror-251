import os
import sys
import time

from colorama import Fore, Style
from fpdf import FPDF
from py_openai_assistant.Assistant import Assistant
from py_openai_assistant.FileManager import FileManager

from file_utils.FileUtils import FileUtils


class OpenAIAssistant:
    def __init__(self, dlp_categories_file="dlp/dlp_categories.md", text_data="./text_data", pdf_data="./pdf_data"):
        self.text_data = text_data
        self.pdf_data = pdf_data
        self.assistant = Assistant(api_key=os.getenv("OPENAI_API_KEY"), data_folder=self.text_data)
        self.assistant.create(name="DLP Test Data Assistant",
                              instructions="You are an assistant that will provide Data Loss "
                                           "Preventing mock data for different categories")
        self.fm = FileManager(assistant=self.assistant)
        self.fm.file_db["ASSISTANT_ID"] = self.assistant.assistant_id
        self.dlp_categories_file = dlp_categories_file
        self.file_utils = FileUtils()

    def run(self):
        print(f"{Fore.BLUE}Starting DLP Data Generation {Style.RESET_ALL}\n")
        if self.fm.upload_file(self.dlp_categories_file, "DLP Categories") is None:
            raise ValueError("File upload failed")

        # Start time
        start_time = time.time()
        thread, run = self.assistant.create_thread_and_run(
            "I will give you a file with DLP categories and you will give me "
            "mock data for each category. The mock data should be structurally valid. "
            "Mock data for languages other then english should use the their character set"
            " and therefore response should be in UTF-8. Do not add additional "
            "commentary")
        self.assistant.check_run(thread.id, run.id)
        # End time
        end_time = time.time()
        # Calculate elapsed time in seconds
        elapsed_time = end_time - start_time
        print(f"{Fore.BLUE}Elapsed time: {elapsed_time}, seconds{Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA} Saving DLP Data... {Style.RESET_ALL}\n")
        filepath = self.assistant.save_last_message_to_file(self.assistant.get_response(thread), "dlp_data.txt")
        self.file_utils.convert_single_txt_to_pdf(os.path.basename(filepath), self.text_data, self.pdf_data)

