from typing import Union
import json
import numpy as np
import h5py


def h5_to_nh5(h5_path: str, nh5_path: str, *, suppress_float64_warnings: bool = False, allow_int64: bool = False):
    """Converts an h5 file to an nh5 file.

    Only a limited subset of h5 files are supported. The h5 file must contain only groups and datasets.
    The resulting nh5 file will not include any compression or chunking.

    For most visualization purposes, float32 is sufficient. So, if the h5 file contains float64 datasets,
    a warning will be printed. To suppress this warning, set suppress_float64_warnings to True.

    If the h5 file contains int64 or uint64 datasets, an error will be raised. To allow int64 or uint64
    datasets, set allow_int64 to True. The rationale is that 64-bit integers are not (easily) supported by
    JavaScript, so they cannot be (easily) handled on the frontend.

    Args:
        h5_path (str): Path to the h5 file.
        nh5_path (str): Path to the nh5 file.
        suppress_float64_warnings (bool, optional): If True, suppresses warnings about float64
            datasets being converted to float32. Defaults to False.
        allow_int64 (bool, optional): If True, allows int64 or uint64 datasets to be converted.
            Otherwise raises an error if an int64 or uint64 dataset is encountered. Defaults to False.
    """
    with h5py.File(h5_path, "r") as h5_file:
        with open(nh5_path, "wb") as nh5_file:
            header = {"datasets": [], "groups": []}
            all_groups_in_h5_file = _get_h5_groups(h5_file)
            for group in all_groups_in_h5_file:
                header["groups"].append(
                    {"path": group.name, "attrs": json.loads(_attrs_to_json(group))}
                )
            all_datasets_in_h5_file = _get_h5_datasets(h5_file)
            position = 0
            for dataset in all_datasets_in_h5_file:
                dtype = _dtype_to_str(dataset)
                if not allow_int64 and dtype in ["int64", "uint64"]:
                    raise ValueError(f"Unsupported dtype: {dtype}")
                if not suppress_float64_warnings and dtype == "float64":
                    print(
                        f"Warning: Converting float64 dataset '{dataset.name}' to float32. "
                        "Consider using float32 to save space."
                    )
                header["datasets"].append(
                    {
                        "path": dataset.name,
                        "attrs": json.loads(_attrs_to_json(dataset)),
                        "dtype": dtype,
                        "shape": _format_shape(dataset),
                        "position": int(position),
                    }
                )
                position += _get_dataset_byte_count(dataset)
            header_json = json.dumps(header).encode("utf-8")
            nh5_file.write(f"nh5|1|{len(header_json)}|".encode("utf-8"))
            nh5_file.write(header_json)
            position = 0
            for dataset in all_datasets_in_h5_file:
                nh5_file.write(dataset[...].tobytes())
                position += _get_dataset_byte_count(dataset)


def _get_h5_groups(h5_file: h5py.File) -> list:
    """Returns a list of all groups in an h5 file.

    Args:
        h5_file (h5py.File): The h5 file.

    Returns:
        list: A list of all groups in the h5 file.
    """
    groups = []

    # include root group
    groups.append(h5_file)

    def _get_groups(name, obj):
        if isinstance(obj, h5py.Group):
            groups.append(obj)

    h5_file.visititems(_get_groups)
    return groups


def _get_h5_datasets(h5_file: h5py.File) -> list:
    """Returns a list of all datasets in an h5 file.

    Args:
        h5_file (h5py.File): The h5 file.

    Returns:
        list: A list of all datasets in the h5 file.
    """
    datasets = []

    def _get_datasets(name, obj):
        if isinstance(obj, h5py.Dataset):
            datasets.append(obj)

    h5_file.visititems(_get_datasets)
    return datasets


