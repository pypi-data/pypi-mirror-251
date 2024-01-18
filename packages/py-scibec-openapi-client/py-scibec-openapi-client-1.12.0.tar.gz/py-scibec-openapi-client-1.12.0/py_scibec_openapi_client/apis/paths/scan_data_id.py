from py_scibec_openapi_client.paths.scan_data_id.get import ApiForget
from py_scibec_openapi_client.paths.scan_data_id.put import ApiForput
from py_scibec_openapi_client.paths.scan_data_id.delete import ApiFordelete
from py_scibec_openapi_client.paths.scan_data_id.patch import ApiForpatch


class ScanDataId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
