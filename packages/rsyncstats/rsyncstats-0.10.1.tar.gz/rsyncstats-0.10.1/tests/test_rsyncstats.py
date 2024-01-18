import pytest
import os
from rsyncstats import *

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )

@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'rsync_1_day.log'),
    os.path.join(FIXTURE_DIR, 'unit_1.log'),
    os.path.join(FIXTURE_DIR, 'unit_2.log'),
    os.path.join(FIXTURE_DIR, 'unit_3.log'),
    os.path.join(FIXTURE_DIR, 'unit_4.log')
)
def test_parse_ringserver_log(datafiles):
    path = str(datafiles)
    event_result = {'timestamp': 1551752883,
                     'pid': '27615',
                     'logtype': 'rsync to',
                     'sentbytes': '184494',
                     'receivedbytes': '19414234',
                     'totalbytes': '19609565',
                     'module': 'PORTAL-PRODUCTS-RW',
                     'directory': '/seedlinkplots/',
                     'user': 'resifportal',
                     'hostname': b'khadLrK6HR6v',
                     'clientip': '152.77.1.6',
                     'endtime': 1551752888,
                     'geohash': 'u0h0fpnzj9ft',
                     'city': 'Grenoble'}
    event = parse_log(os.path.join(path, 'unit_1.log'))[0]
    for k in ['timestamp','geohash','clientip','module','totalbytes', 'sentbytes']:
            assert k in event
            assert event[k] == event_result[k]

    event_result = {'timestamp': 1551791779, 'pid': '21612', 'logtype': 'rsync to', 'sentbytes': '4912389', 'receivedbytes': '1148837211', 'totalbytes': '70591149056', 'module': 'RAP-SDS', 'directory': '/', 'user': 'rap', 'hostname': b'0lfWYkMCCaxc', 'clientip': '152.77.159.221', 'endtime': 1551792005, 'geohash': 'u0h0fpnzj9ft', 'city': 'Grenoble'}
    event = parse_log(os.path.join(path, 'unit_2.log'))[0]
    for k in ['timestamp','geohash','clientip','module','totalbytes', 'sentbytes']:
            assert k in event
            assert event[k] == event_result[k]

    event_result = {'timestamp': 1551808825, 'pid': '6154', 'logtype': 'rsync on', 'sentbytes': '24132995', 'receivedbytes': '122', 'totalbytes': '1006481408', 'module': 'Z32015-VALIDATED-DATA', 'directory': '/2019/A208A', 'user': 'Z32015', 'hostname': b'wLOnnDA90G3K', 'clientip': '134.59.147.15', 'endtime': 1551808827, 'geohash': 'spv0tjy4ntet', 'city': 'Nice'}
    event = parse_log(os.path.join(path, 'unit_3.log'))[-1]
    for k in ['timestamp','geohash','clientip','module','totalbytes', 'sentbytes']:
            assert k in event
            assert event[k] == event_result[k]

    event = parse_log(os.path.join(path, 'unit_4.log'))
    assert event == []
