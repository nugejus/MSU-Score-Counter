from ports import WebClientPort, ParserPort

class FetchGradesUseCase:
    def __init__(self, client: WebClientPort, parser: ParserPort):
        self.client = client
        self.parser = parser

    def execute(self, diploma_only:bool = True):
        self.client.click("link", "Оценки")
        self.client.wait(2.0)
        html = self.client.page_source()
        return self.parser.extract_success_rows(html, diploma_only=diploma_only)
