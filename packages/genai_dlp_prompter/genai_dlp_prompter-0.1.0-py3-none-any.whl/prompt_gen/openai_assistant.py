import os
import sys
import time

from colorama import Fore, Style
from py_openai_assistant.Assistant import Assistant
from py_openai_assistant.FileManager import FileManager

from file_utils.FileUtils import FileUtils


class OpenAIPromptAssistant:
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

    def generate_dlp_prompt(self, category, description):
        # Construct the prompt for OpenAI

        bank_details_prompt = (
            "Hey, I was updating my international contact list and needed to include bank details. "
            "For Australia, I've got the BSB as 082-082 and the account number is 123456789. "
            "In Canada, the transit number is 03101, the institution number is 001, and the account number is 1234567. "
            "For Israel, the bank code is 10, branch code is 905, and the account number is 12345678. "
            "Lastly, in Japan, the bank name is みずほ銀行 (Mizuho Bank), the branch is 東京支店 (Tokyo Branch), "
            "and the account number is 1234567. Can you check if these details are correctly formatted for each country?"
        )

        user_prompt = (
            f"Create a chat prompt for the DLP category '{category}', described as: '{description}'. "
            "The prompt should include structurally valid and representative mock data for this category."
            "For categories relevant to non-English "
            "languages, please use appropriate character sets, and ensure the response is in UTF-8 format."
            "Do not add any commentary or additional information to the prompt."
            "Here is an example of what the prompt should look like:"
            "##"
            "{bank_details_prompt}"
        )
        # Start time
        start_time = time.time()
        thread, run = self.assistant.create_thread_and_run(user_prompt)

        self.assistant.check_run(thread.id, run.id)
        # End time
        end_time = time.time()
        # Calculate elapsed time in seconds
        elapsed_time = end_time - start_time
        print(f"{Fore.BLUE}Elapsed time: {elapsed_time}, seconds{Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA} Saving Prompt Data... {Style.RESET_ALL}\n")
        filepath = self.assistant.save_last_message_to_file(self.assistant.get_response(thread), "prompt_data.txt")
        self.file_utils.convert_single_txt_to_pdf(os.path.basename(filepath), self.text_data, self.pdf_data)

    def run(self):
        print(f"{Fore.BLUE}Starting Prompt Data Generation {Style.RESET_ALL}\n")
        if self.fm.upload_file(self.dlp_categories_file, "DLP Categories") is None:
            raise ValueError("File upload failed")

        # Read the file and process each line
        with open(self.dlp_categories_file, 'r') as file:
            for line in file:
                # Extract category and description from each line
                parts = line.split(":")
                category = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''

                # Generate the chat prompt for each category
                self.generate_dlp_prompt(category, description)


