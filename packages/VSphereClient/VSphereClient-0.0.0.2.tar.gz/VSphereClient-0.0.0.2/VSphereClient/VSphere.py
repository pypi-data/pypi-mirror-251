# @Time : 2024-01-04 11:21
# @Author  : inflower
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
# @FileName: VSphere
# @Software: PyCharm
import time
from collections import namedtuple

from pyVmomi import vim
try:
    from pyvim.connect import SmartConnectNoSSL
except:
    from pyVim.connect import SmartConnectNoSSL

ReturnStruct = namedtuple('ReturnStruct', ['code', 'message', 'data'])
ReturnStruct.__new__.__defaults__ = (False, '', None)


class VSphere(object):
    def __init__(self, host, user, password, port, ssl):
        self.config = None
        self.host = host
        self.user = user
        self.pwd = password
        self.port = port
        self.sslContext = ssl
        self.client = SmartConnectNoSSL(host=host,
                                        user=user,
                                        pwd=password,
                                        port=443
                                        )
        self.content = self.client.RetrieveContent()

    def _get_all_objs(self, obj_type, folder=None):
        """
        根据对象类型获取这一类型的所有对象
        """
        if folder is None:
            # content = self.client.RetrieveContent()
            container = self.content.viewManager.CreateContainerView(self.content.rootFolder, obj_type, True)
            # container = self.content.viewManager.CreateContainerView(content, obj_type, True)
        else:
            container = self.content.viewManager.CreateContainerView(folder, obj_type, True)
        return container.view

    def _get_obj(self, obj_type, name):
        """
        根据对象类型和名称来获取具体对象
        """
        obj = None
        content = self.client.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, obj_type, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def _get_obj_by_id(self, obj_type, _id, folder=None):
        """
        根据对象编号获取实例
        """
        obj = None
        view = self._get_all_objs(obj_type, folder=folder)
        for c in view:
            if _id:
                if c._moId == _id:
                    obj = c
                    break
            else:
                obj = None
                break
        return obj

    def get_data_center(self):
        """
        数据中心列表
        """
        datacenter_objs = self._get_all_objs([vim.Datacenter])
        data = []
        for i in datacenter_objs:
            datacenter_data = {
                'name': i.name,
                'id': i._moId
            }
            data.append(datacenter_data)
        return data

    def get_cluster(self, data_center_id):
        """
        集群列表
        """
        cluster_objs = self._get_all_objs([vim.Datacenter])
        cluster_list = []
        for data_center in cluster_objs:
            if data_center_id == data_center._moId:
                container = self.content.viewManager.CreateContainerView(data_center, [vim.ComputeResource],
                                                                         True).view  # 数据中心下集群
                for cluster in container:
                    if cluster._wsdlName == 'ClusterComputeResource':
                        cluster_list.append({"name": cluster.name, "id": cluster._moId})
        return cluster_list

    def get_host(self, data_center_id, cluster_id):
        """
        获取集群的物理机列表
        """
        cluster_objs = self._get_all_objs([vim.Datacenter])
        host_list = []
        for data_center in cluster_objs:
            if data_center_id == data_center._moId:
                container = self.content.viewManager.CreateContainerView(data_center, [vim.ComputeResource],
                                                                         True).view
                for cluster in container:
                    if cluster._moId == cluster_id:
                        host_list.extend([{"name": host.name, "id": host._moId} for host in cluster.host])
                        return host_list
        return host_list

    def get_vm(self, data_center_id, cluster_id):
        """
        获取集群的虚拟机列表
        """
        vm_list = []
        for data_center in self._get_all_objs([vim.Datacenter]):
            if data_center_id == data_center._moId:
                container = self.content.viewManager.CreateContainerView(data_center, [vim.ComputeResource],
                                                                         True).view
                for cluster in container:
                    if cluster._moId == cluster_id:
                        for virtual_machine in self._get_all_objs([vim.VirtualMachine], cluster):
                            vm_list.append({
                                "id": virtual_machine._moId,
                                "name": virtual_machine.name,
                                "cpu": virtual_machine.summary.config.numCpu,
                                "memory": virtual_machine.summary.config.memorySizeMB,
                                "status": str(virtual_machine.summary.runtime.powerState),
                                "ip": virtual_machine.summary.guest.ipAddress,
                                "os": virtual_machine.summary.config.guestFullName,
                            })
                        return vm_list
        return vm_list

    def get_storage_cluster(self):
        """
        存储集群列表
        """
        storage_cluster_objs = self._get_all_objs([vim.StoragePod])
        storage_cluster_list = []
        for storage_cluster in storage_cluster_objs:
            storage_cluster_list.append({"name": storage_cluster.name, "id": storage_cluster._moId})
        return storage_cluster_list

    def get_storage_by_id(self, datacenter_id, cluster_id, host_id, disk_id):
        """
        获取存储实例
        """
        for data_center in self._get_all_objs([vim.Datacenter]):
            if datacenter_id == data_center._moId:
                for cluster in self._get_all_objs([vim.ComputeResource], data_center):
                    if cluster._moId == cluster_id:
                        for host in cluster.host:
                            if host_id:
                                if host._moId == host_id:
                                    for storage_pod in host.datastore:
                                        if storage_pod._moId == disk_id:
                                            return storage_pod
                            else:
                                for storage_pod in host.datastore:
                                    if storage_pod._moId == disk_id:
                                        return storage_pod
        return None

    def get_storage_by_host(self, datacenter_id, cluster_id, host_id):
        """
        获取物理机对应的存储集群列表
        """
        storage_list = []
        for data_center in self._get_all_objs([vim.Datacenter]):
            if datacenter_id == data_center._moId:
                for cluster in self._get_all_objs([vim.ComputeResource], data_center):
                    if cluster._moId == cluster_id:
                        for host in cluster.host:
                            if host_id:
                                if host._moId == host_id:
                                    storage_list.extend(
                                        [{'name': storage_pod.name, 'id': storage_pod._moId} for storage_pod in
                                         host.datastore])
                                    return storage_list
                            else:
                                storage_list.extend(
                                    [{'name': storage_pod.name, 'id': storage_pod._moId} for storage_pod in
                                     host.datastore])
        return storage_list

    def get_vlan(self, datacenter_id):
        """
        获取虚拟网卡列表
        """
        network_list = []
        for data_center in self._get_all_objs([vim.Datacenter]):
            if datacenter_id == data_center._moId:
                for network in data_center.network:
                    network_list.append({"name": network.name, "id": network._moId})
                return network_list
        return network_list

    def device_nic(self, vm, network_id, switch_type):
        """
        获取网段的实例
        :param vm: 虚拟机模板对象
        :param network_id: 要修改的网络段名称
        :param switch_type: 网络段类型
        :return:
        """
        device_change = []
        no_vlan = False
        for device in vm.config.hardware.device:
            # 判断是否存在网络适配器
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nicspec = vim.vm.device.VirtualDeviceSpec()
                # 一定要是vim.vm.device.VirtualDeviceSpec.Operation.edit  代表编辑
                nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
                nicspec.device = device
                nicspec.device.wakeOnLanEnabled = True
                if switch_type == 1:
                    # 标准交换机设置
                    nicspec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
                    network = self._get_obj_by_id([vim.Network], network_id)
                    nicspec.device.backing.network = network
                    nicspec.device.backing.deviceName = network.name
                    nicspec.device.backing.useAutoDetect = False
                else:
                    # 判断网络段是否在分组交换机网络范围
                    network = self._get_obj_by_id([vim.dvs.DistributedVirtualPortgroup], network_id)
                    # network = self._get_obj([vim.Network], network_name)
                    if network is None:
                        # logger.error(u'分组交换机没有{0}网段'.format(network_name))
                        no_vlan = True
                        break
                    # 分布式交换机设置
                    dvs_port_connection = vim.dvs.PortConnection()
                    dvs_port_connection.portgroupKey = network.key
                    dvs_port_connection.switchUuid = network.config.distributedVirtualSwitch.uuid
                    nicspec.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
                    nicspec.device.backing.port = dvs_port_connection
                    # nicspec.device.backing.useAutoDetect = True
                # 网络段配置设置
                nicspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
                nicspec.device.connectable.startConnected = True
                nicspec.device.connectable.allowGuestControl = True
                nicspec.device.connectable.connected = True
                nicspec.device.connectable.status = 'untried'
                nicspec.device.wakeOnLanEnabled = True
                nicspec.device.addressType = 'assigned'
                device_change.append(nicspec)
                break
        if device_change:
            return device_change
        else:
            if not no_vlan:
                pass
        return device_change

    def add_disk(self, vm, data_disk_size, disk_type):
        """
        添加磁盘到虚拟机
        """
        unit_number = 0
        controller = None
        for device in vm.config.hardware.device:
            if hasattr(device.backing, 'fileName'):
                unit_number = int(device.unitNumber) + 1
                if unit_number == 7:
                    unit_number += 1
                if unit_number >= 16:
                    return "we don't support this many disks"
            if isinstance(device, vim.vm.device.VirtualSCSIController):
                controller = device
        if controller is None:
            return "Disk SCSI controller not found!"
        # add disk here
        dev_changes = []
        new_disk_kb = int(data_disk_size) * 1024 * 1024
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        elif disk_type == 'eager':
            disk_spec.device.backing.thinProvisioned = False
            disk_spec.device.backing.eagerlyScrub = True
        elif disk_type == "lazy":
            disk_spec.device.backing.thinProvisioned = False
            disk_spec.device.backing.eagerlyScrub = False
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        return dev_changes

    def get_cluster_by_datacenter(self, name=None, datacenter=None):
        """
        根据数据中心实例获取集群实例
        """
        if datacenter:
            folder = datacenter.hostFolder
        else:
            folder = self.content.rootFolder

        container = self.content.viewManager.CreateContainerView(folder, [vim.ClusterComputeResource], True)
        clusters = container.view
        for cluster in clusters:
            if cluster.name == name:
                return cluster
        return None

    def get_vms_by_cluster(self, vmFolder):
        """
        根据集群实例获取虚机实例列表
        """
        content = self.client.content
        objView = content.viewManager.CreateContainerView(vmFolder, [vim.VirtualMachine], True)
        vmList = objView.view
        objView.Destroy()
        return vmList

    def get_max_free_space_datastore(self, cluster=None):
        """
        获取集群里拥有最大空闲空间的存储集群
        """
        select_store = None
        last_space = 0
        if cluster:
            virtual_machine = list(cluster.datastore)
        else:
            virtual_machine = self._get_all_objs([vim.Datastore])
        for v in virtual_machine:
            if v.name.lower().find('local') > -1:
                continue
            if select_store is None:
                select_store = v
                last_space = v.info.freeSpace
            else:
                if v.info.freeSpace > last_space:
                    select_store = v
                    last_space = v.info.freeSpace
        return select_store

    def get_customspec(self, template, *, vm_ip=None, vm_subnetmask=None, vm_gateway=None, vm_dns=None,
                       vm_domain=None, vm_hostname=None, vm_password='ABC12345678'):
        """
        IP等信息的配置函数
        :param vm_password:
        :param template: 模板对象
        :param vm_ip:
        :param vm_subnetmask:
        :param vm_gateway:
        :param vm_dns:
        :param vm_domain:
        :param vm_hostname:
        :return:
        """
        # IP 子网掩码 网关配置(配置单个网卡信息)
        guest_map = vim.vm.customization.AdapterMapping()
        guest_map.adapter = vim.vm.customization.IPSettings()
        guest_map.adapter.ip = vim.vm.customization.FixedIp()
        guest_map.adapter.ip.ipAddress = vm_ip
        guest_map.adapter.subnetMask = vm_subnetmask
        guest_map.adapter.gateway = vm_gateway
        # # 域配置
        # if vm_domain:
        #     guest_map.adapter.dnsDomain = vm_domain

        # 全局网络配置信息
        global_ip_setting = vim.vm.customization.GlobalIPSettings()
        if vm_dns:
            if isinstance(vm_dns, str):
                global_ip_setting.dnsServerList = vm_dns.split(',')
            else:
                global_ip_setting.dnsServerList = vm_dns

            # global_ip_setting.dnsSuffixList = vm_domain

        if 'win' in template.config.guestId:
            # Windows
            # 用户信息
            user_data = vim.vm.customization.UserData()
            user_data.computerName = vim.vm.customization.FixedName()
            if vm_hostname:
                user_data.computerName.name = vm_hostname
                user_data.fullName = 'Administrator'
                user_data.orgName = 'Administrators'

            # 所属域
            identification = vim.vm.customization.Identification()
            if vm_domain:
                identification.domainAdmin = vm_domain

            # 密码信息
            password_instance = vim.vm.customization.Password()
            password_instance.value = vm_password if vm_password else 'root'
            password_instance.plainText = True

            gui_unattended = vim.vm.customization.GuiUnattended()
            gui_unattended.autoLogon = True
            gui_unattended.autoLogonCount = 1
            gui_unattended.password = password_instance

            ident = vim.vm.customization.Sysprep()
            ident.guiUnattended = gui_unattended
            ident.identification = identification
            ident.userData = user_data
        else:
            # Linux
            ident = vim.vm.customization.LinuxPrep()
            if vm_domain:
                ident.domain = vm_domain
            ident.hostName = vim.vm.customization.FixedName()
            if vm_hostname:
                ident.hostName.name = vm_hostname

        # 自定义配置
        custom_spec = vim.vm.customization.Specification()
        # 添加网卡列表
        custom_spec.nicSettingMap = [guest_map]
        # 添加全局网络配置DNS
        custom_spec.globalIPSettings = global_ip_setting
        # 添加认证信息
        custom_spec.identity = ident
        return custom_spec

    # 自定义设置操作系统及网络适配器
    def _get_customizationspec(self, vm_ip, mask, gateway, vmtemplate_os, vm_dns):
        vmtemplate_os = vmtemplate_os.lower()
        # 设置IP
        if vm_ip:
            ip = vim.CustomizationFixedIp()
            ip.ipAddress = vm_ip
        else:
            ip = vim.CustomizationDhcpIpGenerator()
        # 设置网卡
        adapter_ipsetting = vim.CustomizationIPSettings()
        adapter_ipsetting.ip = ip
        if mask:
            adapter_ipsetting.subnetMask = mask
        if gateway:
            adapter_ipsetting.gateway = gateway
        # 设置nicMap
        nic_setting_map = vim.CustomizationAdapterMapping()
        nic_setting_map.adapter = adapter_ipsetting
        nic_setting_maps = [nic_setting_map]
        # 设置globalIPSettings
        global_ip_settings = vim.CustomizationGlobalIPSettings()
        global_ip_settings.dnsServerList = vm_dns
        if vmtemplate_os.find("win") > -1:
            identity = self._get_identity_win()
        else:
            identity = self._get_identity_linux()
        # 设置customizationspec
        customizationspec = vim.CustomizationSpec()
        customizationspec.nicSettingMap = nic_setting_maps
        customizationspec.globalIPSettings = global_ip_settings
        customizationspec.identity = identity
        return customizationspec

    # 配置windows系统
    @classmethod
    def _get_identity_win(cls):
        # windows配置
        # 设置Unattend
        gui_unattended = vim.CustomizationGuiUnattended()
        gui_unattended.autoLogon = False
        gui_unattended.autoLogonCount = 0
        gui_unattended.timeZone = 210
        # 设置identification
        identification = vim.CustomizationIdentification()
        identification.joinWorkgroup = "WorkGroup"
        computer_name_data = vim.CustomizationVirtualMachineName()
        # 设置user_data
        user_data = vim.CustomizationUserData()
        user_data.computerName = computer_name_data
        user_data.fullName = 'Administrator'  # "user"
        user_data.orgName = 'Administrators'  # "org"
        # user_data.productId = ""
        # 设置identity
        identity = vim.CustomizationSysprep()
        identity.guiUnattended = gui_unattended
        identity.identification = identification
        identity.userData = user_data

        password = vim.vm.customization.Password()
        password.value = 'Aa123456,.'
        password.plainText = True
        identity.guiUnattended.password = password
        return identity

    # 配置linux系统
    @classmethod
    def _get_identity_linux(cls):
        # Linux配置
        host_name = vim.CustomizationVirtualMachineName()
        # 设置identity
        identity = vim.CustomizationLinuxPrep()
        identity.hostName = host_name
        identity.domain = ""
        # identity.timeZone = "Asia/Shanghai"
        return identity

    def wait_for_task(self, task):  # noqa
        """
        等待执行结果
        """
        while True:
            if task.info.state == 'success':
                return ReturnStruct(True, '执行成功')

            if task.info.state == 'error':
                return ReturnStruct(False, task.info.error.msg)

            time.sleep(0.5)

    def clone_vm(self, *, template_name, vm_name, datacenter_id, cluster_id, host_id, cpu_num=None, memory=None,
                 vm_ip=None, vm_subnetmask=None, vm_gateway=None, vm_dns=None, vm_domain=None, network_id=None,
                 data_disk_id=None, data_disk_size=None, password=None):
        """
        创建虚拟机
        """
        # 获取模版
        template = self._get_obj([vim.VirtualMachine], template_name)
        # 模版不存在
        if template is None:
            return ReturnStruct(False, '模版不存在')
        # 选择克隆的虚拟机存放位置,通过数据中心获取对象
        datacenter = self._get_obj_by_id([vim.Datacenter], datacenter_id)
        # 数据中心不存在
        if datacenter is None:
            return ReturnStruct(False, '数据中心不存在')
        vm_folder = datacenter.vmFolder
        # 获取集群
        cluster = self._get_obj_by_id([vim.ClusterComputeResource], cluster_id, datacenter)
        if not cluster:
            return ReturnStruct(False, '集群不存在')
        vms = self.get_vms_by_cluster(cluster)
        vms_name = [i.name for i in vms]
        if vm_name in vms_name:
            return ReturnStruct(False, '虚拟机已经存在')

        # 网络初始化信息
        customization = None
        if all([vm_ip, vm_subnetmask, vm_gateway, vm_domain]):
            customization = self.get_customspec(template,
                                                vm_ip=vm_ip,
                                                vm_subnetmask=vm_subnetmask,
                                                vm_gateway=vm_gateway,
                                                vm_domain=vm_domain,
                                                vm_dns=vm_dns,
                                                vm_hostname=vm_name,
                                                vm_password=password)
            # customization = self._get_customizationspec(vm_ip, vm_subnetmask, vm_gateway, template_name,
            #                                                        vm_dns)

        # 存储及网络设备的硬件选择
        device_change = []
        # 指定网络段配置
        device_nic_change = self.device_nic(
            vm=template,
            network_id=network_id,
            switch_type=1
        )
        if device_nic_change:
            device_change.extend(device_nic_change)
        # 修改硬盘大小
        if data_disk_size:
            disk_change = self.add_disk(template, data_disk_size, 'thin')
            if isinstance(disk_change, list):
                device_change.extend(disk_change)
            else:
                return ReturnStruct(False, disk_change)

        # 配置CPU内存，存储及网络
        vm_conf = vim.vm.ConfigSpec()
        if cpu_num:
            vm_conf.numCPUs = cpu_num
        if memory:
            vm_conf.memoryMB = memory
        vm_conf.deviceChange = device_change

        # 获取存储实例
        resource_pool = cluster.resourcePool
        relocate_spec = vim.vm.RelocateSpec()
        relocate_spec.pool = resource_pool
        datastore = self.get_storage_by_id(datacenter_id, cluster_id, host_id, data_disk_id)
        if datastore:
            relocate_spec.datastore = datastore
        else:
            return ReturnStruct(False, '存储实例未查询到')

        # 生成克隆配置
        clone_spec = vim.vm.CloneSpec()
        # 获取存储实例(硬件配置)
        clone_spec.location = relocate_spec
        # 配置CPU内存，存储及网络(硬件配置)
        if vm_conf is not None:
            clone_spec.config = vm_conf
        # 克隆完成直接启动
        clone_spec.powerOn = True
        # 网络初始化信息(软件配置)
        clone_spec.customization = customization

        task = template.Clone(folder=vm_folder, name=vm_name, spec=clone_spec)
        result = self.wait_for_task(task)
        return result

    def power_off(self, vm_name):
        """
        关机
        """
        vm = self._get_obj([vim.VirtualMachine], vm_name)
        if vm is None:
            return ReturnStruct(False, '未找到主机')
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            task = vm.PowerOff()
            while task.info.state not in [vim.TaskInfo.State.success,
                                          vim.TaskInfo.State.error]:
                time.sleep(0.5)
        else:
            return ReturnStruct(False, '不是开机状态')
        if task.info.state == vim.TaskInfo.State.success:
            data = ReturnStruct(True)
        elif task.info.state == vim.TaskInfo.State.error:
            data = ReturnStruct(False, task.info.error.msg)
        else:
            data = ReturnStruct(False, '其它未知错误')
        return data

    def power_on(self, vm_name):
        """
        开机
        """
        vm = self._get_obj([vim.VirtualMachine], vm_name)
        if vm is None:
            return ReturnStruct(False, '未找到主机')
        if vm.runtime.powerState != vim.VirtualMachinePowerState.poweredOn:
            task = vm.PowerOn()
            while task.info.state not in [vim.TaskInfo.State.success,
                                          vim.TaskInfo.State.error]:
                time.sleep(0.5)
        else:
            return ReturnStruct(False, '不是非开机状态')
        if task.info.state == vim.TaskInfo.State.success:
            data = ReturnStruct(True)
        elif task.info.state == vim.TaskInfo.State.error:
            data = ReturnStruct(False, task.info.error.msg)
        else:
            data = ReturnStruct(False, '其它未知错误')
        return data

    def remove(self, vm_name):
        """
        移除虚拟机
        """
        vm = self._get_obj([vim.VirtualMachine], vm_name)
        if vm is None:
            return ReturnStruct(False, '未找到主机')
        task = vm.Destroy()
        while task.info.state not in [vim.TaskInfo.State.success,
                                      vim.TaskInfo.State.error]:
            time.sleep(0.5)
        if task.info.state == vim.TaskInfo.State.success:
            data = ReturnStruct(True)
        elif task.info.state == vim.TaskInfo.State.error:
            data = ReturnStruct(False, task.info.error.msg)
        else:
            data = ReturnStruct(False, '其它未知错误')
        return data

    def change_password(self, is_win, vm_name, username, old_password, new_password):
        start_time = time.time()
        while True:
            if time.time() - start_time > 60 * 5:
                return ReturnStruct(False, '等待主机启动成功超时')
            vm = self._get_obj([vim.VirtualMachine], vm_name)
            if vm is None:
                return ReturnStruct(False, '未找到主机')
            if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
                break
            time.sleep(5)
        try:
            if is_win:
                pm = self.content.guestOperationsManager.processManager
                argument = vim.vm.guest.ProcessManager.ProgramSpec(
                    programPath=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',
                    arguments=' -Command "& {net user  ' + username + ' ' + new_password + '}"')
                creds = vim.vm.guest.NamePasswordAuthentication(username=username, password=old_password)
                res = pm.StartProgramInGuest(vm, creds, argument)
            else:
                pm = self.content.guestOperationsManager.processManager
                argument = vim.vm.guest.ProcessManager.ProgramSpec(
                    programPath=r'/bin/echo',
                    arguments=' \'' + new_password + '\'|passwd --stdin root')

                creds = vim.vm.guest.NamePasswordAuthentication(username=username, password=old_password)
                res = pm.StartProgramInGuest(vm, creds, argument)
            time.sleep(10)
        except Exception as e:
            return ReturnStruct(False, '修改密码失败: ' + str(e))
        return ReturnStruct(True, '', res)


