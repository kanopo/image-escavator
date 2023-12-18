import io
import os
import shutil
import sys

import fitz  # PyMuPDF


def extract_images_from_pdf(pdf_path, output_folder):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf = fitz.open(pdf_path)

    for i, page in enumerate(pdf):
        image_list = page.get_images()

        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {i}")
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]  # xref is the reference number of the image
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = (
                    f"{output_folder}/image_page_{i}_{image_index}.{image_ext}"
                )
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)
        else:
            print("[!] No images found on page", i)

    pdf.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_pdf> <output_directory>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_dir = sys.argv[2]
    extract_images_from_pdf(pdf_file, output_dir)

    shutil.make_archive(output_dir, "zip", output_dir)
    shutil.rmtree(output_dir)
