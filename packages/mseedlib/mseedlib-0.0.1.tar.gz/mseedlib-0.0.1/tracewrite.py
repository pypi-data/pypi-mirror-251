#!/usr/bin/env python3

import math
from mseedlib import MSTraceList, timestr2nstime, sampletime


def sine_gen3(start_degree=[0, 45, 90], yield_count=100, total=1000):
    '''A generator returning 3 continuing sequences for a sine values.

    The default starting degree values are 0, 45, and 90 in order to
    generate 3 different sine waves.

    Each iteration yields a tuple of 3 lists of continuing sine values.
    '''
    generated = 0
    while generated < total:
        bite_size = min(yield_count, total - generated)

        # Yield a tuple of 3 lists of continuing sine values
        yield (list(map(lambda x: int(math.sin(math.radians(x)) * 500),
                        range(start_degree[0], start_degree[0] + bite_size))),
               list(map(lambda x: int(math.sin(math.radians(x)) * 500),
                    range(start_degree[1], start_degree[1] + bite_size))),
               list(map(lambda x: int(math.sin(math.radians(x)) * 500),
                        range(start_degree[2], start_degree[2] + bite_size))))

        start_degree = [r + bite_size for r in start_degree]
        generated += bite_size


output_file = "test.mseed"
output_handle = open(output_file, 'wb')


def record_handler(record, output):
    '''A callback function for MSTraceList.set_record_handler()
    Writes the record to the specified output stream
    '''
    output.write(bytes(record))


# Create new MSTraceList
mstl = MSTraceList()

# Set record handler
mstl.set_record_handler(record_handler, output_handle)

total_samples = 0
total_records = 0
sample_rate = 50.0
start_time = timestr2nstime("2024-01-01T15:13:55.123456789Z")
format_version = 3
record_length = 512

# Add data to the trace list from a generator of pseudo signals
for (sine1, sine2, sine3) in sine_gen3(yield_count=100, total=2000):

    # Add the pseudo signals to the trace list
    mstl.add_data(sourceid="FDSN:XX_TEST__B_S_1",
                  data_samples=sine1, sample_type='i', sample_rate=sample_rate,
                  start_time=start_time)

    mstl.add_data(sourceid="FDSN:XX_TEST__B_S_2",
                  data_samples=sine2, sample_type='i', sample_rate=sample_rate,
                  start_time=start_time)

    mstl.add_data(sourceid="FDSN:XX_TEST__B_S_3",
                  data_samples=sine3, sample_type='i', sample_rate=sample_rate,
                  start_time=start_time)

    # Advance time stamp by number of samples added for next iteration
    start_time = sampletime(start_time, len(sine1), sample_rate)

    # Pack trace list into records
    (packed_samples, packed_records) = mstl.pack(flush_data=False,
                                                 format_version=format_version,
                                                 record_length=record_length)

    total_samples += packed_samples
    total_records += packed_records

# A final call to MSTraceList.pack() with flush_data=True is required to
# flush any remaining data samples to records
(packed_samples, packed_records) = mstl.pack(flush_data=True,
                                             format_version=format_version,
                                             record_length=record_length)

total_samples += packed_samples
total_records += packed_records

output_handle.close()

print(f"Packed {total_samples} samples into {total_records} records")
