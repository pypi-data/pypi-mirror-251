from _typeshed import Incomplete as Incomplete
from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union

class Cgroup(Enum):
    host: str
    private: str

class CredentialSpec(BaseModel):
    class Config:
        extra: Incomplete
    config: Optional[str]
    file: Optional[str]
    registry: Optional[str]

class Condition(Enum):
    service_started: str
    service_healthy: str
    service_completed_successfully: str

class DependsOn(BaseModel):
    class Config:
        extra: Incomplete
    restart: Optional[bool]
    condition: Condition

class Extend(BaseModel):
    class Config:
        extra: Incomplete
    service: str
    file: Optional[str]

class Logging(BaseModel):
    class Config:
        extra: Incomplete
    driver: Optional[str]
    options: Optional[Dict[None, Optional[Union[str, float]]]]

class Port(BaseModel):
    class Config:
        extra: Incomplete
    mode: Optional[str]
    host_ip: Optional[str]
    target: Optional[int]
    published: Optional[Union[str, int]]
    protocol: Optional[str]

class PullPolicy(Enum):
    always: str
    never: str
    if_not_present: str
    build: str
    missing: str

class Ulimit(BaseModel):
    class Config:
        extra: Incomplete
    hard: int
    soft: int

class Selinux(Enum):
    z: str
    Z: str

class Bind(BaseModel):
    class Config:
        extra: Incomplete
    propagation: Optional[str]
    create_host_path: Optional[bool]
    selinux: Optional[Selinux]

class Volume2(BaseModel):
    class Config:
        extra: Incomplete
    nocopy: Optional[bool]

class Tmpfs(BaseModel):
    class Config:
        extra: Incomplete
    size: Optional[Union[None, str]]
    mode: Optional[float]

class Volume1(BaseModel):
    class Config:
        extra: Incomplete
    type: str
    source: Optional[str]
    target: Optional[str]
    read_only: Optional[bool]
    consistency: Optional[str]
    bind: Optional[Bind]
    volume: Optional[Volume2]
    tmpfs: Optional[Tmpfs]

class Healthcheck(BaseModel):
    class Config:
        extra: Incomplete
    disable: Optional[bool]
    interval: Optional[str]
    retries: Optional[float]
    test: Optional[Union[str, List[str]]]
    timeout: Optional[str]
    start_period: Optional[str]

class Order(Enum):
    start_first: str
    stop_first: str

class RollbackConfig(BaseModel):
    class Config:
        extra: Incomplete
    parallelism: Optional[int]
    delay: Optional[str]
    failure_action: Optional[str]
    monitor: Optional[str]
    max_failure_ratio: Optional[float]
    order: Optional[Order]

class UpdateConfig(BaseModel):
    class Config:
        extra: Incomplete
    parallelism: Optional[int]
    delay: Optional[str]
    failure_action: Optional[str]
    monitor: Optional[str]
    max_failure_ratio: Optional[float]
    order: Optional[Order]

class Limits(BaseModel):
    class Config:
        extra: Incomplete
    cpus: Optional[Union[float, str]]
    memory: Optional[str]
    pids: Optional[int]

class RestartPolicy(BaseModel):
    class Config:
        extra: Incomplete
    condition: Optional[str]
    delay: Optional[str]
    max_attempts: Optional[int]
    window: Optional[str]

class Preference(BaseModel):
    class Config:
        extra: Incomplete
    spread: Optional[str]

class Placement(BaseModel):
    class Config:
        extra: Incomplete
    constraints: Optional[List[str]]
    preferences: Optional[List[Preference]]
    max_replicas_per_node: Optional[int]

class DiscreteResourceSpec(BaseModel):
    class Config:
        extra: Incomplete
    kind: Optional[str]
    value: Optional[float]

class GenericResource(BaseModel):
    class Config:
        extra: Incomplete
    discrete_resource_spec: Optional[DiscreteResourceSpec]

class GenericResources(BaseModel):
    __root__: List[GenericResource]

class ConfigItem(BaseModel):
    class Config:
        extra: Incomplete
    subnet: Optional[str]
    ip_range: Optional[str]
    gateway: Optional[str]
    aux_addresses: Optional[Dict[None, str]]

class Ipam(BaseModel):
    class Config:
        extra: Incomplete
    driver: Optional[str]
    config: Optional[List[ConfigItem]]
    options: Optional[Dict[None, str]]

class External(BaseModel):
    class Config:
        extra: Incomplete
    name: Optional[str]

class External2(BaseModel):
    name: Optional[str]

class Command(BaseModel):
    __root__: Optional[Union[str, List[str]]]

