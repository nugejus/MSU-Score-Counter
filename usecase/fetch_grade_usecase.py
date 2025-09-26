from ports import WebClientPort, ParserPort


class FetchGradesUseCase:
    """Use case for fetching grades from the web client.

    This use case automates navigation to the grades page,
    retrieves the HTML source, and parses it into structured
    grade entries using the provided parser.
    """

    def __init__(self, client: WebClientPort, parser: ParserPort):
        """Initialize the FetchGradesUseCase.

        Args:
            client (WebClientPort): A web client adapter (e.g., Selenium client).
            parser (ParserPort): A parser adapter for extracting grade entries
                from HTML.
        """
        self.client = client
        self.parser = parser

    def execute(self, diploma_only: bool = True):
        """Fetch and parse grade entries.

        This method navigates to the "Оценки" (Grades) page,
        retrieves the HTML source, and extracts grade entries
        using the parser.

        Args:
            diploma_only (bool): If True, include only rows marked as
                diploma-related (default: True).

        Returns:
            list[GradeEntry]: A list of structured grade entries.

        Example:
            >>> usecase = FetchGradesUseCase(client, parser)
            >>> grades = usecase.execute(diploma_only=False)
            >>> for g in grades:
            ...     print(g.subject, g.mark)
        """
        self.client.click("link", "Оценки")
        self.client.wait(2.0)
        html = self.client.page_source()
        return self.parser.extract_success_rows(html, diploma_only=diploma_only)
