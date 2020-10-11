# bump_version: TODO later
VERSION = v0.1.3
DATA_FILE = ${HOME}/.local/share/pycites/Trade_database_download_v2020.1.csv.gz

install:
	poetry install
build:
	poetry build
download_cites_data:
	get_cites_data --force_update
publish:
	poetry publish
release: install build download_cites_data publish
	gh release create ${VERSION} ${DATA_FILE}