from dataclasses import dataclass
import gdown
from align_data.common.alignment_dataset import AlignmentDataset, DataEntry
import zipfile
import os
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class AudioTranscripts(AlignmentDataset):

    otter_zip_url: str

    def __post_init__(self):
        self.setup()
        self.transcript_path = self.write_jsonl_path.parent / 'raw' / 'transcripts'
        if not os.path.exists(self.transcript_path):
            os.makedirs(self.transcript_path)
            self._pull_from_gdrive()
        self.file_list = [xx for xx in self.transcript_path.files('*.md')]

    def _pull_from_gdrive(self):
        logger.info("Pulling from gdrive")
        gdown.download(url=self.otter_zip_url,
                       output=self.transcript_path / "transcripts.zip",
                       quiet=False)
        logger.info("Unzipping")
        with zipfile.ZipFile(self.transcript_path / "transcripts.zip", 'r') as zip_ref:
            zip_ref.extractall(self.transcript_path)

    def fetch_entries(self):
        for ii, filename in enumerate(self.file_list):
            if self._entry_done(ii):
                logger.info(f"Already done {ii}")
                continue

            logger.info(f"Processing {filename}")
            text = open(os.path.join(self.transcript_path,
                        'transcripts', filename), "r").read()
            title = filename.split(".")[0]

            date = re.search(r"\d{4}\d{2}\d{2}", filename).group(0)
            date = date[:4] + "-" + date[4:6] + "-" + date[6:]

            new_entry = DataEntry({
                "source": "audio-transcripts",
                "source_filetype": "audio",
                "url": "n/a",
                "converted_with": "otter-ai",
                "title": title,
                "authors": "unknown",
                "date_published": str(date),
                "text": text,
            })
            new_entry.add_id()
            yield new_entry
