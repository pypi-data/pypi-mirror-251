from pdfriend.classes.platforms import Platform
import shutil

def clear():
    if Platform.BackupDir.exists():
        shutil.rmtree(Platform.BackupDir.as_posix())

    Platform.BackupDir.mkdir()
