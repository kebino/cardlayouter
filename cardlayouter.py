import pygame
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Card Layout Tool")
    parser.add_argument("--input", type=str, help="Path to the input directory", required=True)
    parser.add_argument("--output", type=str, help="Path to the output directory", required=True)
    parser.add_argument("--paper", type=str, default="a4", help="Size of the paper (e.g., A4, Letter)")
    parser.add_argument("--padding", type=int, default=0, help="padding size in pixels")
    parser.add_argument("--prefix", type=str, default="page", help="Prefix for output files")
    parser.add_argument("--no-cut-line", action='store_true', help="Disable cut lines around cards")
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
    # card size in inches
    card_width_in = 2.5
    card_height_in = 3.5
    # card size in pixels
    card_size = (card_width_in * dpi, card_height_in * dpi)

    # Initialize Pygame
    pygame.init()

    if args.paper not in paper_sizes:
        print(f"Unsupported paper size: {args.paper}")
        return
    
    paper_size = paper_sizes[args.paper]

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    cards_per_row = int((paper_size[0] - args.padding) // (card_size[0] + args.padding))
    cards_per_col = int((paper_size[1] - args.padding) // (card_size[1] + args.padding))
    cards_per_page = cards_per_row * cards_per_col

    # Load card images from input directory recursively
    card_images = []
    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                card_images.append(os.path.join(root, file))
    total_pages = (len(card_images) + cards_per_page - 1) // cards_per_page

    for page_num in range(total_pages):
        # create a surface with opacity for the paper
        paper_surface = pygame.Surface((int(paper_size[0]), int(paper_size[1])), pygame.SRCALPHA)

        for i in range(cards_per_page):
            card_index = page_num * cards_per_page + i
            if card_index >= len(card_images):
                break
            
            card_image_path = os.path.join(args.input, card_images[card_index])
            if args.verbose:
                print(f"Loading card image: {card_image_path}")
            card_image = pygame.image.load(card_image_path)
            card_image = pygame.transform.scale(card_image, (int(card_size[0]), int(card_size[1])))

            row = i // cards_per_row
            col = i % cards_per_row
            x = args.padding + col * (card_size[0] + args.padding)
            y = args.padding + row * (card_size[1] + args.padding)

            paper_surface.blit(card_image, (x, y))

            if not args.no_cut_line:
                line_color = (0, 0, 0)
                line_width = 1
                # Draw cut lines
                pygame.draw.rect(paper_surface, line_color, (x, y, card_size[0] + 10, card_size[1] + 10), line_width)

        output_path = os.path.join(args.output, f"{args.prefix}_{page_num + 1}.png")
        pygame.image.save(paper_surface, output_path)
        if args.verbose:
            print(f"Saved: {output_path}")
    
    print(f"Total pages created: {total_pages}\ncards per page: {cards_per_page} \nsaved to {args.output}")

    pygame.quit()

if __name__ == "__main__":
    main()