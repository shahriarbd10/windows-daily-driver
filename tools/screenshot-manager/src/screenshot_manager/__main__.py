try:
	from .app import main
except ImportError:
	# PyInstaller can execute this file as a top-level script.
	from screenshot_manager.app import main


if __name__ == "__main__":
	main()
