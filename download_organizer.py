import os
import hashlib
import shutil
from pathlib import Path

class DownloadOrganizer:
    # Subfolder definitions
    SUB_FOLDERS = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
        "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
        "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi", ".bat"]
    }

    def __init__(self, download_dir: Path | None = None) -> None:
        self.download_directory = download_dir or (Path.home() / "Downloads")
        # Invert mapping: {".jpg": "Images", ".png": "Images", ...}
        self.extension_map = {
            ext.lower(): folder 
            for folder, exts in self.SUB_FOLDERS.items() 
            for ext in exts
        }

    def create_sub_folders(self) -> None:
        """Create target subfolders if they do not exist."""
        self.download_directory.mkdir(parents=True, exist_ok=True)
        for folder_name in self.SUB_FOLDERS:
            (self.download_directory / folder_name).mkdir(exist_ok=True)

    def _get_unique_path(self, destination: Path) -> Path:
        """Generates a non-conflicting path if destination already exists."""
        if not destination.exists():
            return destination
        
        counter = 1
        stem, suffix, parent = destination.stem, destination.suffix, destination.parent
        while destination.exists():
            destination = parent / f"{stem}_{counter}{suffix}"
            counter += 1
            
        return destination

    def organize_files(self) -> None:
        """Move loose files into designated subfolders."""
        if not self.download_directory.exists():
            return

        self.create_sub_folders()

        for item in self.download_directory.iterdir():
            if item.is_dir():
                continue

            folder_name = self.extension_map.get(item.suffix.lower())
            if folder_name:
                target_folder = self.download_directory / folder_name
                target_path = self._get_unique_path(target_folder / item.name)

                try:
                    shutil.move(str(item), str(target_path))
                    print(f"Moved: {item.name} -> {folder_name}/{target_path.name}")
                except OSError as e:
                    print(f"Failed to move {item.name}: {e}")

    @staticmethod
    def calculate_file_hash(file_path: Path, chunk_size: int = 65536) -> str:
        """Calculate SHA-256 hash using 64KB chunks for optimal disk I/O."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except OSError:
            return ""

    def remove_duplicate_files(self) -> None:
        """Identify and delete identical files across the directory tree."""
        if not self.download_directory.exists():
            return

        files_by_size = {}
        # First pass: Group by file size to avoid hashing unique files
        for item in self.download_directory.rglob("*"):
            if item.is_file():
                try:
                    files_by_size.setdefault(item.stat().st_size, []).append(item)
                except OSError:
                    continue

        seen_hashes = set()
        duplicates_removed = 0

        # Second pass: Only hash files that share identical byte sizes
        for size, files in files_by_size.items():
            if len(files) < 2:
                continue

            for file_path in files:
                file_hash = self.calculate_file_hash(file_path)
                if not file_hash:
                    continue

                if file_hash in seen_hashes:
                    try:
                        file_path.unlink()
                        print(f"Deleted duplicate: {file_path}")
                        duplicates_removed += 1
                    except OSError as e:
                        print(f"Failed to delete {file_path}: {e}")
                else:
                    seen_hashes.add(file_hash)

        print(f"Cleanup complete. Total duplicate files removed: {duplicates_removed}")

    def remove_empty_folders(self) -> None:
        """Recursively delete empty folders bottom-up."""
        if not self.download_directory.exists():
            return

        removed_count = 0
        # os.walk bottom-up ensures child folders delete before checking parents
        for root, dirs, _ in os.walk(self.download_directory, topdown=False):
            for dir_name in dirs:
                folder_path = Path(root) / dir_name
                try:
                    folder_path.rmdir()  # Fails automatically if folder isn't empty
                    print(f"Removed empty folder: {folder_path.relative_to(self.download_directory)}")
                    removed_count += 1
                except OSError:
                    continue

        print(f"Cleanup complete. Removed {removed_count} empty folder(s).")
