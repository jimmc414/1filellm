import unittest
import os
import tempfile
import shutil
from onefilellm import process_github_repo, process_arxiv_pdf, process_local_folder, fetch_youtube_transcript, crawl_and_extract_text

class TestDataAggregation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.temp_dir, "uncompressed_output.txt")
        self.compressed_file = os.path.join(self.temp_dir, "compressed_output.txt")
        self.urls_list_file = os.path.join(self.temp_dir, "processed_urls.txt")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_github_repo(self):
        print("\nTesting GitHub repository processing...")
        repo_url = "https://github.com/jimmc414/onefilellm"
        process_github_repo(repo_url, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("GitHub repository processing test passed.")

    def test_arxiv_pdf(self):
        print("\nTesting arXiv PDF processing...")
        arxiv_url = "https://arxiv.org/abs/2401.14295"
        process_arxiv_pdf(arxiv_url, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("arXiv PDF processing test passed.")

    def test_local_folder(self):
        print("\nTesting local folder processing...")
        local_path = "C:\\python\\onefilellm"
        process_local_folder(local_path, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("Local folder processing test passed.")

    def test_youtube_transcript(self):
        print("\nTesting YouTube transcript fetching...")
        video_url = "https://www.youtube.com/watch?v=KZ_NlnmPQYk"
        transcript = fetch_youtube_transcript(video_url)
        self.assertIsInstance(transcript, str)
        self.assertGreater(len(transcript), 0)
        print("YouTube transcript fetching test passed.")

    def test_webpage_crawl(self):
        print("\nTesting webpage crawling and text extraction...")
        webpage_url = "https://llm.datasette.io/en/stable/"
        max_depth = 1
        include_pdfs = False
        ignore_epubs = True
        crawl_and_extract_text(webpage_url, self.output_file, self.urls_list_file, max_depth, include_pdfs, ignore_epubs)
        self.assertTrue(os.path.exists(self.output_file))
        self.assertTrue(os.path.exists(self.urls_list_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("Webpage crawling and text extraction test passed.")

if __name__ == "__main__":
    unittest.main()