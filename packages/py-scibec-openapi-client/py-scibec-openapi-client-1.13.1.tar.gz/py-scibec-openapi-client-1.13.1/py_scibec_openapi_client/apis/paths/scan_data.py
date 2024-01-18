from py_scibec_openapi_client.paths.scan_data.get import ApiForget
from py_scibec_openapi_client.paths.scan_data.post import ApiForpost
from py_scibec_openapi_client.paths.scan_data.patch import ApiForpatch


class ScanData(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
