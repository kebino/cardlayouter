import pygame
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Card Layout Tool")
    parser.add_argument("--input", type=str, help="Path to the input directory", required=True)
    parser.add_argument("--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("--paper", type=str, default="a4", help="Size of the paper (e.g., A4, Letter)")
    parser.add_argument("--padding", type=int, default=0, help="Vertical padding between rows in pixels")
    parser.add_argument("--column-padding", type=int, default=20, help="Horizontal padding between columns in pixels")
    parser.add_argument("--prefix", type=str, default="page", help="Prefix for output files")
    parser.add_argument("--no-cut-line", action='store_true', help="Disable cut lines around cards")
    parser.add_argument("--bleed", type=int, default=10, help="Bleed size in pixels (default: 10px)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for output images")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose output")
    args = parser.parse_args()

    dpi = args.dpi
    paper_sizes = {
        "a4": (8.27 * dpi, 11.69 * dpi),
        "letter": (8.5 * dpi, 11 * dpi),
        "legal": (8.5 * dpi, 14 * dpi),
        "a3": (11.69 * dpi, 16.54 * dpi),
        "a5": (5.83 * dpi, 8.27 * dpi),
        "b5": (6.93 * dpi, 9.84 * dpi),
        "tabloid": (11 * dpi, 17 * dpi),
        "executive": (7.25 * dpi, 10.5 * dpi),
        "folio": (8.5 * dpi, 13 * dpi),
        "statement": (5.5 * dpi, 8.5 * dpi),
        "ledger": (17 * dpi, 11 * dpi),
        "half_letter": (5.5 * dpi, 8.5 * dpi),
        "a6": (4.13 * dpi, 5.83 * dpi),
        "c5": (6.38 * dpi, 9.02 * dpi),
        "dl": (3.94 * dpi, 8.27 * dpi),
    }

    card_width_in = 2.5
    card_height_in = 3.5
    card_size = (card_width_in * dpi, card_height_in * dpi)

    pygame.init()

    if args.paper not in paper_sizes:
        print(f"Unsupported paper size: {args.paper}")
        return
    
    paper_size = paper_sizes[args.paper]
    os.makedirs(args.output, exist_ok=True)

    cards_per_row = int((paper_size[0] - args.column_padding) // (card_size[0] + args.column_padding))
    cards_per_col = int((paper_size[1] - args.padding) // (card_size[1] + args.padding))
    cards_per_page = cards_per_row * cards_per_col

    total_width_needed = cards_per_row * card_size[0] + (cards_per_row - 1) * args.column_padding
    if total_width_needed > paper_size[0]:
        args.column_padding = int((paper_size[0] - cards_per_row * card_size[0]) / (cards_per_row - 1))
        if args.verbose:
            print(f"Adjusted column padding to fit: {args.column_padding}px")

    card_images = []
    for root, _, files in os.walk(args.input):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                card_images.append(os.path.join(root, file))

    total_pages = (len(card_images) + cards_per_page - 1) // cards_per_page

    for page_num in range(total_pages):
        paper_surface = pygame.Surface((int(paper_size[0]), int(paper_size[1])), pygame.SRCALPHA)

        total_cards_width = cards_per_row * card_size[0] + (cards_per_row - 1) * args.column_padding
        total_cards_height = cards_per_col * card_size[1] + (cards_per_col - 1) * args.padding
        offset_x = (paper_size[0] - total_cards_width) // 2
        offset_y = (paper_size[1] - total_cards_height) // 2

        if not args.no_cut_line:
            line_color = (0, 0, 0)
            line_width = 1

            for col in range(cards_per_row):
                lx = offset_x + col * (card_size[0] + args.column_padding)
                pygame.draw.line(paper_surface, line_color, (lx, 0), (lx, paper_size[1]), line_width)
                pygame.draw.line(paper_surface, line_color, (lx + card_size[0], 0), (lx + card_size[0], paper_size[1]), line_width)

            for row in range(cards_per_col):
                ly = offset_y + row * (card_size[1] + args.padding)
                pygame.draw.line(paper_surface, line_color, (0, ly), (paper_size[0], ly), line_width)
                pygame.draw.line(paper_surface, line_color, (0, ly + card_size[1]), (paper_size[0], ly + card_size[1]), line_width)

        for i in range(cards_per_page):
            card_index = page_num * cards_per_page + i
            if card_index >= len(card_images):
                break

            card_image_path = card_images[card_index]
            if args.verbose:
                print(f"Loading card image: {card_image_path}")

            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (int(card_size[0]), int(card_size[1])))

            row = i // cards_per_row
            col = i % cards_per_row

            x = offset_x + col * (card_size[0] + args.column_padding)
            y = offset_y + row * (card_size[1] + args.padding)

            bleed_left = args.bleed
            bleed_right = args.bleed
            bleed_top = args.bleed if row == 0 else 0
            bleed_bottom = args.bleed if row == cards_per_col - 1 else 0

            if args.bleed > 0:
                new_width = int(card_size[0] + bleed_left + bleed_right)
                new_height = int(card_size[1] + bleed_top + bleed_bottom)
                bleed_surface = pygame.Surface((new_width, new_height))

                bleed_surface.blit(card_image, (bleed_left, bleed_top))

                # Left edge extension
                left_strip = card_image.subsurface((0, 0, 1, card_image.get_height()))
                left_strip = pygame.transform.scale(left_strip, (bleed_left, card_image.get_height()))
                bleed_surface.blit(left_strip, (0, bleed_top))

                # Right edge extension
                right_strip = card_image.subsurface((card_image.get_width() - 1, 0, 1, card_image.get_height()))
                right_strip = pygame.transform.scale(right_strip, (bleed_right, card_image.get_height()))
                bleed_surface.blit(right_strip, (bleed_left + card_image.get_width(), bleed_top))

                # Top edge extension
                top_strip = card_image.subsurface((0, 0, card_image.get_width(), 1))
                top_strip = pygame.transform.scale(top_strip, (card_image.get_width(), bleed_top))
                bleed_surface.blit(top_strip, (bleed_left, 0))

                # Bottom edge extension
                bottom_strip = card_image.subsurface((0, card_image.get_height() - 1, card_image.get_width(), 1))
                bottom_strip = pygame.transform.scale(bottom_strip, (card_image.get_width(), bleed_bottom))
                bleed_surface.blit(bottom_strip, (bleed_left, bleed_top + card_image.get_height()))

                card_image = bleed_surface

                x -= bleed_left
                y -= bleed_top

            paper_surface.blit(card_image, (x, y))

        output_path = os.path.join(args.output, f"{args.prefix}_{page_num + 1}.png")
        pygame.image.save(paper_surface, output_path)
        if args.verbose:
            print(f"Saved: {output_path}")

    print(f"Total pages created: {total_pages}")
    print(f"Cards per page: {cards_per_page}")
    print(f"Saved to: {args.output}")
    pygame.quit()

if __name__ == "__main__":
    main()

# default args = python cardlayouter.py --input cards --output pages --paper a4 --padding 0 --dpi 300 --bleed 10

