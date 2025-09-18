from usecase import FetchGradesUseCase, LoginUseCase
from adapter import SeleniumClient, BsParser

def test_fetch_grades_use_case():
    client = SeleniumClient()
    login_uc = LoginUseCase(client, "https://lk.msu.ru/cabinet")

    id_= "songheelee2810@gmail.com"
    pw = "songhee2002"
    login_uc.execute(email=id_, password=pw)

    parser = BsParser()
    parser_uc = FetchGradesUseCase(client, parser)

    result = parser_uc.execute()

    assert result is not None