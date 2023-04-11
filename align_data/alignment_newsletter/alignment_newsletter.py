# %%
import logging

import pandas as pd

from dataclasses import dataclass
from align_data.common.alignment_dataset import AlignmentDataset , DataEntry
from tqdm import tqdm

logger = logging.getLogger(__name__)
    
@dataclass
class AlignmentNewsletter(AlignmentDataset):
    
    COOLDOWN: int = 1
    done_key = "title"
    
    def setup(self) -> None:
        self._setup()
        self.newsletter_xlsx_path = self.write_jsonl_path.parent / "raw" / "alignment_newsletter.xlsx"
        self.df = pd.read_excel(self.newsletter_xlsx_path)

    def fetch_entries(self):
        """
        For each row in the dataframe, create a new entry with the following fields: url, source,
        converted_with, source_type, venue, newsletter_category, highlight, newsletter_number,
        summarizer, opinion, prerequisites, read_more, title, authors, date_published, text

        To update, download the spreadsheet of all the summaries of the newsletter at 
        https://rohinshah.com/alignment-newsletter/ and place it in data/raw/alignment_newsletter.xlsx
        """
        self.setup()
        for ii , row in tqdm(self.df.iterrows()):
            if self._entry_done(row['Title']):
                # logger.info(f"Already done {row['Title']}")
                continue
            new_entry = DataEntry({
                "source": "alignment newsletter",
                "title": str(row["Title"]),
                "authors": str(row["Authors"]),
                "date_published": row["Year"],
                "url": "https://rohinshah.com/alignment-newsletter/",
                "tags": str(row["Category"]),
                "text": f'{row["Email"]}: {row["Title"]}, by {row["Authors"]}. summarized by {row["Summarizer"]}.\n\n{row["Summary"]}\n\n{row["Summarizer"]}\'s opinion: {row["My opinion"]}',
            })
            new_entry.add_id()
            yield new_entry
            
 