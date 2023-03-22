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
            user=dict(required=True, type='str'),
            password=dict(required=True, type='str'),
            job=dict(required=True, type='str'),
            credential=dict(required=True, type='str')
            )
    
    module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=False
            )

    auth = (module.params['user'], module.params['password'])
    url = module.params['url'] + "/api/v2/job_templates/" + str(module.params['job']) + "/launch/"
    credential = module.params['credential']
    payload = {"extra_vars": {}, "credentials": [credential]}
 
    debg = (url, auth, payload)
    result = requests.post(url, auth=auth, json=payload)

    if result.status_code == 201:
        noerror = True
    else:
        noerror = False

    if noerror:
        result = dict(
            changed=True,
            Response=f'Success launch job ' + str(module.params['job'])
            )
        module.exit_json(**result)
    else:
        module.fail_json(msg=f"{debg}")

if __name__ == '__main__':
    main()
