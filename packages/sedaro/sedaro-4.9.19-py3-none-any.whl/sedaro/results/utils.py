import math
import numpy as np

DEFAULT_HOST = 'https://api.sedaro.com'
ENGINE_MAP = {
    '0': 'gnc',
    '1': 'cdh',
    '2': 'power',
    '3': 'thermal',
}
ENGINE_EXPANSION = {
    'gnc': 'Guidance, Navigation, & Control',
    'cdh': 'Command & Data Handling',
    'power': 'Power',
    'thermal': 'Thermal',
}
STATUS_ICON_MAP = {
    "SUCCEEDED": "✅",
    "FAILED": "❌",
    "TERMINATED": "❌",
    "PAUSED": "⏸️",
    "PENDING": "⌛",
    "RUNNING": "⌛",
    "ERROR": "❌"
}
HFILL = 75


def hfill(char="-", len=HFILL):
    print(char * len)


def _element_id_dict(agent_data):
    '''Break out all blocks into a dict where each key is an ID.'''
    out = {}
    for entry in agent_data.values():
        if isinstance(entry, dict):
            for id_, value in entry.items():
                if 'id' in value:
                    if id_ in out:
                        raise ValueError(f"Duplicate ID {id_}")
                    else:
                        out[id_] = value

    return out


def _block_type_in_supers(block_type: str, meta_supers: dict, super_type: str = 'Agent') -> bool:
    if block_type == super_type:
        return True
    elif block_type in meta_supers:
        supertypes = meta_supers[block_type]
        if len(supertypes) == 0:
            return False
        return any(_block_type_in_supers(supertype, meta_supers, super_type=super_type) for supertype in supertypes)
    else:
        return False


def _get_agent_id_name_map(meta):
    '''Get mapping from agent ID to name.'''
    return {
        id_: entry['name']
        for id_, entry in meta['structure']['scenario']['blocks'].items()
        if _block_type_in_supers(entry['type'], meta['structure']['scenario']['_supers'])
    }


def _simplify_series(engine_data: dict, blocks: dict) -> dict:
    '''Build a simplified series data structure

    Creates a dictionary with the following hierarchy:
        Block ID (or root)
            Variable Name
    '''
    data = {'root': {}}
    for key, value in engine_data.items():
        if key in blocks:
            data[key] = {}
            for subkey, subvalue in value.items():
                data[key][subkey] = subvalue
        elif "/" in key:
            # Ignore engine variables
            continue
        else:
            data['root'][key] = value
    return data


def _restructure_data(series, agents, meta):
    '''Build a simplified internal data structure.

    Creates a dictionary with the following key hierarchy:

        Agent Name
            Engine Name (gnc, cdh, power, thermal)
                Time
                Series
                    Block ID (or root)
                        Variable Name
    '''
    data = {}
    blocks = {}
    for series_key in series:
        agent_id, engine_id = series_key.split("/")
        agent_name = agents[agent_id]
        engine_name = ENGINE_MAP[engine_id]

        if agent_name not in data:
            data[agent_name] = {}

        time, sub_series = series[series_key]
        if agent_id not in blocks:
            blocks[agent_id] = _element_id_dict(meta['structure']['agents'].get(agent_id, {}))
        data[agent_name][engine_name] = {
            'time': time,
            'series': _simplify_series(sub_series[agent_id], blocks[agent_id])
        }
    return data, blocks


def _get_series_type(series):
    for entry in series:
        if entry is not None:
            return type(entry).__name__
    else:
        return "None"


def bsearch(ordered_series, value):
    '''Binary search for a value in an ordered series.

    Returns the index of the value in the series, or the index of the immediately
    lower value if the value is not present.
    '''
    def _bsearch(low, high):
        if high == low:
            return low
        mid = math.ceil((high + low) / 2)
        if ordered_series[mid] == value:
            return mid
        elif ordered_series[mid] > value:
            return _bsearch(low, mid-1)
        else:
            return _bsearch(mid, high)
    if value < ordered_series[0]:
        return -1
    return _bsearch(0, len(ordered_series) - 1)


def to_time_major(series):
    if type(series) not in [list, dict]:
        return series
    elif type(series) == dict:
        new = {}
        for k in series:
            new[k] = to_time_major(series[k])
        return new
    else: # type(series) == list
        np_data = np.array(series)
        if np_data.ndim > 1:
            axes = (np_data.ndim - 1,) + tuple(range(np_data.ndim - 1))
            np_data = np.transpose(np_data, axes=axes)
        reshaped_data = np_data.tolist()
        return reshaped_data