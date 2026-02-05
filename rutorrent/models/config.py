import dataclasses

import pydantic


@pydantic.validate_arguments
@dataclasses.dataclass
class Config:
    dht: bool
    check_hash: bool
    bind: str
    """Bind address"""
    dht_port: str
    directory: str
    """Default download directory"""
    download_rate: int
    """Max download rate in bytes"""
    hash_interval: str
    hash_max_tries: str
    hash_read_ahead: str
    http_cacert: str
    http_capath: str
    http_proxy: str
    ip: str
    max_downloads_div: int
    max_downloads_global: int
    max_file_size: int
    max_memory_usage: int
    """Max memory usage in bytes"""
    max_open_files: int
    max_open_http: int
    max_peers: int
    max_peers_seed: int
    max_uploads: int
    max_uploads_global: int
    min_peers_seed: int
    min_peers: int
    peer_exchange: bool
    port_open: bool
    upload_rate: int
    """Max upload rate in bytes"""
    port_random: bool
    port_range: str
    preload_min_size: int
    preload_required_rate: int
    preload_type: int
    proxy_address: str
    receive_buffer_size: int
    safe_sync: bool
    scgi_dont_route: bool
    send_buffer_size: int
    session: str
    """Session directory"""
    session_lock: bool
    session_on_completion: bool
    split_file_size: int
    split_suffix: str
    timeout_safe_sync: int
    timeout_sync: int
    tracker_numwant: int
    use_udp_trackers: bool
    max_uploads_div: int
    max_open_sockets: int
