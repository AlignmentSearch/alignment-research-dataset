from dataclasses import dataclass
import os
import fire
from dataclasses import dataclass
from typing import List , Union
import align_data
from align_data.common.utils import EntryWriter
from align_data.analysis.count_tokens import count_token
from print_jsonl import print_jsonl

# import logging , sys

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@dataclass
class AlignmentDataset:

    out_path : str = "data"

    def cmd_list(self) -> List[str]:
        """
        `cmd_list` is a function that takes in a self parameter and returns a list of strings
        :return: A list of all the datasets
        """
        for name in align_data.ALL_DATASETS:
            print(name)
        return align_data.ALL_DATASETS

    def cmd_fetch(self , name) -> None:
        """
        > This function takes a dataset name and writes the entries of that dataset to a file
        
        :param name: The name of the dataset to fetch
        :return: The path to the file that was written to.
        """
        assert name in align_data.ALL_DATASETS , f"{name} is not a valid dataset name"
        with EntryWriter(name, self.out_path, True) as writer:
            for entry in align_data.get_dataset(name).fetch_entries():
                writer.write(entry)

        return os.path.join(self.out_path, name + ".jsonl")

    def cmd_fetch_all(self) -> str:
        """
        It downloads all the datasets, moves the alignment_newsletter.jsonl file to the processed
        folder, deletes the alignment_newsletter.jsonl file, adds the alignment_newsletter_summaries to
        the datasets, and merges all the files
        :return: The path to the merged file.
        """
        i = 0
        for name in align_data.ALL_DATASETS:
            print(name)
            self.cmd_fetch(name)
            if i == 1:
                break
        
        return None #merge_all_files(out_dir = self.out_path)

    def cmd_count_tokens(self , merged_dataset_path : str) -> None:
        """
        This function counts the number of tokens, words, and characters in the dataset
        :return: None
        """
        assert os.path.exists(merged_dataset_path) , "The path to the merged dataset does not exist"
        count_token(merged_dataset_path)

def main(command : str , out_path : str = "data" , dataset_name : str = None ) -> Union[str , List[str] , None]:
    """
    It downloads the alignment dataset from the internet and saves it to a local directory
    
    :param command: The command to run. Can be one of: list, fetch, fetch_all, count_tokens
    :type command: str
    :param out_path: The path to the directory where the data will be downloaded, defaults to data
    :type out_path: str (optional)
    :param dataset_name: The name of the dataset to fetch
    :type dataset_name: str
    :return: A list of strings.
    """

    assert command in [ "list" , "fetch" , "fetch-all" ] , f"Invalid command: {command}"

    al_dataset = AlignmentDataset(out_path)

    if command == "list":
        return al_dataset.cmd_list()
    elif command == "fetch":
        return al_dataset.cmd_fetch(dataset_name)
    elif command == "fetch-all":
        return al_dataset.cmd_fetch_all()
    elif command == "count-tokens":
        al_dataset.cmd_count_tokens()
        return None

if __name__ == "__main__":
    # fire.Fire(main)

    fetch = [ # tbu = to be updated
        # "agentmodels",  # Fails
        "alignment_newsletter",  # Success
        # "arbital",  # Success
        #"arxiv_papers",  # Success, tbu
        # "audio_transcripts",  # Fails, try more
        # "distill",  # Success, tbu
        # "gdocs",  # Success
        # "gdrive_ebooks",  # Semi success, must manually change Titles, Authors, URLs. tbu
        # "gwern_blog",  # Success, manualy update dates. tbu
        # "nonarxiv_papers",  # Success, manually update dates/urls/tags. tbu
        # "reports",  # Success, missing most dates and urls
        #"stampy"  # Fails
        # "aiimpacts.org",  # Fails
        # "aipulse.org",  # Fails
        # "aisafety.camp",  # Fails
        # "carado.moe",  # Fails
        # "cold.takes",  # Fails
        # "deepmind.blog",  # Fails
        # # "eaforum",  # Fails
        # "generative.ink",  # Fails
        # "intelligence.org",  # Fails
        # "jsteinhardt.wordpress.com",  # Fails
        # # "lesswrong",  # Fails
        # "markdown.ebooks",  # Fails
        # "qualiacomputing.com",  # Fails
        # "vkrakovna.wordpress.com",  # Fails
        # "waitbutwhy",  # Fails
        # "www.yudkowsky.net"  # Fails
    ]
    
    print("\n"*5)
    for name in fetch:
        main("fetch", "data", name)
        print(f"\nDone with {name}.\n\n")
        print_jsonl(f"data/{name}.jsonl", num_lines=20, text_lim=100)   
        
    
    # import os
    # import json

    # # Function to read JSON objects from a .jsonl file
    # def read_jsonl(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         for line in file:
    #             yield json.loads(line.strip())

    # # Function to write JSON objects to a .jsonl file
    # def write_jsonl(file_path, data):
    #     with open(file_path, 'w', encoding='utf-8') as file:
    #         for item in data:
    #             file.write(json.dumps(item, ensure_ascii=False) + '\n')

    # def combine_jsonl_files(directory_path, output_file):
    #     combined_data = []

    #     # Iterate over all files in the directory
    #     for file_name in os.listdir(directory_path):
    #         file_path = os.path.join(directory_path, file_name)

    #         # Check if the file has a .jsonl extension
    #         if file_name.endswith('.jsonl') and os.path.isfile(file_path):
    #             combined_data.extend(list(read_jsonl(file_path)))

    #     # Write the combined data to the output file
    #     write_jsonl(output_file, combined_data)

    # # Usage example
    # input_directory = 'path/to/your/input/directory'
    # output_file = 'combined.jsonl'
    # combine_jsonl_files(input_directory, output_file)
        