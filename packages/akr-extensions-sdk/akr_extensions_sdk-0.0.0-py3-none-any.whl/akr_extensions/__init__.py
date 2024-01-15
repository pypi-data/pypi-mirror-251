from abc import ABC, abstractmethod
from tqdm import tqdm

class AnimeExtension(ABC):
    def __init__(self, debug: True):
        self._debug = debug
    
    def get_anime_choice(self):
        while True:
            u_input = input("Your choice (0 to search again): ")
            self._choice = int(u_input)
            if self._choice != None and self._choice > 0:
                break
    
    def download_to_file(self, response, file_name: str):
        print("Download started:", file_name)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        with open(file_name, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        print("Download complete!")
    
    @abstractmethod
    def list_anime(self):
        pass
    
    @abstractmethod
    def search(self, anime_name):
        pass

    @abstractmethod
    def get_anime_details(self):
        pass
    
    @abstractmethod
    def get_episode(): # This will cover other things until the download
        pass

    @abstractmethod
    def download_episode():
        pass

    @abstractmethod
    def quit():    # Close anything it needs to
        pass