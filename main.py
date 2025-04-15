import os
import shutil
from PIL import Image
import argparse

def is_image_corrupt(image_path):
    """
    Memeriksa apakah gambar rusak atau tidak
    dengan mencoba membukanya menggunakan PIL
    """
    try:
        with Image.open(image_path) as img:
            # Mencoba memuat gambar ke memori untuk mengecek apakah rusak
            img.verify()
            # Jika tidak error, coba juga load image
            img = Image.open(image_path)
            img.load()
        return False  # Gambar bagus
    except (IOError, SyntaxError, OSError):
        return True  # Gambar rusak

def sort_images(source_folder, good_folder, corrupt_folder):
    """
    Memindai folder sumber dan memindahkan gambar ke folder yang sesuai
    """
    # Buat folder jika belum ada
    os.makedirs(good_folder, exist_ok=True)
    os.makedirs(corrupt_folder, exist_ok=True)
    
    # Format gambar yang didukung
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # Statistik
    total_images = 0
    corrupt_count = 0
    good_count = 0
    
    print(f"Memindai folder: {source_folder}")
    
    # Memeriksa semua file di folder sumber
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        
        # Skip jika bukan file atau bukan gambar
        if not os.path.isfile(file_path):
            continue
            
        ext = os.path.splitext(filename)[1].lower()
        if ext not in image_extensions:
            continue
            
        total_images += 1
        print(f"Memeriksa {filename}... ", end="")
        
        # Periksa apakah gambar rusak
        if is_image_corrupt(file_path):
            dest_path = os.path.join(corrupt_folder, filename)
            shutil.copy2(file_path, dest_path)
            print("RUSAK")
            corrupt_count += 1
        else:
            dest_path = os.path.join(good_folder, filename)
            shutil.copy2(file_path, dest_path)
            print("BAGUS")
            good_count += 1
    
    print("\nSelesai!")
    print(f"Total gambar diperiksa: {total_images}")
    print(f"Gambar bagus: {good_count}")
    print(f"Gambar rusak: {corrupt_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program untuk memisahkan foto bagus dan rusak")
    parser.add_argument("--source", "-s", required=True, help="Folder sumber yang berisi foto/gambar")
    parser.add_argument("--good", "-g", default="good_images", help="Folder untuk menyimpan gambar bagus")
    parser.add_argument("--corrupt", "-c", default="corrupt_images", help="Folder untuk menyimpan gambar rusak")
    
    args = parser.parse_args()
    
    sort_images(args.source, args.good, args.corrupt)
