# TODO: bump version on release
VERSION = 0.1.4
DATA_FILE = ${HOME}/.local/share/pycites/Trade_database_download_v2021.1.csv.gz

install:
	poetry install
build:
	poetry build
download_cites_data:
	poetry run get_cites_data --force_update
	poetry run  python -c "import pycites; assert pycites.__version__ == '${VERSION}'; print(pycites.load_data())"
# TODO: update publish and release
publish:
	poetry publish
release: install build download_cites_data publish
	gh release create ${VERSION} ${DATA_FILE}