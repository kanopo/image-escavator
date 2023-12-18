import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

import fitz

# Gruvbox color scheme
colors = {
    "bg": "#282828",
    "text": "#ebdbb2",
    "button_bg": "#458588",
    "button_fg": "#ebdbb2",
    "status": "#b16286",
}


def create_button(parent, text, command, padx=10, pady=10):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=colors["button_bg"],
        fg=colors["button_fg"],
        padx=padx,
        pady=pady,
        borderwidth=0,
    )


def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_file.set(file_path)
        status_label.config(text="Selected PDF: " + os.path.basename(file_path))


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder.set(folder_path)
        status_label.config(text="Output folder selected")


def extract_images_from_pdf(pdf_path, output_folder):
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


def extract():
    if pdf_file.get() and output_folder.get():
        extract_images_from_pdf(pdf_file.get(), output_folder.get())
        # shutil.make_archive(output_folder.get(), "zip", output_folder.get())
        # shutil.rmtree(output_folder.get())
        messagebox.showinfo("Success", "Images extracted and zipped successfully")
        status_label.config(text="Done!")
    else:
        messagebox.showwarning("Warning", "Please select a PDF and output folder")


# GUI Design
root = tk.Tk()
root.title("PDF Image Extractor")
root.geometry("500x250")
root.configure(bg=colors["bg"])

pdf_file = tk.StringVar()
output_folder = tk.StringVar()

frame = tk.Frame(root, bg=colors["bg"])
frame.pack(pady=20)

select_pdf_button = create_button(frame, "Select PDF", select_pdf)
select_pdf_button.pack(side=tk.LEFT, padx=10)

select_output_button = create_button(
    frame, "Select Output Folder", select_output_folder
)
select_output_button.pack(side=tk.LEFT, padx=10)

process_button = create_button(root, "Extract", extract, pady=15)
process_button.pack(pady=20)

status_label = tk.Label(root, text="", fg=colors["status"], bg=colors["bg"])
status_label.pack(pady=10)

root.mainloop()
