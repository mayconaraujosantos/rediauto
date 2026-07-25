.PHONY: sync run icon demo build clean

sync:
	uv sync

run:
	uv run main.py

icon:
	uv run python scripts/gerar_icone.py

demo:
	uv run python scripts/gerar_demo.py

build: icon
	uv run pyinstaller --onefile --windowed --name rediauto --icon assets/icon.ico --add-data "assets/icon.ico;assets" main.py

clean:
	rm -rf build dist rediauto.spec
