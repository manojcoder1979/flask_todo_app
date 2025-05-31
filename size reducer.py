import fitz  # PyMuPDF

def compress_pdf(input_path, output_path, image_quality=20):
    doc = fitz.open(input_path)
    for page in doc:
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Compress image using PIL
            from PIL import Image
            from io import BytesIO
            
            image = Image.open(BytesIO(image_bytes))
            buffer = BytesIO()
            image.save(buffer, format=image_ext, quality=image_quality)
            
            doc.update_image(xref, buffer.getvalue())
    doc.save(output_path, garbage=4, deflate=True)
    print(f"Compressed PDF saved to: {output_path}")

# Example usage
compress_pdf("input.pdf", "compressed_output.pdf", image_quality=30)
