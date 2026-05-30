class DraftCreator:
    def create_draft(self, to: str, subject: str, html_body: str, attachment_path: str) -> str | None:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass
