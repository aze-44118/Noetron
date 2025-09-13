# Data Directory

This directory contains sample text files for testing Noetron.

## Sample Files

- `spinoza/` - Sample texts from Spinoza (French)
- `spinoza_en/` - Sample texts from Spinoza (English)
- `merleau_ponty/` - Sample texts from Merleau-Ponty (French)

## Adding Your Own Data

1. Create a new folder in this directory
2. Add your `.txt` files to the folder
3. Use the folder name with Noetron commands:

```bash
python cli/main.py process -i your_folder_name
```

## File Format

- Files should be in `.txt` format
- UTF-8 encoding recommended
- One text per file
- No special formatting required
