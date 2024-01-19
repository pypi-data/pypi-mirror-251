from reserver import Uploader

# main pypi account
pypi_token= "pypi-AgEIcHlwaS5vcmcCJDRmNThmNDFkLTZhNTYtNDU2Ny05YjhlLTM4YzNkNTczMDA4NgACKlszLCJiMjNmNjZlYS1iZGEzLTQ4NzYtYTdmNy02ZjZlYjYwM2I4NTMiXQAABiAqGQglXAgXzZUL5Ik-NsC1R8TidtKtZRZzbA32C8KiCA"
# main pypi account new password: "kwhM8Pp$S@sCx6m"

# test.pypi account
test_pypi_token = "pypi-AgENdGVzdC5weXBpLm9yZwIkMTFkZDhjNWMtMTY2My00OWMyLTlmZGItZWZkMzU2NDQxMWJlAAIqWzMsIjJhYjkwZjE4LWQ1ODItNGFiNy05NTYwLWUxN2ZiZTcwY2Y2NyJdAAAGIDVymuINEbiyhSBeB_-ysIapdi_wHTTjD9vpV6mFGzvu"
# test pypi account new password: "fgtwwU64X7yEE6z"

def test(token, is_test_pypi_account):
    uploader = Uploader(token, is_test_pypi_account)
    uploader.upload_to_pypi("sample_test_package_from_reserver")

test(pypi_token, False)
# test(test_pypi_token, True)