def _attrs_to_json(group: Union[h5py.Group, h5py.Dataset]) -> str:
    """Converts the attributes of an HDF5 group or dataset to a JSON-serializable format."""
    attrs_dict = {}
    for attr_name in group.attrs:
        value = group.attrs[attr_name]

        # Convert NumPy arrays to lists
        if isinstance(value, np.ndarray):
            value = value.tolist()
        # Handle other non-serializable types as needed
        if isinstance(value, np.int64):
            value = int(value)

        attrs_dict[attr_name] = value

    return json.dumps(attrs_dict)


def _dtype_to_str(dataset: h5py.Dataset) -> str:
    """Converts the dtype of an HDF5 dataset to a string."""
    dtype = dataset.dtype
    if dtype == np.dtype("int8"):
        return "int8"
    elif dtype == np.dtype("uint8"):
        return "uint8"
    elif dtype == np.dtype("int16"):
        return "int16"
    elif dtype == np.dtype("uint16"):
        return "uint16"
    elif dtype == np.dtype("int32"):
        return "int32"
    elif dtype == np.dtype("uint32"):
        return "uint32"
    elif dtype == np.dtype("int64"):
        return "int64"
    elif dtype == np.dtype("uint64"):
        return "uint64"
    elif dtype == np.dtype("float32"):
        return "float32"
    elif dtype == np.dtype("float64"):
        return "float64"
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")


def _format_shape(dataset: h5py.Dataset) -> list:
    """Formats the shape of an HDF5 dataset to a list."""
    shape = dataset.shape
    return [int(dim) for dim in shape]


def _get_dataset_byte_count(dataset: h5py.Dataset) -> int:
    """Returns the number of bytes in an HDF5 dataset."""
    dtype = dataset.dtype
    shape = dataset.shape
    shape_prod = np.prod(shape)
    bc = _get_entry_byte_count(dtype)
    return shape_prod * bc


def _get_entry_byte_count(dtype: str):
    if dtype == "int8":
        return 1
    elif dtype == "uint8":
        return 1
    elif dtype == "int16":
        return 2
    elif dtype == "uint16":
        return 2
    elif dtype == "int32":
        return 4
    elif dtype == "uint32":
        return 4
    elif dtype == "int64":
        return 8
    elif dtype == "uint64":
        return 8
    elif dtype == "float32":
        return 4
    elif dtype == "float64":
        return 8
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")


def nh5_to_h5(nh5_path: str, h5_path: str):
    """Converts an nh5 file to an h5 file.

    Args:
        nh5_path (str): Path to the nh5 file.
        h5_path (str): Path to the h5 file.
    """
    with open(nh5_path, "rb") as nh5_file:
        initial_text = nh5_file.read(100).decode("utf-8")
        parts = initial_text.split("|")
        if len(parts) < 4:
            raise ValueError("Invalid nh5 file")
        if parts[0] != "nh5":
            raise ValueError("Invalid nh5 file")
        if parts[1] != "1":
            raise ValueError("Invalid nh5 file version")
        header_length = int(parts[2])
        nh5_file.seek(len('|'.join(parts[:3])) + 1)
        header_json = nh5_file.read(header_length).decode("utf-8")
        header = json.loads(header_json)
        header_offset = len('|'.join(parts[:3])) + 1 + header_length
        with h5py.File(h5_path, "w") as h5_file:
            for group in header["groups"]:
                if not h5_file.get(group["path"]):
                    h5_group = h5_file.create_group(group["path"])
                for attr_name, attr_value in group["attrs"].items():
                    h5_group.attrs[attr_name] = attr_value
            for dataset in header["datasets"]:
                num_bytes = _get_entry_byte_count(dataset["dtype"]) * np.prod(dataset["shape"])
                nh5_file.seek(header_offset + dataset["position"])
                buf = nh5_file.read(num_bytes)
                x = np.frombuffer(buf, dtype=dataset["dtype"]).reshape(dataset["shape"])
                h5_dataset = h5_file.create_dataset(
                    dataset["path"],
                    data=x
                )
                for attr_name, attr_value in dataset["attrs"].items():
                    h5_dataset.attrs[attr_name] = attr_value
