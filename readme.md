## Card Layouter

Card Layouter is a Python tool for arranging card images onto printable pages, supporting various paper sizes and customizable options. It is ideal for creating print-ready sheets for board games, trading cards, and prototypes.

### Features
- Supports multiple paper sizes (A4, Letter, Legal, etc.)
- Customizable DPI and padding
- Automatically arranges cards in rows and columns
- Draws optional cut lines around cards
- Recursively loads images from input directory
- Outputs pages as PNG files

### Requirements
- Python 3.12+
- pygame

Install dependencies:
```bash
pip install -r requirements.txt
```

### How to Run
Run the tool from the command line:
```bash
python cardlayouter.py --input <input_dir> --output <output_dir> [options]
```

#### Options
- `--input` (required): Path to directory containing card images (PNG/JPG)
- `--output` (required): Path to directory for output pages
- `--paper`: Paper size (default: a4)
- `--padding`: Padding in pixels between cards (default: 0)
- `--prefix`: Prefix for output files (default: page)
- `--no-cut-line`: Disable cut lines around cards
- `--dpi`: DPI for output images (default: 300)

### How to Use
1. Place your card images in a folder (e.g., `cards/`).
2. Run the script with the desired options. Example:
	```bash
	python cardlayouter.py --input cards --output pages --paper a4 --padding 20 --dpi 300
	```
    the only required arguments are --input and --output
    ```bash
    python cardlayouter.py --input cards --output pages
    ```
3. Find the generated PNG pages in your output directory (e.g., `pages/`).
4. Print the pages and cut out your cards!

---

#### List of valid paper sizes

The following values are accepted for the `--paper` argument:

| Argument      | Size (inches)         |
|--------------|----------------------|
| a4           | 8.27 x 11.69         |
| letter       | 8.5 x 11             |
| legal        | 8.5 x 14             |
| a3           | 11.69 x 16.54        |
| a5           | 5.83 x 8.27          |
| b5           | 6.93 x 9.84          |
| tabloid      | 11 x 17              |
| executive    | 7.25 x 10.5          |
| folio        | 8.5 x 13             |
| statement    | 5.5 x 8.5            |
| ledger       | 17 x 11              |
| half_letter  | 5.5 x 8.5            |
| a6           | 4.13 x 5.83          |
| c5           | 6.38 x 9.02          |
| dl           | 3.94 x 8.27          |
---
For more details, see the script and comments in `cardlayouter.py`.
