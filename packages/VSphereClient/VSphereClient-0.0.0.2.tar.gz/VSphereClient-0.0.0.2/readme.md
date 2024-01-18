### VSphere Client

install:
```shell
pip install VSphereClient
```

request demo:

```python
if __name__ == '__main__':
    from VSphereClient import VSphere
    
    ip = '10.x.x.x'
    user = 'username'
    password = 'password'
    port = 443
    vm = VSphere(host=ip, user=user, password=password, port=port, ssl=None)

    data_center = vm.get_data_center()
    print('data_center', data_center)
    cluster = vm.get_cluster(data_center[0]['id'])
    print('cluster', cluster)
    host = vm.get_host(data_center[0]['id'], cluster[0]['id'])
    print('host', host)
    vm_list = vm.get_vm(data_center[0]['id'], cluster[0]['id'])
    print('vm_list', vm_list)
    store_cluster = vm.get_storage_cluster()
    print('store_cluster', store_cluster)
    store_list = vm.get_storage_by_host(data_center[0]['id'], cluster[0]['id'], host[0]['id'])
    print('store_list', store_list)
    store_list = vm.get_storage_by_host(data_center[0]['id'], cluster[0]['id'], '')
    print(store_list)
    vlan = vm.get_vlan(data_center[0]['id'])
    print('vlan', vlan)
    # windows: 'HQ-T-Temp-WIN2016EN-2023Q2', '123456'
    # linux: 'HQ-T-Temp-redhat7.9-2023Q2', '123456'
    clone_res = vm.clone_vm(template_name='HQccc023Q2',
                            vm_name='ops-test-00001',
                            datacenter_id=data_center[0]['id'],
                            cluster_id=cluster[0]['id'],
                            host_id=host[0]['id'],
                            cpu_num=8,
                            memory=16384,
                            vm_ip='192.168.1.10',
                            vm_subnetmask='255.255.255.0',
                            vm_gateway='192.168.1.1',
                            vm_dns=["10.1.1.1", "10.1.1.2"],
                            vm_domain='abc.auto',
                            network_id=vlan[0]['id'],
                            data_disk_id=store_list[0]['id'],
                            data_disk_size=130,
                            password='Aa123456,.'
                            )
    print('clone_res', clone_res)
    # windows 修改密码
    result = vm.change_password(is_win=True, vm_name='ops-test-00002',
                                username='administrator',
                                old_password='Aa123456,./789',
                                new_password='Aa123456,./788')
    print(result)
    # linux 修改密码
    result = vm.change_password(is_win=False, vm_name='ops-test-00001',
                                username='root',
                                old_password='MZyyty1O5ty!2lT2l',
                                new_password='MD2DHHD!aIup03H2u')
    print(result)
```
