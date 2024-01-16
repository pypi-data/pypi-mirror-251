from dsbot import client


class TestClient(client.BotClient):
    def test_input(self, event, message):
        self.dispatch(
            event,
            client=self,
            message=message,
        )
