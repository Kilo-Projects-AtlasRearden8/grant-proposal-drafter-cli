import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from grant_proposal_drafter.client import LLMClient, LLMError
from grant_proposal_drafter.drafter import (
    DISCLAIMER,
    SECTION_ORDER,
    SECTION_TITLES,
    GrantDrafter,
)
from grant_proposal_drafter.cli import build_parser, main


CAPTURED = {}


class MockHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        CAPTURED["last_payload"] = json.loads(body)
        response = {
            "choices": [
                {
                    "message": {
                        "content": f"Mock draft content for model {CAPTURED['last_payload'].get('model')}",
                    }
                }
            ]
        }
        data = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


class MockServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        cls.base_url = f"http://127.0.0.1:{server.server_address[1]}"
        cls._server = server

    def test_client_chat_round_trip(self):
        client = LLMClient(base_url=self.base_url, model="mock-model")
        content = client.chat([{"role": "user", "content": "hello"}])
        self.assertIn("mock-model", content)
        self.assertFalse(CAPTURED["last_payload"]["stream"])

    def test_client_missing_endpoint_raises(self):
        client = LLMClient(base_url="http://127.0.0.1:1", model="x", timeout=2)
        with self.assertRaises(LLMError):
            client.chat([{"role": "user", "content": "hello"}])

    def test_draft_all_sections(self):
        client = LLMClient(base_url=self.base_url, model="mock-model")
        drafter = GrantDrafter(client)
        details = {
            "title": "Community Literacy Program",
            "organization": "Asdale Dynamics, LLC",
            "amount": "$50,000",
        }
        sections = drafter.draft_all(details)
        self.assertEqual(set(sections), set(SECTION_ORDER))
        for name in SECTION_ORDER:
            self.assertIn("Mock draft content", sections[name])
        markdown = drafter.render_markdown(details, sections)
        self.assertIn("Community Literacy Program", markdown)
        self.assertIn(DISCLAIMER, markdown)

    def test_detail_values_flow_into_markdown(self):
        client = LLMClient(base_url=self.base_url, model="mock-model")
        drafter = GrantDrafter(client)
        details = {
            "title": "Sunshine Garden Project",
            "organization": "Sunshine Neighborhood Association",
            "amount": "$12,000",
            "goals": "Grow fresh vegetables for the neighborhood food pantry.",
            "activities": "Weekly gardening workshops and harvest days.",
        }
        sections = drafter.draft_all(details)
        markdown = drafter.render_markdown(details, sections)
        self.assertIn("# Sunshine Garden Project", markdown)
        self.assertIn("Sunshine Neighborhood Association", markdown)
        self.assertIn("$12,000", markdown)
        self.assertIn(DISCLAIMER, markdown)

    def test_render_markdown_structure(self):
        client = LLMClient(base_url=self.base_url, model="mock-model")
        drafter = GrantDrafter(client)
        sections = {name: f"Draft for {name}" for name in SECTION_ORDER}
        markdown = drafter.render_markdown(
            {"title": "T", "organization": "O"}, sections
        )
        self.assertIn("# T", markdown)
        self.assertIn("Education-Only Disclaimer", markdown)
        self.assertIn(DISCLAIMER, markdown)
        for name in SECTION_ORDER:
            self.assertIn(f"## {SECTION_TITLES[name]}", markdown)
            self.assertIn(f"Draft for {name}", markdown)

    def test_cli_writes_file(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp:
            output = os.path.join(tmp, "draft.md")
            parser = build_parser()
            argv = [
                "--input", "tests/fixture_project.json",
                "--output", output,
                "--base-url", self.base_url,
                "--model", "mock-model",
            ]
            exit_code = main(argv)
            self.assertEqual(exit_code, 0)
            with open(output, "r", encoding="utf-8") as handle:
                markdown = handle.read()
            self.assertIn("Community Literacy Program", markdown)
            self.assertIn(DISCLAIMER, markdown)
            for name in SECTION_ORDER:
                self.assertIn(f"## {SECTION_TITLES[name]}", markdown)

    def test_cli_endpoint_down(self):
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmp:
            output = os.path.join(tmp, "draft.md")
            parser = build_parser()
            argv = [
                "--output", output,
                "--base-url", "http://127.0.0.1:1",
                "--timeout", "2",
            ]
            exit_code = main(argv)
            self.assertNotEqual(exit_code, 0)
            self.assertFalse(os.path.exists(output))


FIXTURE = {
    "title": "Community Literacy Program",
    "organization": "Asdale Dynamics, LLC",
    "amount": "$50,000",
    "duration": "12 months",
    "target_population": "adult learners in Marion County",
    "problem_statement": "Local adults lack access to free literacy classes.",
    "goals": "Improve adult literacy in Marion County.",
    "activities": "Weekly classes and tutoring.",
    "budget_items": "Instructor wages, materials, space rental.",
    "evaluation_metrics": "Reading assessments and attendance.",
    "sustainability": "Local grants and donations.",
}


if __name__ == "__main__":
    import os

    os.makedirs("tests", exist_ok=True)
    with open(os.path.join("tests", "fixture_project.json"), "w", encoding="utf-8") as handle:
        json.dump(FIXTURE, handle)
    unittest.main()
