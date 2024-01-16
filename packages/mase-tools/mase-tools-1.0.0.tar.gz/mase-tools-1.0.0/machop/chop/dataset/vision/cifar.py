from torch.utils.data import Dataset
from torchvision import datasets
import os
from ..utils import add_dataset_info


@add_dataset_info(
    name="cifar10",
    dataset_source="torchvision",
    available_splits=("train", "test"),
    image_classification=True,
    num_classes=10,
    image_size=(3, 32, 32),
)
class Cifar10Mase(datasets.CIFAR10):
    def __init__(
        self, root: os.PathLike, train: bool, transform: callable, download: bool
    ) -> None:
        super().__init__(root, train=train, transform=transform, download=download)

    def prepare_data(self) -> None:
        pass

    def setup(self) -> None:
        pass


@add_dataset_info(
    name="cifar100",
    dataset_source="torchvision",
    available_splits=("train", "test"),
    image_classification=True,
    num_classes=100,
    image_size=(3, 32, 32),
)
class Cifar100Mase(datasets.CIFAR100):
    test_dataset_available: bool = True
    pred_dataset_available: bool = False

    info = {
        "num_classes": 100,
        "image_size": (3, 32, 32),
    }

    def __init__(
        self, root: os.PathLike, train: bool, transform: callable, download: bool
    ) -> None:
        super().__init__(root, train=train, transform=transform, download=download)

    def prepare_data(self) -> None:
        pass

    def setup(self) -> None:
        pass


def get_cifar_dataset(
    name: str, path: os.PathLike, train: bool, transform: callable
) -> Dataset:
    match name.lower():
        case "cifar10":
            dataset = Cifar10Mase(path, train=train, transform=transform, download=True)
        case "cifar100":
            dataset = Cifar100Mase(
                path, train=train, transform=transform, download=True
            )
        case _:
            raise ValueError(f"Unknown dataset {name}")
    return dataset
