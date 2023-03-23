#!/usr/bin/python

'''
Documentation:
    Description:

    Parameter:
'''

import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native

def main():
    module_args = dict(
            url=dict(required=True, type='str'),
            api_v=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            job=dict(required=True, type='str'),
            )

    module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=False
            )

    auth = (module.params['user'], module.params['password'])
    url = module.params['url'] + "/api/v" + module.params['api_v'] + "/workflow_job_templates/" + module.params['job'] + "/launch/"

    result = requests.post(url, auth=auth)

    if result.status_code == 201:
        result = dict(
            changed=True,
            Response=f'Success launch job ' + module.params['job']
            )
        module.exit_json(**result)
    elif result.status_code == 401:
        module.fail_json(msg=f'Error401 - Incorrect login credentials')
    elif result.status_code == 400:
        module.fail_json(msg=f'Error400 - Invalid request')
    elif result.status_code == 404:
        module.fail_json(msg=f'Error404 - Incorrect job id or api version')
    else:
        module.fail_json(msg=f'Error launch job {result}')

if __name__ == '__main__':
    main()
