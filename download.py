import qmpy_rester as qr
import json
import os

PAGE_LIMIT = 1500

if not os.path.exists('query_files'):
    os.mkdir('query_files')


def download_by_batch(batch_num):

    with qr.QMPYRester() as q:
        kwargs = {'limit': PAGE_LIMIT,
                  'offset': batch_num * PAGE_LIMIT,
                  'fields': 'name,delta_e,composition,prototype,volume,natoms,band_gap,stability',
                  }
        data = q.get_oqmd_phases(verbose=False, **kwargs)


    with open('query_files/query_' + str(491+batch_num) + '.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    # if data['meta']['more_data_available'] is None:
    #     return True
    # else:
    #     return False
    if batch_num >150:
        return False
    else:
        return True


if __name__ == "__main__":
    batch_num = 0
    while download_by_batch(batch_num):
        batch_num = batch_num + 1