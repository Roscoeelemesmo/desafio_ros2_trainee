import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class MonitoramentoNode(Node):
    def __init__(self):
        super().__init__('node_monitoramento')
        self.subscription = self.create_subscription(Bool, '/validacao', self.listener_callback, 10)
        self.get_logger().info('Nó de Monitoramento iniciado. Escutando /validacao...')

    def listener_callback(self, msg):
        if not msg.data:
            self.get_logger().info('[MONITOR] Status: O sistema permanece em ESPERA (False).')
        else:
            self.get_logger().info('[MONITOR] Status: O sistema foi LIBERADO para operação (True)!')

def main(args=None):
    rclpy.init(args=args)
    node = MonitoramentoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
