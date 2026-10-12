import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class AcionamentoNode(Node):
    def __init__(self):
        super().__init__('node_acionamento')
        self.client = self.create_client(Empty, '/acionamento')
        self.get_logger().info('Nó de Acionamento iniciado. Aguardando 10 segundos para solicitar a liberação...')
        self.timer = self.create_timer(10.0, self.timer_callback)
        self.requisicao_enviada = False

    def timer_callback(self):
        if self.requisicao_enviada:
            return
        self.timer.cancel()
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Serviço /acionamento indisponível, tentando...')
        request = Empty.Request()
        self.client.call_async(request)
        self.get_logger().info('Solicitação de acionamento enviada!')
        self.requisicao_enviada = True

def main(args=None):
    rclpy.init(args=args)
    node = AcionamentoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
