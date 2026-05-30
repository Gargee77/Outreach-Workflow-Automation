import pytest
from src.draft_creator import DraftCreator
from src.gmail_api_creator import GmailApiDraftCreator


def test_draft_creator_raises_not_implemented():
    creator = DraftCreator()
    with pytest.raises(NotImplementedError):
        creator.create_draft("a@b.com", "Subject", "<p>body</p>", "resume.pdf")


def test_draft_creator_context_manager_returns_self():
    creator = DraftCreator()
    with creator as c:
        assert c is creator


def test_gmail_api_creator_raises_not_implemented():
    creator = GmailApiDraftCreator(credentials_path="credentials.json")
    with pytest.raises(NotImplementedError):
        creator.create_draft("a@b.com", "Subject", "<p>body</p>", "resume.pdf")