if __name__ == '__main__':
    ip = '10.186.177.177'
    user = 'bk@vsphere.local'
    password = 'Geely@HANGZHOU#2022'
    port = 443
    vm = VSphere(host=ip, user=user, password=password, port=port, ssl=None)

    # data_center = vm.get_data_center()
    # print('data_center', data_center)
    # cluster = vm.get_cluster(data_center[0]['id'])
    # print('cluster', cluster)
    # host = vm.get_host(data_center[0]['id'], cluster[0]['id'])
    # print('host', host)
    # vm_list = vm.get_vm(data_center[0]['id'], cluster[0]['id'])
    # print('vm_list', vm_list)
    # store_cluster = vm.get_storage_cluster()
    # print('store_cluster', store_cluster)
    # store_list = vm.get_storage_by_host(data_center[0]['id'], cluster[0]['id'], host[0]['id'])
    # print('store_list', store_list)
    # # store_list = vm.get_storage_by_host(data_center[0]['id'], cluster[0]['id'], '')
    # # print(store_list)
    # vlan = vm.get_vlan(data_center[0]['id'])
    # print('vlan', vlan)
    # # windows: 'HQ-T-Temp-WIN2016EN-VMware6.5-2023Q2', 'po$v&UXBt@r2&mm3'
    # # linux: 'HQ-T-Temp-redhat7.9-VMware6.5-2023Q2', '!QAZ@WSX#EDC@1qaz'
    # clone_res = vm.clone_vm(template_name='HQ-T-Temp-redhat7.9-VMware6.5-2023Q2',
    #                         vm_name='ops-test-00001',
    #                         datacenter_id=data_center[0]['id'],
    #                         cluster_id=cluster[0]['id'],
    #                         host_id=host[0]['id'],
    #                         cpu_num=8,
    #                         memory=16384,
    #                         vm_ip='10.186.212.10',
    #                         vm_subnetmask='255.255.255.0',
    #                         vm_gateway='10.186.212.1',
    #                         vm_dns=["10.3.3.3", "10.3.3.4"],
    #                         vm_domain='geely.auto',
    #                         network_id=vlan[0]['id'],
    #                         data_disk_id=store_list[0]['id'],
    #                         data_disk_size=130,
    #                         password='Aa123456,.'
    #                         )
    # print('clone_res', clone_res)
    # windows 修改密码
    # result = vm.change_password(is_win=True, vm_name='ops-test-00002',
    #                             username='administrator',
    #                             old_password='Aa123456,./789',
    #                             new_password='Aa123456,./788')
    # print(result)
    # linux 修改密码
    result = vm.change_password(is_win=False, vm_name='ops-test-00001',
                                username='root',
                                old_password='MZyyty1O5ty!2lT2l',
                                new_password='MD2DHHD!aIup03H2u')
    print(result)
