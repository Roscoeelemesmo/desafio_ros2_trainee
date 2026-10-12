import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_srvs.srv import Empty

class ValidacaoNode(Node):
    def __init__(self):
        super().__init__('node_validacao')
        self.estado_liberado = False
        self.srv = self.create_service(Empty, '/acionamento', self.acionamento_callback)
        self.publisher_ = self.create_publisher(Bool, '/validacao', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info('Nó de Validação iniciado. Sistema em STANDBY (False).')

    def acionamento_callback(self, request, response):
        if not self.estado_liberado:
            self.estado_liberado = True
            self.get_logger().info('Requisição recebida! Sistema liberado (True).')
        else:
            self.get_logger().info('Serviço chamado, mas o sistema já estava liberado.')
        return response

    def timer_callback(self):
        msg = Bool()
        msg.data = self.estado_liberado
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ValidacaoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
