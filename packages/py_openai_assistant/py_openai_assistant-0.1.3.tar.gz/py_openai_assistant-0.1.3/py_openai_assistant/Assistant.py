import os
import time

import openai
from colorama import Fore, Style


class Assistant:
    def __init__(self, client=None, api_key=None, data_folder="./text_data"):
        if client:
            self.client = client
        elif api_key:
            self.client = openai.Client(api_key=api_key)
        else:
            raise ValueError("client or key must not be None")
        self.assistant_id = None
        self.data_folder = data_folder

    def create(self, assistant_id="deadbeef", name="Helpful Assistant",
               instructions="You are an assistant", model="gpt-4-1106-preview"):
        try:
            # try to reuse an assistant
            assistant = self.client.beta.assistants.retrieve(assistant_id=assistant_id)
        except openai.NotFoundError as e:
            assistant = self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=model
            )

        self.assistant_id = assistant.id

    def delete_all_assistants(self):
        try:
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                response = self.client.beta.assistants.delete(assistant.id)
                if not response.deleted:
                    print(f"Failed to delete Assistant with ID {assistant.id}")
            print("All assistants have been deleted.")
            return True
        except Exception as e:
            print("Error:", e)

    def delete_by_id(self, assistant_id):
        try:
            self.client.beta.assistants.delete(assistant_id)
            print(f"Assistant with ID {assistant_id} has been deleted.")
        except Exception as e:
            print("Error:", e)

    def delete_by_name(self, name):
        try:
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == name:
                    self.client.beta.assistants.delete(assistant.id)
                    print(f"Assistant with name '{name}' has been deleted.")
            print(f"No assistant found with the name '{name}'.")
        except Exception as e:
            print("Error:", e)

    def get_by_name(self, name):
        matching_assistants = []
        try:
            assistants = self.client.beta.assistants.list()
            for assistant in assistants.data:
                if assistant.name == name:
                    matching_assistants.append(assistant)
            if matching_assistants:
                print(f"Found {len(matching_assistants)} assistants with the name '{name}'.")
            else:
                print(f"No assistant found with the name '{name}'.")
        except Exception as e:
            print("Error:", e)
        return matching_assistants

    def check_run(self, thread_id, run_id):
        while True:
            # Refresh the run object to get the latest status
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if run.status == "completed":
                print(f"{Fore.GREEN} Run is completed.{Style.RESET_ALL}")
                break
            elif run.status == "expired":
                print(f"{Fore.RED}Run is expired.{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.YELLOW} OpenAI: Run is not yet completed. Waiting...{run.status} {Style.RESET_ALL}")
                time.sleep(1)  # Wait for 1 second before checking again

    def submit_user_message(self, thread, user_message):
        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )

    def create_thread_and_run(self, user_input):
        thread = self.client.beta.threads.create()
        print(f"{Fore.MAGENTA} Thread Info: {thread.id} {Style.RESET_ALL}")
        # show_json(thread)
        run = self.submit_user_message(thread, user_input)
        return thread, run

    def get_response(self, thread):
        messages = self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")
        return messages

    def _get_filename_with_incrementing_suffix(self, base_file_name):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        base_name, extension = os.path.splitext(base_file_name)
        counter = 1

        # Increment the suffix until an unused name is found
        while os.path.exists(os.path.join(self.data_folder, f"{base_name}_{counter}{extension}")):
            counter += 1
        new_file_path = os.path.join(self.data_folder, f"{base_name}_{counter}{extension}")
        return new_file_path

    def save_last_message_to_file(self, messages: [], filename: str):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        filepath = self._get_filename_with_incrementing_suffix(filename)
        if len(messages) == 0:
            print(f"No message to save")
        else:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(f'{messages.data[-1].content[0].text.value}\n')
                file.close()
                return filepath
