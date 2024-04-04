import unittest
import os
import tempfile
import shutil
from onefilellm import process_github_repo, process_arxiv_pdf, process_local_folder, fetch_youtube_transcript, crawl_and_extract_text, process_doi_or_pmid, process_github_pull_request, process_github_issue

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
        repo_content = process_github_repo(repo_url)
        self.assertIsInstance(repo_content, str)
        self.assertGreater(len(repo_content), 0)
        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(repo_content)
        self.assertTrue(os.path.exists(self.output_file))
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
        local_path = "C:\\python\\1filellm"
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

    def test_process_doi(self):
        print("\nTesting DOI processing...")
        doi = "10.1053/j.ajkd.2017.08.002"
        process_doi_or_pmid(doi, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("DOI processing test passed.")

    def test_process_pmid(self):
        print("\nTesting PMID processing...")
        pmid = "29203127"
        process_doi_or_pmid(pmid, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("PMID processing test passed.")

    def test_process_github_pull_request(self):
        print("\nTesting GitHub pull request processing...")
        pull_request_url = "https://github.com/dear-github/dear-github/pull/102"
        pull_request_content = process_github_pull_request(pull_request_url, self.output_file)
        self.assertIsInstance(pull_request_content, str)
        self.assertGreater(len(pull_request_content), 0)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("GitHub pull request processing test passed.")

    def test_process_github_issue(self):
        print("\nTesting GitHub issue processing...")
        issue_url = "https://github.com/isaacs/github/issues/1191"
        issue_content = process_github_issue(issue_url, self.output_file)
        self.assertIsInstance(issue_content, str)
        self.assertGreater(len(issue_content), 0)
        self.assertTrue(os.path.exists(self.output_file))
        with open(self.output_file, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertGreater(len(content), 0)
        print("GitHub issue processing test passed.")

if __name__ == "__main__":
    unittest.main()
