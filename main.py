#PDF to JPG,JPEG,PNG converter(With PyMuPDF )
import fitz
import os

def pdf_to_img(pdf_path,image_type,output_folder):
    os.makedirs(output_folder,exist_ok=True)
    doc=fitz.open(pdf_path)
    output_images=[]
    zoom = 2  # Increase resolution for better quality
    for i, page in enumerate(doc):
        if image_type.lower() == 'png':
            pix=page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True) # For PNG, we can include alpha channel for transparency if needed
        else:
            pix=page.get_pixmap(matrix=fitz.Matrix(zoom, zoom)) # For JPG/JPEG, we don't need alpha channel
        filename=f"image_{i+1}.{image_type}"
        path=os.path.join(output_folder,filename)
        
        pix.save(path)
        
        output_images.append(path)
    doc.close()
    return output_images