class ListOfStrings(BaseModel):
    __root__: List[str]

class ListOrDict(BaseModel):
    __root__: Union[Dict[None, Optional[Union[str, float, bool]]], List[str]]

class BlkioLimit(BaseModel):
    class Config:
        extra: Incomplete
    path: Optional[str]
    rate: Optional[Union[int, str]]

class BlkioWeight(BaseModel):
    class Config:
        extra: Incomplete
    path: Optional[str]
    weight: Optional[int]

class ServiceConfigOrSecretItem(BaseModel):
    class Config:
        extra: Incomplete
    source: Optional[str]
    target: Optional[str]
    uid: Optional[str]
    gid: Optional[str]
    mode: Optional[float]

class ServiceConfigOrSecret(BaseModel):
    __root__: List[Union[str, ServiceConfigOrSecretItem]]

class Constraints(BaseModel):
    __root__: Any

class BuildItem(BaseModel):
    class Config:
        extra: Incomplete
    context: Optional[str]
    dockerfile: Optional[str]
    dockerfile_inline: Optional[str]
    args: Optional[ListOrDict]
    ssh: Optional[ListOrDict]
    labels: Optional[ListOrDict]
    cache_from: Optional[List[str]]
    cache_to: Optional[List[str]]
    no_cache: Optional[bool]
    additional_contexts: Optional[ListOrDict]
    network: Optional[str]
    pull: Optional[bool]
    target: Optional[str]
    shm_size: Optional[Union[int, str]]
    extra_hosts: Optional[ListOrDict]
    isolation: Optional[str]
    privileged: Optional[bool]
    secrets: Optional[ServiceConfigOrSecret]
    tags: Optional[List[str]]
    platforms: Optional[List[str]]

class BlkioConfig(BaseModel):
    class Config:
        extra: Incomplete
    device_read_bps: Optional[List[BlkioLimit]]
    device_read_iops: Optional[List[BlkioLimit]]
    device_write_bps: Optional[List[BlkioLimit]]
    device_write_iops: Optional[List[BlkioLimit]]
    weight: Optional[int]
    weight_device: Optional[List[BlkioWeight]]

class Network1(BaseModel):
    class Config:
        extra: Incomplete
    aliases: Optional[ListOfStrings]
    ipv4_address: Optional[str]
    ipv6_address: Optional[str]
    link_local_ips: Optional[ListOfStrings]
    priority: Optional[float]

class Device(BaseModel):
    class Config:
        extra: Incomplete
    capabilities: Optional[ListOfStrings]
    count: Optional[Union[str, int]]
    device_ids: Optional[ListOfStrings]
    driver: Optional[str]
    options: Optional[ListOrDict]

class Devices(BaseModel):
    __root__: List[Device]

class Network(BaseModel):
    class Config:
        extra: Incomplete
    name: Optional[str]
    driver: Optional[str]
    driver_opts: Optional[Dict[None, Union[str, float]]]
    ipam: Optional[Ipam]
    external: Optional[External]
    internal: Optional[bool]
    enable_ipv6: Optional[bool]
    attachable: Optional[bool]
    labels: Optional[ListOrDict]

class Volume(BaseModel):
    class Config:
        extra: Incomplete
    name: Optional[str]
    driver: Optional[str]
    driver_opts: Optional[Dict[None, Union[str, float]]]
    external: Optional[External]
    labels: Optional[ListOrDict]

class Secret(BaseModel):
    class Config:
        extra: Incomplete
    name: Optional[str]
    environment: Optional[str]
    file: Optional[str]
    external: Optional[External2]
    labels: Optional[ListOrDict]
    driver: Optional[str]
    driver_opts: Optional[Dict[None, Union[str, float]]]
    template_driver: Optional[str]

class Config(BaseModel):
    class Config:
        extra: Incomplete
    name: Optional[str]
    file: Optional[str]
    external: Optional[External2]
    labels: Optional[ListOrDict]
    template_driver: Optional[str]

class StringOrList(BaseModel):
    __root__: Union[str, ListOfStrings]

class Reservations(BaseModel):
    class Config:
        extra: Incomplete
    cpus: Optional[Union[float, str]]
    memory: Optional[str]
    generic_resources: Optional[GenericResources]
    devices: Optional[Devices]

class Resources(BaseModel):
    class Config:
        extra: Incomplete
    limits: Optional[Limits]
    reservations: Optional[Reservations]

