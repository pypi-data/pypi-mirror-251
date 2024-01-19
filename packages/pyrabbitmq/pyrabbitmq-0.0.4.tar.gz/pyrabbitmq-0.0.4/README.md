# pyrabbitmq


```python

from pyrabbitmq import connection
rmq = connection.Instance()

# or

rmq = connection.Instance(
    rabbitmq_host="127.0.0.1",
    rabbitmq_port="5673",
    rabbitmq_admin_user="guest",
    rabbitmq_admin_password="guest",
    rabbitmq_tls_enabled=False
)
v = rmq.VirtualHost
v.create('a-vhost-name')
u = rmq.User
u.create('test-user','test-user-password')

```
