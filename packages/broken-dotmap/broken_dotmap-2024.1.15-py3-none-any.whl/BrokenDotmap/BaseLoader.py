from . import *

T = TypeVar("T")

@attrs.define
class BaseLoader(ABC):

    # Global values
    loaders = list()

    # Self values
    value: T = attrs.field(default=None)

    # # Must implement own methods

    @staticmethod
    @abstractmethod
    def acronyms(self) -> Set[str]:
        ...

    @staticmethod
    @abstractmethod
    def extensions(self) -> Set[str]:
        ...

    @abstractmethod
    def load(self) -> T:
        ...

    @abstractmethod
    def dump(self, path: Path) -> None:
        ...

    @abstractmethod
    def can_load(key: str, value: Any=None) -> bool:
        ...

    # # Default implementations

    def __call__(self, value: Any) -> Self:
        """Handle calling the instance as a function"""
        self.value = value
        return self

    # # Class DotLoader methods

    @contextlib.contextmanager
    def safe_define() -> None:
        """Safely define a new DotLoader class"""
        try:
            yield
        except ImportError as e:
            print(f"Failed to import a module for DotLoader {e}")
            pass
        except BaseException as e:
            raise e
        finally:
            pass

    def find_loader(key: str, value: Any=None, acronym: str=None) -> Optional[Self]:
        """Find a loader that can load the given key"""
        for match in BaseLoader.loaders:
            if match.can_load(key=key, value=value):
                return match
        return None

