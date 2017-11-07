# OpenStack Apps

This repository will contain userdata for *apps* and/or *images* to be used on the CloudVPS OpenStack environment.

## Structure

The basic folder structure is based on these properties of a glance image: *os_type / os_distro / os_version.userdata*

This *userdata* file is used as-is, and passed as-is to the OpenStack Compute API as [userdata](https://docs.openstack.org/nova/latest/user/user-data.html) parameter.

## Apps
With os_type *apps* there is one exception, as there might not be an actual image for it.

If there is no image in glance, then a *os_version.metadata* file is required, that is set up as follows:

```json
{
    "name": "My Super App",
    "description": "This is my extended description of this super app that i've developed",
    "image_ref": "Ubuntu 16.04 (LTS)",
    "min_ram": 512,
    "min_disk": 40
}
```

The image_ref field can be a glance image uuid, but using the glance image name is preferred, as images are updated regularly and uuid's will be different.
