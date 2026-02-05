from core.storage import S3Manager
from core.loader import CloudDataLoader
from core.database import DatabaseManager

def main():
    s3 = S3Manager()
    loader = CloudDataLoader()
    db = DatabaseManager()

    files = s3.list_raw_files()
    valid_ext = ('.pdf', '.docx', '.xlsx')
    
    for key in files:
        if not key.lower().endswith(valid_ext): continue
        
        print(f"🚀 Обробка: {key}")
        file_bytes = s3.get_file_content(key)
        chunks = loader.get_chunks(file_bytes, key)
        
        if chunks:
            db.upload_chunks(chunks)
            s3.save_chunks_to_s3(key, chunks)
            print(f" Готово: {key}")

if __name__ == "__main__":
    main()