class Deployment(BaseModel):
    class Config:
        extra: Incomplete
    mode: Optional[str]
    endpoint_mode: Optional[str]
    replicas: Optional[int]
    labels: Optional[ListOrDict]
    rollback_config: Optional[RollbackConfig]
    update_config: Optional[UpdateConfig]
    resources: Optional[Resources]
    restart_policy: Optional[RestartPolicy]
    placement: Optional[Placement]

class IncludeItem(BaseModel):
    class Config:
        extra: Incomplete
    path: Optional[StringOrList]
    env_file: Optional[StringOrList]
    project_directory: Optional[str]

class Include(BaseModel):
    __root__: Union[str, IncludeItem]

class Service(BaseModel):
    class Config:
        extra: Incomplete
    deploy: Optional[Deployment]
    annotations: Optional[ListOrDict]
    build: Optional[Union[str, BuildItem]]
    blkio_config: Optional[BlkioConfig]
    cap_add: Optional[List[str]]
    cap_drop: Optional[List[str]]
    cgroup: Optional[Cgroup]
    cgroup_parent: Optional[str]
    command: Optional[Command]
    configs: Optional[ServiceConfigOrSecret]
    container_name: Optional[str]
    cpu_count: Optional[None]
    cpu_percent: Optional[None]
    cpu_shares: Optional[Union[float, str]]
    cpu_quota: Optional[Union[float, str]]
    cpu_period: Optional[Union[float, str]]
    cpu_rt_period: Optional[Union[float, str]]
    cpu_rt_runtime: Optional[Union[float, str]]
    cpus: Optional[Union[float, str]]
    cpuset: Optional[str]
    credential_spec: Optional[CredentialSpec]
    depends_on: Optional[Union[ListOfStrings, Dict[None, DependsOn]]]
    device_cgroup_rules: Optional[ListOfStrings]
    devices: Optional[List[str]]
    dns: Optional[StringOrList]
    dns_opt: Optional[List[str]]
    dns_search: Optional[StringOrList]
    domainname: Optional[str]
    entrypoint: Optional[Command]
    env_file: Optional[StringOrList]
    environment: Optional[ListOrDict]
    expose: Optional[List[Union[str, float]]]
    extends: Optional[Union[str, Extend]]
    external_links: Optional[List[str]]
    extra_hosts: Optional[ListOrDict]
    group_add: Optional[List[Union[str, float]]]
    healthcheck: Optional[Healthcheck]
    hostname: Optional[str]
    image: Optional[str]
    init: Optional[bool]
    ipc: Optional[str]
    isolation: Optional[str]
    labels: Optional[ListOrDict]
    links: Optional[List[str]]
    logging: Optional[Logging]
    mac_address: Optional[str]
    mem_limit: Optional[Union[float, str]]
    mem_reservation: Optional[Union[str, int]]
    mem_swappiness: Optional[int]
    memswap_limit: Optional[Union[float, str]]
    network_mode: Optional[str]
    networks: Optional[Union[ListOfStrings, Dict[None, Optional[Network1]]]]
    oom_kill_disable: Optional[bool]
    oom_score_adj: Optional[None]
    pid: Optional[str]
    pids_limit: Optional[Union[float, str]]
    platform: Optional[str]
    ports: Optional[List[Union[float, str, Port]]]
    privileged: Optional[bool]
    profiles: Optional[ListOfStrings]
    pull_policy: Optional[PullPolicy]
    read_only: Optional[bool]
    restart: Optional[str]
    runtime: Optional[str]
    scale: Optional[int]
    security_opt: Optional[List[str]]
    shm_size: Optional[Union[float, str]]
    secrets: Optional[ServiceConfigOrSecret]
    sysctls: Optional[ListOrDict]
    stdin_open: Optional[bool]
    stop_grace_period: Optional[str]
    stop_signal: Optional[str]
    storage_opt: Optional[Dict[str, Any]]
    tmpfs: Optional[StringOrList]
    tty: Optional[bool]
    ulimits: Optional[Dict[None, Union[int, Ulimit]]]
    user: Optional[str]
    uts: Optional[str]
    userns_mode: Optional[str]
    volumes: Optional[List[Union[str, Volume1]]]
    volumes_from: Optional[List[str]]
    working_dir: Optional[str]

class ComposeSpecification(BaseModel):
    class Config:
        extra: Incomplete
    version: Optional[str]
    name: Optional[None]
    include: Optional[List[Include]]
    services: Optional[Dict[None, Service]]
    networks: Optional[Dict[None, Optional[Network]]]
    volumes: Optional[Dict[None, Optional[Volume]]]
    secrets: Optional[Dict[None, Secret]]
    configs: Optional[Dict[None, Config]]
