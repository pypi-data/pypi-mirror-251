from . import *

with BaseLoader.safe_define():
    import toml

    class LoaderTOML(BaseLoader):

        @staticmethod
        def acronyms() -> Set[str]:
            return {"toml"}

        @staticmethod
        def extensions() -> Set[str]:
            return {".toml"}

        def load(self):
            if BrokenDotmapUtils.empty_file(self.value):
                return BrokenDotmap()

            elif BrokenDotmapUtils.non_empty_file(self.value):
                return BrokenDotmap(toml.load(self.value))

            elif isinstance(self.value, str):
                return BrokenDotmap(toml.loads(self.value))

            elif isinstance(self.value, dict):
                return BrokenDotmap(self.value)

            elif isinstance(self.value, bytes):
                return BrokenDotmap(toml.loads(self.value.decode("utf-8")))
            else:
                raise RuntimeError(f"Cannot load TOML from value {self.value}")

        def dump(self, path: Path):
            print(f":: LoaderTOML.dump()")
            path.write_text(toml.dumps(self.value))

        def can_load(key: str, value: Any=None) -> bool:
            if Path(key).suffix.lower() in LoaderTOML.extensions():
                return True

    BaseLoader.loaders.append(LoaderTOML)
