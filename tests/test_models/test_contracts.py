import base64

from voltarium.models import ContractFile


def test_contract_file_decodes_base64() -> None:
    pdf_bytes = b"%PDF-1.5\nFAKE"
    encoded = base64.b64encode(pdf_bytes).decode()

    contract_file = ContractFile(
        contract_id="123",
        filename="123.pdf",
        content_type="application/pdf",
        content_base64=encoded,
    )

    assert contract_file.content == pdf_bytes
    assert contract_file.content_base64 == encoded
    assert contract_file.content_length == len(pdf_bytes)
