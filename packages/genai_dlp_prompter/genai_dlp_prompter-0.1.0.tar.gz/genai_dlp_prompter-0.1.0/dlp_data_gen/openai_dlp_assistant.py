import os
import time

from colorama import Fore, Style
from fpdf import FPDF
from py_openai_assistant.Assistant import Assistant
from py_openai_assistant.FileManager import FileManager

from file_utils.FileUtils import FileUtils


class OpenAIDLPAssistant:
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

    def read_categories(self):
        categories = []
        with open(self.dlp_categories_file, 'r') as file:
            for line in file:
                # Assuming each category is on a new line and prefixed with a number and period
                if line.strip() and line.lstrip('0123456789. ').startswith('**'):
                    # Extracting the category name
                    category = line.split('**')[1].strip()
                    categories.append(category)
        return categories

    def process_categories_in_batches(self, batch_size=30):
        # Read categories from the file
        categories = self.read_categories()

        # Split categories into batches
        for i in range(0, len(categories), batch_size):
            batch = categories[i:i + batch_size]
            self.process_batch(batch)

    def process_batch(self, batch):
        for category in batch:
            # Construct the prompt for the category
            prompt = f"Generate mock data for the category '{category}'. The mock data should be structurally valid. Mock data for languages other than English should use their character set and therefore response should be in UTF-8. Do not add additional commentary."

            # Make an API call to get mock data for the category
            # Assuming self.assistant is an instance of the Assistant class you're using
            thread, run = self.assistant.create_thread_and_run(prompt)

            # Check the run and wait for the response
            response = self.assistant.check_run(thread.id, run.id)

            # TBD

    def run(self):
        print(f"{Fore.BLUE}Starting DLP Data Generation {Style.RESET_ALL}\n")
        if self.fm.upload_file(self.dlp_categories_file, "DLP Categories") is None:
            raise ValueError("File upload failed")

        # Start time
        start_time = time.time()
        thread, run = self.assistant.create_thread_and_run(
            "Based on the dlp_categories.md file, give me "
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

