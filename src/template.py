import warnings
import yaml
import markdown2
from pathlib import Path


def render_email(full_name: str, company: str, template_path: str, companies_dir: str) -> dict:
    first_name = full_name.split()[0]

    company_file = Path(companies_dir) / f"{company}.yml"
    if not company_file.exists():
        company_file = next(
            (f for f in Path(companies_dir).glob("*.yml") if f.stem.lower() == company.lower()),
            None,
        )
        if company_file is None:
            raise FileNotFoundError(f"No template found for company: {company}")

    with open(company_file, encoding="utf-8") as f:
        company_data = yaml.safe_load(f)

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    if "{{company_body}}" not in template:
        warnings.warn(f"{{{{company_body}}}} placeholder not found in {template_path}", stacklevel=2)

    filled = (
        template
        .replace("{{first_name}}", first_name)
        .replace("{{company_body}}", company_data["body"])
    )

    return {
        "subject": company_data["subject"],
        "html_body": markdown2.markdown(filled),
    }
