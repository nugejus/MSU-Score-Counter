import pytest
from usecase.login_usecase import LoginUseCase
from adapter.selenium_client import SeleniumClient

def test_1():
    client = SeleniumClient()
    obj = LoginUseCase(client, "https://lk.msu.ru/cabinet")

    id_= "songheelee2810@gmail.com"
    pw = "songhee2002"
    obj.execute(email=id_, password=pw)

    assert "Оценки" in obj.client.page_source()