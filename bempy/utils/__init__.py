import json
from typing import Dict, List, Any, TypeVar, Callable

T = TypeVar('T')

def merge(source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges two dictionaries recursively.
    
    This function takes two dictionaries and merges them, with values from the source
    dictionary overriding values in the destination dictionary if they have the same key.
    For nested dictionaries, the merge is done recursively.
    
    Args:
        source (Dict[str, Any]): The source dictionary.
        destination (Dict[str, Any]): The destination dictionary.
        
    Returns:
        Dict[str, Any]: The merged dictionary.
        
    Example:
        >>> a = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
        >>> b = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}
        >>> merge(b, a) == {'first': {'all_rows': {'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
        True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


def uniq_f7(seq: List[T]) -> List[T]:
    """
    Returns a list with duplicate elements removed while preserving order.
    
    Args:
        seq (List[T]): The input sequence.
        
    Returns:
        List[T]: A list with duplicate elements removed.
        
    Example:
        >>> uniq_f7([1, 2, 3, 2, 1, 4])
        [1, 2, 3, 4]
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def safe_serialize(obj: Any) -> str:
    """
    Safely serializes an object to JSON, converting non-serializable objects to strings.
    
    Args:
        obj (Any): The object to serialize.
        
    Returns:
        str: A JSON string representation of the object.
        
    Example:
        >>> class MyClass: pass
        >>> obj = {'name': 'test', 'instance': MyClass()}
        >>> json_str = safe_serialize(obj)
        # json_str will contain a string representation of the object
    """
    default: Callable[[Any], str] = lambda o: str(o)
    return json.dumps(obj, default=default)
