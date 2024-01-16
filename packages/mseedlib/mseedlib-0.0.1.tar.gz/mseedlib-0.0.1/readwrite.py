#!/usr/bin/env python3

from mseedlib import MSRecordReader, TimeFormat

path = 'testdata-3channel-signal.mseed3'
#path'http://ds.iris.edu/files/staff/chad/two.mseed'
#path = '/Users/chad/data/COLA.876.seed'

def handler(buffer, handler_data):
    handler_data.write(buffer)

ofh = open('out.mseed', 'wb')

with MSRecordReader(path, verbose=0, skip_not_data=True, validate_crc=True, unpack_data=True) as msreader:

    msreader.set_record_handler(handler, handler_data=ofh)

    for msr in msreader:
        msr.print(0)
        print(f' StartTime: {msr.start_time_str(timeformat=TimeFormat.ISOMONTHDAY_SPACE_Z)}')
        print(f'  SourceID: {msr.sourceid}')
        print(f'    reclen: {msr.record_length}')
        print()

        #msr.sourceid = "MY new SID"
        msr.encoding = 4
        msr.format_version = 3
        msr.record_length = 512

        (samples, records) = msr.pack(data_samples=msr.data_samples,
                                      sample_type='f',
                                      flush_data=True, verbose=8)

        print(f'Records packed: {records}, samples packed: {samples}')

        break

ofh.close()
