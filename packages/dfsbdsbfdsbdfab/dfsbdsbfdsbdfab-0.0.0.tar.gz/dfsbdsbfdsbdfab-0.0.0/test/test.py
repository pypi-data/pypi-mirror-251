from reserver import util

# pypi account
my_username = "__token__"
my_password = "pypi-AgEIcHlwaS5vcmcCJGRhOWMwMDYwLTQ3M2ItNDFkZS04MGI0LTdkYmU4ZmM4MzYyNQACKlszLCJiMjNmNjZlYS1iZGEzLTQ4NzYtYTdmNy02ZjZlYjYwM2I4NTMiXQAABiC2HwclY81j5mzkE8oc8mK72CP_vXFbRGBYCJCwR7z-IA"
# main pypi account new password: "kwhM8Pp$S@sCx6m"

# test.pypi account
# test account:
# test, password: fgtwwU64X7yEE6z
# my_username = "__token__"
# my_password = "pypi-AgENdGVzdC5weXBpLm9yZwIkODdhMzRiMDMtNmQxNy00MDI3LWFlY2QtYjE0MTUwYjA3ZjkwAAIqWzMsIjJhYjkwZjE4LWQ1ODItNGFiNy05NTYwLWUxN2ZiZTcwY2Y2NyJdAAAGIMBSVR5cnDK5aF6Un49SH4waxGRKQzS36RncEVLw2uke"

util.upload_to_pypi(my_username, my_password, "dfsbdsbfdsbdfab", False)
