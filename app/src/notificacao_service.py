import os
from aws_lambda_powertools import Logger

from src.services.email_service import EmailService

class NotificacaoService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.email_service = EmailService(self.logger)
    
    def enviar_notificacao(self, pedido: dict) -> bool:
        to_emails = [pedido["email_cliente"]]
        subject = f"Pedido {pedido['id_pedido']}"
        
        if "erro" in pedido and pedido["erro"]:
            body_html = f"""
                <html>
                    <body>
                        <h1>Erro ao realizar pagamento.</h1>
                        <p>Por favor tente novamente.</p>
                    </body>
                </html>
                """
        else:
            body_html = f"""
                    <html>
                        <body>
                            <h1>Pagamento realizado com sucesso</h1>
                            <p>Preparando pedido:</p>
                            <p>Total pedido: R$ {pedido['total_pedido']}</p>
                            <ol>
                                {self.items_to_li(pedido['itens'])}
                            </ol>
                        </body>
                    </html>
                    """

        self.email_service.enviar_email(to_emails, subject, body_html)
    
    def items_to_li(self, items):
        html = ""
        for item in items:
            html += f"<li>{item['nome']} ({item['quantidade']} x R$ {item['valor']:.2f})</li>\n"
        return html.strip()
