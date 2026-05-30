import pytest
from src.template import render_email


@pytest.fixture
def project(tmp_path):
    companies_dir = tmp_path / "companies"
    companies_dir.mkdir()
    (companies_dir / "Acme.yml").write_text(
        'subject: "Join Acme"\nbody: "I love **Acme** products."\n',
        encoding="utf-8",
    )
    template = tmp_path / "email_body.md"
    template.write_text(
        "Hi {{first_name}},\n\n{{company_body}}\n\nBest,\n{{email_signature}}",
        encoding="utf-8",
    )
    return tmp_path


def test_first_name_extracted(project):
    result = render_email("Jane Smith", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert "Jane" in result["html_body"]
    assert "Smith" not in result["html_body"]


def test_single_word_name(project):
    result = render_email("Cher", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert "Cher" in result["html_body"]


def test_company_body_markdown_rendered(project):
    result = render_email("Jane Smith", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert "<strong>Acme</strong>" in result["html_body"]


def test_subject_returned(project):
    result = render_email("Jane Smith", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert result["subject"] == "Join Acme"


def test_signature_placeholder_removed(project):
    result = render_email("Jane Smith", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert "{{email_signature}}" not in result["html_body"]


def test_missing_company_raises(project):
    with pytest.raises(FileNotFoundError, match="No template found for company: Unknown"):
        render_email("Jane Smith", "Unknown", str(project / "email_body.md"), str(project / "companies"))


def test_case_insensitive_company_match(project):
    result = render_email("Jane Smith", "acme", str(project / "email_body.md"), str(project / "companies"))
    assert result["subject"] == "Join Acme"


def test_output_is_html(project):
    result = render_email("Jane Smith", "Acme", str(project / "email_body.md"), str(project / "companies"))
    assert "<" in result["html_body"] and ">" in result["html_body"]
