import platformdirs
import pathlib
import shutil

def ensuredir(path: pathlib.Path):
    if not path.exists():
        path.mkdir()


class Platform:
    ConfigDir: pathlib.Path = platformdirs.user_config_path().joinpath("pdfriend")
    CacheDir: pathlib.Path = platformdirs.user_cache_path().joinpath("pdfriend")
    TempDir: pathlib.Path = CacheDir.joinpath("temp")
    BackupDir: pathlib.Path = CacheDir.joinpath("backups")

    @classmethod
    def Init(cls): # make sure the system directories exist
        ensuredir(cls.ConfigDir)
        ensuredir(cls.CacheDir)
        ensuredir(cls.BackupDir)

        if cls.TempDir.exists(): # temp dir always cleared on startup
            shutil.rmtree(cls.TempDir.as_posix())
        cls.TempDir.mkdir()

    @classmethod
    def NewTemp(cls, path_name: str) -> pathlib.Path:
        return cls.TempDir.joinpath(path_name)

    @classmethod
    def NewBackup(cls, path_name: str) -> pathlib.Path:
        return cls.BackupDir.joinpath(path_name)
